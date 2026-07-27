# 🤖 Robô de Automação - Hi Platform (Opt-out)

Este é um script de automação desenvolvido em Python utilizando o **Selenium WebDriver**. O objetivo principal do robô é navegar pela plataforma Hi Platform/Akna e processar rotinas de e-mails de forma automatizada, economizando horas de trabalho manual.

## 🚀 Funcionalidades

- **Navegação Automatizada:** Faz login e percorre as páginas de ações automaticamente (processando milhares de registros).
- **Filtro Inteligente:** Identifica e ignora status inválidos (como "Arquivada" e "Não agendada") para focar apenas nas ações necessárias.
- **Idempotência (Histórico):** Utiliza um arquivo `historico_acoes.txt` local para registrar o que já foi feito, impedindo que o robô processe o mesmo item duas vezes caso seja reiniciado.
- **Segurança de Credenciais:** Arquitetura segura que separa as credenciais (`credenciais.py`) do código principal, mantendo dados sensíveis fora do controle de versão.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Selenium** (Automação web)
- **VS Code** (Ambiente de desenvolvimento)

## 🔒 Aviso sobre clonagem
Para rodar este projeto localmente, é necessário criar um arquivo `credenciais.py` na raiz do projeto contendo as variáveis `EMAIL_LOGIN` e `SENHA_LOGIN` com os dados de acesso à plataforma.
