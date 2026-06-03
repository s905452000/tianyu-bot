import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import os
TOKEN = os.environ.get("TOKEN")


logging.basicConfig(level=logging.INFO)

# 多语言内容
TEXTS = {
    "zh_tw": {
        "welcome": """🌏 *天宇集團 TIANYU GROUP*

歡迎使用天宇集團官方助手！

我們提供以下服務：
🏢 東南亞辦公室出租
📑 公司註冊｜牌照掛靠
🌏 簽證｜保關｜回程機票
🚗 包車租車｜駕照代辦
🛂 第三國護照規劃

🇻🇳 越南 🇵🇭 菲律賓 🇦🇪 杜拜
🇱🇰 斯里蘭卡 🇲🇾 馬來西亞

請選擇服務：""",
        "office": "🏢 *東南亞辦公室出租*\n\n我們在越南、菲律賓、杜拜、斯里蘭卡、馬來西亞提供優質辦公室出租服務。\n\n如需查詢，請聯繫客服。",
        "company": "📑 *公司註冊｜牌照掛靠*\n\n提供東南亞各國公司註冊及牌照掛靠服務，手續簡便，快速辦理。\n\n如需查詢，請聯繫客服。",
        "visa": "🌏 *簽證｜保關｜回程機票*\n\n提供各類簽證辦理、保關及回程機票安排服務。\n\n如需查詢，請聯繫客服。",
        "car": "🚗 *包車租車｜駕照代辦*\n\n提供東南亞各國包車、租車及駕照代辦服務。\n\n如需查詢，請聯繫客服。",
        "passport": "🛂 *第三國護照規劃*\n\n專業第三國護照規劃服務，為您提供最佳方案。\n\n如需查詢，請聯繫客服。",
        "contact": "📞 *聯繫客服*\n\n請直接聯繫我們的客服人員：\n👤 @TY_6789\n\n服務時間：24小時",
        "back": "🔙 返回主選單",
        "btn_office": "🏢 辦公室出租",
        "btn_company": "📑 公司註冊",
        "btn_visa": "🌏 簽證服務",
        "btn_car": "🚗 包車租車",
        "btn_passport": "🛂 護照規劃",
        "btn_contact": "📞 聯繫客服",
        "btn_lang": "🌐 切換語言",
    },
    "zh_cn": {
        "welcome": """🌏 *天宇集团 TIANYU GROUP*

欢迎使用天宇集团官方助手！

我们提供以下服务：
🏢 东南亚办公室出租
📑 公司注册｜牌照挂靠
🌏 签证｜保关｜回程机票
🚗 包车租车｜驾照代办
🛂 第三国护照规划

🇻🇳 越南 🇵🇭 菲律宾 🇦🇪 迪拜
🇱🇰 斯里兰卡 🇲🇾 马来西亚

请选择服务：""",
        "office": "🏢 *东南亚办公室出租*\n\n我们在越南、菲律宾、迪拜、斯里兰卡、马来西亚提供优质办公室出租服务。\n\n如需查询，请联系客服。",
        "company": "📑 *公司注册｜牌照挂靠*\n\n提供东南亚各国公司注册及牌照挂靠服务，手续简便，快速办理。\n\n如需查询，请联系客服。",
        "visa": "🌏 *签证｜保关｜回程机票*\n\n提供各类签证办理、保关及回程机票安排服务。\n\n如需查询，请联系客服。",
        "car": "🚗 *包车租车｜驾照代办*\n\n提供东南亚各国包车、租车及驾照代办服务。\n\n如需查询，请联系客服。",
        "passport": "🛂 *第三国护照规划*\n\n专业第三国护照规划服务，为您提供最佳方案。\n\n如需查询，请联系客服。",
        "contact": "📞 *联系客服*\n\n请直接联系我们的客服人员：\n👤 @TY_6789\n\n服务时间：24小时",
        "back": "🔙 返回主菜单",
        "btn_office": "🏢 办公室出租",
        "btn_company": "📑 公司注册",
        "btn_visa": "🌏 签证服务",
        "btn_car": "🚗 包车租车",
        "btn_passport": "🛂 护照规划",
        "btn_contact": "📞 联系客服",
        "btn_lang": "🌐 切换语言",
    },
    "en": {
        "welcome": """🌏 *TIANYU GROUP*

Welcome to Tianyu Group official assistant!

Our services:
🏢 Southeast Asia Office Rental
📑 Company Registration | License
🌏 Visa | Customs | Return Ticket
🚗 Car Charter | Driver's License
🛂 Third Country Passport Planning

🇻🇳 Vietnam 🇵🇭 Philippines 🇦🇪 Dubai
🇱🇰 Sri Lanka 🇲🇾 Malaysia

Please select a service:""",
        "office": "🏢 *Office Rental*\n\nWe provide quality office rental in Vietnam, Philippines, Dubai, Sri Lanka, Malaysia.\n\nContact our customer service for inquiries.",
        "company": "📑 *Company Registration*\n\nWe provide company registration and license services across Southeast Asia.\n\nContact our customer service for inquiries.",
        "visa": "🌏 *Visa Services*\n\nWe provide visa processing, customs clearance, and return ticket arrangements.\n\nContact our customer service for inquiries.",
        "car": "🚗 *Car Charter & Driver's License*\n\nCar charter, rental and driver's license services across Southeast Asia.\n\nContact our customer service for inquiries.",
        "passport": "🛂 *Third Country Passport Planning*\n\nProfessional third country passport planning services.\n\nContact our customer service for inquiries.",
        "contact": "📞 *Contact Us*\n\nPlease contact our customer service:\n👤 @TY_6789\n\nAvailable: 24 hours",
        "back": "🔙 Back to Menu",
        "btn_office": "🏢 Office Rental",
        "btn_company": "📑 Company Reg.",
        "btn_visa": "🌏 Visa Services",
        "btn_car": "🚗 Car Charter",
        "btn_passport": "🛂 Passport",
        "btn_contact": "📞 Contact Us",
        "btn_lang": "🌐 Change Language",
    },
    "th": {
        "welcome": """🌏 *TIANYU GROUP*

ยินดีต้อนรับสู่ผู้ช่วยอย่างเป็นทางการของ Tianyu Group!

บริการของเรา:
🏢 เช่าสำนักงานในเอเชียตะวันออกเฉียงใต้
📑 จดทะเบียนบริษัท
🌏 วีซ่า | ตั๋วเครื่องบิน
🚗 เช่ารถ | ใบขับขี่
🛂 วางแผนหนังสือเดินทางประเทศที่สาม

กรุณาเลือกบริการ:""",
        "office": "🏢 *เช่าสำนักงาน*\n\nเราให้บริการเช่าสำนักงานในเวียดนาม ฟิลิปปินส์ ดูไบ ศรีลังกา มาเลเซีย\n\nติดต่อฝ่ายบริการลูกค้า",
        "company": "📑 *จดทะเบียนบริษัท*\n\nบริการจดทะเบียนบริษัทในเอเชียตะวันออกเฉียงใต้\n\nติดต่อฝ่ายบริการลูกค้า",
        "visa": "🌏 *บริการวีซ่า*\n\nบริการวีซ่า ศุลกากร และตั๋วเครื่องบิน\n\nติดต่อฝ่ายบริการลูกค้า",
        "car": "🚗 *เช่ารถ*\n\nบริการเช่ารถและใบขับขี่\n\nติดต่อฝ่ายบริการลูกค้า",
        "passport": "🛂 *วางแผนหนังสือเดินทาง*\n\nบริการวางแผนหนังสือเดินทางประเทศที่สาม\n\nติดต่อฝ่ายบริการลูกค้า",
        "contact": "📞 *ติดต่อเรา*\n\nติดต่อฝ่ายบริการลูกค้า:\n👤 @TY_6789\n\nเปิด 24 ชั่วโมง",
        "back": "🔙 กลับเมนูหลัก",
        "btn_office": "🏢 เช่าสำนักงาน",
        "btn_company": "📑 จดทะเบียน",
        "btn_visa": "🌏 วีซ่า",
        "btn_car": "🚗 เช่ารถ",
        "btn_passport": "🛂 หนังสือเดินทาง",
        "btn_contact": "📞 ติดต่อเรา",
        "btn_lang": "🌐 เปลี่ยนภาษา",
    },
    "vi": {
        "welcome": """🌏 *TIANYU GROUP*

Chào mừng đến với trợ lý chính thức của Tianyu Group!

Dịch vụ của chúng tôi:
🏢 Cho thuê văn phòng Đông Nam Á
📑 Đăng ký công ty | Giấy phép
🌏 Visa | Hải quan | Vé máy bay
🚗 Thuê xe | Bằng lái xe
🛂 Lập kế hoạch hộ chiếu nước thứ ba

Vui lòng chọn dịch vụ:""",
        "office": "🏢 *Cho thuê văn phòng*\n\nChúng tôi cung cấp dịch vụ cho thuê văn phòng tại Việt Nam, Philippines, Dubai, Sri Lanka, Malaysia.\n\nLiên hệ bộ phận hỗ trợ.",
        "company": "📑 *Đăng ký công ty*\n\nDịch vụ đăng ký công ty và giấy phép tại Đông Nam Á.\n\nLiên hệ bộ phận hỗ trợ.",
        "visa": "🌏 *Dịch vụ Visa*\n\nDịch vụ xử lý visa, hải quan và vé máy bay.\n\nLiên hệ bộ phận hỗ trợ.",
        "car": "🚗 *Thuê xe*\n\nDịch vụ thuê xe và bằng lái xe tại Đông Nam Á.\n\nLiên hệ bộ phận hỗ trợ.",
        "passport": "🛂 *Kế hoạch hộ chiếu*\n\nDịch vụ lập kế hoạch hộ chiếu nước thứ ba chuyên nghiệp.\n\nLiên hệ bộ phận hỗ trợ.",
        "contact": "📞 *Liên hệ*\n\nLiên hệ bộ phận hỗ trợ:\n👤 @TY_6789\n\nHoạt động 24 giờ",
        "back": "🔙 Quay lại menu",
        "btn_office": "🏢 Thuê văn phòng",
        "btn_company": "📑 Đăng ký",
        "btn_visa": "🌏 Visa",
        "btn_car": "🚗 Thuê xe",
        "btn_passport": "🛂 Hộ chiếu",
        "btn_contact": "📞 Liên hệ",
        "btn_lang": "🌐 Đổi ngôn ngữ",
    },
}

