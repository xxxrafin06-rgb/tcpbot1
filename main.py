# ═══════════════════════════════════════════════════════════════
#   ██████╗  █████╗ ███████╗██╗███╗   ██╗    ████████╗██╗  ██╗████████╗
#   ██╔══██╗██╔══██╗██╔════╝██║████╗  ██║    ╚══██╔══╝╚██╗██╔╝╚══██╔══╝
#   ██████╔╝███████║█████╗  ██║██╔██╗ ██║       ██║    ╚███╔╝    ██║   
#   ██╔══██╗██╔══██║██╔══╝  ██║██║╚██╗██║       ██║    ██╔██╗    ██║   
#   ██║  ██║██║  ██║██║     ██║██║ ╚████║       ██║   ██╔╝ ██╗   ██║   
#   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝       ╚═╝   ╚═╝  ╚═╝   ╚═╝   
#
#              ★ PREMIUM TCP BOT — BY RAFIN TxT ★
#              ▌ Entry Point (শুধু এই ফাইলটি রান করবেন) ▌
# ═══════════════════════════════════════════════════════════════

import asyncio
import time
import sys
from cfonts import render

# ─── অটো ইমপোর্ট (দুটি মডিউল স্বয়ংক্রিয়ভাবে লোড হবে) ───
import login_engine
import bot_core

# ─── bot_core থেকে গ্লোবাল ভেরিয়েবল রেফারেন্স ───
from bot_core import (
    TcPOnLine, TcPChaT,
    build_ob55_online_auth, create_auth_token_chat,
    bot_uid, ToKen, region
)


# ═══════════════════════════════════════════════════════════════
#                    ★ প্রিমিয়াম ডিজাইন ফাংশন ★
# ═══════════════════════════════════════════════════════════════

def print_banner():
    """প্রিমিয়াম ব্যানার প্রিন্ট করবে — RAFIN TxT ব্র্যান্ডেড"""
    banner = render('RAFIN TxT', colors=['red', 'yellow'], align='center')
    sub    = render('PREMIUM TCP BOT', colors=['cyan', 'magenta'], align='center')

    print("\n" + "═" * 70)
    print(banner)
    print(sub)
    print("        ▌ Developed & Powered by RAFIN TxT ▌")
    print("═" * 70 + "\n")


def print_line(title, value, icon="➤"):
    """সুন্দর ফরম্যাটে লাইন প্রিন্ট করবে"""
    print(f"  {icon}  \033[1;36m{title:<14}\033[0m : \033[1;33m{value}\033[0m")


def print_box(title, lines, color="\033[1;35m"):
    """বক্স স্টাইলে ইনফরমেশন দেখাবে"""
    width = 60
    print(f"\n{color}┌{'─' * width}┐\033[0m")
    print(f"{color}│\033[0m  \033[1;33m{title.center(width - 2)}\033[0m {color}│\033[0m")
    print(f"{color}├{'─' * width}┤\033[0m")
    for line in lines:
        print(f"{color}│\033[0m  {line:<{width - 2}} {color}│\033[0m")
    print(f"{color}└{'─' * width}┘\033[0m\n")


def log(level, message):
    """প্রিমিয়াম লেভেলযুক্ত লগ প্রিন্টার"""
    icons = {
        "INFO":  ("\033[1;36m",  "ℹ"),
        "OK":    ("\033[1;32m",  "✔"),
        "WAIT":  ("\033[1;33m",  "⏳"),
        "WARN":  ("\033[1;33m",  "⚠"),
        "ERROR": ("\033[1;31m",  "✘"),
        "BOT":   ("\033[1;35m",  "★"),
    }
    color, icon = icons.get(level, ("\033[1;37m", "•"))
    ts = time.strftime("%H:%M:%S")
    print(f"\033[1;90m[{ts}]\033[0m {color}{icon} {level:<5}\033[0m │ {message}")


# ═══════════════════════════════════════════════════════════════
#                    ★ মূল প্রোগ্রাম শুরু ★
# ═══════════════════════════════════════════════════════════════

