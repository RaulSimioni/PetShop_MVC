# Sistema ERP Pet Shop

Sistema ERP completo para Pet Shop desenvolvido em Flask e Python seguindo o padrão MVC (Model-View-Controller) com interface web completa e API REST.

## 📋 Funcionalidades

### Gestão de Clientes
- Cadastro, consulta, atualização e desativação de clientes
- Validação de CPF e email únicos
- Listagem de pets por cliente
- Interface web com formulários e listagens

### Gestão de Pets
- Cadastro completo de pets com informações detalhadas
- Vinculação com clientes
- Controle de espécie, raça, cor, sexo, peso e observações
- Interface web para gerenciamento

### Gestão de Funcionários
- Cadastro de funcionários com dados pessoais e profissionais
- Controle de cargo, salário e datas de admissão/demissão
- Validação de CPF e email únicos
- Interface web para administração

### Gestão de Serviços
- Cadastro de serviços oferecidos pelo pet shop
- Controle de preços e duração estimada
- Interface web para gerenciamento

### Gestão de Agendamentos
- Sistema completo de agendamento de serviços
- Vinculação de clientes, pets, funcionários e serviços
- Controle de data/hora e status dos agendamentos
- Controle de status (Agendado, Confirmado, Em Andamento, Concluído, Cancelado)
- Validação de conflitos de horário
- Filtros por data, status e funcionário
- Interface web para visualização e gerenciamento

### Sistema de Autenticação
- Sistema de login e registro de usuários
- Controle de sessões
- Interface web para autenticação

## 🏗️ Arquitetura

O sistema segue o padrão MVC (Model-View-Controller) com duas camadas de apresentação:

### Models (Modelos)
Localizados em `src/model/models/`:
- **Cliente**: Dados dos clientes (`cliente.py`)
- **Pet**: Informações dos animais (`pet.py`)
- **Funcionario**: Dados dos funcionários (`funcionario.py`)
- **Servico**: Serviços oferecidos (`servico.py`)
- **Agendamento**: Agendamentos de serviços (`agendamento.py`)
- **User**: Sistema de autenticação (`user.py`)

### Controllers (Controladores)
O sistema possui duas camadas de controladores:

#### API Controllers (`src/controller/api/`)
Controladores REST para integração via API:
- **cliente.py**: CRUD de clientes
- **pet.py**: CRUD de pets
- **funcionario.py**: CRUD de funcionários
- **servico.py**: CRUD de serviços
- **agendamento.py**: CRUD de agendamentos
- **user.py**: Autenticação de usuários

#### View Controllers (`src/controller/views/`)
Controladores para interface web:
- **cliente.py**: Views web de clientes
- **pet.py**: Views web de pets
- **funcionario.py**: Views web de funcionários
- **servico.py**: Views web de serviços
- **agendamento.py**: Views web de agendamentos
- **auth.py**: Views de autenticação

### Views (Visões)
Localizadas em `src/view/templates/`:
- **Interface Web Completa**: Templates HTML com Bootstrap para todas as funcionalidades
- **API REST**: Endpoints JSON para integração externa
- **Sistema de Templates**: Base templates e componentes reutilizáveis
- **Assets Estáticos**: CSS, JavaScript e imagens em `src/view/static/`

### Services e Repositories
- **Services** (`src/model/services/`): Lógica de negócio
- **Repositories** (`src/model/repositories/`): Camada de acesso a dados

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.11+
- pip

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/RaulSimioni/PetShop_MVC.git
cd PetShop_MVC
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Inicialize o banco de dados:
```bash
python init_db.py
```

4. Execute o servidor:
```bash
python src/main.py
```

O servidor estará disponível em:
- **Interface Web**: `http://localhost:5000`
- **API REST**: `http://localhost:5000/api`
- **Dashboard**: `http://localhost:5000/dashboard` (após login)

### Acesso ao Sistema

O sistema possui interface web completa acessível via browser. Para acessar:

1. Abra `http://localhost:5000` no navegador
2. Faça login ou registre-se
3. Acesse o dashboard para gerenciar o pet shop

