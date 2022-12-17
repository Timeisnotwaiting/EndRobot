import os
import re
import math
import requests
import cloudscraper
import urllib.request as urllib
from PIL import Image
from html import escape
from bs4 import BeautifulSoup as bs

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import TelegramError, Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

from EmikoRobot import dispatcher
from EmikoRobot.modules.disable import DisableAbleCommandHandler

combot_stickers_url = "https://combot.org/telegram/stickers?q="

def single_button_maker(text, url):
    markup = InlineKeyboardMarkup(
             [
             [
             InlineKeyboardButton(text, url=url)
             ]
             ]
             )
    return markup

def triple_button_maker(x, y, z):
    markup = InlineKeyboardMarkup(
             [
             [
             InlineKeyboardButton(x[0], url=x[1]),
             InlineKeyboardButton(y[0], url=y[1])
             ],
             [
             InlineKeyboardButton(z[0], url=z[1])
             ]
             ]
             )
    return markup

def stickerid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", The sticker id you are replying is :\n <code>"
            + escape(msg.reply_to_message.sticker.file_id)
            + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get id sticker",
            parse_mode=ParseMode.HTML,
        )


def kang(u: Update, c: CallbackContext):
    try:
        m = u.effective_message
        user = u.effective_user
        mark_name = "YashuAlpha_{}_{}1_by_" + c.bot.username
        pack_link = f"https://t.me/addstickers/{mark_name}"
        kang_markup = triple_button_maker(["Static pack", pack_link.format(user.id, "normal")], ["Animated pack", pack_link.format(user.id, "animated")], ["Video pack", pack_link.format(user.id, "video")])
        emoji = m.text.split()[1] if c.args else "💭"
        title = f"{user.first_name}'s pack by @{c.bot.username}"
        if not m.reply_to_message:
            return m.reply_text("Reply to an image or sticker !", reply_markup=kang_markup)
        if not m.reply_to_message.photo and not m.reply_to_message.sticker:
            return m.reply_text("Reply to an image or a sticker !")
        if m.reply_to_message.photo:
            file_id = m.reply_to_message.photo[-1].file_id
            get_file = c.bot.get_file(file_id)
            get_file.download("yashu.png")
            resize("yashu.png")
            x = "yashu.png"
            format = "normal"
            png = True
        else:
            png = False
            if m.reply_to_message.sticker.is_video:
                format = "video"
            elif m.reply_to_message.sticker.is_animated:
                format = "animated"
            else:
                format = "normal"
            sticid = m.reply_to_message.sticker.file_id
            if format == "video" or format == "animated":
                get_file = c.bot.get_file(sticid)
                x = get_file.download()
            
        alpha = True   
        pack = 1
        name = f"YashuAlpha_{user.id}_{format}{pack}_by_{c.bot.username}"
        try:
            while alpha:
                v = c.bot.get_sticker_set(name)
                stics = len(v.stickers)
                if format == "video" or format == "animated":
                    if stics == 50:
                        pack += 1
                    else:
                        break
                else:
                    if stics == 120:
                        pack += 1
                    else:
                        break
            if stics > 0:
                if format == "video":
                    c.bot.add_sticker_to_set(user_id=user.id, name=name, emojis=emoji, webm_sticker=open(x, "rb"))
                elif format == "animated":
                    c.bot.add_sticker_to_set(user_id=user.id, name=name, emojis=emoji, tgs_sticker=open(x, "rb"))
                else:
                    c.bot.add_sticker_to_set(user_id=user.id, name=name, emojis=emoji, png_sticker=open(x, "rb") if png else sticid)                                  
        except Exception as e:
            print(e)
            if format == "video":
                c.bot.create_new_sticker_set(user_id=user.id, name=name, title=title, emojis=emoji, webm_sticker=open(x, "rb"))
            elif format == "animated":
                c.bot.create_new_sticker_set(user_id=user.id, name=name, title=title, emojis=emoji, tgs_sticker=open(x, "rb"))
            else:
                c.bot.create_new_sticker_set(user_id=user.id, name=name, title=title, emojis=emoji, png_sticker=open(x, "rb") if png else sticid)
        markup = single_button_maker("Pack ✨💭", f"https://t.me/addstickers/{name}")
        m.reply_text(f"Sticker is added to set\n\nEmoji : {emoji}", reply_markup=markup)

    except Exception as e:
        if "Stickerset_invalid" in str(e):
            return m.reply_text("Start me in pm !", reply_markup=single_button_maker("Start !", f"https://t.me/{c.bot.username}"))
        if "blocked" in str(e):
            return m.reply_text("Start me in pm !", reply_markup=single_button_maker("Start !", f"https://t.me/{c.bot.username}"))
        if "occupied" in str(e):
            return m.reply_text("Pack name already occupied, go to @stickers and delete pack name with this bot username !")
        m.reply_text("An unknown error occurred, consider support !")
        print(e)


