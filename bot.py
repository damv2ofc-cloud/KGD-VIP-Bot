import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- ပြင်ဆင်ရန် အပိုင်း ---
TOKEN = '8778413205:AAH8rWFW9OBoxlJJEH0MDWhf146sfTXben8' # BotFather ဆီက Token ထည့်ပါ
ADMIN_ID = 7602102986          # @userinfobot ကရတဲ့ သင့် ID ထည့်ပါ
CHANNEL_LINK = 'https://t.me/+1rbLEXapigAzYjdl' # လူသစ်တွေကို ပို့ပေးမယ့် Channel Link

# Bot စတင်တဲ့အခါ (Start နှိပ်တဲ့အခါ)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Yes, I want to join", callback_data='yes')],
        [InlineKeyboardButton("No, thanks", callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('မင်္ဂလာပါ။ Paid Channel ဝင်ချင်ပါသလား?', reply_markup=reply_markup)

# ခလုတ်တွေကို နှိပ်တဲ့အခါ
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'yes':
        await query.edit_message_text(text="ငွေလွှဲပေးပါ: 09168646167 (200ks)\nလွှဲပြီးရင် ငွေစလစ် ပို့ပေးပါနော်။")
    elif query.data == 'no':
        await query.edit_message_text(text="ဟုတ်ကဲ့ပါခင်ဗျာ။")
    
    # Admin က Done သို့မဟုတ် Cancel နှိပ်တဲ့အခါ
    elif query.data.startswith('approve_'):
        user_id = query.data.split('_')[1]
        await context.bot.send_message(chat_id=user_id, text=f"ငွေပေးချေမှု အောင်မြင်ပါတယ်။ ဝင်ရန်နှိပ်ပါ- {CHANNEL_LINK}")
        await query.edit_message_text(text="အတည်ပြုပြီးပါပြီ 👍")
    elif query.data.startswith('cancel_'):
        user_id = query.data.split('_')[1]
        await context.bot.send_message(chat_id=user_id, text="Error Detected: စလစ် မှားယွင်းနေပါသည်။")
        await query.edit_message_text(text="ပယ်ဖျက်လိုက်ပါပြီ ❌")

# User ပို့လိုက်တဲ့ စလစ်ကို Admin ဆီ Forward လုပ်ခြင်း
async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        user = update.message.from_user
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"User @{user.username} (ID: {user.id}) ဆီက စလစ်ရောက်လာပါပြီ။")
        
        # စလစ်ကို Admin ဆီ ပို့မယ်
        await update.message.forward(chat_id=ADMIN_ID)
        
        # အတည်ပြုဖို့ ခလုတ်ပြမယ်
        admin_keyboard = [
            [InlineKeyboardButton("Done 👍", callback_data=f"approve_{update.message.chat_id}")],
            [InlineKeyboardButton("Cancel ❌", callback_data=f"cancel_{update.message.chat_id}")]
        ]
        await context.bot.send_message(chat_id=ADMIN_ID, text="စစ်ဆေးပြီးရင် ရွေးချယ်ပါ-", reply_markup=InlineKeyboardMarkup(admin_keyboard))
        await update.message.reply_text("စလစ်ကို လက်ခံရရှိပါပြီ။ ခေတ္တစောင့်ပေးပါခင်ဗျာ။")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
  
