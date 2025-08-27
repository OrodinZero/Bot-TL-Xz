import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
import openai

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_KEY

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku bot AI. Ketik pertanyaanmu atau gunakan /help untuk lihat fitur.")

# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Perintah yang tersedia:\n"
        "/start - Mulai bot\n"
        "/help - Lihat perintah\n"
        "/img <prompt> - Buat gambar AI\n"
        "/code <prompt> - Generate kode program\n"
        "\nKetik pesan biasa untuk tanya apa saja."
    )

# Chat GPT-4
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        answer = response['choices'][0]['message']['content']
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Terjadi kesalahan:\n{str(e)}")

# Generate Gambar AI
async def handle_image_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Contoh penggunaan: /img naga di atas motor terbang")
        return
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        await update.message.reply_photo(image_url)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Gagal generate gambar:\n{str(e)}")

# Generate Kode
async def handle_code_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Contoh: /code buat fungsi python hitung luas segitiga")
        return
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Tolong buatkan kode:\n{prompt}"}]
        )
        answer = response['choices'][0]['message']['content']
        await update.message.reply_text(f"```python\n{answer}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Gagal generate kode:\n{str(e)}")

# MAIN
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("img", handle_image_prompt))
    app.add_handler(CommandHandler("code", handle_code_prompt))

    # Chat Handler (Default)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()
