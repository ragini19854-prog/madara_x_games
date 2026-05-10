import re
import asyncio
import random
import string
import time
import requests
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= BOT CONFIG =================

API_ID = 36522229
API_HASH = "7f27443617af60bcb0e23f7147d3eaf9"
BOT_TOKEN = "8652475253:AAEP9fzyBYeyvjxdrkuZSOvPSJjWfPXDLVU"
OWNER_ID = 8441236350
START_IMAGE = "https://i.ibb.co/CpnXpZ5H/image.jpg"
CHANNEL_LINK = "https://t.me/+1NRRqUd1replNTM1"
CHANNEL_NAME = "мα∂αяα"

# ================= START BOT =================

app = Client(
    "ttt_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= STORAGE =================
games = {}
daily_data = {}
booster_data = {}
user_coins = {}
tournaments = {}
user_wins = {}
user_lose = {}
user_skins = {}
user_titles = {}
user_boards = {}
user_shields = {}
banned_users = set()

# ================= FONT CONVERTER =================

_FONT_MAP = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "αв¢∂єƒgнιנкℓмηoρqяѕтυνωхуzΑВ¢∂ЄƑGНΙנКLМΗOΡQЯЅТΥΝΩХΥZ0123456789"
)


def ff(text: str) -> str:
    return text.translate(_FONT_MAP)


# ================= HELPERS =================

foot = f"\n\n╔══════════════════════╗\n     👨‍💻 {CHANNEL_NAME}\n╚══════════════════════╝"


def cN(s):
    if not s:
        return "User"
    return re.sub(r"[_*`\[\]()]", " ", s).strip()


def chk(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    ]
    for s in wins:
        if (
            board[s[0]] != " "
            and board[s[0]] == board[s[1]]
            and board[s[1]] == board[s[2]]
        ):
            return board[s[0]]
    return None if " " in board else "draw"


def aiMv(g):
    empty = [i for i, v in enumerate(g["board"]) if v == " "]

    def fb(board, mark):
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6],
        ]
        for s in lines:
            line = [board[s[0]], board[s[1]], board[s[2]]]
            if line.count(mark) == 2 and " " in line:
                return s[line.index(" ")]
        return -1

    if g["type"] == "ai_easy":
        return random.choice(empty)

    move = fb(g["board"], "O")
    if move == -1:
        move = fb(g["board"], "X")

    if (g["type"] in ["ai_hard", "ai_medium"] or g.get("wager", 0) > 0) and move == -1:
        if g["board"][4] == " ":
            move = 4
        else:
            corners = [i for i in [0, 2, 6, 8] if g["board"][i] == " "]
            if corners:
                move = random.choice(corners)

    if move == -1 or move is None:
        move = random.choice(empty)

    return move


def gLink(cid, mid):
    return (
        "https://t.me/c/"
        + str(cid).replace("-100", "").replace("-", "")
        + "/"
        + str(mid)
    )


def getRank(wins):
    if wins >= 51:
        return {"icon": "👑", "name": "Champion", "tier": 5}
    if wins >= 31:
        return {"icon": "💎", "name": "Diamond", "tier": 4}
    if wins >= 16:
        return {"icon": "🥇", "name": "Gold", "tier": 3}
    if wins >= 6:
        return {"icon": "🥈", "name": "Silver", "tier": 2}
    return {"icon": "🥉", "name": "Bronze", "tier": 1}


