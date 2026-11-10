import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# লগার সেটআপ
logging.basicConfig(level=logging.INFO)

# Railway-এর Environment Variable অথবা সরাসরি টোকেন ও চ্যানেল নাম
TOKEN = os.getenv("TOKEN", "9062513543:AAGZ3GIUpXT3dmOWSFcuykQ3XhCcbgY_f0E")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@kmmostafizur73")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ইউজার চ্যানেলে সাবস্ক্রাইব করেছে কি না তা চেক করার ফাংশন
async def check_user_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        return False

# /start কমান্ড হ্যান্ডলার
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    is_subscribed = await check_user_subscription(user_id)
    
    if not is_subscribed:
        builder = InlineKeyboardBuilder()
        builder.button(text="📢 চ্যানেলে জয়েন করুন", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")
        builder.button(text="🔄 সাবস্ক্রিপশন চেক করুন", callback_data="check_sub")
        builder.adjust(1)
        
        await message.answer(
            f"হ্যালো {user_name}! ⚠️ বটের সার্ভিস ব্যবহার করতে হলে প্রথমে আমাদের অফিশিয়াল চ্যানেলে জয়েন করতে হবে[span_0](start_span)[span_0](end_span)।\n\n"
            "দয়া করে নিচের লিংকে ক্লিক করে জয়েন করুন এবং এরপর 'চেক করুন' বাটনে চাপ দিন।",
            reply_markup=builder.as_markup()
        )
    else:
        await message.answer(
            f"স্বাগতম, {user_name}! ✅ আপনার চ্যানেল সাবস্ক্রিপশন ভেরিফাই হয়েছে[span_1](start_span)[span_1](end_span)।\n\n"
            "এখন আপনি নিচের ফিচারগুলো ব্যবহার করতে পারেন।"
        )

# 'চেক করুন' বাটন কলব্যাক হ্যান্ডলার
@dp.callback_query(F.data == "check_sub")
async def process_check_sub(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    is_subscribed = await check_user_subscription(user_id)
    
    if is_subscribed:
        try:
            await callback.message.delete()
        except:
            pass
            
        await callback.message.answer(
            "ধন্যবাদ! ✅ আপনার সাবস্ক্রিপশন সফলভাবে ভেরিফাই হয়েছে। এখন থেকে বট ব্যবহার করতে পারবেন।"
        )
    else:
        await callback.answer(
            "❌ আপনি এখনো আমাদের চ্যানেলে জয়েন করেননি! দয়া করে আগে জয়েন করুন।", 
            show_alert=True
        )

# মেইন ফাংশন
async def main():
    print("Bot is running smoothly on Railway...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
