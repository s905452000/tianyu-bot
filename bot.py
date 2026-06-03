import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")
logging.basicConfig(level=logging.INFO)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🏢 辦公室出租", callback_data="office"),
         InlineKeyboardButton("📑 公司註冊", callback_data="company")],
        [InlineKeyboardButton("🌏 簽證服務", callback_data="visa"),
         InlineKeyboardButton("🚗 包車租車", callback_data="car")],
        [InlineKeyboardButton("🛂 護照規劃", callback_data="passport"),
         InlineKeyboardButton("📞 聯繫客服", callback_data="contact")],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 返回", callback_data="back")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌏 *天宇集團 TIANYU GROUP*\n\n歡迎！請選擇服務：",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    info = {
        "office": "🏢 *辦公室出租*\n\n越南、菲律賓、杜拜、斯里蘭卡、馬來西亞。\n\n聯繫：@TY_6789",
        "company": "📑 *公司註冊*\n\n東南亞各國公司註冊服務。\n\n聯繫：@TY_6789",
        "visa": "🌏 *簽證服務*\n\n各類簽證辦理。\n\n聯繫：@TY_6789",
        "car": "🚗 *包車租車*\n\n東南亞包車租車服務。\n\n聯繫：@TY_6789",
        "passport": "🛂 *護照規劃*\n\n第三國護照規劃。\n\n聯繫：@TY_6789",
        "contact": "📞 *聯繫客服*\n\n👤 @TY_6789\n\n24小時服務",
    }
    if data == "back":
        await query.edit_message_text("🌏 *天宇集團*\n\n請選擇服務：", parse_mode="Markdown", reply_markup=main_menu())
    elif data in info:
        await query.edit_message_text(info[data], parse_mode="Markdown", reply_markup=back_menu())

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
