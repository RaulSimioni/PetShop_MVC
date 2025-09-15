# Sistema ERP Pet Shop

Sistema ERP completo para Pet Shop desenvolvido em Flask e Python seguindo o padrão MVC (Model-View-Controller).

## 📋 Funcionalidades

### Gestão de Clientes
- Cadastro, consulta, atualização e desativação de clientes
- Validação de CPF e email únicos
- Listagem de pets por cliente

### Gestão de Pets
- Cadastro completo de pets com informações detalhadas
- Vinculação com clientes
- Controle de espécie, raça, cor, sexo, peso e observações

### Gestão de Funcionários
- Cadastro de funcionários com dados pessoais e profissionais
- Controle de cargo, salário e datas de admissão/demissão
- Validação de CPF e email únicos

### Gestão de Serviços
- Cadastro de serviços oferecidos pelo pet shop
- Controle de preços e duração estimada

### Gestão de Agendamentos
- Sistema completo de agendamento de serviços
- Vinculação de clientes, pets, funcionários e serviços
- Controle de data/hora e status dos agendamentos
- Controle de status (Agendado, Confirmado, Em Andamento, Concluído, Cancelado)
- Validação de conflitos de horário
- Filtros por data, status e funcionário

## 🏗️ Arquitetura

O sistema segue o padrão MVC (Model-View-Controller):

### Models (Modelos)
- **Cliente**: Dados dos clientes
- **Pet**: Informações dos animais
- **Funcionario**: Dados dos funcionários
- **Produto**: Catálogo de produtos
- **Servico**: Serviços oferecidos
- **Venda**: Transações de venda
- **ItemVenda**: Itens individuais das vendas
- **Agendamento**: Agendamentos de serviços

### Controllers (Controladores)
- **cliente.py**: CRUD de clientes
- **pet.py**: CRUD de pets
- **funcionario.py**: CRUD de funcionários
- **produto.py**: CRUD de produtos
- **servico.py**: CRUD de serviços
- **venda.py**: Gestão de vendas
- **agendamento.py**: Gestão de agendamentos

### Views (Visões)
- Interface preparada para implementação frontend
- API REST completa para integração

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.11+
- pip

### Instalação

1. Clone o repositório:
```bash
cd petshop_erp
```

2. Ative o ambiente virtual:
```bash
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicialize o banco de dados:
```bash
python init_db.py
```

5. Execute o servidor:
```bash
python src/main.py
```

O servidor estará disponível em `http://localhost:5000`

### Teste do Sistema

Execute os testes automatizados:
```bash
python test_system.py
```

## 📚 API Endpoints

### Clientes
- `GET /api/clientes` - Listar todos os clientes
- `POST /api/clientes` - Criar novo cliente
- `GET /api/clientes/{id}` - Buscar cliente por ID
- `PUT /api/clientes/{id}` - Atualizar cliente
- `DELETE /api/clientes/{id}` - Desativar cliente
- `GET /api/clientes/{id}/pets` - Listar pets do cliente

### Pets
- `GET /api/pets` - Listar todos os pets
- `POST /api/pets` - Criar novo pet
- `GET /api/pets/{id}` - Buscar pet por ID
- `PUT /api/pets/{id}` - Atualizar pet
- `DELETE /api/pets/{id}` - Desativar pet
- `GET /api/pets/cliente/{cliente_id}` - Listar pets por cliente

### Funcionários
- `GET /api/funcionarios` - Listar todos os funcionários
- `POST /api/funcionarios` - Criar novo funcionário
- `GET /api/funcionarios/{id}` - Buscar funcionário por ID
- `PUT /api/funcionarios/{id}` - Atualizar funcionário
- `DELETE /api/funcionarios/{id}` - Desativar funcionário

