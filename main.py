import os
import telebot
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot en funcionamiento"

# Configuración del bot
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8747406142

# Filtro mejorado
@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    try:
        if message.from_user.id != ADMIN_ID:
            text = message.text.lower()
            spam_keywords = ["http", "https", "t.me", ".com", ".net", ".org", ".io", ".xyz", ".me", ".info", ".biz", "www.", "bit.ly", "tinyurl"]
            if any(keyword in text for keyword in spam_keywords):
                bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Error: {e}")

# Ejecución
def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    # Inicia el servidor web en un hilo
    Thread(target=run).start()
    # Inicia el bot sin forzar múltiples conexiones
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