def buildProfile(playerId, playerName):
    w = user_wins.get(playerId, 0)
    l = user_lose.get(playerId, 0)
    total = w + l
    rate = int((w / total) * 100) if total > 0 else 0
    bar = "▓" * (rate // 10) + "░" * (10 - rate // 10)
    rank = getRank(w)
    sk = user_skins.get(playerId)
    ti = user_titles.get(playerId)
    return (
        "┌──── 👤 " + cN(playerName) + " ────┐\n"
        + "│  " + rank["icon"] + " *Rank:* " + rank["name"] + "\n"
        + "│  ✅ *" + str(w) + "W* ❌ *" + str(l) + "L* 🎮 *" + str(total) + "* total\n"
        + "│  🎯 " + bar + " *" + str(rate) + "%* win rate\n"
        + "│  🎭 " + (sk["name"] if sk else "Default")
        + (" │ 🏷 " + ti if ti else "") + "\n"
        + "└────────────────────────────┘"
    )


def is_banned(user_id):
    return user_id in banned_users


async def render_board(client, gid):
    g = games.get(gid)
    if not g:
        return

    uid = g.get("p1")
    sk1 = user_skins.get(uid) or {"x": "❌", "o": "⭕"}
    sk2 = user_skins.get(g.get("p2")) if g.get("p2") and g.get("p2") != "bot" else {"x": "❌", "o": "⭕"}
    xI = sk1.get("x", "❌")
    oI = sk2.get("o", "⭕")
    bT = user_boards.get(uid) or {"empty": "·"}

    def gI(v):
        return xI if v == "X" else oI if v == "O" else bT.get("empty", "·")

    b = g["board"]

    p1 = cN(g.get("p1_name"))
    p2 = cN(g.get("p2_name", "AI"))
    t1 = user_titles.get(g["p1"])
    t2 = user_titles.get(g.get("p2")) if g.get("p2") and g.get("p2") != "bot" else None

    if g.get("status") == "finished":
        if g.get("winner") == "draw":
            txt = (
                "╔══════════════════════╗\n"
                "       🤝 *DRAW GAME*\n"
                "╚══════════════════════╝\n\n"
                + xI + " " + p1 + " vs " + oI + " " + p2 + "\n"
                + "𝗡𝗼 𝘄𝗶𝗻𝗻𝗲𝗿 𝘁𝗵𝗶𝘀 𝘁𝗶𝗺𝗲!"
                + foot
            )
        elif g.get("winner") == "resigned":
            resigner = g.get("resigner")
            winner_name = p2 if resigner == g["p1"] else p1
            loser_name = p1 if resigner == g["p1"] else p2
            txt = (
                "╔══════════════════════╗\n"
                "       🏳️ *RESIGNED*\n"
                "╚══════════════════════╝\n\n"
                + loser_name + " resigned!\n"
                + "🏆 " + winner_name + " wins!"
                + foot
            )
        else:
            winner_mark = g.get("winner")
            winner_name = p1 if winner_mark == "X" else p2
            winner_title = t1 if winner_mark == "X" else t2
            wager_txt = f"\n💰 *+{g['wager'] * 2}* coins!" if g.get("wager", 0) > 0 else ""
            txt = (
                "╔══════════════════════╗\n"
                "       🏆 *WINNER!*\n"
                "╚══════════════════════╝\n\n"
                + ("🏷 " + winner_title + "\n" if winner_title else "")
                + xI + " " + p1 + " vs " + oI + " " + p2 + "\n\n"
                + "🎉 *" + winner_name + "* wins!"
                + wager_txt
                + foot
            )
        gr = [
            [
                InlineKeyboardButton(gI(b[i]), callback_data="noop")
                for i in [0, 1, 2]
            ],
            [
                InlineKeyboardButton(gI(b[i]), callback_data="noop")
                for i in [3, 4, 5]
            ],
            [
                InlineKeyboardButton(gI(b[i]), callback_data="noop")
                for i in [6, 7, 8]
            ],
            [
                InlineKeyboardButton(
                    ff("🔁 Rematch"),
                    callback_data="ttt_rematch " + gid,
                    style=enums.ButtonStyle.SUCCESS
                )
            ],
        ]
    else:
        turn_id = g.get("turn")
        turn_name = p1 if turn_id == g["p1"] else (p2 if turn_id == g.get("p2") else "AI")
        wager_txt = f"\n💰 *Wager:* {g['wager']} coins" if g.get("wager", 0) > 0 else ""
        tourney_txt = "\n⚔️ Tournament Match" if g.get("tourney_id") else ""
        txt = (
            "╔══════════════════════╗\n"
            "       🎮 *TIC-TAC-TOE*\n"
            "╚══════════════════════╝\n\n"
            + xI + " " + p1 + " vs " + oI + " " + p2 + "\n\n"
            + "▶️ *" + turn_name + "'s turn*"
            + wager_txt
            + tourney_txt
            + foot
        )
        gr = [
            [
                InlineKeyboardButton(gI(b[i]), callback_data=f"ttt_move {gid} {i}")
                for i in [0, 1, 2]
            ],
            [
                InlineKeyboardButton(gI(b[i]), callback_data=f"ttt_move {gid} {i}")
                for i in [3, 4, 5]
            ],
            [
                InlineKeyboardButton(gI(b[i]), callback_data=f"ttt_move {gid} {i}")
                for i in [6, 7, 8]
            ],
            [
                InlineKeyboardButton(
                    ff("🏳️ Resign"),
                    callback_data="ttt_resign " + gid,
                    style=enums.ButtonStyle.DANGER
                )
            ],
        ]

    markup = InlineKeyboardMarkup(gr)

    if g.get("is_inline") and g.get("inline_mid"):
        url_req = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
        requests.post(url_req, json={
            "inline_message_id": g["inline_mid"],
            "text": txt,
            "reply_markup": {"inline_keyboard": [
                [{"text": btn.text, "callback_data": btn.callback_data} for btn in row]
                for row in gr
            ]},
            "parse_mode": "Markdown"
        })
    elif g.get("is_group") and g.get("group_cid") and g.get("group_mid"):
        try:
            await client.edit_message_text(
                chat_id=g["group_cid"],
                message_id=g["group_mid"],
                text=txt,
                reply_markup=markup,
                parse_mode=enums.ParseMode.MARKDOWN
            )
        except Exception:
            pass
    else:
        for cid, mid in [(g.get("p1"), g.get("p1_msg")), (g.get("p2"), g.get("p2_msg"))]:
            if cid and mid and cid != "bot":
                try:
                    await client.edit_message_text(
                        chat_id=cid,
                        message_id=mid,
                        text=txt,
                        reply_markup=markup,
                        parse_mode=enums.ParseMode.MARKDOWN
                    )
                except Exception:
                    pass


async def advanceTournament(client, tid, fgid):
    t = tournaments.get(tid)
    if not t or t["status"] != "active":
        return

    fg = games.get(fgid)
    if not fg:
        return

    wid = None
    if fg.get("winner") == "resigned":
        wid = fg["p2"] if fg.get("resigner") == fg["p1"] else fg["p1"]
    elif fg.get("winner") == "X":
        wid = fg["p1"]
    elif fg.get("winner") == "O":
        wid = fg["p2"]

    if wid:
        user_wins[wid] = user_wins.get(wid, 0) + 1
        loser = fg["p2"] if wid == fg["p1"] else fg["p1"]
        if loser:
            user_lose[loser] = user_lose.get(loser, 0) + 1

        cr = t["rounds"][t["current_round"]]
        me = None
        for m in cr:
            if m["gid"] == fgid:
                me = m
                break

        if me and not me.get("winner") and wid:
            wp = me["p1"] if wid == me["p1"]["id"] else me["p2"]
            lp = me["p2"] if wid == me["p1"]["id"] else me["p1"]
            me["winner"] = wp
            if "semifinal_losers" not in t:
                t["semifinal_losers"] = []
            t["semifinal_losers"].append(lp)

        nm = None
        for m in cr:
            if m.get("p2") and m.get("gid") and not m.get("winner"):
                nm = m
                break

        if nm:
            games[nm["gid"]] = {
                "id": nm["gid"],
                "p1": nm["p1"]["id"], "p1_name": nm["p1"]["name"],
                "p2": nm["p2"]["id"], "p2_name": nm["p2"]["name"],
                "board": [" "] * 9,
                "turn": nm["p1"]["id"],
                "status": "playing",
                "is_group": True,
                "group_cid": t["group_cid"],
                "group_mid": t["group_mid"],
                "type": "multi",
                "wager": 0,
                "tourney_id": tid,
            }
            lk = gLink(t["group_cid"], t["group_mid"])
            await client.send_message(nm["p1"]["id"], f"🎮 *YOUR MATCH!*\nVs {cN(nm['p2']['name'])}\n🔗 [Play]({lk})", parse_mode=enums.ParseMode.MARKDOWN)
            await client.send_message(nm["p2"]["id"], f"🎮 *YOUR MATCH!*\nVs {cN(nm['p1']['name'])}\n🔗 [Play]({lk})", parse_mode=enums.ParseMode.MARKDOWN)
            return

    rw = [m.get("winner") for m in t["rounds"][t["current_round"]] if m.get("winner") and m["winner"].get("id") != "split"]

    if len(rw) <= 1:
        ch = rw[0] if rw else None
        sl = t.get("semifinal_losers", [])
        ru = sl[-1] if len(sl) > 0 else None
        tp = sl[-2] if len(sl) > 1 else None

        if ch:
            user_coins[ch["id"]] = user_coins.get(ch["id"], 0) + 500
        if ru and ru.get("id") != "split":
            user_coins[ru["id"]] = user_coins.get(ru["id"], 0) + 200
        if tp and tp.get("id") != "split":
            user_coins[tp["id"]] = user_coins.get(tp["id"], 0) + 100

        rt = "╔══════════════════════╗\n       🏆 *TOURNAMENT OVER*\n╚══════════════════════╝\n\n"
        if ch:
            rt += f"🥇 {cN(ch['name'])} — +500\n"
            await client.send_message(ch["id"], "🏆 *YOU WON!* 🥇 +500 coins!" + foot, parse_mode=enums.ParseMode.MARKDOWN)
        if ru and ru.get("id") != "split":
            rt += f"🥈 {cN(ru['name'])} — +200\n"
            await client.send_message(ru["id"], "🥈 *2nd Place!* +200 coins!" + foot, parse_mode=enums.ParseMode.MARKDOWN)
        if tp and tp.get("id") != "split":
            rt += f"🥉 {cN(tp['name'])} — +100\n"
            await client.send_message(tp["id"], "🥉 *3rd Place!* +100 coins!" + foot, parse_mode=enums.ParseMode.MARKDOWN)

        rt += "\n🎉 GG!" + foot
        t["status"] = "finished"
        try:
            await client.edit_message_text(
                chat_id=t["group_cid"],
                message_id=t["group_mid"],
                text=rt,
                reply_markup=InlineKeyboardMarkup([]),
                parse_mode=enums.ParseMode.MARKDOWN
            )
        except Exception:
            pass
        return

    nrm = []
    for i in range(0, len(rw), 2):
        if i + 1 < len(rw):
            mg = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            nrm.append({"gid": mg, "p1": rw[i], "p2": rw[i + 1], "winner": None})
        else:
            nrm.append({"gid": None, "p1": rw[i], "p2": None, "winner": rw[i]})

    t["rounds"].append(nrm)
    t["current_round"] = len(t["rounds"]) - 1
    tournaments[tid] = t

    fnm = None
    for m in nrm:
        if m.get("p2") and m.get("gid"):
            fnm = m
            break

    if fnm:
        games[fnm["gid"]] = {
            "id": fnm["gid"],
            "p1": fnm["p1"]["id"], "p1_name": fnm["p1"]["name"],
            "p2": fnm["p2"]["id"], "p2_name": fnm["p2"]["name"],
            "board": [" "] * 9,
            "turn": fnm["p1"]["id"],
            "status": "playing",
            "is_group": True,
            "group_cid": t["group_cid"],
            "group_mid": t["group_mid"],
            "type": "multi",
            "wager": 0,
            "tourney_id": tid
        }
        lk = gLink(t["group_cid"], t["group_mid"])
        await client.send_message(fnm["p1"]["id"], f"🎮 *NEXT ROUND!*\nVs {cN(fnm['p2']['name'])}\n🔗 [Play]({lk})", parse_mode=enums.ParseMode.MARKDOWN)
        await client.send_message(fnm["p2"]["id"], f"🎮 *NEXT ROUND!*\nVs {cN(fnm['p1']['name'])}\n🔗 [Play]({lk})", parse_mode=enums.ParseMode.MARKDOWN)


async def show_menu(client, callback_query):
    uid = callback_query.from_user.id
    c = user_coins.get(uid, 0)
    w = user_wins.get(uid, 0)
    await callback_query.message.edit_text(
        "╔══════════════════════╗\n"
        "       🎮 *MAIN MENU*\n"
        "╚══════════════════════╝\n\n"
        "┌──── 💎  ʙᴀʟᴀɴᴄᴇ ────┐\n"
        f"│  💰 {c} ᴄᴏɪɴs  │  🏆 {w} ᴡɪɴs\n"
        "└────────────────────────┘\n\n"
        "𝗖𝗵𝗼𝗼𝘀𝗲 𝘆𝗼𝘂𝗿 𝗺𝗼𝗱𝗲 ⬇️"
        + foot,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(ff("🎯 Quick Match"), callback_data="ttt_quickmatch", style=enums.ButtonStyle.PRIMARY)],
            [
                InlineKeyboardButton(ff("👥 Multiplayer"), callback_data="ttt_multi", style=enums.ButtonStyle.PRIMARY),
                InlineKeyboardButton(ff("🤖 vs AI"), callback_data="ttt_ai_pick", style=enums.ButtonStyle.PRIMARY),
            ],
            [
                InlineKeyboardButton(ff("💰 Wager Match"), callback_data="ttt_wager_pick", style=enums.ButtonStyle.SUCCESS),
                InlineKeyboardButton(ff("🛒 Shop"), callback_data="ttt_shop", style=enums.ButtonStyle.SUCCESS),
            ],
            [
                InlineKeyboardButton(ff("🏆 Leaderboard"), callback_data="ttt_leaderboard", style=enums.ButtonStyle.PRIMARY),
                InlineKeyboardButton(ff("📊 Stats"), callback_data="ttt_stats", style=enums.ButtonStyle.PRIMARY),
            ],
            [InlineKeyboardButton(ff("🎁 Daily"), callback_data="ttt_daily", style=enums.ButtonStyle.SUCCESS)],
        ]),
        parse_mode=enums.ParseMode.MARKDOWN
    )