def makepack_internal(
    update,
    context,
    msg,
    user,
    emoji,
    packname,
    packnum,
    png_sticker=None,
    tgs_sticker=None,
):
    name = user.first_name
    name = name[:50]
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="View Pack", url=f"{packname}")]]
    )
    try:
        extra_version = ""
        if packnum > 0:
            extra_version = " " + str(packnum)
        if png_sticker:
            sticker_pack_name = (
                f"{name}'s stic-pack (@{context.bot.username})" + extra_version
            )
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                sticker_pack_name,
                png_sticker=png_sticker,
                emojis=emoji,
            )
        if tgs_sticker:
            sticker_pack_name = (
                f"{name}'s ani-pack (@{context.bot.username})" + extra_version
            )
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                sticker_pack_name,
                tgs_sticker=tgs_sticker,
                emojis=emoji,
            )

    except TelegramError as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            msg.reply_text(
                "<b>Your Sticker Pack is already created!</b>"
                "\n\nYou can now reply to images, stickers and animated sticker with /steal to add them to your pack"
                "\n\n<b>Send /stickers to find any sticker pack.</b>",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
        elif e.message == "Peer_id_invalid" or "bot was blocked by the user":
            msg.reply_text(
                f"{context.bot.first_name} was blocked by you.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Unblock", url=f"t.me/{context.bot.username}"
                            )
                        ]
                    ]
                ),
            )
        elif e.message == "Internal Server Error: created sticker set not found (500)":
            msg.reply_text(
                "<b>Your Sticker Pack has been created!</b>"
                "\n\nYou can now reply to images, stickers and animated sticker with /steal to add them to your pack"
                "\n\n<b>Send /stickers to find sticker pack.</b>",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
        return

    if success:
        msg.reply_text(
            "<b>Your Sticker Pack has been created!</b>"
            "\n\nYou can now reply to images, stickers and animated sticker with /steal to add them to your pack"
            "\n\n<b>Send /stickers to find sticker pack.</b>",
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )
    else:
        msg.reply_text("Failed to create sticker pack. Possibly due to blek mejik.")


def getsticker(update, context):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        context.bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text(
            "Hello"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please check the file you requested below."
            "\nPlease use this feature wisely!",
            parse_mode=ParseMode.HTML,
        )
        context.bot.sendChatAction(chat_id, "upload_document")
        file_id = msg.reply_to_message.sticker.file_id
        newFile = context.bot.get_file(file_id)
        newFile.download("sticker.png")
        context.bot.sendDocument(chat_id, document=open("sticker.png", "rb"))
        context.bot.sendChatAction(chat_id, "upload_photo")
        context.bot.send_photo(chat_id, photo=open("sticker.png", "rb"))

    else:
        context.bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text(
            "Hello"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get sticker image",
            parse_mode=ParseMode.HTML,
        )


def cb_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    split = msg.text.split(" ", 1)
    if len(split) == 1:
        msg.reply_text("Provide some name to search for pack.")
        return

    scraper = cloudscraper.create_scraper()
    text = scraper.get(combot_stickers_url + split[1]).text
    soup = bs(text, "lxml")
    results = soup.find_all("a", {"class": "sticker-pack__btn"})
    titles = soup.find_all("div", "sticker-pack__title")
    if not results:
        msg.reply_text("No results found :(.")
        return
    reply = f"Stickers for *{split[1]}*:"
    for result, title in zip(results, titles):
        link = result["href"]
        reply += f"\n• [{title.get_text()}]({link})"
    msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


def getsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        new_file = bot.get_file(file_id)
        new_file.download("sticker.png")
        bot.send_document(chat_id, document=open("sticker.png", "rb"))
        os.remove("sticker.png")
    else:
        update.effective_message.reply_text(
            "Please reply to a sticker for me to upload its PNG."
        )


def delsticker(update, context):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        context.bot.delete_sticker_from_set(file_id)
        msg.reply_text("Deleted!")
    else:
        update.effective_message.reply_text(
            "Please reply to sticker message to del sticker"
        )

__mod_name__ = "kang"

__help__ = """
*Help menu for stickers tools*

❂ /stickerid*:* reply to a sticker to me to tell you its file ID.
❂ /getsticker*:* reply to a sticker to me to upload its raw PNG file.
❂ /kang*:* reply to a sticker to add it to your pack.
❂ /delsticker*:* Reply to your anime exist sticker to your pack to delete it.
❂ /stickers*:* Find stickers for given term on combot sticker catalogue
❂ /tiny*:* To make small sticker
❂ /kamuii <1-8> *:* To deepefying stiker
❂ /mmf <reply with text>*:* To draw a text for sticker or pohots
"""


STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid, run_async=True)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker, run_async=True)
KANG_HANDLER = DisableAbleCommandHandler("kang", kang, pass_args=True, run_async=True)
DEL_HANDLER = DisableAbleCommandHandler("delsticker", delsticker, run_async=True)
STICKERS_HANDLER = DisableAbleCommandHandler("stickers", cb_sticker, run_async=True)

dispatcher.add_handler(STICKERS_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(KANG_HANDLER)
dispatcher.add_handler(DEL_HANDLER)
