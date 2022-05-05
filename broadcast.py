import os
import traceback
import logging

from fpdf import FPDF
from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup

from handlers.check_user import handle_user_status
from handlers.database import Database

db = Database(DB_URL, DB_NAME)

@ILovePDF.on_message(filters.private)
async def _(bot, cmd):
    await handle_user_status(bot, cmd)
@ILovePDF.on_message(filters.command("start") & filters.private)
async def startprivate(client, message):
    # return
    chat_id = message.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"#مستخدم_جديد: \n\nمستخدم جديد [{message.from_user.first_name}](tg://user?id={message.from_user.id}) داس ستارت @{BOT_USERNAME} !!",
            )

    raise StopPropagation

@ILovePDF.on_message(filters.private & filters.command("stats"))
async def sts(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    await m.reply_text(
        text=f"**إجمالي المستخدمين في قاعدة البيانات 📂:** `{await db.total_users_count()}`\n\n**إجمالي المستخدمين مع تمكين الإخطار 🔔:** `{await db.total_notif_users_count()}`",
        parse_mode="Markdown",
        quote=True
    )

