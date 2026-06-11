import os
import telebot

# Recupera el token desde las variables de entorno de Render
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 8747406142

@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    try:
        # Si el mensaje no es del admin y tiene enlaces
        if message.from_user.id != ADMIN_ID:
            if "http" in message.text or "t.me" in message.text:
                bot.delete_message(message.chat.id, message.message_id)
                # Usamos send_message en lugar de reply_to para evitar errores de referencia
                bot.send_message(message.chat.id, f"⚠️ @{message.from_user.username}, enlace eliminado. Solo el admin puede enviar enlaces.")
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

bot.infinity_polling()
