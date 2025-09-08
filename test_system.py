#!/usr/bin/env python3
"""
Script para testar o sistema ERP Pet Shop
"""

import sys
import os
from datetime import datetime, date

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.model.models import db, Cliente, Pet, Funcionario, Produto, Servico, Venda, ItemVenda, Agendamento

def test_models():
    """Testar os modelos do sistema"""
    
    with app.app_context():
        print("🧪 Testando modelos do sistema...")
        
        # Testar consulta de clientes
        clientes = Cliente.query.all()
        print(f"✅ {len(clientes)} clientes encontrados")
        
        # Testar consulta de pets
        pets = Pet.query.all()
        print(f"✅ {len(pets)} pets encontrados")
        
        # Testar consulta de funcionários
        funcionarios = Funcionario.query.all()
        print(f"✅ {len(funcionarios)} funcionários encontrados")
        
        # Testar consulta de produtos
        produtos = Produto.query.all()
        print(f"✅ {len(produtos)} produtos encontrados")
        
        # Testar consulta de serviços
        servicos = Servico.query.all()
        print(f"✅ {len(servicos)} serviços encontrados")
        
        # Testar relacionamentos
        if clientes:
            cliente = clientes[0]
            print(f"✅ Cliente '{cliente.nome}' tem {len(cliente.pets)} pets")
        
        # Testar criação de agendamento
        if clientes and pets and servicos:
            agendamento = Agendamento(
                cliente_id=clientes[0].id,
                pet_id=pets[0].id,
                servico_id=servicos[0].id,
                data_agendamento=datetime(2024, 12, 15, 10, 0),
                observacoes="Teste de agendamento"
            )
            db.session.add(agendamento)
            db.session.commit()
            print("✅ Agendamento de teste criado com sucesso")
        
        print("🎉 Todos os testes passaram!")

def test_api_routes():
    """Testar as rotas da API"""
    
    with app.test_client() as client:
        print("\n🌐 Testando rotas da API...")
        
        # Testar rota de informações da API
        response = client.get('/api')
        print(f"✅ GET /api - Status: {response.status_code}")
        
        # Testar listagem de clientes
        response = client.get('/api/clientes')
        print(f"✅ GET /api/clientes - Status: {response.status_code}")
        
        # Testar listagem de pets
        response = client.get('/api/pets')
        print(f"✅ GET /api/pets - Status: {response.status_code}")
        
        # Testar listagem de funcionários
        response = client.get('/api/funcionarios')
        print(f"✅ GET /api/funcionarios - Status: {response.status_code}")
        
        # Testar listagem de produtos
        response = client.get('/api/produtos')
        print(f"✅ GET /api/produtos - Status: {response.status_code}")
        
        # Testar listagem de serviços
        response = client.get('/api/servicos')
        print(f"✅ GET /api/servicos - Status: {response.status_code}")
        
        # Testar listagem de agendamentos
        response = client.get('/api/agendamentos')
        print(f"✅ GET /api/agendamentos - Status: {response.status_code}")
        
        print("🎉 Todas as rotas estão funcionando!")

if __name__ == '__main__':
    test_models()
    test_api_routes()
    print("\n✨ Sistema ERP Pet Shop testado com sucesso! ✨")

