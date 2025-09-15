#!/usr/bin/env python3
"""
Script para inicializar o banco de dados com dados de exemplo
"""

import sys
import os
from datetime import datetime, date

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.model.models import db, Cliente, Pet, Funcionario, Servico

def init_database():
    """Inicializar banco de dados com dados de exemplo"""
    
    with app.app_context():
        # Dropar e recriar todas as tabelas
        db.drop_all()
        db.create_all()
        
        print("Criando dados de exemplo...")
        
        # Criar funcionários
        funcionarios = [
            Funcionario(
                nome="Maria Silva",
                cpf="123.456.789-01",
                telefone="(11) 99999-1111",
                email="maria@petshop.com",
                endereco="Rua das Flores, 123",
                cargo="Veterinária",
                salario=5000.00,
                data_admissao=date(2023, 1, 15)
            ),
            Funcionario(
                nome="João Santos",
                cpf="987.654.321-09",
                telefone="(11) 99999-2222",
                email="joao@petshop.com",
                endereco="Av. Principal, 456",
                cargo="Tosador",
                salario=2500.00,
                data_admissao=date(2023, 3, 10)
            ),
            Funcionario(
                nome="Ana Costa",
                cpf="456.789.123-45",
                telefone="(11) 99999-3333",
                email="ana@petshop.com",
                endereco="Rua do Comércio, 789",
                cargo="Atendente",
                salario=2000.00,
                data_admissao=date(2023, 6, 1)
            )
        ]
        
        for funcionario in funcionarios:
            db.session.add(funcionario)
        
        # Criar clientes
        clientes = [
            Cliente(
                nome="Carlos Oliveira",
                cpf="111.222.333-44",
                telefone="(11) 88888-1111",
                email="carlos@email.com",
                endereco="Rua A, 100"
            ),
            Cliente(
                nome="Fernanda Lima",
                cpf="555.666.777-88",
                telefone="(11) 88888-2222",
                email="fernanda@email.com",
                endereco="Rua B, 200"
            ),
            Cliente(
                nome="Roberto Souza",
                cpf="999.888.777-66",
                telefone="(11) 88888-3333",
                email="roberto@email.com",
                endereco="Rua C, 300"
            )
        ]
        
        for cliente in clientes:
            db.session.add(cliente)
        
        db.session.flush()  # Para obter os IDs
        
        # Criar pets
        pets = [
            Pet(
                nome="Rex",
                especie="Cão",
                raca="Labrador",
                cor="Dourado",
                sexo="Macho",
                data_nascimento=date(2020, 5, 15),
                peso=30.5,
                observacoes="Muito dócil e brincalhão",
                cliente_id=clientes[0].id
            ),
            Pet(
                nome="Mimi",
                especie="Gato",
                raca="Persa",
                cor="Branco",
                sexo="Fêmea",
                data_nascimento=date(2021, 8, 20),
                peso=4.2,
                observacoes="Gosta de carinho",
                cliente_id=clientes[1].id
            ),
            Pet(
                nome="Thor",
                especie="Cão",
                raca="Pastor Alemão",
                cor="Preto e Marrom",
                sexo="Macho",
                data_nascimento=date(2019, 12, 10),
                peso=35.0,
                observacoes="Cão de guarda, muito protetor",
                cliente_id=clientes[2].id
            )
        ]
        
        for pet in pets:
            db.session.add(pet)
        
        # Criar serviços
        servicos = [
            Servico(
                nome="Banho Simples",
                descricao="Banho com shampoo neutro e secagem",
                categoria="Banho",
                preco=25.00,
                duracao_estimada=60,
                observacoes="Inclui corte de unhas"
            ),
            Servico(
                nome="Tosa Completa",
                descricao="Tosa higiênica e estética completa",
                categoria="Tosa",
                preco=45.00,
                duracao_estimada=90,
                observacoes="Inclui banho e perfume"
            ),
            Servico(
                nome="Consulta Veterinária",
                descricao="Consulta clínica geral",
                categoria="Veterinária",
                preco=80.00,
                duracao_estimada=30,
                observacoes="Exame clínico completo"
            ),
            Servico(
                nome="Vacinação",
                descricao="Aplicação de vacinas",
                categoria="Veterinária",
                preco=35.00,
                duracao_estimada=15,
                observacoes="Vacina não inclusa no preço"
            )
        ]
        
        for servico in servicos:
            db.session.add(servico)
        
        # Commit de todas as alterações
        db.session.commit()
        
        print("✅ Banco de dados inicializado com sucesso!")
        print(f"✅ {len(funcionarios)} funcionários criados")
        print(f"✅ {len(clientes)} clientes criados")
        print(f"✅ {len(pets)} pets criados")
        print(f"✅ {len(servicos)} serviços criados")

if __name__ == '__main__':
    init_database()