async def MaiiiinE():
    """লগইন + TCP সার্ভিস চালু করার মূল ফাংশন"""
    global bot_uid, ToKen, region

    # ─── আপনার গেস্ট UID এবং পাসওয়ার্ড এখানে বসান ───
    Uid = '8240708002'
    Pw  = '048CDA2F8FEEB4D8B641F16BEFC789DB8B556681EFA6BB0635DF6BC71883F7CB'
    REGION_PREF = "IND"

    print_banner()
    log("INFO", "লগইন প্রক্রিয়া শুরু হচ্ছে ...")
    log("INFO", f"লক্ষ্য অঞ্চল (Region) : {REGION_PREF}")
    print()

    # ─── লগইন প্রক্রিয়া ───
    try:
        result = await login_engine.do_login(Uid, Pw, REGION_PREF)
    except Exception as e:
        log("ERROR", f"লগইনের সময় সমস্যা হয়েছে : {e}")
        return

    if not result:
        log("ERROR", "লগইন ব্যর্থ হয়েছে, ১০ সেকেন্ড পর পুনরায় চেষ্টা করা হবে ...")
        await asyncio.sleep(10)
        return

    # ─── bot_core এর গ্লোবাল ভেরিয়েবল সেট করুন ───
    bot_core.bot_uid = result["bot_uid"]
    bot_core.ToKen   = result["token"]
    bot_core.region  = result["region"]

    key         = result["key"]
    iv          = result["iv"]
    timestamp   = result["timestamp"]
    online_ip   = result["online_ip"]
    online_port = result["online_port"]
    chat_ip     = result["chat_ip"]
    chat_port   = result["chat_port"]
    acc_name    = result["account_name"]

    # ─── লগইন সফল হলে প্রিমিয়াম তথ্য বক্স ───
    log("OK", "লগইন সফলভাবে সম্পন্ন হয়েছে !")
    print_box(
        "ACCOUNT INFORMATION — RAFIN TxT",
        [
            f"\033[1;37mUID\033[0m      : \033[1;32m{result['bot_uid']}\033[0m",
            f"\033[1;37mName\033[0m     : \033[1;32m{acc_name}\033[0m",
            f"\033[1;37mRegion\033[0m   : \033[1;32m{result['region']}\033[0m",
            f"\033[1;37mServer\033[0m   : \033[1;32m{online_ip}:{online_port}\033[0m",
            f"\033[1;37mChat\033[0m     : \033[1;32m{chat_ip}:{chat_port}\033[0m",
        ]
    )

    # ─── অথেনটিকেশন টোকেন তৈরি ───
    log("INFO", "অথেনটিকেশন টোকেন তৈরি করা হচ্ছে ...")
    ChatAutH        = create_auth_token_chat(int(result["bot_uid"]), result["token"], int(timestamp), key, iv)
    OnlineAutH, _   = build_ob55_online_auth(int(result["bot_uid"]), result["token"], int(timestamp), key, iv)
    log("OK", "অথেনটিকেশন টোকেন সফলভাবে তৈরি হয়েছে।")

    # ─── TCP টাস্ক চালু করা ───
    log("WAIT", "চ্যাট সার্ভারের সাথে সংযোগ স্থাপন করা হচ্ছে ...")
    ready_event = asyncio.Event()
    t1 = asyncio.create_task(
        TcPChaT(chat_ip, chat_port, ChatAutH, key, iv, ready_event, result["region"])
    )
    await ready_event.wait()
    log("OK", "চ্যাট সার্ভার সংযোগ সফল হয়েছে।")

    await asyncio.sleep(1)

    log("WAIT", "অনলাইন সার্ভারের সাথে সংযোগ স্থাপন করা হচ্ছে ...")
    t2 = asyncio.create_task(
        TcPOnLine(online_ip, online_port, key, iv, OnlineAutH)
    )

    # ─── চূড়ান্ত স্ট্যাটাস প্যানেল ───
    print()
    print("═" * 70)
    print(render('BOT ONLINE', colors=['green', 'cyan'], align='center'))
    print("═" * 70)
    print_line("Owner",  "RAFIN TxT")
    print_line("Region", result['region'])
    print_line("Bot UID", result['bot_uid'])
    print_line("Name",   acc_name)
    print_line("Status", "\033[1;32m● RUNNING\033[0m")
    print("═" * 70)
    print(f"   \033[1;35m▌ সমস্ত সিস্টেম সচল — RAFIN TxT এর প্রিমিয়াম বট ▌\033[0m")
    print("═" * 70 + "\n")

    # ─── চিরকাল চলতে থাকবে ───
    await asyncio.gather(t1, t2)


# ═══════════════════════════════════════════════════════════════
#              ★ অটো-রিস্টার্ট লুপ (প্রতি ৭ ঘণ্টায়) ★
# ═══════════════════════════════════════════════════════════════

async def StarTinG():
    """প্রতি ৭ ঘণ্টা পরপর টোকেন রিফ্রেশ করে অটো-রিস্টার্ট করবে"""
    attempt = 0
    while True:
        attempt += 1
        try:
            log("BOT", f"সেশন #{attempt} শুরু হচ্ছে — RAFIN TxT")
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            log("WARN", "টোকেনের সময় শেষ হয়েছে, পুনরায় চালু করা হচ্ছে ...")
            await asyncio.sleep(3)
        except KeyboardInterrupt:
            log("WARN", "ব্যবহারকারী দ্বারা বন্ধ করা হয়েছে। বিদায় !")
            sys.exit(0)
        except Exception as e:
            log("ERROR", f"সমস্যা হয়েছে : {e} → ৫ সেকেন্ড পর পুনরায় চেষ্টা ...")
            await asyncio.sleep(5)


# ═══════════════════════════════════════════════════════════════
#                       ★ এন্ট্রি পয়েন্ট ★
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    try:
        asyncio.run(StarTinG())
    except KeyboardInterrupt:
        print("\n\033[1;31m▌ বট বন্ধ করা হয়েছে — RAFIN TxT ▌\033[0m\n")