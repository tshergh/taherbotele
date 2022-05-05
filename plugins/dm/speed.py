# © BugHunterCodeLabs ™
# © bughunter0 / nuhman_pk
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os 
from os import error
import speedtest   
import logging
import pyrogram
import math
from decouple import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message

bughunter0 = Client(
    "SpeedTestBot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@bughunter0.on_message(filters.private)
async def download_upload(bot, message):
     alert = await message.reply_text("Processing....")
     speed = speedtest.Speedtest() 
     await alert.edit("Getting Best server")
     speed.get_best_server()
     await alert.edit(f'**Connected to :** {speed.results.server["sponsor"]} ({speed.results.server["name"]})')
     message = await message.reply_text("Checking Download / Upload Speed ...")
     downloadspeed = speed.download()
     downloadspeed = downloadspeed/1000000 # bit to kbps
     uploadspeed = speed.upload()
     uploadspeed = uploadspeed/1000000 # bit to kbps
     await alert.delete()
     await message.edit_text(f' **Download Speed :** `{downloadspeed} kbps` \n**Upload Speed :** `{uploadspeed} kbps` \n**Server :** {speed.results.server["sponsor"]} ({speed.results.server["name"]})\n \n © @BugHunterBots')

bughunter0.run()