### Produtos
- `GET /api/produtos` - Listar todos os produtos
- `POST /api/produtos` - Criar novo produto
- `GET /api/produtos/{id}` - Buscar produto por ID
- `PUT /api/produtos/{id}` - Atualizar produto
- `DELETE /api/produtos/{id}` - Desativar produto
- `GET /api/produtos/estoque-baixo` - Produtos com estoque baixo
- `GET /api/produtos/categoria/{categoria}` - Produtos por categoria

### Serviços
- `GET /api/servicos` - Listar todos os serviços
- `POST /api/servicos` - Criar novo serviço
- `GET /api/servicos/{id}` - Buscar serviço por ID
- `PUT /api/servicos/{id}` - Atualizar serviço
- `DELETE /api/servicos/{id}` - Desativar serviço
- `GET /api/servicos/categoria/{categoria}` - Serviços por categoria

### Vendas
- `GET /api/vendas` - Listar todas as vendas
- `POST /api/vendas` - Criar nova venda
- `GET /api/vendas/{id}` - Buscar venda por ID
- `PUT /api/vendas/{id}/cancelar` - Cancelar venda
- `GET /api/vendas/cliente/{cliente_id}` - Vendas por cliente

### Agendamentos
- `GET /api/agendamentos` - Listar agendamentos (com filtros opcionais)
- `POST /api/agendamentos` - Criar novo agendamento
- `GET /api/agendamentos/{id}` - Buscar agendamento por ID
- `PUT /api/agendamentos/{id}` - Atualizar agendamento
- `PUT /api/agendamentos/{id}/status` - Atualizar status do agendamento
- `DELETE /api/agendamentos/{id}` - Cancelar agendamento
- `GET /api/agendamentos/cliente/{cliente_id}` - Agendamentos por cliente
- `GET /api/agendamentos/funcionario/{funcionario_id}` - Agendamentos por funcionário

## 🗄️ Banco de Dados

O sistema utiliza SQLite por padrão, mas pode ser facilmente configurado para PostgreSQL ou MySQL através das configurações no arquivo `src/config.py`.

### Estrutura das Tabelas

- **clientes**: Dados dos clientes
- **pets**: Informações dos pets
- **funcionarios**: Dados dos funcionários
- **produtos**: Catálogo de produtos
- **servicos**: Serviços oferecidos
- **vendas**: Cabeçalho das vendas
- **itens_venda**: Itens das vendas
- **agendamentos**: Agendamentos de serviços

## 🔧 Configuração

As configurações do sistema estão no arquivo `src/config.py`:

- **Development**: Configurações para desenvolvimento
- **Production**: Configurações para produção
- **Testing**: Configurações para testes

## 📦 Dependências

- Flask: Framework web
- Flask-SQLAlchemy: ORM para banco de dados
- Flask-CORS: Suporte a CORS
- Flask-Migrate: Migrações de banco de dados
- python-dateutil: Manipulação de datas

## 🧪 Dados de Exemplo

O sistema inclui dados de exemplo que são criados automaticamente:

- 3 funcionários (Veterinária, Tosador, Atendente)
- 3 clientes com seus respectivos pets
- 3 produtos (Ração, Shampoo, Brinquedo)
- 4 serviços (Banho, Tosa, Consulta, Vacinação)

## 🔒 Segurança

- Validação de dados de entrada
- Soft delete (desativação) em vez de exclusão física
- Validação de CPF e email únicos
- Controle de estoque automático
- Validação de conflitos de agendamento

## 🚀 Próximos Passos

Para implementar um frontend completo, você pode:

1. Criar uma interface web usando React, Vue.js ou Angular
2. Implementar autenticação e autorização
3. Adicionar relatórios e dashboards
4. Implementar notificações por email/SMS
5. Adicionar backup automático do banco de dados

## 📄 Licença

Este projeto foi desenvolvido como um sistema ERP completo para Pet Shops, seguindo as melhores práticas de desenvolvimento em Python e Flask.

## 👥 Suporte

Para dúvidas ou sugestões sobre o sistema, consulte a documentação da API em `/api` quando o servidor estiver rodando.

