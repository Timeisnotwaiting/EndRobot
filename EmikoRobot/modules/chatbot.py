from asyncio import gather, sleep
from Python_ARQ import ARQ
from pyrogram import filters, Client as app, enums
from pyrogram.types import Message
from aiohttp import ClientSession 
from Spoiled.Database.chatbot import check_chatbot, add_chatbot, rm_chatbot
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM

ARQ_API_KEY = "PNZJLN-ZZFHVK-USQLIZ-MQEWJN-ARQ"
ARQ_API_URL = "https://arq.hamker.in"

aiohttpsession = ClientSession()

arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

chatbot_group=5

BOT_ID = None

async def eor(m: Message, text="?"):
    if m.from_user.is_self:
        await m.edit(text)
    else:
        await m.reply(text)

async def chat_bot_toggle(message: Message, is_userbot: bool):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    db = await check_chatbot()
    db = db["userbot"] if is_userbot else db["bot"]
    if status == "enable":
        if chat_id not in db:
            await add_chatbot(chat_id, is_userbot=is_userbot)
            text = "Chatbot Enabled!"
            return await eor(message, text=text)
        await eor(message, text="ChatBot Is Already Enabled.")
    elif status == "disable":
        if chat_id in db:
            await rm_chatbot(chat_id, is_userbot=is_userbot)
            return await eor(message, text="Chatbot Disabled!")
        await eor(message, text="ChatBot Is Already Disabled.")
    else:
        await eor(message, text="**Usage:**\n/chatbot [ENABLE|DISABLE]")


# Enabled | Disable Chatbot

markup = IKM(
         [
         [
         IKB("Enable ✅", callback_data="chatbot_enable"),
         IKB("Disable ❌", callback_data="chatbot_disable")
         ],
         [
         IKB("Close 🗑️", callback_data="chatbot_close")
         ]
         ]
         )

id = None

@app.on_message(filters.command("chatbot"))
async def chatbot_status(_, message: Message):
    global id
    id = message.from_user.id
    await message.reply("Choose from below !", reply_markup=markup)

@app.on_callback_query(filters.regex("chatbot_enable"))
async def en_cbq(_, q):
    global id
    if id != q.from_user.id:
        return await q.answer()
    chat_id = q.message.chat.id
    db = await check_chatbot()
    db = db["bot"]
    if chat_id in db:
        return await q.answer("Chatbot already enabled !", show_alert=True)
    await q.answer("Enabling Chatbot !", show_alert=True)
    await add_chatbot(chat_id, is_userbot=False)
    await q.edit_message_text(f"Chatbot enabled in **{q.message.chat.title}** !")
    
@app.on_callback_query(filters.regex("chatbot_disable"))
async def di_cbq(_, q):
    global id
    if id != q.from_user.id:
        return await q.answer()
    chat_id = q.message.chat.id
    db = await check_chatbot()
    db = db["bot"]
    if not chat_id in db:
        return await q.answer("Chatbot isn't enabled !", show_alert=True)
    await q.answer("Disabling Chatbot !", show_alert=True)
    await rm_chatbot(chat_id, is_userbot=False)
    await q.edit_message_text(f"Chatbot disabled in **{q.message.chat.title}** !")

@app.on_callback_query(filters.regex("chatbot_close"))
async def close_cbq(_, q):
    global id
    if id != q.from_user.id:
        return await q.answer()
    await q.answer("closing...")
    await q.message.delete()
    

async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result


async def type_and_send(yashu, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await yashu.send_chat_action(chat_id, enums.ChatAction.TYPING)
    response, _ = await gather(lunaQuery(query, user_id), sleep(3))
    await message.reply_text(response)
    await yashu.send_chat_action(chat_id, enums.ChatAction.CANCEL)


@app.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded,
    group=chatbot_group
)
async def chatbot_talk(_, message: Message):
    global BOT_ID
    if not BOT_ID:
        BOT_ID = (await _.get_me()).id
    db = await check_chatbot()
    if message.chat.id not in db["bot"]:
        return
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    await type_and_send(_, message)
