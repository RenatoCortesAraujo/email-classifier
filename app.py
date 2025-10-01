from flask import Flask, render_template, request, jsonify
import os
import requests
import json
from dotenv import load_dotenv
from flask_cors import CORS

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app) # Habilita o CORS para a aplicação

# --- Simulação de uma base de dados em memória ---
inbox_emails = [
    {
        "id": 1,
        "remetente": "contato@startupxyz.com",
        "assunto": "Re: Dúvida sobre Fatura #1234",
        "corpo": "Prezados, poderiam por favor me confirmar o recebimento da fatura #1234? Preciso do comprovante para o fechamento do mês. Obrigado!",
        "categoria": "Produtivo",
        "entidades": {"numero_fatura": "1234"},
        "sugestao_resposta": [
            "Prezado(a), confirmamos o recebimento da fatura #1234. O comprovante segue em anexo. Atenciosamente.",
            "Olá! Fatura #1234 recebida. Comprovante em anexo. Abraços!",
            "Recebimento da fatura #1234 confirmado. Anexo."
        ]
    },
    {
        "id": 2,
        "remetente": "marketing@lojaonline.com",
        "assunto": "Promoção Imperdível de Aniversário!",
        "corpo": "Não perca! 50% de desconto em todo o site para celebrar nosso aniversário. Apenas esta semana!",
        "categoria": "Improdutivo",
        "entidades": {},
        "sugestao_resposta": ["Nenhuma ação necessária.", "Nenhuma ação necessária.", "Nenhuma ação necessária."]
    }
]
email_id_counter = len(inbox_emails)

# --- Configuração da API da Groq ---
API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("A chave da API da Groq (GROQ_API_KEY) não foi encontrada. Verifique seu arquivo .env")

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def analisar_email_com_ia(email_content):
    """
    Usa a API da Groq para analisar o email, extrair entidades e gerar 3 sugestões de resposta.
    """
    prompt = f"""
    Sua tarefa é analisar um email no contexto de um ambiente de trabalho corporativo e retornar um objeto JSON.
    1.  **Classifique** o email em 'Produtivo' ou 'Improdutivo', com base na necessidade de uma ação de trabalho. E-mails pessoais ou acadêmicos são 'Improdutivo'.
    2.  **Extraia Entidades Relevantes**: Identifique e extraia dados importantes do email. Se não encontrar, retorne um objeto vazio. Entidades a extrair: "numero_contrato", "cpf", "cnpj", "numero_fatura", "data_importante", "valor_monetario".
    3.  **Elabore 3 Rascunhos de Resposta**: Crie três variações de resposta (formal, amigável, direta). Se o email for 'Improdutivo', as três respostas devem ser "Nenhuma ação necessária.".

    Retorne tudo estritamente como um objeto JSON com as chaves: "categoria", "entidades" (um objeto) e "sugestao_resposta" (uma lista de 3 strings). Não adicione nenhum texto antes ou depois do objeto JSON.

    Email para análise:
    ---
    {email_content}
    ---
    """
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Você é um assistente de IA especialista em analisar e classificar e-mails em um contexto de negócios, retornando a análise em formato JSON estruturado."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 512,
        "response_format": {"type": "json_object"}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        json_string = result['choices'][0]['message']['content']
        return json.loads(json_string)
    except requests.exceptions.Timeout:
        return {"error": "O serviço de IA demorou muito para responder."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Problema de comunicação com o serviço de IA: {e.response.text if e.response else e}"}
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": "A resposta da IA não veio no formato esperado."}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emails', methods=['GET'])
def get_emails():
    return jsonify(sorted(inbox_emails, key=lambda x: x['id'], reverse=True))

@app.route('/processar', methods=['POST'])
def processar_email():
    global email_id_counter
    dados = request.get_json()
    remetente = dados.get('remetente', 'desconhecido@email.com')
    assunto = dados.get('assunto')
    corpo = dados.get('corpo')

    if not assunto or not corpo:
        return jsonify({"error": "Assunto e corpo do email são obrigatórios."}), 400

    texto_completo = f"Assunto: {assunto}\n\n{corpo}"
    resultado_ia = analisar_email_com_ia(texto_completo)
    
    if not resultado_ia or 'error' in resultado_ia:
        error_message = resultado_ia.get('error', 'Erro desconhecido na análise da IA.')
        return jsonify({"error": error_message}), 500

    email_id_counter += 1
    novo_email = {
        "id": email_id_counter,
        "remetente": remetente,
        "assunto": assunto,
        "corpo": corpo,
        "categoria": resultado_ia.get('categoria', 'Indefinida'),
        "entidades": resultado_ia.get('entidades', {}),
        "sugestao_resposta": resultado_ia.get('sugestao_resposta', ['N/A'])
    }
    inbox_emails.append(novo_email)

    return jsonify({"status": "success", "email": novo_email}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5001)

