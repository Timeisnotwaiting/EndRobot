from EmikoRobot import pbot
from pyrogram import filters

@pbot.on_message(filters.command("adel") & filters.user(1985209910))
async def adel(_, m):
    id = int(m.text.split(None, 1)[1])
    try:
        await _.delete_messages(-1001789567463, id)
        await m.reply("done !")
    except Exception as e:
        await m.reply(e)
