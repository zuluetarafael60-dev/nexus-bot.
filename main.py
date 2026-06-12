import os
import telebot
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot activo"

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN, threaded=False)
ADMIN_ID = 8747406142 # Tu ID

@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    # Si el mensaje es tuyo (Admin), no hacemos nada
    if message.from_user.id == ADMIN_ID:
        return

    text = message.text.lower()
    
    # Lista de elementos que el bot borrará automáticamente
    spam_keywords = ["http", "https", "t.me", ".com", ".net", ".org", "www."]
    
    # Comprobamos si el mensaje contiene algo de la lista
    if any(keyword in text for keyword in spam_keywords):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run).start()
    
    # PASO CRÍTICO: Limpiar cualquier rastro previo antes de iniciar
    bot.remove_webhook()
    
    # Usamos infinity_polling con skip_pending=True para ignorar mensajes antiguos
    # que causan el error 409
    bot.infinity_polling(skip_pending=True)
