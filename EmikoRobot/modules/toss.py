from EmikoRobot import pbot as killua
from pyrogram.types import filters
import random

@killua.on_message(filters.command(["coin", "toss"]))
async def toss(_, m):
    YashuAlpha = None
    men = m.from_user.mention
    txt = "{} flipped a coin!\n\nIt's {}!"
    poss = ["heads", "tails"]
    fin = random.choice(poss)
    await m.reply(txt.format(men, fin))
    return YashuAlpha
