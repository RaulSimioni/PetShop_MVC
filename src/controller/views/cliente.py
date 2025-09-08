from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.model.models import db, Cliente
from sqlalchemy import or_
import math

cliente_views_bp = Blueprint('cliente_views', __name__)

@cliente_views_bp.route('/clientes')
def listar_clientes():
    """Página de listagem de clientes"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '', type=str)
    status = request.args.get('status', '', type=str)
    
    try:
        query = Cliente.query
        
        # Aplicar filtros
        if search:
            query = query.filter(or_(
                Cliente.nome.ilike(f'%{search}%'),
                Cliente.cpf.like(f'%{search}%'),
                Cliente.email.ilike(f'%{search}%')
            ))
        
        if status == 'true':
            query = query.filter(Cliente.ativo == True)
        elif status == 'false':
            query = query.filter(Cliente.ativo == False)
        
        # Ordenação
        query = query.order_by(Cliente.nome)
        
        # Paginação
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        clientes = pagination.items
        
        return render_template('clientes/listar.html', 
                             clientes=clientes, 
                             pagination=pagination)
    
    except Exception as e:
        flash(f'Erro ao carregar clientes: {str(e)}', 'error')
        return render_template('clientes/listar.html', clientes=[])

@cliente_views_bp.route('/clientes/novo', methods=['GET', 'POST'])
def novo_cliente():
    """Página de cadastro de novo cliente"""
    if request.method == 'GET':
        return render_template('clientes/novo.html')
    
    try:
        data = request.form
        
        # Validações básicas
        if not data.get('nome') or not data.get('cpf') or not data.get('telefone'):
            flash('Nome, CPF e telefone são obrigatórios', 'error')
            return render_template('clientes/novo.html')
        
        # Limpar CPF e telefone
        cpf = data.get('cpf', '').replace('.', '').replace('-', '').replace(' ', '')
        telefone = data.get('telefone', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        
        # Verificar se CPF já existe
        if Cliente.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado no sistema', 'error')
            return render_template('clientes/novo.html')
        
        # Verificar se email já existe (se fornecido)
        email = data.get('email', '').strip()
        if email and Cliente.query.filter_by(email=email).first():
            flash('Email já cadastrado no sistema', 'error')
            return render_template('clientes/novo.html')
        
        # Criar novo cliente
        cliente = Cliente(
            nome=data.get('nome').strip(),
            cpf=cpf,
            telefone=telefone,
            email=email if email else None,
            endereco=data.get('endereco', '').strip() if data.get('endereco', '').strip() else None
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        flash(f'Cliente {cliente.nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('cliente_views.visualizar_cliente', cliente_id=cliente.id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cadastrar cliente: {str(e)}', 'error')
        return render_template('clientes/novo.html')

@cliente_views_bp.route('/clientes/<int:cliente_id>')
def visualizar_cliente(cliente_id):
    """Página de visualização de cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        return render_template('clientes/visualizar.html', cliente=cliente)
    
    except Exception as e:
        flash(f'Erro ao carregar cliente: {str(e)}', 'error')
        return redirect(url_for('cliente_views.listar_clientes'))

@cliente_views_bp.route('/clientes/<int:cliente_id>/editar', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    """Página de edição de cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        if request.method == 'GET':
            return render_template('clientes/editar.html', cliente=cliente)
        
        # Processar formulário POST
        data = request.form
        
        # Validações básicas
        if not data.get('nome') or not data.get('cpf') or not data.get('telefone'):
            flash('Nome, CPF e telefone são obrigatórios', 'error')
            return render_template('clientes/editar.html', cliente=cliente)
        
        # Limpar CPF e telefone
        cpf = data.get('cpf', '').replace('.', '').replace('-', '').replace(' ', '')
        telefone = data.get('telefone', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        
        # Verificar se CPF já existe em outro cliente
        cpf_existente = Cliente.query.filter_by(cpf=cpf).first()
        if cpf_existente and cpf_existente.id != cliente.id:
            flash('CPF já cadastrado para outro cliente', 'error')
            return render_template('clientes/editar.html', cliente=cliente)
        
        # Verificar se email já existe em outro cliente
        email = data.get('email', '').strip()
        if email:
            email_existente = Cliente.query.filter_by(email=email).first()
            if email_existente and email_existente.id != cliente.id:
                flash('Email já cadastrado para outro cliente', 'error')
                return render_template('clientes/editar.html', cliente=cliente)
        
        # Atualizar dados do cliente
        cliente.nome = data.get('nome').strip()
        cliente.cpf = cpf
        cliente.telefone = telefone
        cliente.email = email if email else None
        cliente.endereco = data.get('endereco', '').strip() if data.get('endereco', '').strip() else None
        cliente.ativo = 'ativo' in data
        
        db.session.commit()
        
        flash(f'Cliente {cliente.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('cliente_views.visualizar_cliente', cliente_id=cliente.id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar cliente: {str(e)}', 'error')
        return render_template('clientes/editar.html', cliente=cliente)

@cliente_views_bp.route('/clientes/<int:cliente_id>/deletar', methods=['POST'])
def deletar_cliente(cliente_id):
    """Desativar cliente (soft delete)"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Verificar se tem pets, vendas ou agendamentos ativos
        if cliente.pets or cliente.vendas or cliente.agendamentos:
            # Soft delete - apenas desativar
            cliente.ativo = False
            db.session.commit()
            flash(f'Cliente {cliente.nome} foi desativado', 'warning')
        else:
            # Se não tem relacionamentos, permite delete real (opcional)
            cliente.ativo = False
            db.session.commit()
            flash(f'Cliente {cliente.nome} foi desativado', 'warning')
        
        return redirect(url_for('cliente_views.listar_clientes'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao desativar cliente: {str(e)}', 'error')
        return redirect(url_for('cliente_views.visualizar_cliente', cliente_id=cliente_id))

@cliente_views_bp.route('/clientes/<int:cliente_id>/ativar', methods=['POST'])
def ativar_cliente(cliente_id):
    """Reativar cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        cliente.ativo = True
        db.session.commit()
        
        flash(f'Cliente {cliente.nome} foi reativado', 'success')
        return redirect(url_for('cliente_views.visualizar_cliente', cliente_id=cliente_id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao reativar cliente: {str(e)}', 'error')
        return redirect(url_for('cliente_views.visualizar_cliente', cliente_id=cliente_id))

# Rotas auxiliares para busca e filtros
@cliente_views_bp.route('/clientes/buscar')
def buscar_clientes():
    """API endpoint para busca de clientes (para autocomplete, etc)"""
    try:
        query = request.args.get('q', '')
        limit = min(request.args.get('limit', 10, type=int), 50)
        
        if not query or len(query) < 2:
            return {'clientes': []}
        
        clientes = Cliente.query.filter(
            Cliente.ativo == True
        ).filter(or_(
            Cliente.nome.ilike(f'%{query}%'),
            Cliente.cpf.like(f'%{query}%'),
            Cliente.email.ilike(f'%{query}%')
        )).limit(limit).all()
        
        return {
            'clientes': [
                {
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'cpf': cliente.cpf,
                    'telefone': cliente.telefone,
                    'email': cliente.email
                }
                for cliente in clientes
            ]
        }
    
    except Exception as e:
        return {'erro': str(e)}, 500
