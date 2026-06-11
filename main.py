import os
import telebot
from flask import Flask
from threading import Thread

# Configuración básica para engañar a Render
app = Flask(__name__)
@app.route('/')
def home():
    return "El bot está activo"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Configuración del bot
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8747406142

@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    try:
        if message.from_user.id != ADMIN_ID:
            if "http" in message.text or "t.me" in message.text:
                bot.delete_message(message.chat.id, message.message_id)
                bot.send_message(message.chat.id, "⚠️ Enlace eliminado.")
    except Exception as e:
        print(e)

# Iniciar el servidor web y el bot al mismo tiempo
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()
