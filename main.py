
import os
import telebot
from flask import Flask
from threading import Thread

# Configuración básica para mantener vivo el proceso en Render
app = Flask(__name__)
@app.route('/')
def home():
    return "El bot está activo y vigilando."

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Configuración del bot
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8747406142

@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    try:
        # Si el mensaje proviene del administrador, el bot lo ignora completamente
        if message.from_user.id != ADMIN_ID:
            
            # Convertimos el texto a minúsculas para detectar enlaces aunque usen Mayúsculas
            text = message.text.lower()
            
            # Lista completa de términos que identifican enlaces o spam
            # Incluye extensiones comunes y dominios sospechosos
            spam_keywords = [
                "http", "https", "t.me", ".com", ".net", ".org", ".io", 
                ".xyz", ".me", ".info", ".biz", "www.", "bit.ly", "tinyurl"
            ]
            
            # Verificamos si alguna de esas palabras está en el mensaje
            if any(keyword in text for keyword in spam_keywords):
                bot.delete_message(message.chat.id, message.message_id)
                # El bot borra y no responde nada para ser discreto (o puedes descomentar la siguiente línea)
                # bot.send_message(message.chat.id, "⚠️ Enlace detectado y eliminado.")
    except Exception as e:
        print(f"Error al procesar mensaje: {e}")

# Iniciar el servidor web y el bot al mismo tiempo
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()
