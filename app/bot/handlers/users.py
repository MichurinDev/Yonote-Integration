from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot

from config import config as cfg
from api import api

user_router = Router(name="user_router")
bot = Bot(token=cfg.BOT_TOKEN)


@user_router.message(Command('start'))
async def welcome_message(msg: Message):
    if msg.from_user.id != cfg.ADMIN_ID:
        await msg.answer("<i>Доступ запрещен</i>")
        return

    await msg.answer("<b>Добро пожаловать!</b>\n\nОтправьте текст по следующей структуре: \n\n<b>Заголовок</b>\nТег1, тег2, тег3\n\nТекст")


@user_router.message(Command('id'))
async def welcome_message(msg: Message):
    await msg.reply(f"Ваш User ID: <code>{msg.from_user.id}</code>")


@user_router.message()
async def messages(msg: Message):
    text = msg.text
    title, tags, content = text.split("\n", 2)
    tags = ", ".join(list(map(lambda x: f"**#{x}**", tags.split(", "))))

    create_doc = await api.create_document(
        collectionUrlId="tftofsJza5",
        title=title,
        text=f"{tags}\n\n{content}",
        parentDocumentUrlId="qhsKXsBo82",
        publish=True
    )

    if create_doc["ok"]:
        doc_url = cfg.YONOTE_DOMAIN + create_doc["data"]["url"]
        await msg.answer(f'<a href="{doc_url}">Документ</a> создан!')
    else:
        await msg.answer(f"Ошибка: {create_doc['message']}")
        print(create_doc["error"])