user_lang = {}

def get_lang(user_id):
    return user_lang.get(user_id, "zh_tw")

def main_keyboard(lang):
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["btn_office"], callback_data="office"),
         InlineKeyboardButton(t["btn_company"], callback_data="company")],
        [InlineKeyboardButton(t["btn_visa"], callback_data="visa"),
         InlineKeyboardButton(t["btn_car"], callback_data="car")],
        [InlineKeyboardButton(t["btn_passport"], callback_data="passport"),
         InlineKeyboardButton(t["btn_contact"], callback_data="contact")],
        [InlineKeyboardButton(t["btn_lang"], callback_data="lang")],
    ])

def lang_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇹🇼 中文繁體", callback_data="set_zh_tw"),
         InlineKeyboardButton("🇨🇳 简体中文", callback_data="set_zh_cn")],
        [InlineKeyboardButton("🇺🇸 English", callback_data="set_en"),
         InlineKeyboardButton("🇹🇭 ภาษาไทย", callback_data="set_th")],
        [InlineKeyboardButton("🇻🇳 Tiếng Việt", callback_data="set_vi")],
    ])

def back_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(TEXTS[lang]["back"], callback_data="back")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    await update.message.reply_text(
        TEXTS[lang]["welcome"],
        parse_mode="Markdown",
        reply_markup=main_keyboard(lang)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = get_lang(uid)
    data = query.data

    if data == "lang":
        await query.edit_message_text("🌐 Please select language / 请选择语言:", reply_markup=lang_keyboard())
    elif data.startswith("set_"):
        new_lang = data.replace("set_", "")
        user_lang[uid] = new_lang
        lang = new_lang
        await query.edit_message_text(TEXTS[lang]["welcome"], parse_mode="Markdown", reply_markup=main_keyboard(lang))
    elif data == "back":
        await query.edit_message_text(TEXTS[lang]["welcome"], parse_mode="Markdown", reply_markup=main_keyboard(lang))
    elif data in ["office", "company", "visa", "car", "passport", "contact"]:
        await query.edit_message_text(TEXTS[lang][data], parse_mode="Markdown", reply_markup=back_keyboard(lang))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
