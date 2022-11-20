import asyncio 
from EmikoRobot import pbot
from pyrogram import filters
from pyrogram.errors import FloodWait
from ..ex_plugins.dbfunctions import get_served_chats
from .sql.users_sql import get_schats

@pbot.on_message(filters.command("broadcast") & filters.user(5754821527))
async def broadcast(_, message):
    if message.reply_to_message:
        x = message.reply_to_message.message_id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
            )
        query = message.text.split(None, 1)[1]
    sent = 0
    pinned = 0
    #chats = []
    chats = get_schats()
    #for schat in schats:
        #chats.append(schat["chat_id"])
    for i in chats:
        try:
            if message.reply_to_message:
                ok = await _.forward_messages(i, y, x)
                sent += 1
                try:
                    await _.pin_chat_message(i, ok.message_id)
                    pinned += 1
                except:
                    continue 
            else:
                ok = await _.send_message(i, query)
                sent += 1
                try:
                    await _.pin_chat_message(i, ok.message_id)
                    pinned += 1
                except:
                    continue
        except FloodWait as e:
            flood_time = int(e.x)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except Exception:
            continue
    try:
        await message.reply_text(
            f"**Broadcasted Message In {sent} Chats and pinned in {str(pinned)} Chats**"
        )
    except:
        pass

@pbot.on_message(filters.command("bcast") & filters.user(5754821527))
async def broadcast(_, message):
    x = int(m.text.split()[1]) if len(m.command) > 1 else 0
    y = m.chat.id
    sent = 0
    pinned = 0
    #chats = []
    chats = get_schats()
    #for schat in schats:
        #chats.append(schat["chat_id"])
    for i in chats:
        try:
            ok = await _.forward_messages(i, y, x)
            sent += 1
            try:
                await _.pin_chat_message(i, ok.message_id)
                pinned += 1
            except:
                continue
        except FloodWait as e:
            flood_time = int(e.x)
            if flood_time > 200:
                continue
            await asyncio.sleep(flood_time)
        except Exception:
            continue
    try:
        await message.reply_text(
            f"**Broadcasted Message In {sent} Chats and pinned in {str(pinned)} Chats**"
        )
    except:
        pass
