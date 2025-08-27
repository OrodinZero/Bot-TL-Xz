from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Fungsi untuk menangani perintah /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Halo! Aku siap membantu!')

# Fungsi untuk menangani pesan masuk
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    # Panggil API Venice.ai untuk memproses pesan
    response = requests.post('https://api.venice.ai/v1/chat/completions', json={"prompt": user_message})
    ai_response = response.json()['choices'][0]['message']['content']
    update.message.reply_text(ai_response)

def main() -> None:
    # Ganti 'YOUR_TELEGRAM_BOT_TOKEN' dengan token bot Telegram kamu
    updater = Updater("8426056007:AAFeqRjKhkczX6rWKGcG0ou7TZ3JNgxV_C8")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
