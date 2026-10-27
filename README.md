# Cadastro de Alunos com Notificação por E-mail

Aplicação web desenvolvida em Python com Flask para realizar o cadastro de alunos e enviar notificações por e-mail utilizando a API do Mailgun.

O projeto foi organizado em módulos para facilitar a manutenção, a organização do código e a realização de testes automatizados.

## Funcionalidades

- Cadastro de usuários com nome e usuário.
- Utilização do prontuário `PT3026931`.
- Envio de notificações por meio da API do Mailgun.
- Envio para os destinatários configurados na aplicação, incluindo o endereço institucional e `flaskaulasweb@zohomail.com`.
- Campo para informar um endereço de e-mail adicional.
- Registro dos envios de e-mail no banco de dados.
- Página para consultar o histórico de e-mails enviados.
- Tratamento de erros durante o envio de mensagens.
- Testes automatizados com pytest.

## Tecnologias utilizadas

- Python
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bootstrap
- Flask-Moment
- SQLite
- Mailgun API
- Requests
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
│   └── views.py
├── models/
│   ├── __init__.py
│   └── usuario.py
├── services/
│   ├── __init__.py
│   └── email_service.py
├── tests/
│   ├── test_app.py
│   └── test_email_service.py
├── templates/
│   └── index.html
├── static/
├── config.py
├── forms.py
├── flasky.py
├── requirements.txt
└── README.md
```

**Observação:** a estrutura acima representa os principais arquivos do projeto. Outros templates, arquivos estáticos e arquivos de migração podem existir no repositório.

## Organização por módulos

### `app/`

Contém a criação da aplicação Flask, as extensões utilizadas, as configurações e os modelos do banco de dados.

### `main/`

Contém o Blueprint principal, as visualizações e o tratamento de erros da aplicação.

### `services/`

Contém os serviços separados da lógica das páginas. O arquivo `email_service.py` é responsável por preparar e enviar as notificações pelo Mailgun.

### `models/`

Contém o pacote de modelos auxiliares. Os modelos atualmente utilizados pela aplicação estão definidos em `app/models.py`.

### `tests/`

Contém os testes automatizados das páginas e do serviço de envio de e-mails.

## Configuração do Mailgun

A aplicação utiliza a API do Mailgun para enviar notificações, evitando depender de um servidor SMTP local.

Configure as variáveis de ambiente necessárias no arquivo `.env`, de acordo com a leitura realizada em `config.py`:

```dotenv
FLASKY_ADMIN=flaskaulasweb@zohomail.com,seu-email-institucional
MAILGUN_API_KEY=sua-chave-do-mailgun
MAILGUN_DOMAIN=seu-dominio-configurado-no-mailgun
MAILGUN_BASE_URL=https://api.mailgun.net
SECRET_KEY=sua-chave-secreta
```

Substitua os valores de exemplo pelos dados da sua configuração. Utilize o endereço institucional real no lugar de `seu-email-institucional`.

**Importante:** não publique o arquivo `.env`, chaves de API ou senhas no GitHub. Os destinatários também devem estar configurados corretamente no ambiente de execução.

## Como funciona o envio de e-mails

1. O usuário preenche e envia o formulário de cadastro.
2. A aplicação processa os dados informados.
3. O serviço de e-mail reúne os destinatários configurados e o endereço adicional, quando fornecido.
4. A mensagem é enviada por meio da API do Mailgun.
5. A mensagem contém o usuário cadastrado, o nome do aluno e o prontuário.
6. Quando o Mailgun aceita a solicitação, a aplicação registra o resultado no banco de dados.
7. O histórico pode ser consultado na página `/emails-enviados`.

A aceitação da solicitação pelo Mailgun não garante, por si só, a entrega final da mensagem na caixa de entrada.

## Executar os testes

Para executar os testes automatizados, utilize:

```bash
python -m pytest -v tests/
```

Os testes verificam as páginas principais e simulam respostas da API do Mailgun, permitindo testar o serviço sem enviar mensagens reais.

## Executar a aplicação

Com as dependências instaladas e as variáveis de ambiente configuradas, execute:

```bash
python flasky.py
```

O comando inicia a aplicação conforme a configuração definida no projeto. Em ambientes hospedados, como o PythonAnywhere, siga também as configurações específicas do servidor.

## Repositório

GitHub: https://github.com/Jhon0498/cadastro-alunos-email
