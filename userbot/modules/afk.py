# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

from datetime import datetime
import time
from random import choice, randint
from asyncio import sleep

from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN)
from userbot.events import register

# ========================= CONSTANTS ============================
AFKSTR = [
    "Aku sibuk. Tolong tinggalkan pesan secara pribadi dan ketika saya kembali saya akan membalas pesan anda!",
    "Saya pergi sekarang. Jika Anda butuh sesuatu, tinggalkan pesan setelah bunyi beep:\n`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep`!",
    "Anda merindukan saya, lain kali cari waktu lebih baik.",
    "Saya akan kembali dalam beberapa menit dan jika tidak...,\ntunggu lebih lama.",
    "Saya tidak di sini sekarang, jadi saya mungkin di tempat lain.",
    "Bunga mawar itu berwarna merah,\nBunga violet berwarna biru,\nTinggalkan pesan untukku,\nDan aku akan kembali padamu.",
    "Terkadang hal terbaik dalam hidup layak untuk ditunggu…\naku akan segera kembali.",
    "Aku akan segera kembali,\ntapi jika aku tidak segera kembali,\nSaya akan kembali lagi nanti.",
    "Jika kamu belum mengetahuinya,\nAku tidak di sini.",
    "Hello, welcome to my away message, how may I ignore you today?",
    "I'm away over 7 seas and 7 countries,\n7 waters and 7 continents,\n7 mountains and 7 hills,\n7 plains and 7 mounds,\n7 pools and 7 lakes,\n7 springs and 7 meadows,\n7 cities and 7 neighborhoods,\n7 blocks and 7 houses...\n\nWhere not even your messages can reach me!",
    "Saya sedang tidak menggunakan keyboard saat ini, tetapi jika Anda akan berteriak cukup keras, saya mungkin akan mendengar Anda.",
    "I went that way\n---->",
    "I went this way\n<----",
    "Tolong tinggalkan pesan dan buat saya merasa lebih penting daripada sebelumnya.",
    "Saya tidak disini jadi berhentilah menulis kepada saya,\natau anda juga tidak akan menemukan saya meskipun layar anda penuh tulisan.",
    "Jika saya ada di sini,\nAku akan memberitahumu dimana aku berada.\n\nTapi saya tidak,\njadi tanya saya kapan saya kembali...",
    "Saya Offline!\nSaya tidak tahu kapan saya akan kembali!\nSemoga beberapa menit dari sekarang!",
    "Saya tidak ada saat ini, jadi silakan tinggalkan nama, nomor, dan alamat Anda dan saya akan menemui Anda nanti.",
    "Maaf, saya tidak di sini sekarang.\nJangan ragu untuk berbicara dengan userbot saya selama Anda mau.\nSaya akan menghubungi Anda lagi nanti.",
    "Saya yakin Anda mengharapkan pesan terbalas!\nNamun saya sedang Offline",
    "Hidup ini sangat singkat, begitu banyak yang harus dilakukan...\nSaya akan melakukan salah satunya..",
    "Saya tidak di sini sekarang...\ntetapi jika saya...\n\nbukankah itu luar biasa?",
]

global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
afk_start = {}

# =================================================================
@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    global reason
    USER_AFK = {}
    afk_time = None
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if string:
        AFKREASON = string
        await afk_e.edit(f"Saya akan Offline\
        \nKarena: `{string}`")
    else:
        await afk_e.edit("Saya akan Offline")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#OFFLINE\nNezuko-bot akan menggantikan anda")
    ISAFK = True
    afk_time = datetime.now()  # pylint:disable=E0602
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if ISAFK:
        ISAFK = False
        msg = await notafk.respond("Saya tidak lagi AFK.")
        time.sleep(3)
        await msg.delete()
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "Anda telah menerima " + str(COUNT_MSG) + " pesan dari " +
                str(len(USERS)) + " obrolan saat Anda pergi",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                    " telah mengirimmu " + "`" + str(USERS[i]) + " pesan`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "a while ago"
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "Kemarin"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m` yang lalu"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s` yang lalu"
            else:
                afk_since = f"`{int(seconds)}s` yang lalu"
            if mention.sender_id not in USERS:
                if AFKREASON:
                    await mention.reply(f"Saya masih AFK sejak itu {afk_since}.\
                        \nKarena: `{AFKREASON}`")
                else:
                    await mention.reply(str(choice(AFKSTR)))
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await mention.reply(f"Saya masih AFK sejak itu {afk_since}.\
                            \nKarena: `{AFKREASON}`")
                    else:
                        await mention.reply(str(choice(AFKSTR)))
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "a while ago"
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "Yesterday"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h{int(minutes)}m` ago"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m{int(seconds)}s` ago"
            else:
                afk_since = f"`{int(seconds)}s` ago"
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(f"I'm AFK since {afk_since}.\
                        \nReason: `{AFKREASON}`")
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(f"I'm still AFK since {afk_since}.\
                            \nReason: `{AFKREASON}`")
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


CMD_HELP.update({
    "afk":
    ".afk [Alasan Opsional]\
\nUsage: Menetapkan anda sebagai afk.\nBalasan untuk siapa saja yang menandai/PM \
Anda memberi tahu mereka bahwa Anda AFK (alasan).\n\nMematikan AFK saat Anda mengetik apa pun, di mana pun.\
"
})