### Teste do Sistema

Execute os testes automatizados:
```bash
python test_system.py
```

## 📚 API Endpoints

### Usuários/Autenticação
- `POST /api/users/register` - Registrar novo usuário
- `POST /api/users/login` - Login de usuário
- `GET /api/users/profile` - Perfil do usuário atual

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

### Serviços
- `GET /api/servicos` - Listar todos os serviços
- `POST /api/servicos` - Criar novo serviço
- `GET /api/servicos/{id}` - Buscar serviço por ID
- `PUT /api/servicos/{id}` - Atualizar serviço
- `DELETE /api/servicos/{id}` - Desativar serviço

### Agendamentos
- `GET /api/agendamentos` - Listar agendamentos (com filtros opcionais)
- `POST /api/agendamentos` - Criar novo agendamento
- `GET /api/agendamentos/{id}` - Buscar agendamento por ID
- `PUT /api/agendamentos/{id}` - Atualizar agendamento
- `PUT /api/agendamentos/{id}/status` - Atualizar status do agendamento
- `DELETE /api/agendamentos/{id}` - Cancelar agendamento
- `GET /api/agendamentos/cliente/{cliente_id}` - Agendamentos por cliente
- `GET /api/agendamentos/funcionario/{funcionario_id}` - Agendamentos por funcionário

## 🌐 Interface Web

O sistema possui interface web completa com as seguintes páginas:

### Autenticação
- `/login` - Página de login
- `/register` - Página de registro
- `/logout` - Logout do sistema

### Dashboard
- `/dashboard` - Painel principal com resumo do sistema

### Clientes
- `/clientes` - Listar clientes
- `/clientes/novo` - Cadastrar novo cliente
- `/clientes/{id}` - Visualizar cliente
- `/clientes/{id}/editar` - Editar cliente

### Pets
- `/pets` - Listar pets
- `/pets/novo` - Cadastrar novo pet
- `/pets/{id}` - Visualizar pet
- `/pets/{id}/editar` - Editar pet

### Funcionários
- `/funcionarios` - Listar funcionários
- `/funcionarios/novo` - Cadastrar novo funcionário
- `/funcionarios/{id}` - Visualizar funcionário
- `/funcionarios/{id}/editar` - Editar funcionário

### Serviços
- `/servicos` - Listar serviços
- `/servicos/novo` - Cadastrar novo serviço
- `/servicos/{id}` - Visualizar serviço
- `/servicos/{id}/editar` - Editar serviço

### Agendamentos
- `/agendamentos` - Listar agendamentos
- `/agendamentos/novo` - Criar novo agendamento
- `/agendamentos/{id}` - Visualizar agendamento
- `/agendamentos/{id}/editar` - Editar agendamento

## 🗄️ Banco de Dados

O sistema utiliza SQLite por padrão, mas pode ser facilmente configurado para PostgreSQL ou MySQL através das configurações no arquivo `src/config.py`.

### Estrutura das Tabelas

- **users**: Sistema de autenticação
- **clientes**: Dados dos clientes
- **pets**: Informações dos pets
- **funcionarios**: Dados dos funcionários
- **servicos**: Serviços oferecidos
- **agendamentos**: Agendamentos de serviços

### Configurações de Banco

O arquivo `src/config.py` contém três ambientes:
- **Development**: SQLite local para desenvolvimento
- **Production**: Configurado para PostgreSQL em produção
- **Testing**: SQLite em memória para testes

##  Dependências

- **Flask 3.1.1**: Framework web
- **Flask-SQLAlchemy 3.1.1**: ORM para banco de dados
- **Flask-CORS 6.0.0**: Suporte a CORS
- **Flask-Migrate 4.1.0**: Migrações de banco de dados
- **python-dateutil 2.9.0**: Manipulação de datas
- **SQLAlchemy 2.0.41**: ORM e abstração de banco
- **Werkzeug 3.1.3**: Utilitários WSGI
- **Jinja2 3.1.6**: Engine de templates

## 🧪 Dados de Exemplo

