from EmikoRobot import pbot
import random
from pyrogram import filters

@pbot.on_message(filters.command("judge"))
async def judge(_, m):
    if not m.reply_to_message:
        return await m.reply("<code>You need to reply to someone.</code>")
    x = m.reply_to_message.from_user.mention
    y = ["is lying!", "is telling the truth."]
    z = random.choice(y)
    return await m.reply(x + " " + z)
