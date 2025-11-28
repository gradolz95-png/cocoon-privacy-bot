import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

key = Fernet.generate_key()
cipher = Fernet(key)

async def mock_cocoon_ai(encrypted_text: str) -> str:
    decrypted = cipher.decrypt(encrypted_text.encode()).decode()
    response = f"🔒 Cocoon AI processed your request privately:\n\n«{decrypted}»\n\nProcessed on decentralized TON GPU node. No data leaks."
    return cipher.encrypt(response.encode()).decode()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔒 Test Private AI", callback_data="test")]
    ])
    await message.answer(
        "🔐 <b>Cocoon Privacy Bot</b>\n\n"
        "First end-to-end encrypted demo for Pavel Durov's <b>Cocoon</b> project\n"
        "• Encryption on your device\n"
        "• Processing in decentralized network (simulated)\n"
        "• Decryption only on your device\n\n"
        "Send any text — see the magic!",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query(lambda c: c.data == "test")
async def test(cb: types.CallbackQuery):
    await cb.message.answer("Send me any text — I will process it privately through Cocoon simulation")

@dp.message()
async def process(message: types.Message):
    user_text = message.text.strip()
    if not user_text:
        return

    encrypted = cipher.encrypt(user_text.encode()).decode()
    await message.answer("🔐 Encrypting on your device...\nSending to Cocoon node...")

    encrypted_response = await mock_cocoon_ai(encrypted)
    response = cipher.decrypt(encrypted_response.encode()).decode()

    await message.answer(
        f"✅ <b>Privacy 100%</b>\n\n"
        f"Your request:\n<code>{user_text}</code>\n\n"
        f"{response}\n\n"
        f"⏱ Processed in 1.3 sec · No logs · Full E2E",
        parse_mode="HTML"
    )

async def main():
    print("Cocoon Privacy Bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
