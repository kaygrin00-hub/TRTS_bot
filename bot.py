import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ["TOKEN"]

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 Проверить документ", callback_data="check")],
        [InlineKeyboardButton("🧮 Рассчитать стоимость", callback_data="price")],
        [InlineKeyboardButton("📝 Оставить заявку", callback_data="contact")],
        [InlineKeyboardButton("❓ Вопросы по ТРТС", callback_data="faq")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Привет! Выберите раздел:", reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Напишите @TRTS_RF_bot для связи с менеджером")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Оставьте заявку:\n\nИмя:\nТелефон:\nЧто интересует:")

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Частые вопросы:\n\n1. Сколько стоит сертификация?\n2. Сроки?\n3. Какие документы нужны?\n\nНапишите ваш вопрос — ответим!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = f"📝 Заявка от {user.first_name} (@{user.username}):\n\n{update.message.text}"
    await context.bot.send_message(chat_id=os.environ["CHAT_ID"], text=text)
    await update.message.reply_text("Спасибо! Заявка отправлена. Свяжемся с вами.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=os.environ["WEBHOOK_URL"]
    )

if __name__ == "__main__":
    main()