def build_main_menu_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(ff("🎯 Quick Match"), callback_data="ttt_quickmatch", style=enums.ButtonStyle.PRIMARY)],
        [
            InlineKeyboardButton(ff("👥 Multiplayer"), callback_data="ttt_multi", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(ff("🤖 vs AI"), callback_data="ttt_ai_pick", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(ff("💰 Wager Match"), callback_data="ttt_wager_pick", style=enums.ButtonStyle.SUCCESS),
            InlineKeyboardButton(ff("🛒 Shop"), callback_data="ttt_shop", style=enums.ButtonStyle.SUCCESS),
        ],
        [
            InlineKeyboardButton(ff("🏆 Leaderboard"), callback_data="ttt_leaderboard", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(ff("📊 Stats"), callback_data="ttt_stats", style=enums.ButtonStyle.PRIMARY),
        ],
        [InlineKeyboardButton(ff("🎁 Daily"), callback_data="ttt_daily", style=enums.ButtonStyle.SUCCESS)],
    ])


# ================= /START COMMAND =================

@app.on_message(filters.command("start"))
async def start(client, message):
    if is_banned(message.from_user.id):
        await message.reply_text("🚫 You are banned from using this bot.")
        return

    # Animation sequence
    loading_1 = await message.reply_text("<b>ʜʟᴏ</b>", parse_mode=enums.ParseMode.HTML)
    await asyncio.sleep(0.4)
    await loading_1.edit_text("<b>ʜʟᴏ ʙᴀʙʏ</b>", parse_mode=enums.ParseMode.HTML)
    await asyncio.sleep(0.4)
    await loading_1.edit_text("<b>ʟᴏᴀᴅɪɴɢ</b>", parse_mode=enums.ParseMode.HTML)
    await asyncio.sleep(0.3)
    await loading_1.edit_text("<b>ʟᴏᴀᴅɪɴɢ.</b>", parse_mode=enums.ParseMode.HTML)
    await asyncio.sleep(0.3)
    await loading_1.edit_text("<b>ʟᴏᴀᴅɪɴɢ..</b>", parse_mode=enums.ParseMode.HTML)
    await asyncio.sleep(0.3)
    await loading_1.edit_text("<b>ʟᴏᴀᴅɪɴɢ...</b>", parse_mode=enums.ParseMode.HTML)
    await asyncio.sleep(0.3)
    await loading_1.edit_text("<b>˹ 𝐌ᴀᴅᴀʀᴀ</b>", parse_mode=enums.ParseMode.HTML)
    await asyncio.sleep(0.4)
    await loading_1.edit_text("<b>˹ 𝐌ᴀᴅᴀʀᴀ ꭙ</b>", parse_mode=enums.ParseMode.HTML)
    await asyncio.sleep(0.4)
    await loading_1.edit_text("<b>˹ 𝐌ᴀᴅᴀʀᴀ ꭙ 𝐆ᴀᴍᴇ ♪ ˼</b>", parse_mode=enums.ParseMode.HTML)
    await asyncio.sleep(0.8)
    await loading_1.delete()

    uid = message.from_user.id
    c = user_coins.get(uid, 0)
    w = user_wins.get(uid, 0)
    name = message.from_user.first_name

    caption = (
        "╔══════════════════════╗\n"
        "       🎮 *MAIN MENU*\n"
        "╚══════════════════════╝\n\n"
        f"🙏 *Welcome, {cN(name)}!*\n\n"
        "┌──── 💎  ʙᴀʟᴀɴᴄᴇ ────┐\n"
        f"│  💰 {c} ᴄᴏɪɴs  │  🏆 {w} ᴡɪɴs\n"
        "└────────────────────────┘\n\n"
        "𝗖𝗵𝗼𝗼𝘀𝗲 𝘆𝗼𝘂𝗿 𝗺𝗼𝗱𝗲 ⬇️"
        + foot
    )

    try:
        await message.reply_photo(
            photo=START_IMAGE,
            caption=caption,
            reply_markup=build_main_menu_markup(),
            parse_mode=enums.ParseMode.MARKDOWN
        )
    except Exception:
        await message.reply_text(
            caption,
            reply_markup=build_main_menu_markup(),
            parse_mode=enums.ParseMode.MARKDOWN
        )


# ================= /CHALLENGE COMMAND =================

@app.on_message(filters.command("challenge"))
async def challenge(client, message):
    if is_banned(message.from_user.id):
        await message.reply_text("🚫 You are banned from using this bot.")
        return

    if message.chat.type == "private":
        await message.reply_text("❌ Use in a *Group*!", parse_mode=enums.ParseMode.MARKDOWN)
        return

    if len(message.command) < 2:
        await message.reply_text("Usage:\n`/challenge @user`\n`/challenge @user 100`", parse_mode=enums.ParseMode.MARKDOWN)
        return

    target = message.command[1]
    if not target.startswith("@"):
        await message.reply_text("❌ `/challenge @username`", parse_mode=enums.ParseMode.MARKDOWN)
        return

    target_user = target.replace("@", "")
    if message.from_user.username and message.from_user.username.lower() == target_user.lower():
        await message.reply_text("🚫 Can't challenge yourself!")
        return

    bet = 0
    if len(message.command) > 2:
        try:
            bet = max(0, int(message.command[2]))
        except Exception:
            bet = 0

    coins = user_coins.get(message.from_user.id, 0)
    if bet > 0 and coins < bet:
        await message.reply_text(f"❌ Need *{bet}*, have *{coins}*", parse_mode=enums.ParseMode.MARKDOWN)
        return

    gid = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    games[gid] = {
        "id": gid,
        "p1": message.from_user.id,
        "p1_name": message.from_user.first_name,
        "target_username": target_user,
        "p2": None, "p2_name": "???",
        "board": [" "] * 9,
        "turn": message.from_user.id,
        "status": "waiting_acceptance",
        "is_group": True,
        "group_cid": message.chat.id,
        "wager": bet
    }

    bet_line = f"\n💰 *Bet:* {bet} coins each!" if bet > 0 else ""
    sent = await message.reply_text(
        f"╔══════════════════════╗\n"
        f"       ⚔️ *CHALLENGE!*\n"
        f"╚══════════════════════╝\n\n"
        f"👤 *From:* {cN(message.from_user.first_name)}\n"
        f"🎯 *To:* {target}{bet_line}\n\n"
        f"{target}, accept the battle!\n\n"
        f"╔══════════════════════╗\n"
        f"     👨‍💻 {CHANNEL_NAME}\n"
        f"╚══════════════════════╝",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(ff("🤝 Accept Challenge"), callback_data=f"ttt_acc {gid}", style=enums.ButtonStyle.SUCCESS)]
        ]),
        parse_mode=enums.ParseMode.MARKDOWN
    )
    games[gid]["group_mid"] = sent.id


# ================= /DAILY COMMAND =================

@app.on_message(filters.command("daily"))
async def daily(client, message):
    if is_banned(message.from_user.id):
        await message.reply_text("🚫 You are banned from using this bot.")
        return

    user_id = message.from_user.id
    now = int(time.time())
    lc = daily_data.get(user_id)

    if lc and (now - lc) < 86400:
        r = 86400 - (now - lc)
        h = r // 3600
        m = (r % 3600) // 60
        await message.reply_text(f"⏰ Come back in *{h}h {m}m*", parse_mode=enums.ParseMode.MARKDOWN)
        return

    boost = booster_data.get(user_id)
    reward = 200 if (boost and (now - boost) < 604800) else 100
    user_coins[user_id] = user_coins.get(user_id, 0) + reward
    daily_data[user_id] = now

    msg = f"🎁 *+{reward} NepCoins!*"
    if reward > 100:
        msg += "\n🚀 *Booster 2x active!*"
    msg += f"\n💰 Balance: {user_coins[user_id]}"
    await message.reply_text(msg, parse_mode=enums.ParseMode.MARKDOWN)


# ================= /HELP COMMAND =================

@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    if is_banned(message.from_user.id):
        await message.reply_text("🚫 You are banned from using this bot.")
        return

    await message.reply_text(
        "╔══════════════════════╗\n"
        "       📖 *USER GUIDE*\n"
        "          ᴠ11  ᴘʀᴏ\n"
        "╚══════════════════════╝\n\n"
        "┌──── 🎮  ᴄᴏᴍᴍᴀɴᴅs ────┐\n"
        "│  `/start` — Menu\n"
        "│  `/daily` — +100 coins\n"
        "│  `/challenge @user` — Fight\n"
        "│  `/challenge @user 100` — Bet\n"
        "│  `/tournament` — Bracket\n"
        "│  `/help` — This guide\n"
        "└────────────────────────┘\n\n"
        "┌──── 🧠  ᴀɪ ʟᴇᴠᴇʟs ────┐\n"
        "│  🟢 Easy ∙ 🟡 Med ∙ 🔴 Hard\n"
        "└────────────────────────┘\n\n"
        "┌──── 🛒  sʜᴏᴘ ────┐\n"
        "│  🎭 10 Skins (200-300)\n"
        "│  🏷 5 Titles (150-400)\n"
        "│  🎨 4 Boards (100-200)\n"
        "│  🎰 Lucky Box (150)\n"
        "│  🚀 Booster 2x daily (500)\n"
        "│  🛡 Shield 3 losses (300)\n"
        "└────────────────────────┘\n\n"
        "┌──── ⚔️  ᴛᴏᴜʀɴᴇʏ ────┐\n"
        "│  🥇 1st: 500 coins\n"
        "│  🥈 2nd: 200 coins\n"
        "│  🥉 3rd: 100 coins\n"
        "└────────────────────────┘\n\n"
        f"╔══════════════════════╗\n"
        f"     👨‍💻 {CHANNEL_NAME}\n"
        f"╚══════════════════════╝",
        parse_mode=enums.ParseMode.MARKDOWN
    )


# ================= /TOURNAMENT COMMAND =================

