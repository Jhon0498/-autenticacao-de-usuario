# Atualização — Autenticação de Usuários Flasky

## Sobre a atualização

Nesta atualização, foi implementado o sistema de autenticação de usuários no projeto Flasky, permitindo realizar cadastro de contas, login, logout e confirmação de e-mail.

A implementação utiliza Flask, Flask-Login, Flask-WTF e SQLAlchemy.

## Funcionalidades implementadas

- Cadastro de novos usuários.
- Login utilizando e-mail e senha.
- Logout de usuários autenticados.
- Criptografia de senhas com hash.
- Verificação de senhas cadastradas.
- Geração de tokens para confirmação de contas.
- Envio de e-mail de confirmação utilizando Mailgun.
- Restrição de acesso para usuários que ainda não confirmaram suas contas.
- Opção para solicitar um novo e-mail de confirmação.
- Menu de navegação dinâmico conforme o estado de autenticação.

## Rotas da aplicação

| Rota | Funcionalidade |
|---|---|
| `/` | Página inicial do Flasky |
| `/login` | Login de usuários |
| `/logout` | Encerrar sessão |
| `/register` | Cadastro de contas |
| `/unconfirmed` | Página de conta não confirmada |
| `/confirm/<token>` | Confirmar conta pelo token |
| `/confirm` | Solicitar novo e-mail de confirmação |
| `/cadastro` | Cadastro de alunos |
| `/emails-enviados` | Histórico de e-mails enviados |

## Segurança

As senhas não são armazenadas em texto puro. O sistema utiliza hash seguro para armazenar e verificar as senhas.

A confirmação de conta é realizada por meio de tokens assinados, e usuários não confirmados possuem restrições de acesso às demais páginas da aplicação.

## Organização dos arquivos

- `app/__init__.py`: inicialização da aplicação.
- `app/models.py`: modelos do banco de dados.
- `app/extensions.py`: extensões utilizadas.
- `app/auth/forms.py`: formulários de login e cadastro.
- `app/auth/views.py`: rotas de autenticação.
- `app/email.py`: envio dos e-mails de confirmação.
- `templates/auth/`: páginas e modelos de e-mail da autenticação.
- `templates/home.html`: página inicial do Flasky.
- `tests/test_auth.py`: testes de autenticação.

## Testes

Para executar os testes automatizados, utilize:

```bash
python -m pytest -v tests/
```

Os testes verificam as páginas principais, autenticação, cadastro, confirmação de contas, envio de e-mails e proteção de senhas.

## Serviços de e-mail

O envio de e-mails de confirmação utiliza a API do Mailgun.

As credenciais devem ser configuradas em variáveis de ambiente, sem serem publicadas no GitHub.

## Observação

As funcionalidades anteriores de cadastro de alunos e histórico de e-mails foram mantidas durante a implementação da autenticação.

---

**Projeto:** Flasky — Autenticação de Usuários  
**Atualização:** Implementação do sistema de autenticação e confirmação de contas.