O sistema inclui dados de exemplo que são criados automaticamente na inicialização:

- **Funcionários**: Veterinária, Tosador, Atendente
- **Clientes**: Clientes de exemplo com seus respectivos pets
- **Serviços**: Banho, Tosa, Consulta, Vacinação
- **Agendamentos**: Agendamentos de exemplo para demonstração

## 🔒 Segurança

- **Autenticação**: Sistema de login/registro com sessões Flask
- **Validação de dados**: Entrada validada em formulários e API
- **Soft delete**: Desativação em vez de exclusão física dos registros
- **Validação única**: CPF e email únicos para clientes e funcionários
- **Controle de acesso**: Sessões para controle de usuários logados
- **Sanitização**: Prevenção de injeção SQL através do ORM SQLAlchemy

## ⚙️ Estrutura de Configuração

O arquivo `src/config.py` contém três classes de configuração:

### Development
- SQLite local (`database/app.db`)
- Debug habilitado
- Secret key padrão

### Production  
- PostgreSQL configurável via variável de ambiente
- Debug desabilitado
- Secret key via variável de ambiente

### Testing
- SQLite em memória
- Configurações otimizadas para testes

## 🚀 Próximos Passos

O sistema já possui uma base sólida com interface web e API completas. Algumas melhorias futuras podem incluir:

### Funcionalidades Avançadas
1. **Dashboard Analytics**: Gráficos e métricas de desempenho
2. **Relatórios**: Relatórios financeiros e operacionais
3. **Notificações**: Email/SMS para lembretes de agendamento
4. **Sistema de Permissões**: Níveis diferentes de acesso por usuário
5. **Backup Automático**: Backup automático do banco de dados

### Integrações
1. **Pagamentos**: Integração com gateways de pagamento
2. **WhatsApp API**: Comunicação direta com clientes
3. **Calendário**: Sincronização com Google Calendar
4. **Sistema de Estoque**: Controle de produtos e materiais

### Melhorias Técnicas
1. **Testes Unitários**: Cobertura completa de testes
2. **Docker**: Containerização da aplicação
3. **CI/CD**: Pipeline de integração contínua
4. **Monitoramento**: Logs e métricas de sistema

## 🛠️ Desenvolvimento

### Estrutura de Pastas
```
src/
├── controller/          # Controladores
│   ├── api/            # API REST endpoints
│   └── views/          # Controladores web
├── model/              # Camada de dados
│   ├── models/         # Modelos SQLAlchemy
│   ├── repositories/   # Repositórios de dados
│   └── services/       # Lógica de negócio
└── view/               # Interface web
    ├── static/         # CSS, JS, imagens
    └── templates/      # Templates HTML
```

### Adicionando Nova Funcionalidade

1. **Criar Model**: Adicionar em `src/model/models/`
2. **Criar Repository**: Adicionar em `src/model/repositories/`
3. **Criar Service**: Adicionar em `src/model/services/`
4. **Criar API Controller**: Adicionar em `src/controller/api/`
5. **Criar View Controller**: Adicionar em `src/controller/views/`
6. **Criar Templates**: Adicionar em `src/view/templates/`
7. **Registrar Blueprints**: Adicionar em `src/main.py`

## 📄 Licença

Este projeto foi desenvolvido como um sistema ERP completo para Pet Shops, seguindo as melhores práticas de desenvolvimento em Python e Flask.

## 👥 Suporte

Para dúvidas ou sugestões sobre o sistema:
- Consulte a documentação da API em `/api` quando o servidor estiver rodando
- Acesse o dashboard web em `http://localhost:5000/dashboard` para interface visual
- Verifique os logs do sistema para troubleshooting

## 📊 Status do Projeto

✅ **Implementado:**
- Sistema de autenticação completo
- CRUD completo para todas as entidades
- Interface web responsiva com Bootstrap
- API REST completa
- Validações e segurança básica
- Banco de dados SQLite com migrações

🔄 **Em desenvolvimento:**
- Dashboard com analytics
- Sistema de relatórios
- Notificações automáticas
- Testes unitários completos

