# Sistema de Cadastro de Alunos com Notificação por E-mail

Aplicação web desenvolvida em Python com Flask para cadastrar usuários e enviar notificações por e-mail utilizando a API do Mailgun.

## Funcionalidades

- Cadastro de usuários por formulário.
- Validação dos dados informados.
- Verificação de usuários já cadastrados.
- Envio de notificações por e-mail usando o Mailgun.
- Inclusão do e-mail informado no formulário como destinatário adicional.
- Envio de informações do cadastro, incluindo nome, usuário e prontuário fixo `PT3026931`.
- Registro e consulta dos e-mails enviados.
- Testes automatizados com Pytest.

## Tecnologias utilizadas

- Python
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Requests
- Mailgun API
- Pytest

## Estrutura do projeto

```text
cadastro-alunos-email/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   └── models.py
├── main/
│   ├── __init__.py
│   ├── errors.py
│   ├── routes.py
│   └── views.py
├── migrations/
├── templates/
├── tests/
├── forms.py
├── config.py
├── flasky.py
├── requirements.txt
└── .gitignore
```

A estrutura acima é ilustrativa. Os arquivos listados devem corresponder à versão atual do repositório.

## Como executar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/Jhon0498/cadastro-alunos-email.git
cd cadastro-alunos-email
```

### 2. Criar e ativar um ambiente virtual

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

No Linux ou macOS:

```bash
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Configure as variáveis necessárias no arquivo `.env`, de acordo com `config.py`:

- `SECRET_KEY` ou `FLASK_SECRET_KEY`
- `DATABASE_URL`, caso seja utilizada uma URL de banco de dados personalizada
- `FLASKY_ADMIN`
- `MAILGUN_API_KEY`
- `MAILGUN_DOMAIN`
- `MAILGUN_BASE_URL`, se necessário

Não publique senhas, tokens ou chaves privadas no GitHub.

### 5. Executar a aplicação

```bash
python flasky.py
```

O endereço local padrão do Flask é:

```text
http://127.0.0.1:5000
```

## Testes

Execute os testes automatizados com:

```bash
python -m pytest -v tests/
```

## Objetivo acadêmico

Projeto desenvolvido para praticar o desenvolvimento de aplicações web com Flask, formulários, banco de dados, organização modular, envio de notificações por API e testes automatizados.

## Autor

Jhonatan Mendes Morão

## Licença

Projeto desenvolvido para fins educacionais.
