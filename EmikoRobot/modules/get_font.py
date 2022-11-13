from EmikoRobot import pbot
from pyrogram import filters

ALPHABETS = "abcdefghijklmnopqrstuvwxyz"

SERIF = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"

ALLCAPS = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"

@pbot.on_message(filters.command("getfont"))
async def gf(_, m):
    if len(m.command) < 2:
        return await m.reply("give some text bruh ! 🥲")
    s = m.text.split()
    x = []
    for y in s:
        for a in y:
            if a.lower() in ALPHABETS:
                x.append(y)
    txt = ""
    
