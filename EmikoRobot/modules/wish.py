from EmikoRobot import pbot
import random

@pbot.on_message(filters.command("wish"))
async def wish(_, m):
    txt = m.text.split(None, 1)[1]
    if not txt:
        return await m.reply("""You can use /wish as a general Wishing Well of sorts

For example:
/wish I could date you 😍, or
/wish that sushi was 🍣 in /emojify, or
/wish I had someone to /cuddle at night...""")
    
    x = []
    for i in range(0, 101):
        x.append(i)
    y = random.choice(x)
    return await m.reply(f"""Your wish has been cast. ✨

chance of success: {y}%""")
