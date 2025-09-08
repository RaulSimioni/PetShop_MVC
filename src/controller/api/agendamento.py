from flask import Blueprint, jsonify, request
from src.model.models import db, Agendamento, Cliente, Pet, Servico, Funcionario
from datetime import datetime, timedelta

agendamento_bp = Blueprint('agendamento', __name__)

@agendamento_bp.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    """Listar todos os agendamentos"""
    try:
        # Filtros opcionais
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        status = request.args.get('status')
        funcionario_id = request.args.get('funcionario_id')
        
        query = Agendamento.query
        
        # Aplicar filtros
        if data_inicio:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
                query = query.filter(Agendamento.data_agendamento >= data_inicio_dt)
            except ValueError:
                return jsonify({'erro': 'Formato de data_inicio inválido. Use YYYY-MM-DD'}), 400
        
        if data_fim:
            try:
                data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Agendamento.data_agendamento < data_fim_dt)
            except ValueError:
                return jsonify({'erro': 'Formato de data_fim inválido. Use YYYY-MM-DD'}), 400
        
        if status:
            query = query.filter(Agendamento.status == status)
        
        if funcionario_id:
            query = query.filter(Agendamento.funcionario_id == funcionario_id)
        
        agendamentos = query.order_by(Agendamento.data_agendamento).all()
        return jsonify([agendamento.to_dict() for agendamento in agendamentos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@agendamento_bp.route('/agendamentos', methods=['POST'])
def create_agendamento():
    """Criar novo agendamento"""
    try:
        data = request.json
        
        # Validações básicas
        required_fields = ['cliente_id', 'pet_id', 'servico_id', 'data_agendamento']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'erro': f'{field} é obrigatório'}), 400
        
        # Verificar se cliente, pet e serviço existem
        cliente = Cliente.query.get(data['cliente_id'])
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
        
        pet = Pet.query.get(data['pet_id'])
        if not pet:
            return jsonify({'erro': 'Pet não encontrado'}), 404
        
        # Verificar se o pet pertence ao cliente
        if pet.cliente_id != data['cliente_id']:
            return jsonify({'erro': 'Pet não pertence ao cliente informado'}), 400
        
        servico = Servico.query.get(data['servico_id'])
        if not servico:
            return jsonify({'erro': 'Serviço não encontrado'}), 404
        
        # Verificar funcionário se informado
        funcionario_id = data.get('funcionario_id')
        if funcionario_id:
            funcionario = Funcionario.query.get(funcionario_id)
            if not funcionario:
                return jsonify({'erro': 'Funcionário não encontrado'}), 404
        
        # Converter data de agendamento
        try:
            data_agendamento = datetime.strptime(data['data_agendamento'], '%Y-%m-%d %H:%M')
        except ValueError:
            return jsonify({'erro': 'Formato de data_agendamento inválido. Use YYYY-MM-DD HH:MM'}), 400
        
        # Verificar se a data não é no passado
        if data_agendamento < datetime.now():
            return jsonify({'erro': 'Não é possível agendar para uma data no passado'}), 400
        
        # Verificar conflitos de horário (se funcionário informado)
        if funcionario_id:
            conflito = Agendamento.query.filter(
                Agendamento.funcionario_id == funcionario_id,
                Agendamento.data_agendamento == data_agendamento,
                Agendamento.status.in_(['Agendado', 'Confirmado', 'Em Andamento'])
            ).first()
            
            if conflito:
                return jsonify({'erro': 'Funcionário já possui agendamento neste horário'}), 400
        
        agendamento = Agendamento(
            cliente_id=data['cliente_id'],
            pet_id=data['pet_id'],
            servico_id=data['servico_id'],
            funcionario_id=funcionario_id,
            data_agendamento=data_agendamento,
            observacoes=data.get('observacoes'),
            valor_estimado=data.get('valor_estimado', servico.preco),
            tempo_estimado=data.get('tempo_estimado', servico.duracao_estimada)
        )
        
        db.session.add(agendamento)
        db.session.commit()
        
        return jsonify(agendamento.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@agendamento_bp.route('/agendamentos/<int:agendamento_id>', methods=['GET'])
def get_agendamento(agendamento_id):
    """Buscar agendamento por ID"""
    try:
        agendamento = Agendamento.query.get_or_404(agendamento_id)
        return jsonify(agendamento.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@agendamento_bp.route('/agendamentos/<int:agendamento_id>', methods=['PUT'])
def update_agendamento(agendamento_id):
    """Atualizar agendamento"""
    try:
        agendamento = Agendamento.query.get_or_404(agendamento_id)
        data = request.json
        
        # Verificar se pode ser alterado
        if agendamento.status in ['Concluído', 'Cancelado']:
            return jsonify({'erro': 'Não é possível alterar agendamento concluído ou cancelado'}), 400
        
        # Verificar funcionário se informado
        if data.get('funcionario_id'):
            funcionario = Funcionario.query.get(data['funcionario_id'])
            if not funcionario:
                return jsonify({'erro': 'Funcionário não encontrado'}), 404
        
        # Converter data de agendamento se fornecida
        if data.get('data_agendamento'):
            try:
                data_agendamento = datetime.strptime(data['data_agendamento'], '%Y-%m-%d %H:%M')
                
                # Verificar se a data não é no passado
                if data_agendamento < datetime.now():
                    return jsonify({'erro': 'Não é possível agendar para uma data no passado'}), 400
                
                # Verificar conflitos de horário
                funcionario_id = data.get('funcionario_id', agendamento.funcionario_id)
                if funcionario_id:
                    conflito = Agendamento.query.filter(
                        Agendamento.funcionario_id == funcionario_id,
                        Agendamento.data_agendamento == data_agendamento,
                        Agendamento.status.in_(['Agendado', 'Confirmado', 'Em Andamento']),
                        Agendamento.id != agendamento_id
                    ).first()
                    
                    if conflito:
                        return jsonify({'erro': 'Funcionário já possui agendamento neste horário'}), 400
                
                agendamento.data_agendamento = data_agendamento
            except ValueError:
                return jsonify({'erro': 'Formato de data_agendamento inválido. Use YYYY-MM-DD HH:MM'}), 400
        
        # Atualizar campos
        agendamento.funcionario_id = data.get('funcionario_id', agendamento.funcionario_id)
        agendamento.observacoes = data.get('observacoes', agendamento.observacoes)
        agendamento.valor_estimado = data.get('valor_estimado', agendamento.valor_estimado)
        agendamento.tempo_estimado = data.get('tempo_estimado', agendamento.tempo_estimado)
        agendamento.status = data.get('status', agendamento.status)
        
        db.session.commit()
        
        return jsonify(agendamento.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@agendamento_bp.route('/agendamentos/<int:agendamento_id>/status', methods=['PUT'])
def update_status_agendamento(agendamento_id):
    """Atualizar status do agendamento"""
    try:
        agendamento = Agendamento.query.get_or_404(agendamento_id)
        data = request.json
        
        if not data.get('status'):
            return jsonify({'erro': 'Status é obrigatório'}), 400
        
        status_validos = ['Agendado', 'Confirmado', 'Em Andamento', 'Concluído', 'Cancelado']
        if data['status'] not in status_validos:
            return jsonify({'erro': f'Status deve ser um dos seguintes: {", ".join(status_validos)}'}), 400
        
        agendamento.status = data['status']
        db.session.commit()
        
        return jsonify(agendamento.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@agendamento_bp.route('/agendamentos/<int:agendamento_id>', methods=['DELETE'])
def delete_agendamento(agendamento_id):
    """Cancelar agendamento"""
    try:
        agendamento = Agendamento.query.get_or_404(agendamento_id)
        agendamento.status = 'Cancelado'
        db.session.commit()
        
        return jsonify({'mensagem': 'Agendamento cancelado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@agendamento_bp.route('/agendamentos/cliente/<int:cliente_id>', methods=['GET'])
def get_agendamentos_by_cliente(cliente_id):
    """Listar agendamentos de um cliente"""
    try:
        agendamentos = Agendamento.query.filter_by(cliente_id=cliente_id).order_by(Agendamento.data_agendamento.desc()).all()
        return jsonify([agendamento.to_dict() for agendamento in agendamentos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@agendamento_bp.route('/agendamentos/funcionario/<int:funcionario_id>', methods=['GET'])
def get_agendamentos_by_funcionario(funcionario_id):
    """Listar agendamentos de um funcionário"""
    try:
        agendamentos = Agendamento.query.filter_by(funcionario_id=funcionario_id).order_by(Agendamento.data_agendamento).all()
        return jsonify([agendamento.to_dict() for agendamento in agendamentos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

