from EmikoRobot import pbot
from pyrogram import filters

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABETS = []
for u in ALPHABET:
    ALPHABETS.append(u)

SERIF = "๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐๐"

ALLCAPS = "แดสแดแดแดาษขสษชแดแดสแดษดแดแดวซสsแดแดแด แดกxสแดข"

@pbot.on_message(filters.command("getfont"))
async def gf(_, m):
    if len(m.command) < 2:
        return await m.reply("give some text bruh ! ๐ฅฒ")
    s = m.text.split()
    x = []
    for y in s:
        ch = 0
        if ch == 0:
            pass
            ch += 1
        else:
            x.append(y)
    txt = ""
    for b in x:
        for c in b:
            cnt = 0
            ind = ALPHABETS.index(c)
            if cnt == 0:
                txt += SERIF[ind]
                cnt += 1
            else:
                txt += ALLCAPS[ind]
                cnt += 1
    return await m.reply(txt)