@app.on_message(filters.command("tournament"))
async def tournament_cmd(client, message):
    if is_banned(message.from_user.id):
        await message.reply_text("🚫 You are banned from using this bot.")
        return

    if message.chat.type == "private":
        await message.reply_text("❌ Use in a *Group*!", parse_mode=enums.ParseMode.MARKDOWN)
        return

    tid = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    t = {
        "id": tid,
        "creator": message.from_user.id,
        "creator_name": message.from_user.first_name,
        "players": [{"id": message.from_user.id, "name": message.from_user.first_name}],
        "max": 8,
        "status": "registering",
        "rounds": [],
        "current_round": 0,
        "group_cid": message.chat.id,
        "group_mid": None,
        "semifinal_losers": []
    }
    res = await message.reply_text(
        "╔══════════════════════╗\n"
        "       ⚔️ *TOURNAMENT*\n"
        "╚══════════════════════╝\n\n"
        f"🎮 Host: {cN(message.from_user.first_name)}\n"
        "👥 Players: 1/8\n\n"
        f"1. {cN(message.from_user.first_name)}\n\n"
        "┌──── 🏆  ᴘʀɪᴢᴇs ────┐\n"
        "│  🥇 1st — 500 coins\n"
        "│  🥈 2nd — 200 coins\n"
        "│  🥉 3rd — 100 coins\n"
        "└────────────────────────┘"
        + foot,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(ff("🎮 Join Tournament"), callback_data="trn_join " + tid, style=enums.ButtonStyle.PRIMARY)],
            [InlineKeyboardButton(ff("🚀 Begin"), callback_data="trn_start " + tid, style=enums.ButtonStyle.SUCCESS)],
        ]),
        parse_mode=enums.ParseMode.MARKDOWN
    )
    if res:
        t["group_mid"] = res.id
    tournaments["trn_" + tid] = t


# ================= /PING COMMAND =================

@app.on_message(filters.command("ping"))
async def ping(client, message):
    if is_banned(message.from_user.id):
        await message.reply_text("🚫 You are banned from using this bot.")
        return

    start_t = time.time()
    msg = await message.reply_text("🏓 Pinging...")
    elapsed = round((time.time() - start_t) * 1000)
    await msg.delete()

    caption = (
        "╔══════════════════════╗\n"
        "       🏓 *PONG!*\n"
        "╚══════════════════════╝\n\n"
        f"⚡ Speed: `{elapsed}ms`\n"
        f"🤖 Bot: *Online*\n"
        f"🎮 Status: *Ready to play!*"
        + foot
    )
    try:
        await message.reply_photo(
            photo=START_IMAGE,
            caption=caption,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff("🎮 Play Now"), callback_data="ttt_restart", style=enums.ButtonStyle.PRIMARY)]
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
    except Exception:
        await message.reply_text(caption, parse_mode=enums.ParseMode.MARKDOWN)


# ================= OWNER COMMANDS =================

@app.on_message(filters.command("addcoins") & filters.user(OWNER_ID))
async def add_coins(client, message):
    if len(message.command) < 3:
        await message.reply_text("Usage: `/addcoins <user_id> <amount>`", parse_mode=enums.ParseMode.MARKDOWN)
        return
    try:
        target_id = int(message.command[1])
        amount = int(message.command[2])
    except ValueError:
        await message.reply_text("❌ Invalid user ID or amount.")
        return
    user_coins[target_id] = user_coins.get(target_id, 0) + amount
    await message.reply_text(
        f"✅ *Added {amount} coins* to user `{target_id}`\n"
        f"💰 New balance: *{user_coins[target_id]}*",
        parse_mode=enums.ParseMode.MARKDOWN
    )


@app.on_message(filters.command("removecoins") & filters.user(OWNER_ID))
async def remove_coins(client, message):
    if len(message.command) < 3:
        await message.reply_text("Usage: `/removecoins <user_id> <amount>`", parse_mode=enums.ParseMode.MARKDOWN)
        return
    try:
        target_id = int(message.command[1])
        amount = int(message.command[2])
    except ValueError:
        await message.reply_text("❌ Invalid user ID or amount.")
        return
    user_coins[target_id] = max(0, user_coins.get(target_id, 0) - amount)
    await message.reply_text(
        f"✅ *Removed {amount} coins* from user `{target_id}`\n"
        f"💰 New balance: *{user_coins[target_id]}*",
        parse_mode=enums.ParseMode.MARKDOWN
    )


@app.on_message(filters.command("setcoins") & filters.user(OWNER_ID))
async def set_coins(client, message):
    if len(message.command) < 3:
        await message.reply_text("Usage: `/setcoins <user_id> <amount>`", parse_mode=enums.ParseMode.MARKDOWN)
        return
    try:
        target_id = int(message.command[1])
        amount = int(message.command[2])
    except ValueError:
        await message.reply_text("❌ Invalid user ID or amount.")
        return
    user_coins[target_id] = amount
    await message.reply_text(
        f"✅ *Set coins* for user `{target_id}` to *{amount}*",
        parse_mode=enums.ParseMode.MARKDOWN
    )


