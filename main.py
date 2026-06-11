import telebot

# SUSTITUYE EL TOKEN POR EL NUEVO QUE TE DÉ BOTFATHER
TOKEN ='8689021231:AAEMchNL1ty54Kr8McGSrqbHjE6fCtx8Vmg'
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 8747406142

@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    if message.from_user.id != ADMIN_ID:
        if "http" in message.text or "t.me" in message.text:
            bot.delete_message(message.chat.id, message.message_id)
            bot.reply_to(message, "⚠️ Enlace detectado y eliminado. Solo el administrador puede enviar enlaces.")

bot.polling()
