# Cadastro de Alunos com Notificação por E-mail

Aplicação web desenvolvida em **Python e Flask** para gerenciamento de cadastros de alunos e envio automatizado de notificações por e-mail utilizando a API do Mailgun.

O projeto utiliza uma arquitetura modular, banco de dados SQLite e testes automatizados com Pytest, buscando facilitar a manutenção, a organização e a evolução da aplicação.

## Funcionalidades

- **Cadastro de alunos:** registro de informações dos alunos por meio de formulário.
- **Consulta de registros:** visualização dos alunos cadastrados.
- **Edição de alunos:** atualização dos dados de registros existentes.
- **Exclusão de alunos:** remoção de registros cadastrados.
- **Notificações por e-mail:** envio de mensagens utilizando a API do Mailgun.
- **Destinatários configuráveis:** envio para endereços definidos na configuração da aplicação.
- **E-mail adicional:** possibilidade de informar um destinatário extra no formulário.
- **Histórico de envios:** armazenamento e consulta dos registros de e-mails enviados.
- **Tratamento de erros:** controle de falhas durante o processo de envio.
- **Testes automatizados:** validação das funcionalidades utilizando Pytest.

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem de programação |
| Flask | Framework web |
| Flask-WTF | Construção e validação de formulários |
| Flask-SQLAlchemy | Integração com banco de dados |
| Flask-Migrate | Controle de migrações |
| Flask-Bootstrap | Componentes de interface |
| Flask-Moment | Formatação de datas e horários |
| SQLite | Banco de dados |
| Mailgun API | Envio de e-mails |
| Requests | Requisições HTTP |
| Pytest | Testes automatizados |

## Estrutura do projeto

A aplicação está organizada em módulos, separando a inicialização, as rotas, os modelos, os serviços e os testes.

```text
cadastro-alunos-email/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   └── models.py
│
├── main/
│   ├── __init__.py
│   ├── errors.py
│   └── views.py
│
├── services/
│   ├── __init__.py
│   └── email_service.py
│
├── tests/
│   ├── test_app.py
│   └── test_email_service.py
│
├── templates/
│   └── index.html
│
├── static/
│
├── migrations/
│
├── config.py
├── forms.py
├── flasky.py
├── requirements.txt
└── README.md
```

*Estrutura representativa dos principais arquivos e diretórios.*

## Organização por módulos

### `app/`

Responsável pela inicialização da aplicação Flask, configuração das extensões e definição dos modelos utilizados no banco de dados.

### `main/`

Contém o Blueprint principal, as rotas da aplicação, as funcionalidades de cadastro, edição, exclusão e o tratamento de erros.

### `services/`

Centraliza serviços separados da lógica das rotas. O módulo `email_service.py` é responsável pela comunicação com a API do Mailgun e pelo envio das notificações.

### `tests/`

Armazena os testes automatizados das funcionalidades da aplicação e do serviço de envio de e-mails.

### `migrations/`

Armazena os arquivos utilizados para controlar as alterações na estrutura do banco de dados.

## Como funciona o envio de e-mails

1. O usuário preenche e envia o formulário de cadastro.
2. A aplicação valida e processa as informações.
3. O serviço de e-mail reúne os destinatários configurados e o endereço adicional, quando informado.
4. A mensagem é enviada por meio da API do Mailgun.
5. O conteúdo da mensagem inclui as informações do cadastro.
6. Quando o Mailgun aceita a solicitação, o resultado é registrado no banco de dados.
7. Os registros podem ser consultados na página de histórico de e-mails enviados.

**Observação:** a aceitação da solicitação pelo Mailgun não garante, por si só, a entrega final da mensagem na caixa de entrada do destinatário.

## Configuração do ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/Jhon0498/cadastro-alunos-email.git
cd cadastro-alunos-email
```

### 2. Criar um ambiente virtual

```bash
python -m venv venv
```

Ativação no Windows:

```bash
venv\Scripts\activate
```

Ativação no Linux:

```bash
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Configure as credenciais e os parâmetros necessários no ambiente de execução:

```env
FLASKY_ADMIN=seu-email@exemplo.com
MAILGUN_API_KEY=sua-chave-do-mailgun
MAILGUN_DOMAIN=seu-dominio-configurado-no-mailgun
MAILGUN_BASE_URL=https://api.mailgun.net
SECRET_KEY=sua-chave-secreta
```

Substitua os valores de exemplo pelos dados da sua configuração.

**Segurança:** não publique arquivos `.env`, chaves de API, senhas ou bancos de dados com informações reais no GitHub.

## Executar a aplicação

Com as dependências instaladas e as configurações necessárias definidas:

```bash
python flasky.py
```

A aplicação será iniciada conforme as configurações definidas no projeto.

## Executar os testes

Para executar os testes automatizados:

```bash
python -m pytest -v tests/
```

Os testes verificam as principais funcionalidades e simulam respostas da API do Mailgun, evitando o envio de mensagens reais durante os testes do serviço.

## Hospedagem

O projeto está configurado para execução no **PythonAnywhere**, ambiente utilizado para hospedar a aplicação Flask.

## Repositório

GitHub: https://github.com/Jhon0498/cadastro-alunos-email