@app.on_message(filters.command("ban") & filters.user(OWNER_ID))
async def ban_user(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/ban <user_id>`", parse_mode=enums.ParseMode.MARKDOWN)
        return
    try:
        target_id = int(message.command[1])
    except ValueError:
        await message.reply_text("❌ Invalid user ID.")
        return
    if target_id == OWNER_ID:
        await message.reply_text("❌ Cannot ban the owner!")
        return
    banned_users.add(target_id)
    await message.reply_text(f"🚫 User `{target_id}` has been *banned*.", parse_mode=enums.ParseMode.MARKDOWN)


@app.on_message(filters.command("unban") & filters.user(OWNER_ID))
async def unban_user(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/unban <user_id>`", parse_mode=enums.ParseMode.MARKDOWN)
        return
    try:
        target_id = int(message.command[1])
    except ValueError:
        await message.reply_text("❌ Invalid user ID.")
        return
    banned_users.discard(target_id)
    await message.reply_text(f"✅ User `{target_id}` has been *unbanned*.", parse_mode=enums.ParseMode.MARKDOWN)


@app.on_message(filters.command("bannedlist") & filters.user(OWNER_ID))
async def banned_list(client, message):
    if not banned_users:
        await message.reply_text("✅ No banned users.", parse_mode=enums.ParseMode.MARKDOWN)
        return
    ids = "\n".join(f"• `{uid}`" for uid in banned_users)
    await message.reply_text(f"🚫 *Banned Users:*\n{ids}", parse_mode=enums.ParseMode.MARKDOWN)


@app.on_message(filters.command("ownerhelp") & filters.user(OWNER_ID))
async def owner_help(client, message):
    await message.reply_text(
        "╔══════════════════════╗\n"
        "       👑 *OWNER PANEL*\n"
        "╚══════════════════════╝\n\n"
        "┌──── 💰 ᴄᴏɪɴ ᴄᴏᴍᴍᴀɴᴅs ────┐\n"
        "│ `/addcoins <id> <amt>` — Add coins\n"
        "│ `/removecoins <id> <amt>` — Remove coins\n"
        "│ `/setcoins <id> <amt>` — Set coins\n"
        "└────────────────────────┘\n\n"
        "┌──── 🚫 ʙᴀɴ ᴄᴏᴍᴍᴀɴᴅs ────┐\n"
        "│ `/ban <id>` — Ban user\n"
        "│ `/unban <id>` — Unban user\n"
        "│ `/bannedlist` — List banned users\n"
        "└────────────────────────┘",
        parse_mode=enums.ParseMode.MARKDOWN
    )


# ================= CALLBACK QUERY HANDLER =================

@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    if not data or data == "noop":
        await callback_query.answer()
        return

    user_id = callback_query.from_user.id

    if is_banned(user_id):
        await callback_query.answer("🚫 You are banned from using this bot.", show_alert=True)
        return

    # ═══ MENU ═══
    if data == "ttt_restart":
        await show_menu(client, callback_query)
        return

    # ═══ AI PICK ═══
    if data == "ttt_ai_pick":
        await callback_query.message.edit_text(
            "╔══════════════════════╗\n"
            "       🤖 *VS AI*\n"
            "╚══════════════════════╝\n\n"
            "Choose difficulty:" + foot,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(ff("🟢 Easy"), callback_data="ttt_go ai_easy", style=enums.ButtonStyle.SUCCESS),
                    InlineKeyboardButton(ff("🟡 Medium"), callback_data="ttt_go ai_medium", style=enums.ButtonStyle.PRIMARY),
                    InlineKeyboardButton(ff("🔴 Hard"), callback_data="ttt_go ai_hard", style=enums.ButtonStyle.DANGER),
                ],
                [InlineKeyboardButton(ff("🔙 Menu"), callback_data="ttt_restart", style=enums.ButtonStyle.PRIMARY)],
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    # ═══ GAME INIT (AI or Multiplayer) ═══
    if data == "ttt_multi" or data.startswith("ttt_go "):
        ty = "multi" if data == "ttt_multi" else data.split(" ")[1]
        ng = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        is_ai = ty in ["ai_easy", "ai_medium", "ai_hard"]
        games[ng] = {
            "id": ng,
            "p1": user_id,
            "p1_name": callback_query.from_user.first_name,
            "p1_msg": None,
            "p2": "bot" if is_ai else None,
            "p2_name": "AI" if is_ai else "???",
            "p2_msg": None,
            "board": [" "] * 9,
            "turn": user_id,
            "status": "playing" if is_ai else "waiting",
            "type": ty,
            "wager": 0,
        }
        if is_ai:
            res = await callback_query.message.edit_text("🎮 *Game starting...*", parse_mode=enums.ParseMode.MARKDOWN)
            games[ng]["p1_msg"] = res.id
            await render_board(client, ng)
        else:
            me = await client.get_me()
            link = f"https://t.me/{me.username}?start=ttt_{ng}"
            res = await callback_query.message.edit_text(
                "╔══════════════════════╗\n"
                "       👥 *MULTIPLAYER*\n"
                "╚══════════════════════╝\n\n"
                "Share this link to invite a friend!\n\n"
                f"🔗 `{link}`"
                + foot,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(ff("❌ Cancel"), callback_data=f"ttt_cancel {ng}", style=enums.ButtonStyle.DANGER)],
                ]),
                parse_mode=enums.ParseMode.MARKDOWN
            )
            games[ng]["p1_msg"] = res.id
        return

    # ═══ ACCEPT CHALLENGE ═══
    if data.startswith("ttt_acc "):
        gid = data.split(" ")[1]
        g = games.get(gid)
        if not g or g["status"] != "waiting_acceptance":
            await callback_query.answer("Game no longer available!", show_alert=True)
            return

        uname = (callback_query.from_user.username or "").lower()
        target = (g.get("target_username") or "").lower()
        if uname and target and uname != target:
            return await callback_query.answer(f"🚫 Only @{g['target_username']}!", show_alert=True)

        if g.get("wager", 0) > 0:
            pc = user_coins.get(user_id, 0)
            if pc < g["wager"]:
                return await callback_query.answer(f"❌ Need {g['wager']} coins!", show_alert=True)
            user_coins[user_id] = user_coins.get(user_id, 0) - g["wager"]

        g["p2"] = user_id
        g["p2_name"] = callback_query.from_user.first_name
        g["status"] = "playing"
        g["turn"] = g["p1"]

        res1 = await client.send_message(g["p1"], "🎮 *Game started!*", parse_mode=enums.ParseMode.MARKDOWN)
        g["p1_msg"] = res1.id
        res2 = await callback_query.message.reply_text("🎮 *Game started!*", parse_mode=enums.ParseMode.MARKDOWN)
        g["p2_msg"] = res2.id
        games[gid] = g
        await render_board(client, gid)
        await callback_query.answer("✅ Accepted!")
        return

    # ═══ CANCEL GAME ═══
    if data.startswith("ttt_cancel "):
        gid = data.split(" ")[1]
        g = games.get(gid)
        if not g:
            return
        if user_id == g["p1"]:
            if g.get("wager", 0) > 0:
                user_coins[user_id] = user_coins.get(user_id, 0) + g["wager"]
            games.pop(gid, None)
            await show_menu(client, callback_query)
        return

    # ═══ QUICK MATCH (Matchmaking) ═══
    if data == "ttt_quickmatch":
        now = int(time.time())
        queue = tournaments.get("mm_queue", [])
        queue = [q for q in queue if now - q["timestamp"] < 300 and q["id"] != user_id]

        if len(queue) > 0:
            opponent = queue.pop(0)
            tournaments["mm_queue"] = queue
            gid = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            games[gid] = {
                "id": gid,
                "p1": opponent["id"], "p1_name": opponent["name"],
                "p2": user_id, "p2_name": callback_query.from_user.first_name,
                "p1_msg": None, "p2_msg": None,
                "p1_ready": False, "p2_ready": False,
                "board": [" "] * 9,
                "turn": opponent["id"],
                "status": "confirming",
                "type": "multi",
                "wager": 0,
                "is_quickmatch": True
            }
            p1Profile = buildProfile(opponent["id"], opponent["name"])
            p2Profile = buildProfile(user_id, callback_query.from_user.first_name)

            if opponent.get("msg_id"):
                try:
                    await client.edit_message_text(
                        chat_id=opponent["id"],
                        message_id=opponent["msg_id"],
                        text=(
                            "╔══════════════════════╗\n       🎯 *MATCH FOUND!*\n╚══════════════════════╝\n\n"
                            "Your opponent:\n\n" + p2Profile + "\n\nPress ✅ Ready to start!" + foot
                        ),
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton(ff("✅ Ready!"), callback_data=f"ttt_qready {gid}", style=enums.ButtonStyle.SUCCESS)],
                            [InlineKeyboardButton(ff("❌ Decline"), callback_data=f"ttt_qdecline {gid}", style=enums.ButtonStyle.DANGER)],
                        ]),
                        parse_mode=enums.ParseMode.MARKDOWN
                    )
                    games[gid]["p1_confirm_msg"] = opponent["msg_id"]
                except Exception:
                    pass

            await callback_query.message.edit_text(
                "╔══════════════════════╗\n       🎯 *MATCH FOUND!*\n╚══════════════════════╝\n\n"
                "Your opponent:\n\n" + p1Profile + "\n\nPress ✅ Ready to start!" + foot,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(ff("✅ Ready!"), callback_data=f"ttt_qready {gid}", style=enums.ButtonStyle.SUCCESS)],
                    [InlineKeyboardButton(ff("❌ Decline"), callback_data=f"ttt_qdecline {gid}", style=enums.ButtonStyle.DANGER)],
                ]),
                parse_mode=enums.ParseMode.MARKDOWN
            )
            games[gid]["p2_confirm_msg"] = callback_query.message.id
            await callback_query.answer("🎯 Match Found!")
        else:
            queue.append({
                "id": user_id,
                "name": callback_query.from_user.first_name,
                "chat_id": callback_query.message.chat.id,
                "msg_id": callback_query.message.id,
                "timestamp": now
            })
            tournaments["mm_queue"] = queue
            myProfile = buildProfile(user_id, callback_query.from_user.first_name)
            await callback_query.message.edit_text(
                "╔══════════════════════╗\n       🎯 *QUICK MATCH*\n╚══════════════════════╝\n\n"
                "🔍 *Searching for opponent...*\n\n"
                "┌──── ⏳ sᴛᴀᴛᴜs ────┐\n│ Waiting for a player...\n│ ⏱ Timeout: 5 minutes\n└────────────────────┘\n\n"
                "Your profile:\n\n" + myProfile + "\n\n💡 _Invite friends to play!_" + foot,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(ff("🔄 Refresh"), callback_data="ttt_qrefresh", style=enums.ButtonStyle.PRIMARY)],
                    [InlineKeyboardButton(ff("❌ Cancel Search"), callback_data="ttt_qcancel", style=enums.ButtonStyle.DANGER)],
                ]),
                parse_mode=enums.ParseMode.MARKDOWN
            )
            await callback_query.answer("🔍 Searching...")
        return

    # ═══ QUICK MATCH READY ═══
    if data.startswith("ttt_qready "):
        gid = data.split(" ")[1]
        g = games.get(gid)
        if not g or g["status"] != "confirming":
            return

        if user_id == g["p1"]:
            g["p1_ready"] = True
        elif user_id == g["p2"]:
            g["p2_ready"] = True
        else:
            await callback_query.answer("🚫 Not your match!", show_alert=True)
            return

        if g["p1_ready"] and g["p2_ready"]:
            g["status"] = "playing"
            res1 = await client.send_message(g["p1"], "🎮 *Game starting...*", parse_mode=enums.ParseMode.MARKDOWN)
            if res1:
                g["p1_msg"] = res1.id
            res2 = await client.send_message(g["p2"], "🎮 *Game starting...*", parse_mode=enums.ParseMode.MARKDOWN)
            if res2:
                g["p2_msg"] = res2.id
            games[gid] = g
            await render_board(client, gid)
            for pid, mid in [(g["p1"], g.get("p1_confirm_msg")), (g["p2"], g.get("p2_confirm_msg"))]:
                if mid:
                    try:
                        await client.edit_message_text(
                            chat_id=pid, message_id=mid,
                            text="╔══════════════════════╗\n       ✅ *GAME ON!*\n╚══════════════════════╝\n\n🎮 Both players ready!\n⬇️ Board is below." + foot,
                            parse_mode=enums.ParseMode.MARKDOWN
                        )
                    except Exception:
                        pass
            await callback_query.answer("🎮 Game started!")
        else:
            games[gid] = g
            await callback_query.message.edit_text(
                "╔══════════════════════╗\n       🎯 *MATCH FOUND!*\n╚══════════════════════╝\n\n✅ *You are READY!*\n\n⏳ Waiting for opponent to confirm..." + foot,
                parse_mode=enums.ParseMode.MARKDOWN
            )
            await callback_query.answer("✅ Ready! Waiting for opponent...")
        return

    # ═══ QUICK MATCH DECLINE ═══
    if data.startswith("ttt_qdecline "):
        gid = data.split(" ")[1]
        g = games.get(gid)
        if not g or g["status"] != "confirming":
            return

        g["status"] = "declined"
        games[gid] = g
        decliner_id = user_id
        other_id = g["p2"] if decliner_id == g["p1"] else g["p1"]
        other_msg = g.get("p2_confirm_msg") if decliner_id == g["p1"] else g.get("p1_confirm_msg")

        if other_msg:
            try:
                await client.edit_message_text(
                    chat_id=other_id, message_id=other_msg,
                    text="╔══════════════════════╗\n       ❌ *DECLINED*\n╚══════════════════════╝\n\nOpponent declined the match.\nSearch again!" + foot,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(ff("🎯 Search Again"), callback_data="ttt_quickmatch", style=enums.ButtonStyle.PRIMARY)],
                        [InlineKeyboardButton(ff("🔙 Menu"), callback_data="ttt_restart", style=enums.ButtonStyle.PRIMARY)],
                    ]),
                    parse_mode=enums.ParseMode.MARKDOWN
                )
            except Exception:
                pass

        await callback_query.answer("❌ Match declined.")
        await show_menu(client, callback_query)
        return

    # ═══ QUICK MATCH REFRESH ═══
    if data == "ttt_qrefresh":
        now = int(time.time())
        queue = tournaments.get("mm_queue", [])
        queue = [q for q in queue if now - q["timestamp"] < 300]
        me = next((q for q in queue if q["id"] == user_id), None)
        if not me:
            tournaments["mm_queue"] = queue
            try:
                await callback_query.message.edit_text(
                    "╔══════════════════════╗\n       🎯 *QUICK MATCH*\n╚══════════════════════╝\n\n❌ *Match not found.*\nNo users online.\n\nTry again later!" + foot,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(ff("🎯 Try Again"), callback_data="ttt_quickmatch", style=enums.ButtonStyle.PRIMARY)],
                        [InlineKeyboardButton(ff("🔙 Menu"), callback_data="ttt_restart", style=enums.ButtonStyle.PRIMARY)],
                    ]),
                    parse_mode=enums.ParseMode.MARKDOWN
                )
            except Exception:
                pass
            await callback_query.answer("⏰ Search expired!", show_alert=True)
        else:
            elapsed = now - me["timestamp"]
            remaining = 300 - elapsed
            await callback_query.answer(f"🔍 Still searching... ({remaining//60}m {remaining%60}s left)")
        return

    # ═══ CANCEL SEARCH ═══
    if data == "ttt_qcancel":
        queue = tournaments.get("mm_queue", [])
        tournaments["mm_queue"] = [q for q in queue if q["id"] != user_id]
        await callback_query.answer("❌ Search cancelled.")
        await show_menu(client, callback_query)
        return

    # ═══ DAILY REWARD ═══
    if data == "ttt_daily":
        now = int(time.time())
        lc = daily_data.get(user_id)
        if lc and (now - lc) < 86400:
            r = 86400 - (now - lc)
            await callback_query.answer(f"⏰ {r//3600}h {(r%3600)//60}m", show_alert=True)
            return
        boost = booster_data.get(user_id)
        reward = 200 if (boost and (now - boost) < 604800) else 100
        user_coins[user_id] = user_coins.get(user_id, 0) + reward
        daily_data[user_id] = now
        await callback_query.answer(f"🎁 +{reward} coins!" + (" (2x Boost!)" if reward > 100 else ""), show_alert=True)
        await show_menu(client, callback_query)
        return

    # ═══ STATS ═══
    if data == "ttt_stats":
        w = user_wins.get(user_id, 0)
        l = user_lose.get(user_id, 0)
        c = user_coins.get(user_id, 0)
        sk = user_skins.get(user_id)
        ti = user_titles.get(user_id)
        bd = user_boards.get(user_id)
        sh = user_shields.get(user_id, 0)
        rate = 0 if (w + l) == 0 else (w * 100 // (w + l))
        bar = "▓" * (rate // 10) + "░" * (10 - (rate // 10))
        await callback_query.message.edit_text(
            "╔══════════════════════╗\n       📊 *MY PROFILE*\n╚══════════════════════╝\n\n"
            "┌──── ⚔️  ʙᴀᴛᴛʟᴇ ʟᴏɢ ────┐\n"
            f"│  ✅ Wins: *{w}*\n│  ❌ Losses: *{l}*\n│  📊 {bar} *{rate}%*\n"
            "└────────────────────────────┘\n\n"
            "┌──── 🎒  ɪɴᴠᴇɴᴛᴏʀʏ ────┐\n"
            f"│  💰 *{c}* NepCoins\n"
            f"│  🎭 {(sk['name'] if sk else 'Default')}\n"
            f"│  🏷 {(ti if ti else 'None')}\n"
            f"│  🎨 {(bd['name'] if bd else 'Classic')}\n"
            f"│  🛡 {sh} shields left\n"
            "└────────────────────────────┘" + foot,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff("🔙 Back"), callback_data="ttt_restart", style=enums.ButtonStyle.PRIMARY)]
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    # ═══ LEADERBOARD ═══
    if data == "ttt_leaderboard":
        so = sorted(user_wins.items(), key=lambda x: x[1], reverse=True)[:10]
        t_txt = "╔══════════════════════╗\n       🏆 *CHAMPIONS*\n╚══════════════════════╝\n\n"
        if not so:
            t_txt += "_No heroes yet!_"
        for i, (pid, wins) in enumerate(so):
            prefix = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  •"
            t_txt += f"{prefix} `{pid}`: *{wins} W*\n"
        await callback_query.message.edit_text(
            t_txt + foot,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff("🔙 Back"), callback_data="ttt_restart", style=enums.ButtonStyle.PRIMARY)]
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    # ═══ SHOP ═══
    if data == "ttt_shop":
        c = user_coins.get(user_id, 0)
        await callback_query.message.edit_text(
            "╔══════════════════════╗\n       🛒 *SHOP*\n╚══════════════════════╝\n\n"
            f"┌──── 💎 ────┐\n│  💰 *{c}* coins\n└──────────────┘\n\n"
            "🎭 *Skins* — Custom X/O marks\n"
            "🏷 *Titles* — Victory badges\n"
            "🎨 *Boards* — Grid themes\n"
            "🎰 *Lucky Box* — Gamble!\n"
            "🚀 *Booster* — 2x daily\n"
            "🛡 *Shield* — Block losses" + foot,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff("🎭 Skins"), callback_data="ttt_skins", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton(ff("🏷 Titles"), callback_data="ttt_titles", style=enums.ButtonStyle.PRIMARY)],
                [InlineKeyboardButton(ff("🎨 Boards"), callback_data="ttt_boards", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton(ff("🎰 Lucky ₡150"), callback_data="ttt_lucky", style=enums.ButtonStyle.SUCCESS)],
                [InlineKeyboardButton(ff("🚀 Booster ₡500"), callback_data="ttt_booster", style=enums.ButtonStyle.SUCCESS), InlineKeyboardButton(ff("🛡 Shield ₡300"), callback_data="ttt_shield", style=enums.ButtonStyle.SUCCESS)],
                [InlineKeyboardButton(ff("🔙 Menu"), callback_data="ttt_restart", style=enums.ButtonStyle.PRIMARY)],
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    # ═══ SKINS PAGE 1 ═══
    if data == "ttt_skins":
        await callback_query.message.edit_text(
            "╔══════════════════════╗\n       🎭 *SKINS*\n╚══════════════════════╝\n\n200 coins each — Page 1" + foot,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff("🔥 Fire"), callback_data="ttt_buy fire", style=enums.ButtonStyle.DANGER), InlineKeyboardButton(ff("👑 Royal"), callback_data="ttt_buy royal", style=enums.ButtonStyle.SUCCESS), InlineKeyboardButton(ff("🐱 Pets"), callback_data="ttt_buy pets", style=enums.ButtonStyle.PRIMARY)],
                [InlineKeyboardButton(ff("⚡ Energy"), callback_data="ttt_buy energy", style=enums.ButtonStyle.SUCCESS), InlineKeyboardButton(ff("🌟 Stars"), callback_data="ttt_buy stars", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton(ff("🌈 Rainbow"), callback_data="ttt_buy rainbow", style=enums.ButtonStyle.PRIMARY)],
                [InlineKeyboardButton(ff("Page 2 →"), callback_data="ttt_skins2", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton(ff("❌ Default (Free)"), callback_data="ttt_buy default", style=enums.ButtonStyle.DANGER)],
                [InlineKeyboardButton(ff("🔙 Shop"), callback_data="ttt_shop", style=enums.ButtonStyle.PRIMARY)],
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    # ═══ SKINS PAGE 2 ═══
    if data == "ttt_skins2":
        await callback_query.message.edit_text(
            "╔══════════════════════╗\n       🎭 *PREMIUM SKINS*\n╚══════════════════════╝\n\n300 coins each — Page 2" + foot,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff("🎃 Halloween"), callback_data="ttt_buy halloween", style=enums.ButtonStyle.DANGER), InlineKeyboardButton(ff("🎄 Xmas"), callback_data="ttt_buy xmas", style=enums.ButtonStyle.SUCCESS)],
                [InlineKeyboardButton(ff("👾 Alien"), callback_data="ttt_buy alien", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton(ff("🍔 Food"), callback_data="ttt_buy food", style=enums.ButtonStyle.SUCCESS)],
                [InlineKeyboardButton(ff("← Page 1"), callback_data="ttt_skins", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton(ff("🔙 Shop"), callback_data="ttt_shop", style=enums.ButtonStyle.PRIMARY)],
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    # ═══ BUY SKINS ═══
    if data.startswith("ttt_buy "):
        si = data.split(" ")[1]
        sk_catalog = {
            "fire": {"name": "Fire", "x": "🔥", "o": "❄️", "cost": 200},
            "royal": {"name": "Royal", "x": "👑", "o": "💎", "cost": 200},
            "pets": {"name": "Pets", "x": "🐱", "o": "🐶", "cost": 200},
            "energy": {"name": "Energy", "x": "⚡", "o": "💥", "cost": 200},
            "stars": {"name": "Stars", "x": "⭐", "o": "🌙", "cost": 200},
            "rainbow": {"name": "Rainbow", "x": "🟥", "o": "🟦", "cost": 200},
            "halloween": {"name": "Halloween", "x": "🎃", "o": "👻", "cost": 300},
            "xmas": {"name": "Xmas", "x": "🎅", "o": "🎄", "cost": 300},
            "alien": {"name": "Alien", "x": "👾", "o": "🛸", "cost": 300},
            "food": {"name": "Food", "x": "🍔", "o": "🍕", "cost": 300},
            "default": {"name": "Default", "x": "❌", "o": "⭕", "cost": 0},
        }
        ch = sk_catalog.get(si)
        if not ch:
            return
        c = user_coins.get(user_id, 0)
        if c < ch["cost"]:
            return await callback_query.answer(f"❌ Need {ch['cost']} coins!", show_alert=True)
        if ch["cost"] > 0:
            user_coins[user_id] = c - ch["cost"]
        user_skins[user_id] = ch
        await callback_query.answer(f"🎭 {ch['name']} equipped! {ch['x']}/{ch['o']}", show_alert=True)
        await show_menu(client, callback_query)
        return

    # ═══ TITLES ═══
    if data == "ttt_titles":
        await callback_query.message.edit_text(
            "╔══════════════════════╗\n       🏷 *TITLES*\n╚══════════════════════╝\n\nShown when you win!" + foot,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff("⚡ Lightning ₡150"), callback_data="ttt_tit lightning", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton(ff("🐉 Dragon ₡150"), callback_data="ttt_tit dragon", style=enums.ButtonStyle.PRIMARY)],
                [InlineKeyboardButton(ff("💀 Destroyer ₡250"), callback_data="ttt_tit destroyer", style=enums.ButtonStyle.DANGER), InlineKeyboardButton(ff("👑 King ₡250"), callback_data="ttt_tit king", style=enums.ButtonStyle.SUCCESS)],
                [InlineKeyboardButton(ff("🔱 God of War ₡400"), callback_data="ttt_tit godofwar", style=enums.ButtonStyle.DANGER), InlineKeyboardButton(ff("❌ Remove"), callback_data="ttt_tit none", style=enums.ButtonStyle.DANGER)],
                [InlineKeyboardButton(ff("🔙 Shop"), callback_data="ttt_shop", style=enums.ButtonStyle.PRIMARY)],
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    # ═══ BUY TITLES ═══
    if data.startswith("ttt_tit "):
        ti_key = data.split(" ")[1]
        ts = {
            "lightning": {"name": "⚡ Lightning", "cost": 150},
            "dragon": {"name": "🐉 Dragon", "cost": 150},
            "destroyer": {"name": "💀 Destroyer", "cost": 250},
            "king": {"name": "👑 King", "cost": 250},
            "godofwar": {"name": "🔱 God of War", "cost": 400},
            "none": {"name": None, "cost": 0},
        }
        ch = ts.get(ti_key)
        if not ch:
            return
        c = user_coins.get(user_id, 0)
        if c < ch["cost"]:
            return await callback_query.answer(f"❌ Need {ch['cost']} coins!", show_alert=True)
        if ch["cost"] > 0:
            user_coins[user_id] = c - ch["cost"]
        user_titles[user_id] = ch["name"]
        msg = "Removed!" if not ch["name"] else f"{ch['name']} equipped!"
        await callback_query.answer("🏷 " + msg, show_alert=True)
        await show_menu(client, callback_query)
        return

    # ═══ BOARDS ═══
    if data == "ttt_boards":
        await callback_query.message.edit_text(
            "╔══════════════════════╗\n       🎨 *BOARDS*\n╚══════════════════════╝\n\nChanges empty cell style!" + foot,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff("▫️ Clean ₡100"), callback_data="ttt_brd clean", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton(ff("🔲 Bold ₡100"), callback_data="ttt_brd bold", style=enums.ButtonStyle.PRIMARY)],
                [InlineKeyboardButton(ff("💠 Diamond ₡200"), callback_data="ttt_brd diamond", style=enums.ButtonStyle.SUCCESS), InlineKeyboardButton(ff("🟢 Neon ₡200"), callback_data="ttt_brd neon", style=enums.ButtonStyle.SUCCESS)],
                [InlineKeyboardButton(ff("· Classic (Free)"), callback_data="ttt_brd default", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton(ff("🔙 Shop"), callback_data="ttt_shop", style=enums.ButtonStyle.PRIMARY)],
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    # ═══ BOARD BUY ═══
    if data.startswith("ttt_brd "):
        bi = data.split(" ")[1]
        bs = {
            "clean": {"name": "Clean", "empty": "▫️", "cost": 100},
            "bold": {"name": "Bold", "empty": "🔲", "cost": 100},
            "diamond": {"name": "Diamond", "empty": "💠", "cost": 200},
            "neon": {"name": "Neon", "empty": "🟢", "cost": 200},
            "default": {"name": "Classic", "empty": "·", "cost": 0},
        }
        ch = bs.get(bi)
        if not ch:
            return
        c = user_coins.get(user_id, 0)
        if c < ch["cost"]:
            return await callback_query.answer(f"❌ Need {ch['cost']} coins!", show_alert=True)
        if ch["cost"] > 0:
            user_coins[user_id] = c - ch["cost"]
        user_boards[user_id] = ch
        await callback_query.answer(f"🎨 {ch['name']} equipped!", show_alert=True)
        await show_menu(client, callback_query)
        return

    # ═══ LUCKY BOX ═══
    if data == "ttt_lucky":
        c = user_coins.get(user_id, 0)
        if c < 150:
            return await callback_query.answer("❌ Need 150 coins!", show_alert=True)
        user_coins[user_id] = c - 150
        pz = [50, 75, 100, 150, 200, 300, 500]
        won = random.choice(pz)
        user_coins[user_id] += won
        bal = user_coins[user_id]
        net = won - 150
        await callback_query.message.edit_text(
            "╔══════════════════════╗\n       🎰 *LUCKY BOX*\n╚══════════════════════╝\n\n"
            f"🎁 Won: *{won}* coins!\n💰 Net: {('+' if net >= 0 else '')}{net}\n💰 Balance: {bal}" + foot,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff("🎰 Try Again ₡150"), callback_data="ttt_lucky", style=enums.ButtonStyle.SUCCESS)],
                [InlineKeyboardButton(ff("🔙 Shop"), callback_data="ttt_shop", style=enums.ButtonStyle.PRIMARY)],
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    # ═══ BOOSTER ═══
    if data == "ttt_booster":
        c = user_coins.get(user_id, 0)
        if c < 500:
            return await callback_query.answer("❌ Need 500 coins!", show_alert=True)
        now = int(time.time())
        ex = booster_data.get(user_id)
        if ex and now - ex < 604800:
            return await callback_query.answer("⚡ Booster already active!", show_alert=True)
        user_coins[user_id] = c - 500
        booster_data[user_id] = now
        await callback_query.answer("🚀 2x Daily for 7 days!", show_alert=True)
        await show_menu(client, callback_query)
        return

    # ═══ SHIELD ═══
    if data == "ttt_shield":
        c = user_coins.get(user_id, 0)
        if c < 300:
            return await callback_query.answer("❌ Need 300 coins!", show_alert=True)
        ex = user_shields.get(user_id, 0)
        if ex and ex > 0:
            return await callback_query.answer(f"🛡 Already active! {ex} left", show_alert=True)
        user_coins[user_id] = c - 300
        user_shields[user_id] = 3
        await callback_query.answer("🛡 3 loss shields activated!", show_alert=True)
        await show_menu(client, callback_query)
        return

    # ═══ WAGER PICK ═══
    if data == "ttt_wager_pick":
        c = user_coins.get(user_id, 0)
        await callback_query.message.edit_text(
            "╔══════════════════════╗\n       💰 *WAGER MATCH*\n╚══════════════════════╝\n\n"
            f"💰 Coins: *{c}*\nBet vs Hard AI — Winner takes double!" + foot,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff("50 Coins"), callback_data="ttt_wager 50", style=enums.ButtonStyle.SUCCESS), InlineKeyboardButton(ff("100 Coins"), callback_data="ttt_wager 100", style=enums.ButtonStyle.SUCCESS)],
                [InlineKeyboardButton(ff("250 Coins"), callback_data="ttt_wager 250", style=enums.ButtonStyle.PRIMARY), InlineKeyboardButton(ff("500 Coins"), callback_data="ttt_wager 500", style=enums.ButtonStyle.DANGER)],
                [InlineKeyboardButton(ff("🔙 Back"), callback_data="ttt_restart", style=enums.ButtonStyle.PRIMARY)],
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    # ═══ WAGER START ═══
    if data.startswith("ttt_wager "):
        a = int(data.split(" ")[1])
        c = user_coins.get(user_id, 0)
        if c < a:
            return await callback_query.answer(f"❌ Need {a} coins!", show_alert=True)
        user_coins[user_id] = c - a
        ng = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        games[ng] = {
            "id": ng,
            "p1": user_id, "p1_name": callback_query.from_user.first_name,
            "p1_msg": callback_query.message.id,
            "p2": "bot", "p2_name": "Smart AI",
            "p2_msg": None,
            "board": [" "] * 9,
            "turn": user_id,
            "status": "playing",
            "type": "ai_hard",
            "wager": a,
        }
        res = await callback_query.message.edit_text("🎮 *Wager game starting...*", parse_mode=enums.ParseMode.MARKDOWN)
        games[ng]["p1_msg"] = res.id
        await render_board(client, ng)
        return

    # ═══ RESIGN GAME ═══
    if data.startswith("ttt_resign "):
        gid = data.split(" ")[1]
        g = games.get(gid)
        if not g:
            return
        if user_id != g["p1"] and user_id != g.get("p2"):
            return await callback_query.answer("🚫 Not your game!", show_alert=True)

        g["status"] = "finished"
        g["winner"] = "resigned"
        g["resigner"] = user_id
        loser_id = user_id
        winner_id = g["p2"] if user_id == g["p1"] else g["p1"]

        sh = user_shields.get(loser_id, 0)
        if sh and sh > 0:
            user_shields[loser_id] = sh - 1
        else:
            user_lose[loser_id] = user_lose.get(loser_id, 0) + 1

        if winner_id and winner_id != "bot":
            user_wins[winner_id] = user_wins.get(winner_id, 0) + 1

        if g.get("wager", 0) > 0 and winner_id != "bot":
            user_coins[winner_id] = user_coins.get(winner_id, 0) + g["wager"] * 2

        games[gid] = g
        await render_board(client, gid)

        if g.get("tourney_id"):
            await asyncio.sleep(3)
            await advanceTournament(client, g["tourney_id"], gid)

        await callback_query.answer()
        return

    # ═══ REMATCH GAME ═══
    if data.startswith("ttt_rematch "):
        gid = data.split(" ")[1]
        g = games.get(gid)
        if not g:
            return
        g["board"] = [" "] * 9
        g["status"] = "playing"
        g["winner"] = None
        g["turn"] = g["p1"]
        g["wager"] = 0
        games[gid] = g
        await render_board(client, gid)
        await callback_query.answer("🔁 Rematch!")
        return

    # ═══ TOURNAMENT JOIN ═══
    if data.startswith("trn_join "):
        tid = data.split(" ")[1]
        t = tournaments.get("trn_" + tid)
        if not t or t["status"] != "registering":
            return
        if any(p["id"] == user_id for p in t["players"]):
            return await callback_query.answer("Already in!")
        if len(t["players"]) >= t["max"]:
            return await callback_query.answer("Tournament is full!")
        t["players"].append({"id": user_id, "name": callback_query.from_user.first_name})
        tournaments["trn_" + tid] = t
        pl = "\n".join(f"{i+1}. {cN(p['name'])}" for i, p in enumerate(t["players"]))
        await callback_query.message.edit_text(
            "╔══════════════════════╗\n       ⚔️ *TOURNAMENT*\n╚══════════════════════╝\n\n"
            f"👥 {len(t['players'])}/{t['max']}\n\n{pl}\n\n🥇500 🥈200 🥉100" + foot,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(ff(f"🎮 Join ({len(t['players'])}/{t['max']})"), callback_data=f"trn_join {tid}", style=enums.ButtonStyle.PRIMARY)],
                [InlineKeyboardButton(ff("🚀 Begin"), callback_data=f"trn_start {tid}", style=enums.ButtonStyle.SUCCESS)],
            ]),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        await callback_query.answer("Joined!")
        return

    # ═══ TOURNAMENT START ═══
    if data.startswith("trn_start "):
        tid = data.split(" ")[1]
        t = tournaments.get("trn_" + tid)
        if not t or t["status"] != "registering":
            return
        if user_id != t["creator"]:
            return await callback_query.answer("Host only!", show_alert=True)
        if len(t["players"]) < 2:
            return await callback_query.answer("Need 2+ players!", show_alert=True)

        pl = t["players"][:]
        random.shuffle(pl)
        mt = []
        for i in range(0, len(pl), 2):
            if i + 1 < len(pl):
                mg = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                mt.append({"gid": mg, "p1": pl[i], "p2": pl[i + 1], "winner": None})
            else:
                mt.append({"gid": None, "p1": pl[i], "p2": None, "winner": pl[i]})

        t["status"] = "active"
        t["rounds"] = [mt]
        t["current_round"] = 0
        t["semifinal_losers"] = []
        tournaments["trn_" + tid] = t

        for p in t["players"]:
            try:
                await client.send_message(
                    p["id"],
                    "⚔️ *TOURNAMENT STARTED!*\n" + f"🏆 {len(t['players'])} players!\n" + "🥇500 🥈200 🥉100\n\nHead to the group!" + foot,
                    parse_mode=enums.ParseMode.MARKDOWN
                )
            except Exception:
                pass

        fm = next((m for m in mt if m.get("p2") and m.get("gid")), None)
        if fm:
            games[fm["gid"]] = {
                "id": fm["gid"],
                "p1": fm["p1"]["id"], "p1_name": fm["p1"]["name"],
                "p2": fm["p2"]["id"], "p2_name": fm["p2"]["name"],
                "p1_msg": None, "p2_msg": None,
                "board": [" "] * 9,
                "turn": fm["p1"]["id"],
                "status": "playing",
                "is_group": True,
                "group_cid": t["group_cid"],
                "group_mid": t["group_mid"],
                "type": "multi",
                "wager": 0,
                "tourney_id": tid,
            }
            lk = gLink(t["group_cid"], t["group_mid"])
            try:
                await client.send_message(fm["p1"]["id"], f"🎮 *YOUR MATCH!*\nVs {cN(fm['p2']['name'])}\n🔗 [Play]({lk})", parse_mode=enums.ParseMode.MARKDOWN)
                await client.send_message(fm["p2"]["id"], f"🎮 *YOUR MATCH!*\nVs {cN(fm['p1']['name'])}\n🔗 [Play]({lk})", parse_mode=enums.ParseMode.MARKDOWN)
            except Exception:
                pass
        return

    # ═══ TOURNAMENT REMATCH ═══
    if data.startswith("trn_rematch "):
        parts = data.split(" ")
        gid = parts[2] if len(parts) > 2 else None
        if not gid:
            return
        g = games.get(gid)
        if not g:
            await callback_query.answer()
            return
        g["board"] = [" "] * 9
        g["status"] = "playing"
        g["winner"] = None
        g["turn"] = g["p1"]
        games[gid] = g
        await render_board(client, gid)
        await callback_query.answer("Rematch!")
        return

    # ═══ TOURNAMENT SPLIT ═══
    if data.startswith("trn_split "):
        parts = data.split(" ")
        if len(parts) < 3:
            return
        tid = parts[1]
        gid = parts[2]
        t = tournaments.get("trn_" + tid)
        g = games.get(gid)
        if not t or not g:
            return
        cr = t["rounds"][t["current_round"]]
        me = next((m for m in cr if m["gid"] == gid), None)
        if me:
            me["winner"] = {"id": "split", "name": "Split"}
            if "semifinal_losers" not in t:
                t["semifinal_losers"] = []
            t["semifinal_losers"].append(me["p1"])
            t["semifinal_losers"].append(me["p2"])
        tournaments["trn_" + tid] = t
        user_coins[g["p1"]] = user_coins.get(g["p1"], 0) + 50
        if g["p2"] != "bot":
            user_coins[g["p2"]] = user_coins.get(g["p2"], 0) + 50
        await callback_query.answer("Split! +50 each.")
        await advanceTournament(client, tid, gid)
        return

    # ═══ TOURNAMENT NEXT ═══
    if data.startswith("trn_next "):
        parts = data.split(" ")
        if len(parts) < 3:
            return
        tid = parts[1]
        fgid = parts[2]
        await advanceTournament(client, tid, fgid)
        await callback_query.answer("⚔️ Advancing...")
        return

    # ═══ MOVES & AI ═══
    if data.startswith("ttt_move "):
        parts = data.split(" ")
        gid = parts[1]
        idx = int(parts[2])
        g = games.get(gid)
        if not g or g["status"] != "playing":
            return

        if user_id != g["p1"] and user_id != g.get("p2"):
            return await callback_query.answer("🚫 Spectator!", show_alert=True)
        if user_id != g["turn"]:
            return await callback_query.answer("⏳ Not your turn!", show_alert=True)
        if g["board"][idx] != " ":
            return await callback_query.answer("🚫 Cell taken!")

        g["board"][idx] = "X" if user_id == g["p1"] else "O"
        g["last_move"] = int(time.time())

        fr = chk(g["board"])
        if fr:
            g["status"] = "finished"
            g["winner"] = fr
            if fr != "draw":
                wI = g["p1"] if fr == "X" else g["p2"]
                lI = g["p2"] if fr == "X" else g["p1"]
                if wI != "bot":
                    user_wins[wI] = user_wins.get(wI, 0) + 1
                if lI and lI != "bot":
                    sh = user_shields.get(lI, 0)
                    if sh and sh > 0:
                        user_shields[lI] = sh - 1
                    else:
                        user_lose[lI] = user_lose.get(lI, 0) + 1
                if g.get("wager", 0) > 0 and wI != "bot":
                    user_coins[wI] = user_coins.get(wI, 0) + g["wager"] * 2
            else:
                if g.get("wager", 0) > 0 and not g.get("tourney_id"):
                    user_coins[g["p1"]] = user_coins.get(g["p1"], 0) + g["wager"]
                    if g["p2"] != "bot":
                        user_coins[g["p2"]] = user_coins.get(g["p2"], 0) + g["wager"]

            games[gid] = g
            await render_board(client, gid)
            if g.get("tourney_id"):
                await asyncio.sleep(3)
                await advanceTournament(client, g["tourney_id"], gid)
            await callback_query.answer()
            return

        g["turn"] = g["p2"] if g["turn"] == g["p1"] else g["p1"]

        if g.get("turn") == "bot":
            m = aiMv(g)
            g["board"][m] = "O"
            ar = chk(g["board"])
            if ar:
                g["status"] = "finished"
                g["winner"] = ar
                if ar != "draw":
                    sh = user_shields.get(g["p1"], 0)
                    if sh and sh > 0:
                        user_shields[g["p1"]] = sh - 1
                    else:
                        user_lose[g["p1"]] = user_lose.get(g["p1"], 0) + 1
                elif g.get("wager", 0) > 0:
                    user_coins[g["p1"]] = user_coins.get(g["p1"], 0) + g["wager"]
            g["turn"] = g["p1"]

        games[gid] = g
        await render_board(client, gid)
        await callback_query.answer()
        return

    await callback_query.answer()


# ================= RUN =================

print(f"🎮 мα∂αяα Bot starting...")
app.run()
