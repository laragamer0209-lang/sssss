import os
import time
import threading
import json
import urllib.request
import urllib.parse
from flask import Flask

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = os.getenv("9005514591:AAGGJE9Uk0UYGeowY276YPhG-l3hRtA44ZA")

# Servidor web simples para o Render manter o bot ativo 24/7
app = Flask(__name__)

@app.route('/')
def home():
    return "Jarvis está online na nuvem 24/7!"

def enviar_mensagem_telegram(chat_id, texto):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        dados = urllib.parse.urlencode({'chat_id': chat_id, 'text': texto}).encode('utf-8')
        req = urllib.request.Request(url, data=dados)
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Erro ao enviar: {e}")

def escutar_telegram():
    print("[Telegram Nuvem] Jarvis ativo e à escuta...")
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=35) as resposta:
                resultado = json.loads(resposta.read().decode('utf-8'))
                if resultado.get("ok"):
                    for update in resultado.get("result", []):
                        offset = update["update_id"] + 1
                        if "message" in update and "text" in update["message"]:
                            chat_id = update["message"]["chat"]["id"]
                            texto_recebido = update["message"]["text"]
                            print(f"Recebido: {texto_recebido}")

                            # Resposta automática na nuvem
                            resposta_ia = f"Recebi a tua mensagem: '{texto_recebido}'. (Estou a correr 24/7 na nuvem!)"
                            enviar_mensagem_telegram(chat_id, resposta_ia)
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    # Inicia o ouvinte do Telegram numa thread em segundo plano
    t = threading.Thread(target=escutar_telegram, daemon=True)
    t.start()

    # Inicia o servidor web na porta exigida pelo Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)