# fileName : plugins/checkPdf.py
# copyright ©️ 2021 nabilanavab




import fitz
import shutil
from pdf import PROCESS
from pyrogram.types import Message
from plugins.toKnown import toKnown
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




#--------------->
#--------> LOCAL VAR.
#------------------->

encryptedMsg = """`الملف مشفر` 🔐

أسم الملف: `{}`
حجم الملف: `{}`

`عدد الصفحات: {}`✌️"""


codecMsg = """__أنا لا أفعل أي شيء مع هذا الملف__ 😏

🐉  `خطأ في الكود`  🐉"""

#--------------->
#--------> CHECKS PDF CODEC, IS ENCRYPTED OR NOT
#------------------->


async def checkPdf(file_path, callbackQuery):
    try:
        chat_id=callbackQuery.message.chat.id
        message_id=callbackQuery.message.message_id
        
        fileName=callbackQuery.message.reply_to_message.document.file_name
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        
        with fitz.open(file_path) as doc:
            
            isEncrypted=doc.is_encrypted
            number_of_pages=doc.pageCount
            
            if isEncrypted:
                await callbackQuery.edit_message_text(
                    encryptedMsg.format(
                        fileName, await gSF(fileSize), number_of_pages
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "إنهاء 🔓",
                                    callback_data = "Kdecrypt"
                                )
                            ]
                        ]
                    )
                )
                if callbackQuery.data not in ["decrypt", "Kdecrypt"]:
                    PROCESS.remove(chat_id)
                    # try Coz(at the time of merge there is no such dir but checking)
                    try:
                        shutil.rmtree(f'{message_id}')
                    except Exception:
                        pass
                return "encrypted"
            
            else:
                await toKnown(callbackQuery, number_of_pages)
                return "pass"
            
    except Exception:
        await callbackQuery.edit_message_text(
            text=codecMsg,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "❌ خطأ في الكود ❌",
                            callback_data="error"
                        )
                    ]
                ]
            )
        )
        PROCESS.remove(chat_id)
        # try Coz(at the time of merge there is no such dir but checking)
        try:
            shutil.rmtree(f'{message_id}')
        except Exception:
            pass
        return "notPdf"


#                                                                                  Telegram: @nabilanavab
