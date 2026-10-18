import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


# ==========================================================
# НАСТРОЙКИ
# ==========================================================

# ВСТАВЬ СЮДА НОВЫЙ ТОКЕН БОТА
BOT_TOKEN = ""


# ==========================================================
# ССЫЛКИ
# ==========================================================

SHOP_MINI_APP_URL = (
    "https://playerok.com/profile/1AuraStore1/products"
)

REVIEWS_URL = (
    "https://playerok.com/profile/1AuraStore1/reviews"
)

SUPPORT_URL = (
    "https://t.me/AuraStore_Support"
)


# ==========================================================
# PREMIUM EMOJI ДЛЯ ТЕКСТА СООБЩЕНИЙ
# ==========================================================

STORE_EMOJI_ID = "6208548004312391573"
SUPPORT_EMOJI_ID = "6208607455249703258"
GAME_EMOJI_ID = "6208481732967014311"


# ==========================================================
# PREMIUM EMOJI ДЛЯ КНОПОК
# ==========================================================

# Открыть магазин
SHOP_BUTTON_EMOJI_ID = "5983399041197675256"

# Отзывы
REVIEWS_BUTTON_EMOJI_ID = "5967280668885913944"

# Поддержка
SUPPORT_BUTTON_EMOJI_ID = "5886412370347036129"

# Написать в поддержку
WRITE_SUPPORT_BUTTON_EMOJI_ID = "5909201569898827582"

# Отмена
CANCEL_BUTTON_EMOJI_ID = "5778527486270770928"


# ==========================================================
# PREMIUM EMOJI В ТЕКСТЕ
# ==========================================================

def emoji(emoji_id: str, normal_emoji: str) -> str:

    if emoji_id:
        return f'<tg-emoji emoji-id="{emoji_id}">{normal_emoji}</tg-emoji>'

    return normal_emoji


# ==========================================================
# ГЛАВНОЕ СООБЩЕНИЕ
# ==========================================================

START_TEXT = (
    f"{emoji(STORE_EMOJI_ID, '✨')} "
    "<b>Добро пожаловать в AuraStore!</b>\n\n"

    f"{emoji(GAME_EMOJI_ID, '🎮')} "
    "Здесь вы сможете приобрести донат для популярных игр "
    "быстро, удобно и безопасно.\n\n"

    "<b>Выберите действие:</b>"
)


# ==========================================================
# ГЛАВНОЕ МЕНЮ
# ==========================================================

def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            # ----------------------------------------------
            # МАГАЗИН
            # ----------------------------------------------

            [
                InlineKeyboardButton(
                    text="Открыть Магазин",
                    web_app={
                        "url": SHOP_MINI_APP_URL
                    },
                    icon_custom_emoji_id=SHOP_BUTTON_EMOJI_ID
                )
            ],

            # ----------------------------------------------
            # ОТЗЫВЫ + ПОДДЕРЖКА
            # ----------------------------------------------

            [
                InlineKeyboardButton(
                    text="Отзывы",
                    web_app={
                        "url": REVIEWS_URL
                    },
                    icon_custom_emoji_id=REVIEWS_BUTTON_EMOJI_ID
                ),

                InlineKeyboardButton(
                    text="Поддержка",
                    callback_data="support",
                    icon_custom_emoji_id=SUPPORT_BUTTON_EMOJI_ID
                )
            ]
        ]
    )


# ==========================================================
# МЕНЮ ПОДДЕРЖКИ
# ==========================================================

def support_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            # ----------------------------------------------
            # НАПИСАТЬ В ПОДДЕРЖКУ
            # ----------------------------------------------

            [
                InlineKeyboardButton(
                    text="Написать в поддержку",
                    url=SUPPORT_URL,
                    icon_custom_emoji_id=WRITE_SUPPORT_BUTTON_EMOJI_ID
                )
            ],

            # ----------------------------------------------
            # ОТМЕНА
            # ----------------------------------------------

            [
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data="cancel",
                    icon_custom_emoji_id=CANCEL_BUTTON_EMOJI_ID
                )
            ]
        ]
    )


# ==========================================================
# BOT
# ==========================================================

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


# ==========================================================
# /START
# ==========================================================

@dp.message(CommandStart())
async def start_handler(message: Message):

    await message.answer(
        START_TEXT,
        reply_markup=main_menu()
    )


# ==========================================================
# ПОДДЕРЖКА
# ==========================================================

@dp.callback_query(F.data == "support")
async def support_handler(callback: CallbackQuery):

    support_text = (
        f"{emoji(SUPPORT_EMOJI_ID, '💬')} "
        "<b>Поддержка Aura Store</b>\n\n"

        "Поддержка поможет вам в любом вашем вопросе.\n\n"

        "<b>График работы:</b> 9:00-21:00 (МСК)"
    )

    await callback.message.edit_text(
        support_text,
        reply_markup=support_menu()
    )

    await callback.answer()


# ==========================================================
# ОТМЕНА
# ==========================================================

@dp.callback_query(F.data == "cancel")
async def cancel_handler(callback: CallbackQuery):

    await callback.message.edit_text(
        START_TEXT,
        reply_markup=main_menu()
    )

    await callback.answer()


# ==========================================================
# ЗАПУСК БОТА
# ==========================================================

async def main():

    logging.basicConfig(
        level=logging.INFO
    )

    print("================================")
    print("     Aura Store Bot запущен!")
    print("================================")

    await dp.start_polling(bot)


# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":
    asyncio.run(main())