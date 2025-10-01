# Caixa de Entrada Inteligente com IA
# 📝 Descrição
Este projeto é uma solução para o Case Prático do processo seletivo da AutoU. O objetivo é criar uma aplicação web que utiliza Inteligência Artificial para automatizar a leitura, classificação e resposta de e-mails, simulando um ambiente corporativo de alto volume de mensagens.

A aplicação classifica os e-mails em categorias (Produtivo ou Improdutivo), extrai informações importantes do texto e sugere múltiplas opções de resposta, otimizando o tempo da equipe e aumentando a produtividade.

# 🚀 Links de Acesso
Aplicação na Nuvem: [Acesse a aplicação aqui](INSIRA O LINK DA SUA APLICAÇÃO HOSPEDADA AQUI)

Vídeo Demonstrativo: [Assista ao vídeo no YouTube](INSIRA O LINK DO SEU VÍDEO AQUI)

# ✨ Funcionalidades
Caixa de Entrada Realista: Interface com tema escuro, abas para e-mails "Recebidos" e "Enviados".

Classificação com IA: Análise automática para categorizar e-mails em Produtivo (requer ação) ou Improdutivo.

Extração de Entidades: A IA identifica e extrai dados importantes do corpo do e-mail (ex: número de contrato, CPF, valores).

Múltiplas Sugestões de Resposta: Para e-mails produtivos, a IA oferece 3 templates de resposta com tons diferentes (formal, amigável, direto).

Resposta Rápida: Botão para preencher o compositor de e-mail automaticamente com a sugestão escolhida.

Lógica Inteligente: O botão de resposta é desabilitado para e-mails improdutivos, evitando ações desnecessárias.

Upload de Arquivos: Permite analisar e-mails a partir de arquivos .txt.

Busca e Filtro: Funcionalidade de busca para encontrar e-mails por remetente ou assunto.

Notificações Modernas: Feedbacks de sucesso ou erro através de notificações "toast", sem alerts que interrompem o fluxo.

Interface Focada: O compositor de e-mail é escondido ao visualizar uma mensagem para uma melhor experiência de leitura.

# 🛠️ Tecnologias Utilizadas
Backend: Python 3, Flask

Inteligência Artificial: API da Groq (Modelo Llama 3.1)

Frontend: HTML5, CSS3, JavaScript (sem frameworks)

Hospedagem: Render

Dependências Python: Flask-Cors, Requests, python-dotenv, Gunicorn

# 📂 Estrutura do Projeto

```bash
email-classifier/
├── .gitignore
├── README.md
├── app.py              # Lógica do backend e API
├── requirements.txt    # Dependências do Python
├── scripts/
│   ├── run.bat         # Script para rodar a aplicação
│   └── setup.bat       # Script para configurar o ambiente
└── templates/
    └── index.html      # Interface do usuário
   ``` 

# ⚙️ Como Executar Localmente
Siga os passos abaixo para rodar o projeto em seu computador.

Pré-requisitos:

Python 3.x

Git

1. Clone o Repositório:

git clone [https://github.com/RenatoCortesAraujo/email-classifier.git](https://github.com/RenatoCortesAraujo/email-classifier.git)
cd email-classifier

2. Configure o Ambiente (Windows):
Execute o script de configuração para criar o ambiente virtual e instalar as dependências.

# Navegue até a pasta de scripts e execute o setup
.\scripts\setup.bat

(Para outros sistemas, crie um ambiente virtual manualmente e instale as dependências com pip install -r requirements.txt)

3. Crie o Arquivo de Variáveis de Ambiente:

Crie um arquivo chamado .env na raiz do projeto.

Adicione sua chave da API da Groq dentro dele, como no exemplo abaixo:

GROQ_API_KEY="sua_chave_secreta_aqui"

4. Rode a Aplicação (Windows):
Execute o script para iniciar o servidor.

.\scripts\run.bat
