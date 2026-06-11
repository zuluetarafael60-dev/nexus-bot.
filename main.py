import os
import telebot
from flask import Flask
from threading import Thread

# Configuración de Flask para que Render crea que es un servicio web
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot activo"

# Configuración del bot
TOKEN = os.environ.get('TOKEN')
# Usamos 'threaded=False' para evitar conflictos de concurrencia
bot = telebot.TeleBot(TOKEN, threaded=False)
ADMIN_ID = 8747406142

@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    try:
        # El admin tiene inmunidad
        if message.from_user.id != ADMIN_ID:
            text = message.text.lower()
            
            # Lista extensa de detección
            spam_keywords = [
                "http", "https", "t.me", ".com", ".net", ".org", ".io", 
                ".xyz", ".me", ".info", ".biz", "www.", "bit.ly", "tinyurl",
                ".co", ".gl", ".tk", ".ml", ".club", ".top"
            ]
            
            # Verificación lógica
            if any(keyword in text for keyword in spam_keywords):
                bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Error detectado: {e}")

# Servidor web en segundo plano
def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    # Inicia el hilo web
    Thread(target=run).start()
    
    # IMPORTANTE: Eliminamos cualquier Webhook antiguo antes de iniciar el polling
    bot.remove_webhook()
    
    # Iniciamos el polling de forma más conservadora
    bot.infinity_polling(timeout=20, long_polling_timeout=20)
