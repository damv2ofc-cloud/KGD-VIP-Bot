import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- ပြင်ဆင်ရန် အချက်အလက်များ ---
TOKEN = '8778413205:8080674847:AAEfaIbwH5dqbfcdm2lmVY85XKqSmOQKpcs'
ADMIN_ID = 7602102986  

# ဒီနေရာမှာ သင်ရလာတဲ့ File ID ရှည်ကြီးကို ထည့်ပေးပါ (ဥပမာ Bot ဆီ ပုံပို့ပြီး စမ်းကြည့်လို့ရပါတယ်)
# အခုလောလောဆယ် File name နေရာမှာ အစားထိုးထားပါတယ်
START_PHOTO_ID = 'Stpic.png' # <--- ဒီနေရာမှာ File ID (သို့မဟုတ်) Link ထည့်ပါ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("VIP ဝင်ပါမယ်", callback_data='join_vip')],
        [InlineKeyboardButton("မဝင်တော့ပါ", callback_data='cancel_vip')],
        [InlineKeyboardButton("VIP အကြောင်းသိချင်ပါတယ်", callback_data='about_vip')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # reply_text အစား reply_photo ကို ပြောင်းသုံးထားပါတယ်
    await update.message.reply_photo(
        photo=START_PHOTO_ID,
        caption="Bot - VIP ဝင်မှာလားခင်ဗျ..?", 
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'join_vip':
        payment_text = (
            "တစ်သက်စာဝင်ခ [ 𝗟𝗶𝗳𝗲 𝗧𝗶𝗺𝗲 ]\n\n"
            "𝟮𝟬,𝟬𝟬𝟬 𝗞𝘆𝗮𝘁𝘀 [ 𝟮𝟬𝗞 ]\n\n"
            "𝗡𝘂𝗺𝗯𝗲𝗿 - 09401627843\n"
            "𝗞𝗽𝗮𝘆 - 𝗠𝘆𝗶𝗻𝘁 𝗞𝗵𝗮𝗶𝗻𝗴\n"
            "𝗪𝗮𝘃𝗲𝗣𝗮𝘆 - 𝗠𝘆𝗶𝗻𝘁 𝗞𝗵𝗮𝗶𝗻𝗴\n"
            "ငွေလွှဲပြီးရင် 'စလစ်' ပို့ပေးပါဗျ။"
        )
        # Edit လုပ်ရင် စာသားပဲပြမှာမို့ edit_message_text ကို ဆက်သုံးထားပါတယ်
        await query.edit_message_text(text=payment_text)

    elif query.data == 'cancel_vip':
        await query.edit_message_text(text="ထပ်မံကြိုးစားကြည့်နိုင်ပါသည်။")

    elif query.data == 'about_vip':
        about_text = "ဝင်ရောက်စုံစမ်းနိုင်ပါတယ်ဗျ။\nhttps://t.me/KoGyiDamTuto/4"
        await query.edit_message_text(text=about_text)

    elif query.data.startswith('approve_'):
        user_id = query.data.split('_')[1]
        await context.bot.send_message(chat_id=user_id, text="ငွေပေးချေမှုအောင်မြင်ပါသည်။ ဝင်ရန်နှိပ်ပါ။\n\nhttps://t.me/+1rbLEXapigAzYjdl")
        await query.edit_message_text(text="✅ Link ပို့ပေးလိုက်ပါပြီ။")

    elif query.data.startswith('reject_'):
        user_id = query.data.split('_')[1]
        await context.bot.send_message(chat_id=user_id, text="‌‌ငွေပေးချေမှုမအောင်မြင်ပါ။")
        await query.edit_message_text(text="❌ ငြင်းပယ်လိုက်ပါပြီ။")

async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    # ID ရှာချင်ရင် ဒီနေရာမှာ Print ထုတ်ကြည့်လို့ရတယ် (ဖုန်း Terminal မှာ ပေါ်လာမယ်)
    print(f"Photo ID: {update.message.photo[-1].file_id}")
    
    await update.message.reply_text("'စလစ်' ကို လက်ခံရရှိပါပြီ။ ခေတ္တစောင့်ပေးပါခင်ဗျ။")
    
    admin_kb = [
        [InlineKeyboardButton("Confirm ✅", callback_data=f"approve_{user.id}")],
        [InlineKeyboardButton("Cancel ❌", callback_data=f"reject_{user.id}")]
    ]
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"စလစ်အသစ်ရောက်လာပါပြီ!\nUser: {user.first_name} (ID: {user.id})",
        reply_markup=InlineKeyboardMarkup(admin_kb)
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("restart", start)) 
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
