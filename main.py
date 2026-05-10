import random
import string
import time
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= BOT CONFIG =================

API_ID = 36522229
API_HASH = "7f27443617af60bcb0e23f7147d3eaf9"
BOT_TOKEN = "8652475253:AAEP9fzyBYeyvjxdrkuZSOvPSJjWfPXDLVU"

# ================= START BOT =================

app = Client(
"ttt_bot",
api_id=API_ID,
api_hash=API_HASH,
bot_token=BOT_TOKEN
)

 # ================= TEMP GAME STORAGE =================
games = {}
daily_data = {}
booster_data = {}
user_coins = {}
tournaments = {}
user_wins = {}
user_lose = {}

# ================= JOIN GAME FUNCTION =================

async def join_game(client, message, gid):
    await message.reply_text(f"Joining Game: {gid}")


# ================= /START COMMAND =================
@app.on_message(filters.command("start"))
async def start(client, message):

    params = message.command[1] if len(message.command) > 1 else None

    # ================= JOIN GAME =================
    if params and params.startswith("ttt_"):

        gid = params.split("_")[1]

        await message.reply_text(
            f"Joining Game ID: {gid}"
        )

        await join_game(client, message, gid)
        return

    # ================= QUICK MATCH =================
    if params == "quickmatch":

        joined = True

        # Force Join Check
        try:
            member = await client.get_chat_member(
                "@EDITING_PFP",
                message.from_user.id
            )

            if member.status in ["left", "kicked"]:
                joined = False

        except:
            joined = False

        if not joined:
            await message.reply_text(
                "🛡 Join @EDITING_PFP first!",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "📢 Join",
                            url="https://t.me/EDITING_PFP"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "✅ Done",
                            callback_data="ttt_restart"
                        )
                    ]
                ]),
                parse_mode="markdown"
            )
            return

        co2 = 0
        wi2 = 0

        await message.reply_text(
            f"╔══════════════════════╗\n"
            f"       🎯 *QUICK MATCH*\n"
            f"╚══════════════════════╝\n\n"
            f"💰 {co2} | 🏆 {wi2} wins\n\n"
            f"Tap below to find an opponent!\n\n"
            f"╔══════════════════════╗\n"
            f"     👨‍💻 @SexiMadara\n"
            f"╚══════════════════════╝",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🎯 Find Match",
                        callback_data="ttt_quickmatch"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 Full Menu",
                        callback_data="ttt_restart"
                    )
                ]
            ]),
            parse_mode="markdown"
        )
        return

    # ================= NORMAL START =================
    joined = True

    # Force Join Check
    try:
        member = await client.get_chat_member(
            "@EDITING_PFP",
            message.from_user.id
        )

        if member.status in ["left", "kicked"]:
            joined = False

    except:
        joined = False

    if not joined:
        await message.reply_text(
            "🛡 *ACCESS RESTRICTED*\n"
            "━━━━━━━━━━━━━━━\n"
            "Join @EDITING_PFP to play!\n"
            "━━━━━━━━━━━━━━━\n"
            "👨‍💻 *By:* SexiMadara",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📢 Join",
                        url="https://t.me/EDITING_PFP"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "✅ Done",
                        callback_data="ttt_restart"
                    )
                ]
            ]),
            parse_mode="markdown"
        )
        return

    co = 0
    wi = 0

    await message.reply_text(
        f"╔══════════════════════╗\n"
        f"       🎮 *TIC-TAC-TOE PRO*\n"
        f"          ᴠ11  ᴘʀᴇᴍɪᴜᴍ\n"
        f"╚══════════════════════╝\n\n"
        f"┌──── 👋  ᴡᴇʟᴄᴏᴍᴇ ────┐\n"
        f"│  {message.from_user.first_name}\n"
        f"└──────────────────────┘\n\n"
        f"┌──── 💎  ᴀᴄᴄᴏᴜɴᴛ ────┐\n"
        f"│  💰 {co} ᴄᴏɪɴs\n"
        f"│  🏆 {wi} ᴡɪɴs\n"
        f"└──────────────────────┘\n\n"
        f"⚡ Multiplayer ∙ AI ∙ Wager\n"
        f"🛒 Shop ∙ 🏆 Tournaments\n\n"
        f"╔══════════════════════╗\n"
        f"     👨‍💻 @SexiMadara\n"
        f"╚══════════════════════╝",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎯 Quick Match",
                    callback_data="ttt_quickmatch"
                )
            ],
            [
                InlineKeyboardButton(
                    "👥 Multiplayer",
                    callback_data="ttt_multi"
                ),
                InlineKeyboardButton(
                    "🤖 vs AI",
                    callback_data="ttt_ai_pick"
                )
            ],
            [
                InlineKeyboardButton(
                    "💰 Wager Match",
                    callback_data="ttt_wager_pick"
                ),
                InlineKeyboardButton(
                    "🛒 Shop",
                    callback_data="ttt_shop"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏆 Leaderboard",
                    callback_data="ttt_leaderboard"
                ),
                InlineKeyboardButton(
                    "📊 My Stats",
                    callback_data="ttt_stats"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎁 Daily Reward",
                    callback_data="ttt_daily"
                )
            ]
        ]),
        parse_mode="markdown"
    )

# ================= /CHALLENGE COMMAND =================
@app.on_message(filters.command("challenge"))
async def challenge(client, message):

    # Group Check
    if message.chat.type == "private":
        await message.reply_text(
            "❌ Use in a *Group*!",
            parse_mode="markdown"
        )
        return

    # Force Join Check
    joined = True

    try:
        member = await client.get_chat_member(
            "@EDITING_PFP",
            message.from_user.id
        )

        if member.status in ["left", "kicked"]:
            joined = False

    except:
        joined = False

    if not joined:
        await message.reply_text(
            "🛡 Join @EDITING_PFP first!",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📢 Join",
                        url="https://t.me/EDITING_PFP"
                    )
                ]
            ]),
            parse_mode="markdown"
        )
        return

    # Command Params
    if len(message.command) < 2:
        await message.reply_text(
            "Usage:\n`/challenge @user`\n`/challenge @user 100`",
            parse_mode="markdown"
        )
        return

    target = message.command[1]

    if not target.startswith("@"):
        await message.reply_text(
            "❌ `/challenge @username`",
            parse_mode="markdown"
        )
        return

    target_user = target.replace("@", "")

    if (
        message.from_user.username and
        message.from_user.username.lower() == target_user.lower()
    ):
        await message.reply_text(
            "🚫 Can't challenge yourself!"
        )
        return

    # Bet System
    bet = 0

    if len(message.command) > 2:
        try:
            bet = int(message.command[2])

            if bet < 0:
                bet = 0

        except:
            bet = 0

    # Demo Coins
    coins = 1000

    if bet > 0:
        if coins < bet:
            await message.reply_text(
                f"❌ Need *{bet}*, have *{coins}*",
                parse_mode="markdown"
            )
            return

    # Generate Game ID
    gid = ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=8
        )
    )

    # Save Game Data
    games[gid] = {
        "id": gid,
        "p1": message.from_user.id,
        "p1_name": message.from_user.first_name,
        "target_username": target_user,
        "p2": None,
        "p2_name": "???",
        "board": [" ", " ", " ", " ", " ", " ", " ", " ", " "],
        "turn": message.from_user.id,
        "status": "waiting_acceptance",
        "is_group": True,
        "group_cid": message.chat.id,
        "wager": bet
    }

    bet_line = (
        f"\n💰 *Bet:* {bet} coins each!"
        if bet > 0 else ""
    )

    # Send Challenge Message
    sent = await message.reply_text(
        f"╔══════════════════════╗\n"
        f"       ⚔️ *CHALLENGE!*\n"
        f"╚══════════════════════╝\n\n"
        f"👤 *From:* {message.from_user.first_name}\n"
        f"🎯 *To:* {target}{bet_line}\n\n"
        f"{target}, accept the battle!\n\n"
        f"╔══════════════════════╗\n"
        f"     👨‍💻 SexiMadara\n"
        f"╚══════════════════════╝",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🤝 Accept Challenge",
                    callback_data=f"ttt_acc {gid}"
                )
            ]
        ]),
        parse_mode="markdown"
    )

    # Save Message ID
    games[gid]["group_mid"] = sent.id

# ================= /DAILY COMMAND =================

@app.on_message(filters.command("daily"))
async def daily(client, message):

    user_id = message.from_user.id
    now = int(time.time())

    lc = daily_data.get(user_id)

    # Cooldown Check
    if lc and (now - lc) < 86400:

        r = 86400 - (now - lc)

        h = r // 3600
        m = (r % 3600) // 60

        await message.reply_text(
            f"⏰ Come back in *{h}h {m}m*",
            parse_mode="markdown"
        )
        return

    # Booster Check
    boost = booster_data.get(user_id)

    reward = 100

    if boost and (now - boost) < 604800:
        reward = 200

    # Add Coins
    current_balance = user_coins.get(user_id, 0)
    user_coins[user_id] = current_balance + reward

    # Save Daily Time
    daily_data[user_id] = now

    # Message
    msg = f"🎁 *+{reward} NepCoins!*"

    if reward > 100:
        msg += "\n🚀 *Booster 2x active!*"

    msg += f"\n💰 Balance: {user_coins[user_id]}"

    await message.reply_text(
        msg,
        parse_mode="markdown"
    )

# ================= CALLBACK QUERY HANDLER =================

@app.on_callback_query()
async def handle_callback_query(client, callback_query):

    data = callback_query.data

    if not data:
        return

    # ═══ 1. MEMBERSHIP CHECK ═══

    joined = True

    try:
        member = await client.get_chat_member(
            "@EDITING_PFP",
            callback_query.from_user.id
        )

        if member.status in ["left", "kicked"]:
            joined = False

    except:
        joined = False

    if (
        not joined
        and data != "ttt_restart"
        and not data.startswith("ttt_acc")
        and not data.startswith("trn_")
    ):

        return await callback_query.answer(
            "❗ Join @EDITING_PFP!",
            show_alert=True
        )

# ═══ 2. HELPERS ═══

foot = "\n\n╔══════════════════════╗\n     👨‍💻 @EDITING_PFP\n╚══════════════════════╝"


def cN(s):
    if not s:
        return "User"

    for ch in ["_", "*", "`", "[", "]", "(", ")"]:
        s = s.replace(ch, " ")

    return s.strip()


def chk(board):

    wins = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
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

    empty = []

    for i, v in enumerate(g["board"]):
        if v == " ":
            empty.append(i)

    def fb(board, mark):

        lines = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
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

    if (g["type"] == "ai_hard" or g["wager"] > 0) and move == -1:

        if g["board"][4] == " ":
            move = 4

        else:

            corners = [
                i for i in [0, 2, 6, 8]
                if g["board"][i] == " "
            ]

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


# ================= GROUP LINK =================

def gLink(cid, mid):

    return (
        "https://t.me/c/"
        + str(cid).replace("-100", "").replace("-", "")
        + "/"
        + str(mid)
    )


# ================= ADVANCE TOURNAMENT =================

async def advanceTournament(client, tid, fgid):

    t = tournaments.get(tid)

    if not t or t["status"] != "active":
        return

    fg = games.get(fgid)

    if not fg:
        return

    # Determine Winner
    wid = None

    if fg.get("winner") == "resigned":

        if fg.get("resigner") == fg["p1"]:
            wid = fg["p2"]
        else:
            wid = fg["p1"]

    elif fg.get("winner") == "X":
        wid = fg["p1"]

    elif fg.get("winner") == "O":
        wid = fg["p2"]

async def advanceTournament(client, tid, fgid):

    t = tournaments.get(tid)

    if not t or t["status"] != "active":
        return

    fg = games.get(fgid)

    if not fg:
        return

    # Determine Winner
    wid = None

    if fg.get("winner") == "resigned":

        if fg.get("resigner") == fg["p1"]:
            wid = fg["p2"]
        else:
            wid = fg["p1"]

    elif fg.get("winner") == "X":
        wid = fg["p1"]

    elif fg.get("winner") == "O":
        wid = fg["p2"]

    # ================= WIN/LOSE TRACK =================
    if wid:

        user_win_res = Libs.ResourcesLib.anotherUserRes(
            "ttt_win",
            wid
        )

        user_win_res.add(1)

        loser = None

        if wid == fg["p1"]:
            loser = fg["p2"]

        elif wid == fg["p2"]:
            loser = fg["p1"]

        if loser:
            user_lose_res = Libs.ResourcesLib.anotherUserRes(
                "ttt_lose",
                loser
            )

            user_lose_res.add(1)

        # Update Match
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

        # Find Next Match
        nm = None

        for m in cr:

            if (
                m.get("p2")
                and m.get("gid")
                and not m.get("winner")
            ):
                nm = m
                break

        if nm:

            games[nm["gid"]] = {
                "id": nm["gid"],
                "p1": nm["p1"]["id"],
                "p1_name": nm["p1"]["name"],
                "p2": nm["p2"]["id"],
                "p2_name": nm["p2"]["name"],
                "board": [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                "turn": nm["p1"]["id"],
                "status": "playing",
                "is_group": True,
                "group_cid": t["group_cid"],
                "group_mid": t["group_mid"],
                "type": "multi",
                "wager": 0,
                "tourney_id": tid,
            }

            lk = gLink(
                t["group_cid"],
                t["group_mid"]
            )

            await client.send_message(
                nm["p1"]["id"],
                f"🎮 *YOUR MATCH!*\n"
                f"Vs {cN(nm['p2']['name'])}\n"
                f"🔗 [Play]({lk})",
                parse_mode="markdown"
            )

            await client.send_message(
                nm["p2"]["id"],
                f"🎮 *YOUR MATCH!*\n"
                f"Vs {cN(nm['p1']['name'])}\n"
                f"🔗 [Play]({lk})",
                parse_mode="markdown"
            )

            return
    # Tournament Finished
    rw = []

    for m in cr:

        w = m.get("winner")

        if w and w.get("id") != "split":
            rw.append(w)

    if len(rw) <= 1:

        ch = rw[0] if rw else None

        sl = t.get("semifinal_losers", [])

        ru = sl[-1] if len(sl) > 0 else None
        tp = sl[-2] if len(sl) > 1 else None

        if ch:
            user_coins[ch["id"]] = user_coins.get(ch["id"], 0) + 500

        if ru and ru["id"] != "split":
            user_coins[ru["id"]] = user_coins.get(ru["id"], 0) + 200

        if tp and tp["id"] != "split":
            user_coins[tp["id"]] = user_coins.get(tp["id"], 0) + 100

        rt = (
            "╔══════════════════════╗\n"
            "       🏆 *TOURNAMENT OVER*\n"
            "╚══════════════════════╝\n\n"
        )

        if ch:

            rt += f"🥇 {cN(ch['name'])} — +500\n"

            await client.send_message(
                ch["id"],
                "🏆 *YOU WON!* 🥇 +500 coins!" + foot,
                parse_mode="markdown"
            )

        if ru and ru["id"] != "split":

            rt += f"🥈 {cN(ru['name'])} — +200\n"

            await client.send_message(
                ru["id"],
                "🥈 *2nd Place!* +200 coins!" + foot,
                parse_mode="markdown"
            )

        if tp and tp["id"] != "split":

            rt += f"🥉 {cN(tp['name'])} — +100\n"

            await client.send_message(
                tp["id"],
                "🥉 *3rd Place!* +100 coins!" + foot,
                parse_mode="markdown"
            )

        rt += "\n🎉 GG!" + foot

        t["status"] = "finished"

        await client.edit_message_text(
            chat_id=t["group_cid"],
            message_id=t["group_mid"],
            text=rt,
            reply_markup=InlineKeyboardMarkup([]),
            parse_mode="markdown"
          )

        return


# ================= CREATE NEXT ROUND =================

    nrm = []

    for i in range(0, len(rw), 2):

        if i + 1 < len(rw):

            mg = ''.join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=8
                )
            )

            nrm.append({
                "gid": mg,
                "p1": rw[i],
                "p2": rw[i + 1],
                "winner": None
            })

        else:

            nrm.append({
                "gid": None,
                "p1": rw[i],
                "p2": None,
                "winner": rw[i]
            })

    t["rounds"].append(nrm)

    t["current_round"] = len(t["rounds"]) - 1

    fnm = None

    for m in nrm:

        if m.get("p2") and m.get("gid"):

            fnm = m
            break

    if fnm:

        games[fnm["gid"]] = {

            "id": fnm["gid"],

            "p1": fnm["p1"]["id"],
            "p1_name": fnm["p1"]["name"],

            "p2": fnm["p2"]["id"],
            "p2_name": fnm["p2"]["name"],

            "board": [
                " ", " ", " ",
                " ", " ", " ",
                " ", " ", " "
            ],

            "turn": fnm["p1"]["id"],

            "status": "playing",

            "is_group": True,

            "group_cid": t["group_cid"],
            "group_mid": t["group_mid"],

            "type": "multi",

            "wager": 0,

            "tourney_id": tid
        }

        lk = gLink(
            t["group_cid"],
            t["group_mid"]
        )

        await client.send_message(

            fnm["p1"]["id"],

            f"🎮 *NEXT ROUND!*\n"
            f"Vs {cN(fnm['p2']['name'])}\n"
            f"🔗 [Play]({lk})",

            parse_mode="markdown"
        )

        await client.send_message(

            fnm["p2"]["id"],

            f"🎮 *NEXT ROUND!*\n"
            f"Vs {cN(fnm['p1']['name'])}\n"
            f"🔗 [Play]({lk})",

            parse_mode="markdown"
        )

async def menu(callback_query):

    c = user_coins.get(callback_query.from_user.id, 0)
    w = 0

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
            [
                InlineKeyboardButton(
                    "🎯 Quick Match",
                    callback_data="ttt_quickmatch"
                )
            ],
            [
                InlineKeyboardButton(
                    "👥 Multiplayer",
                    callback_data="ttt_multi"
                ),
                InlineKeyboardButton(
                    "🤖 vs AI",
                    callback_data="ttt_ai_pick"
                ),
            ],
            [
                InlineKeyboardButton(
                    "💰 Wager Match",
                    callback_data="ttt_wager_pick"
                ),
                InlineKeyboardButton(
                    "🛒 Shop",
                    callback_data="ttt_shop"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🏆 Leaderboard",
                    callback_data="ttt_leaderboard"
                ),
                InlineKeyboardButton(
                    "📊 My Stats",
                    callback_data="ttt_stats"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🎁 Daily Reward",
                    callback_data="ttt_daily"
                )
            ],
        ]),
        parse_mode="markdown"
    )
    # ================= NAVIGATION =================

    if data == "ttt_restart":

        if not joined:

            return await callback_query.answer(
                "❌ Join @EDITING_PFP!",
                show_alert=True
            )

        await menu(callback_query)
        return


    elif data == "ttt_ai_pick":

        await callback_query.message.edit_text(
            "╔══════════════════════╗\n"
            "       🧠 *AI DIFFICULTY*\n"
            "╚══════════════════════╝\n\n"
            "𝗣𝗶𝗰𝗸 𝘆𝗼𝘂𝗿 𝗰𝗵𝗮𝗹𝗹𝗲𝗻𝗴𝗲:"
            + foot,

            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🟢 Easy",
                        callback_data="ttt_go ai_easy"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🟡 Medium",
                        callback_data="ttt_go ai_med"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔴 Hard",
                        callback_data="ttt_go ai_hard"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 Back",
                        callback_data="ttt_restart"
                    )
                ]
            ]),

            parse_mode="markdown"
        )

        return
# ═══ RANK HELPER ═══

def getRank(wins):

    if wins >= 51:
        return {
            "icon": "👑",
            "name": "Champion",
            "tier": 5
        }

    if wins >= 31:
        return {
            "icon": "💎",
            "name": "Diamond",
            "tier": 4
        }

    if wins >= 16:
        return {
            "icon": "🥇",
            "name": "Gold",
            "tier": 3
        }

    if wins >= 6:
        return {
            "icon": "🥈",
            "name": "Silver",
            "tier": 2
        }

    return {
        "icon": "🥉",
        "name": "Bronze",
        "tier": 1
    }


def buildProfile(playerId, playerName):

    w = user_wins.get(playerId, 0)
    l = user_losses.get(playerId, 0)

    total = w + l

    if total == 0:
        rate = 0
    else:
        rate = int((w / total) * 100)

    bar = ""

    for i in range(10):

        if i < rate // 10:
            bar += "▓"
        else:
            bar += "░"

    rank = getRank(w)

    sk = user_skins.get(playerId)
    ti = user_titles.get(playerId)

    return (
        "┌──── 👤 "
        + cN(playerName)
        + " ────┐\n"

        + "│  "
        + rank["icon"]
        + " *Rank:* "
        + rank["name"]
        + "\n"

        + "│  ✅ *"
        + str(w)
        + "W* ❌ *"
        + str(l)
        + "L* 🎮 *"
        + str(total)
        + "* total\n"

        + "│  🎯 "
        + bar
        + " *"
        + str(rate)
        + "%* win rate\n"

        + "│  🎭 "
        + (sk["name"] if sk else "Default")
        + (
            " │ 🏷 " + ti
            if ti else ""
        )
        + "\n"

        + "└────────────────────────────┘"
    )
@app.on_callback_query()
async def callback_handler(client, callback_query):

    data = callback_query.data

    # ═══ 3.5 QUICK MATCH (Matchmaking) ═══

    if data == "ttt_quickmatch":

        now = int(time.time())

        queue = tournaments.get("mm_queue", [])

        # Remove old entries (5 min)
        queue = [
            q for q in queue
            if now - q["timestamp"] < 300
        ]

        # Remove self from queue
        queue = [
            q for q in queue
            if q["id"] != callback_query.from_user.id
        ]

        # MATCH FOUND
        if len(queue) > 0:

            opponent = queue.pop(0)

            tournaments["mm_queue"] = queue

            # Create Match ID
            gid = ''.join(
                random.choices(
                    string.ascii_letters + string.digits,
                    k=8
                )
            )

            # Create Pending Match
            games[gid] = {
                "id": gid,

                "p1": opponent["id"],
                "p1_name": opponent["name"],

                "p2": callback_query.from_user.id,
                "p2_name": callback_query.from_user.first_name,

                "p1_msg": None,
                "p2_msg": None,

                "p1_ready": False,
                "p2_ready": False,

                "board": [
                    " ", " ", " ",
                    " ", " ", " ",
                    " ", " ", " "
                ],

                "turn": opponent["id"],

                "status": "confirming",

                "type": "multi",

                "wager": 0,

                "is_quickmatch": True
            }

            # Build profiles
            p1Profile = buildProfile(
                opponent["id"],
                opponent["name"]
            )

            p2Profile = buildProfile(
                callback_query.from_user.id,
                callback_query.from_user.first_name
            )

            # Show current user's profile to opponent
            if opponent.get("msg_id"):

                await client.edit_message_text(

                    chat_id=opponent["id"],

                    message_id=opponent["msg_id"],

                    text=(
                        "╔══════════════════════╗\n"
                        "       🎯 *MATCH FOUND!*\n"
                        "╚══════════════════════╝\n\n"
                        "Your opponent:\n\n"
                        f"{p2Profile}\n\n"
                        "Press ✅ Ready to start!"
                        f"{foot}"
                    ),

                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                "✅ Ready!",
                                callback_data=f"ttt_qready {gid}"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "❌ Decline",
                                callback_data=f"ttt_qdecline {gid}"
                            )
                        ]
                    ]),

                    parse_mode="markdown"
                )

                games[gid]["p1_confirm_msg"] = opponent["msg_id"]

            # Show opponent profile to current user
            await callback_query.message.edit_text(

                text=(
                    "╔══════════════════════╗\n"
                    "       🎯 *MATCH FOUND!*\n"
                    "╚══════════════════════╝\n\n"
                    "Your opponent:\n\n"
                    f"{p1Profile}\n\n"
                    "Press ✅ Ready to start!"
                    f"{foot}"
                ),

                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "✅ Ready!",
                            callback_data=f"ttt_qready {gid}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "❌ Decline",
                            callback_data=f"ttt_qdecline {gid}"
                        )
                    ]
                ]),

                parse_mode="markdown"
            )

            games[gid]["p2_confirm_msg"] = (
                callback_query.message.id
            )

            await callback_query.answer(
                "🎯 Match Found! Review opponent."
            )

        # NO PLAYER FOUND
        else:

            queue.append({

                "id": callback_query.from_user.id,

                "name": callback_query.from_user.first_name,

                "chat_id": callback_query.message.chat.id,

                "msg_id": callback_query.message.id,

                "timestamp": now
            })

            tournaments["mm_queue"] = queue

            myProfile = buildProfile(
                callback_query.from_user.id,
                callback_query.from_user.first_name
            )

            await callback_query.message.edit_text(

                text=(
                    "╔══════════════════════╗\n"
                    "       🎯 *QUICK MATCH*\n"
                    "╚══════════════════════╝\n\n"
                    "🔍 *Searching for opponent...*\n\n"
                    "┌──── ⏳ sᴛᴀᴛᴜs ────┐\n"
                    "│ Waiting for a player...\n"
                    "│ ⏱ Timeout: 5 minutes\n"
                    "└────────────────────┘\n\n"
                    "Your profile (shown to opponents):\n\n"
                    f"{myProfile}\n\n"
                    "💡 _Invite friends to play!_"
                    f"{foot}"
                ),

                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "🔄 Refresh",
                            callback_data="ttt_qrefresh"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "❌ Cancel Search",
                            callback_data="ttt_qcancel"
                        )
                    ]
                ]),

                parse_mode="markdown"
            )

            await callback_query.answer(
                "🔍 Searching..."
            )

        return
# ═══ READY / DECLINE ═══

    if data.startswith("ttt_qready "):

        gid = data.split(" ")[1"]

        g = games.get(gid)

        if not g or g["status"] != "confirming":
            return

        # Mark player ready
        if callback_query.from_user.id == g["p1"]:

            g["p1_ready"] = True

        elif callback_query.from_user.id == g["p2"]:

            g["p2_ready"] = True

        else:

            await callback_query.answer(
                "🚫 Not your match!",
                show_alert=True
            )
            return

        # Both players ready
        if g["p1_ready"] and g["p2_ready"]:

            g["status"] = "playing"

            # Send game board message to P1
            res1 = await client.send_message(
                chat_id=g["p1"],
                text="🎮 *Game starting...*",
                parse_mode="markdown"
            )

            if res1:
                g["p1_msg"] = res1.id

            # Send game board message to P2
            res2 = await client.send_message(
                chat_id=g["p2"],
                text="🎮 *Game starting...*",
                parse_mode="markdown"
            )

            if res2:
                g["p2_msg"] = res2.id

            games[gid] = g

            # Render board
            await render_board(client, gid)

            # Update confirm messages
            if g.get("p1_confirm_msg"):

                await client.edit_message_text(
                    chat_id=g["p1"],
                    message_id=g["p1_confirm_msg"],
                    text=(
                        "╔══════════════════════╗\n"
                        "       ✅ *GAME ON!*\n"
                        "╚══════════════════════╝\n\n"
                        "🎮 Both players ready!\n"
                        "⬇️ Board is below."
                        + foot
                    ),
                    parse_mode="markdown"
                )

            if g.get("p2_confirm_msg"):

                await client.edit_message_text(
                    chat_id=g["p2"],
                    message_id=g["p2_confirm_msg"],
                    text=(
                        "╔══════════════════════╗\n"
                        "       ✅ *GAME ON!*\n"
                        "╚══════════════════════╝\n\n"
                        "🎮 Both players ready!\n"
                        "⬇️ Board is below."
                        + foot
                    ),
                    parse_mode="markdown"
                )

            await callback_query.answer(
                "🎮 Game started!"
            )

        else:

            # One player ready
            games[gid] = g

            await callback_query.message.edit_text(
                text=(
                    "╔══════════════════════╗\n"
                    "       🎯 *MATCH FOUND!*\n"
                    "╚══════════════════════╝\n\n"
                    "✅ *You are READY!*\n\n"
                    "⏳ Waiting for opponent to confirm..."
                    + foot
                ),
                parse_mode="markdown"
            )

            await callback_query.answer(
                "✅ Ready! Waiting for opponent..."
            )

        return

# ═══ DECLINE MATCH ═══

if data.startswith("ttt_qdecline "):

    gid = data.split(" ")[1]

    g = games.get(gid)

    if not g or g["status"] != "confirming":
        return

    g["status"] = "declined"

    games[gid] = g

    declinerId = callback_query.from_user.id

    otherId = (
        g["p2"]
        if declinerId == g["p1"]
        else g["p1"]
    )

    otherMsg = (
        g.get("p2_confirm_msg")
        if declinerId == g["p1"]
        else g.get("p1_confirm_msg")
    )
# Notify other player

    if otherMsg:

        await client.edit_message_text(

            chat_id=otherId,

            message_id=otherMsg,

            text=(
                "╔══════════════════════╗\n"
                "       ❌ *DECLINED*\n"
                "╚══════════════════════╝\n\n"
                "Opponent declined the match.\n"
                "Search again!"
                + foot
            ),

            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🎯 Search Again",
                        callback_data="ttt_quickmatch"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 Menu",
                        callback_data="ttt_restart"
                    )
                ],
            ]),

            parse_mode="markdown"
        )
# ═══ DECLINE UPDATE ═══

await callback_query.answer("❌ Match declined.")

await menu(callback_query)
return


# ═══ QUICK MATCH REFRESH ═══

if data == "ttt_qrefresh":

    now = int(time.time())

    queue = matchmaking_queue  # or Bot.get("mm_queue") if you are using storage

    queue = [
        q for q in queue
        if now - q["timestamp"] < 300
    ]

    me = None

    for q in queue:
        if q["id"] == callback_query.from_user.id:
            me = q
            break

    if not me:

        matchmaking_queue = queue

        await client.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.id,
            text=(
                "╔══════════════════════╗\n"
                "       🎯 *QUICK MATCH*\n"
                "╚══════════════════════╝\n\n"
                "❌ *Match not found.*\n"
                "No users online.\n\n"
                "Try again later!"
                + foot
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🎯 Try Again", callback_data="ttt_quickmatch")
                ],
                [
                    InlineKeyboardButton("🔙 Menu", callback_data="ttt_restart")
                ],
            ]),
            parse_mode="markdown"
        )

        await callback_query.answer(
            "⏰ Search expired!",
            show_alert=True
        )

        return

    elapsed = now - me["timestamp"]
    remaining = 300 - elapsed

    await callback_query.answer(
        f"🔍 Still searching... ({remaining//60}m {remaining%60}s left)"
    )

    return


# ═══ CANCEL SEARCH ═══

if data == "ttt_qcancel":

    matchmaking_queue = [
        q for q in matchmaking_queue
        if q["id"] != callback_query.from_user.id
    ]

    await callback_query.answer("❌ Search cancelled.")

    await menu(callback_query)

    return
# ═══ INLINE GAME JOIN ═══

if data.startswith("ttt_iln_join "):

    gid = data.split(" ")[1]

    g = games.get(gid)

    if not g:
        return await callback_query.answer(
            "❌ Game expired!",
            show_alert=True
        )

    # Can't join your own game
    if callback_query.from_user.id == g["p1"]:
        return await callback_query.answer(
            "⏳ Waiting for opponent to join!",
            show_alert=True
        )

    # Already started
    if g.get("status") != "inline_waiting":
        return await callback_query.answer(
            "🚫 Game already started!",
            show_alert=True
        )

    # Set player 2
    g["p2"] = callback_query.from_user.id
    g["p2_name"] = callback_query.from_user.first_name
    g["status"] = "playing"
    g["last_move"] = int(time.time())

    # inline message id save (Telegram inline game support)
    if getattr(callback_query, "inline_message_id", None):
        g["inline_mid"] = callback_query.inline_message_id

    games[gid] = g

    # render board call (your function)
    # await render_board(client, gid)

    await callback_query.answer("🎮 Game started! You are ⭕")

    return
# ═══ INLINE PLAY AGAIN ═══

if data.startswith("ttt_iln_new "):

    old_gid = data.split(" ")[1]

    old_g = games.get(old_gid)

    inline_mid = None

    if old_g and old_g.get("inline_mid"):
        inline_mid = old_g["inline_mid"]

    if not inline_mid and getattr(callback_query, "inline_message_id", None):
        inline_mid = callback_query.inline_message_id

    if not inline_mid:
        return await callback_query.answer(
            "❌ Cannot restart here!",
            show_alert=True
        )

    # Create new game
    gid = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    games[gid] = {
        "id": gid,
        "p1": callback_query.from_user.id,
        "p1_name": callback_query.from_user.first_name,
        "p2": None,
        "p2_name": "???",
        "p1_msg": None,
        "p2_msg": None,
        "board": [" "] * 9,
        "turn": callback_query.from_user.id,
        "status": "inline_waiting",
        "is_inline": True,
        "inline_mid": inline_mid,
        "type": "multi",
        "wager": 0,
    }

    # Update inline message (editMessageText via HTTP request)
    import requests

    url = f"https://api.telegram.org/bot{bot_token}/editMessageText"

    text = (
        "╔══════════════════════╗\n"
        "       🎮 *TIC-TAC-TOE*\n"
        "╚══════════════════════╝\n\n"
        f"⚔️ *{callback_query.from_user.first_name}* wants to play again!\n\n"
        "┌──── 🎮 ────┐\n"
        "│  · │ · │ ·\n"
        "│  · │ · │ ·\n"
        "│  · │ · │ ·\n"
        "└──────────────┘\n\n"
        "👇 Tap *Join* to play!\n\n"
        "╔══════════════════════╗\n"
        "     👨‍💻 @nepcodexcc\n"
        "╚══════════════════════╝"
    )

    payload = {
        "inline_message_id": inline_mid,
        "text": text,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🎮 Join & Play!",
                        "callback_data": f"ttt_iln_join {gid}"
                    }
                ]
            ]
        },
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, json=payload)
    except:
        pass

    await callback_query.answer("🎮 New game! Waiting for opponent...")

    return
# ═══ DAILY REWARD ═══

if data == "ttt_daily":

    user_id = callback_query.from_user.id
    now = int(time.time())

    lc = daily_data.get(user_id)

    # cooldown check
    if lc and (now - lc) < 86400:

        r = 86400 - (now - lc)

        await callback_query.answer(
            f"⏰ {r//3600}h {(r%3600)//60}m",
            show_alert=True
        )
        return

    # booster check
    boost = booster_data.get(user_id)

    reward = 100

    if boost and (now - boost) < 604800:
        reward = 200

    # add coins
    user_coins[user_id] = user_coins.get(user_id, 0) + reward

    # save daily
    daily_data[user_id] = now

    await callback_query.answer(
        f"🎁 +{reward} coins!" + (" (2x Boost!)" if reward > 100 else ""),
        show_alert=True
    )

    await menu(callback_query)

    return

# ═══ STATS ═══

if data == "ttt_stats":

    user_id = callback_query.from_user.id

    # ✅ REAL WIN/LOSE TRACKING (IMPORTANT FIX)
    w = Libs.ResourcesLib.anotherUserRes("ttt_win", user_id).value()
    l = Libs.ResourcesLib.anotherUserRes("ttt_lose", user_id).value()

    c = user_coins.get(user_id, 0)

    sk = None
    ti = None
    bd = None
    sh = 0

    rate = 0 if (w + l) == 0 else (w * 100 // (w + l))

    bar = "▓" * (rate // 10) + "░" * (10 - (rate // 10))

    await callback_query.message.edit_text(
        "╔══════════════════════╗\n"
        "       📊 *MY PROFILE*\n"
        "╚══════════════════════╝\n\n"
        "┌──── ⚔️  ʙᴀᴛᴛʟᴇ ʟᴏɢ ────┐\n"
        f"│  ✅ Wins: *{w}*\n"
        f"│  ❌ Losses: *{l}*\n"
        f"│  ?? {bar} *{rate}%*\n"
        "└────────────────────────────┘\n\n"
        "┌──── 🎒  ɪɴᴠᴇɴᴛᴏʀʏ ────┐\n"
        f"│  💰 *{c}* NepCoins\n"
        f"│  🎭 {(sk.name if sk else 'Default')}\n"
        f"│  🏷 {(ti if ti else 'None')}\n"
        f"│  🎨 {(bd.name if bd else 'Classic')}\n"
        f"│  🛡 {sh} shields left\n"
        "└────────────────────────────┘"
        + foot,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="ttt_restart"
                )
            ]
        ]),
        parse_mode="markdown"
    )

    return

if data == "ttt_leaderboard":

    tl = Bot.get("ttt_top_list") or {}

    so = sorted(tl.items(), key=lambda x: x[1], reverse=True)[:10]

    t = (
        "╔══════════════════════╗\n"
        "       🏆 *CHAMPIONS*\n"
        "╚══════════════════════╝\n\n"
    )

    if not so:
        t += "_No heroes yet!_"

    for i, e in enumerate(so):

        prefix = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  •"

        t += f"{prefix} `{e[0]}`: *{e[1]} W*\n"

    await callback_query.message.edit_text(
        t + foot,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="ttt_restart"
                )
            ]
        ]),
        parse_mode="markdown"
    )

    return

# ═══ 6. SHOP ═══

if data == "ttt_shop":

    c = Libs.ResourcesLib.userRes("nepcoins").value()

    await callback_query.message.edit_text(
        "╔══════════════════════╗\n"
        "       🛒 *SHOP*\n"
        "╚══════════════════════╝\n\n"
        "┌──── 💎 ────┐\n"
        f"│  💰 *{c}* coins\n"
        "└──────────────┘\n\n"
        "🎭 *Skins* — Custom X/O marks\n"
        "🏷 *Titles* — Victory badges\n"
        "🎨 *Boards* — Grid themes\n"
        "🎰 *Lucky Box* — Gamble!\n"
        "🚀 *Booster* — 2x daily\n"
        "🛡 *Shield* — Block losses"
        + foot,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎭 Skins", callback_data="ttt_skins"),
                InlineKeyboardButton("🏷 Titles", callback_data="ttt_titles"),
            ],
            [
                InlineKeyboardButton("🎨 Boards", callback_data="ttt_boards"),
                InlineKeyboardButton("🎰 Lucky ₡150", callback_data="ttt_lucky"),
            ],
            [
                InlineKeyboardButton("🚀 Booster ₡500", callback_data="ttt_booster"),
                InlineKeyboardButton("🛡 Shield ₡300", callback_data="ttt_shield"),
            ],
            [
                InlineKeyboardButton("🔙 Menu", callback_data="ttt_restart")
            ],
        ]),
        parse_mode="markdown"
    )

    return

# ═══ SKINS PAGE 1 ═══

if data == "ttt_skins":

    await callback_query.message.edit_text(
        "╔══════════════════════╗\n"
        "       🎭 *SKINS*\n"
        "╚══════════════════════╝\n\n"
        "200 coins each — Page 1"
        + foot,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔥 Fire", callback_data="ttt_buy fire"),
                InlineKeyboardButton("👑 Royal", callback_data="ttt_buy royal"),
                InlineKeyboardButton("🐱 Pets", callback_data="ttt_buy pets"),
            ],
            [
                InlineKeyboardButton("⚡ Energy", callback_data="ttt_buy energy"),
                InlineKeyboardButton("🌟 Stars", callback_data="ttt_buy stars"),
                InlineKeyboardButton("🌈 Rainbow", callback_data="ttt_buy rainbow"),
            ],
            [
                InlineKeyboardButton("Page 2 →", callback_data="ttt_skins2"),
                InlineKeyboardButton("❌ Default (Free)", callback_data="ttt_buy default"),
            ],
            [
                InlineKeyboardButton("🔙 Shop", callback_data="ttt_shop"),
            ],
        ]),
        parse_mode="markdown"
    )

    return

# ═══ SKINS PAGE 2 ═══

if data == "ttt_skins2":

    await callback_query.message.edit_text(
        "╔══════════════════════╗\n"
        "       🎭 *PREMIUM SKINS*\n"
        "╚══════════════════════╝\n\n"
        "300 coins each — Page 2"
        + foot,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎃 Halloween", callback_data="ttt_buy halloween"),
                InlineKeyboardButton("🎄 Xmas", callback_data="ttt_buy xmas"),
            ],
            [
                InlineKeyboardButton("👾 Alien", callback_data="ttt_buy alien"),
                InlineKeyboardButton("🍔 Food", callback_data="ttt_buy food"),
            ],
            [
                InlineKeyboardButton("← Page 1", callback_data="ttt_skins"),
                InlineKeyboardButton("🔙 Shop", callback_data="ttt_shop"),
            ],
        ]),
        parse_mode="markdown"
    )

    return

# ═══ BUY SKINS ═══

if data.startswith("ttt_buy "):

    si = data.split(" ")[1]

    sk = {
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

    ch = sk.get(si)

    if not ch:
        return

    c = Libs.ResourcesLib.userRes("nepcoins").value()

    if c < ch["cost"]:
        return await callback_query.answer(
            f"❌ Need {ch['cost']}",
            show_alert=True
        )

    if ch["cost"] > 0:
        Libs.ResourcesLib.userRes("nepcoins").add(-ch["cost"])

    Bot.set("skin_" + str(user.id), ch)

    await callback_query.answer(
        f"🎭 {ch['name']}! {ch['x']}/{ch['o']}",
        show_alert=True
    )

    menu()

    return

# ═══ TITLES ═══

if data == "ttt_titles":

    await callback_query.message.edit_text(
        "╔══════════════════════╗\n"
        "       🏷 *TITLES*\n"
        "╚══════════════════════╝\n\n"
        "Shown when you win!"
        + foot,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚡ Lightning ₡150", callback_data="ttt_tit lightning"),
                InlineKeyboardButton("🐉 Dragon ₡150", callback_data="ttt_tit dragon"),
            ],
            [
                InlineKeyboardButton("💀 Destroyer ₡250", callback_data="ttt_tit destroyer"),
                InlineKeyboardButton("👑 King ₡250", callback_data="ttt_tit king"),
            ],
            [
                InlineKeyboardButton("🔱 God of War ₡400", callback_data="ttt_tit godofwar"),
                InlineKeyboardButton("❌ Remove", callback_data="ttt_tit none"),
            ],
            [
                InlineKeyboardButton("🔙 Shop", callback_data="ttt_shop"),
            ],
        ]),
        parse_mode="markdown"
    )

    return

# ═══ BUY TITLES ═══

if data.startswith("ttt_tit "):

    ti = data.split(" ")[1]

    ts = {
        "lightning": {"name": "⚡ Lightning", "cost": 150},
        "dragon": {"name": "🐉 Dragon", "cost": 150},
        "destroyer": {"name": "💀 Destroyer", "cost": 250},
        "king": {"name": "👑 King", "cost": 250},
        "godofwar": {"name": "🔱 God of War", "cost": 400},
        "none": {"name": None, "cost": 0},
    }

    ch = ts.get(ti)

    if not ch:
        return

    c = Libs.ResourcesLib.userRes("nepcoins").value()

    if c < ch["cost"]:
        return await callback_query.answer(
            f"❌ Need {ch['cost']}",
            show_alert=True
        )

    if ch["cost"] > 0:
        Libs.ResourcesLib.userRes("nepcoins").add(-ch["cost"])

    Bot.set("title_" + str(user.id), ch["name"])

    msg = "Removed!" if not ch["name"] else f"{ch['name']}!"

    await callback_query.answer(
        "🏷 " + msg,
        show_alert=True
    )

    menu()

    return

# ═══ BOARDS ═══
if data == "ttt_boards":

    await callback_query.message.edit_text(
        "╔══════════════════════╗\n"
        "       🎨 *BOARDS*\n"
        "╚══════════════════════╝\n\n"
        "Changes empty cell style!" + foot,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("▫️ Clean ₡100", callback_data="ttt_brd clean"),
                InlineKeyboardButton("🔲 Bold ₡100", callback_data="ttt_brd bold"),
            ],
            [
                InlineKeyboardButton("💠 Diamond ₡200", callback_data="ttt_brd diamond"),
                InlineKeyboardButton("🟢 Neon ₡200", callback_data="ttt_brd neon"),
            ],
            [
                InlineKeyboardButton("· Classic (Free)", callback_data="ttt_brd default"),
                InlineKeyboardButton("🔙 Shop", callback_data="ttt_shop"),
            ],
        ]),
        parse_mode="Markdown"
    )

    return

# ═══ BOARD BUY SYSTEM ═══
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

    c = Libs.ResourcesLib.userRes("nepcoins").value()

    if c < ch["cost"]:
        return await callback_query.answer(
            f"❌ Need {ch['cost']}",
            show_alert=True
        )

    if ch["cost"] > 0:
        Libs.ResourcesLib.userRes("nepcoins").add(-ch["cost"])

    Bot.set("board_" + str(user.id), ch)

    await callback_query.answer(
        f"🎨 {ch['name']}!",
        show_alert=True
    )

    menu()
    return

# ═══ LUCKY BOX ═══
if data == "ttt_lucky":

    c = Libs.ResourcesLib.userRes("nepcoins").value()

    if c < 150:
        return await callback_query.answer(
            "❌ Need 150",
            show_alert=True
        )

    Libs.ResourcesLib.userRes("nepcoins").add(-150)

    import random

    pz = [50, 75, 100, 150, 200, 300, 500]
    won = random.choice(pz)

    Libs.ResourcesLib.userRes("nepcoins").add(won)

    bal = Libs.ResourcesLib.userRes("nepcoins").value()

    net = won - 150

    await callback_query.message.edit_text(
        "╔══════════════════════╗\n"
        "       🎰 *LUCKY BOX*\n"
        "╚══════════════════════╝\n\n"
        f"🎁 Won: *{won}* coins!\n"
        f"💰 Net: {('+' if net >= 0 else '')}{net}\n"
        f"💰 Balance: {bal}"
        + foot,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎰 Try Again ₡150", callback_data="ttt_lucky")
            ],
            [
                InlineKeyboardButton("🔙 Shop", callback_data="ttt_shop")
            ],
        ]),
        parse_mode="markdown"
    )

    return

# ═══ BOOSTER ═══
if data == "ttt_booster":

    c = Libs.ResourcesLib.userRes("nepcoins").value()

    if c < 500:
        return await callback_query.answer(
            "❌ Need 500",
            show_alert=True
        )

    import time
    now = int(time.time())

    ex = Bot.get("booster_" + str(user.id))

    if ex and now - ex < 604800:
        return await callback_query.answer(
            "⚡ Already active!",
            show_alert=True
        )

    Libs.ResourcesLib.userRes("nepcoins").add(-500)

    Bot.set("booster_" + str(user.id), now)

    await callback_query.answer(
        "🚀 2x Daily for 7 days!",
        show_alert=True
    )

    menu()
    return

# ═══ SHIELD ═══
if data == "ttt_shield":

    c = Libs.ResourcesLib.userRes("nepcoins").value()

    if c < 300:
        return await callback_query.answer(
            "❌ Need 300",
            show_alert=True
        )

    ex = Bot.get("shield_" + str(user.id))

    if ex and ex > 0:
        return await callback_query.answer(
            f"🛡 Active! {ex} left",
            show_alert=True
        )

    Libs.ResourcesLib.userRes("nepcoins").add(-300)

    Bot.set("shield_" + str(user.id), 3)

    await callback_query.answer(
        "🛡 3 loss shields!",
        show_alert=True
    )

    menu()
    return

# ═══ WAGER PICK ═══
if data == "ttt_wager_pick":

    c = Libs.ResourcesLib.userRes("nepcoins").value()

    await callback_query.message.edit_text(
        "╔══════════════════════╗\n"
        "       💰 *WAGER MATCH*\n"
        "╚══════════════════════╝\n\n"
        f"💰 Coins: *{c}*\n"
        "Bet vs Hard AI — Winner takes double!"
        + foot,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("50 Coins", callback_data="ttt_wager 50"),
                InlineKeyboardButton("100 Coins", callback_data="ttt_wager 100"),
            ],
            [
                InlineKeyboardButton("250 Coins", callback_data="ttt_wager 250"),
                InlineKeyboardButton("500 Coins", callback_data="ttt_wager 500"),
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="ttt_restart"),
            ],
        ]),
        parse_mode="markdown"
    )

    return

# ═══ WAGER START ═══
if data.startswith("ttt_wager "):

    a = int(data.split(" ")[1])
    c = Libs.ResourcesLib.userRes("nepcoins").value()

    if c < a:
        return await callback_query.answer(
            f"❌ Need {a}",
            show_alert=True
        )

    Libs.ResourcesLib.userRes("nepcoins").add(-a)

    import random

    ng = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))

    Bot.set(
        "game_" + ng,
        {
            "id": ng,
            "p1": user.id,
            "p1_name": user.first_name,
            "p1_msg": callback_query.message.message_id,
            "p2": "bot",
            "p2_name": "Smart AI",
            "board": [" ", " ", " ", " ", " ", " ", " ", " ", " "],
            "turn": user.id,
            "status": "playing",
            "type": "ai_hard",
            "wager": a,
        },
        "json"
    )

    Bot.runCommand("/render_board", {"gid": ng})

    return

# ═══ GAME INIT ═══
if data == "ttt_multi" or data.startswith("ttt_go "):

    ty = "multi" if data == "ttt_multi" else data.split(" ")[1]

    import random
    ng = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))

    Bot.set(
        "game_" + ng,
        {
            "id": ng,
            "p1": user.id,
            "p1_name": user.first_name,
            "p1_msg": callback_query.message.message_id,
            "p2": None if ty == "multi" else "bot",
            "p2_name": "???" if ty == "multi" else "Smart AI",
            "board": [" ", " ", " ", " ", " ", " ", " ", " ", " "],
            "turn": user.id,
            "status": "waiting" if ty == "multi" else "playing",
            "type": ty,
            "wager": 0,
        },
        "json"
    )

    Bot.runCommand("/render_board", {"gid": ng})

    return

# ═══ ACCEPT GAME ═══
if data.startswith("ttt_acc "):

    gid = data.split(" ")[1]
    g = Bot.get("game_" + gid)

    if not g or g["status"] != "waiting_acceptance":
        return

    # username check (safe fallback)
    uname = (user.username or "").lower()
    target = (g.get("target_username") or "").lower()

    if uname and uname != target:
        return await callback_query.answer(
            f"🚫 Only @{g['target_username']}!",
            show_alert=True
        )

    if g.get("wager", 0) > 0:

        pc = Libs.ResourcesLib.userRes("nepcoins").value()

        if pc < g["wager"]:
            return await callback_query.answer(
                f"❌ Need {g['wager']} coins!",
                show_alert=True
            )

        Libs.ResourcesLib.userRes("nepcoins").add(-g["wager"])

    g["p2"] = user.id
    g["p2_name"] = user.first_name
    g["status"] = "playing"

    Bot.set("game_" + gid, g, "json")

    Bot.runCommand("/render_board", {"gid": gid})

    await callback_query.answer("Accepted!")

    return

# ═══ CANCEL GAME ═══
if data.startswith("ttt_cancel "):

    gid = data.split(" ")[1]
    g = Bot.get("game_" + gid)

    if not g:
        return

    if user.id == g["p1"]:

        if g.get("wager", 0) > 0:
            Libs.ResourcesLib.anotherUserRes("nepcoins", user.id).add(g["wager"])

        menu()

    return

# ═══ RESIGN GAME ═══
if data.startswith("ttt_resign "):

    gid = data.split(" ")[1]
    g = Bot.get("game_" + gid)

    if not g:
        return

    # Only player check
    if user.id != g["p1"] and user.id != g["p2"]:
        return await callback_query.answer(
            "🚫 Not your game!",
            show_alert=True
        )

    g["status"] = "finished"
    g["winner"] = "resigned"
    g["resigner"] = user.id

    loser_id = user.id
    winner_id = g["p2"] if user.id == g["p1"] else g["p1"]

    # Shield logic
    shL = Bot.get("shield_" + str(loser_id))

    if shL and shL > 0:
        Bot.set("shield_" + str(loser_id), shL - 1)
    else:
        Libs.ResourcesLib.anotherUserRes("ttt_lose", loser_id).add(1)

    # Winner update
    if winner_id and winner_id != "bot":

        Libs.ResourcesLib.anotherUserRes("ttt_win", winner_id).add(1)

        tl = Bot.get("ttt_top_list") or {}
        tl[str(winner_id)] = tl.get(str(winner_id), 0) + 1
        Bot.set("ttt_top_list", tl, "json")

    # wager payout
    if g.get("wager", 0) > 0 and winner_id != "bot":
        Libs.ResourcesLib.anotherUserRes("nepcoins", winner_id).add(g["wager"] * 2)

    Bot.set("game_" + gid, g, "json")

    Bot.runCommand("/render_board", {"gid": gid})

    # tournament auto advance (safe async-style replacement)
    if g.get("tourney_id"):
        import asyncio
        await asyncio.sleep(3)
        await advanceTournament(client, g["tourney_id"], gid)

    await callback_query.answer()

    return

# ═══ REMATCH GAME ═══
if data.startswith("ttt_rematch "):

    gid = data.split(" ")[1]
    g = Bot.get("game_" + gid)

    if not g:
        return

    g["board"] = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    g["status"] = "playing"
    g["winner"] = None
    g["turn"] = g["p1"]
    g["wager"] = 0

    Bot.set("game_" + gid, g, "json")

    Bot.runCommand("/render_board", {"gid": gid})

    await callback_query.answer("Rematch!")

    return

# ═══ TOURNAMENT JOIN ═══
if data.startswith("trn_join "):

    tid = data.split(" ")[1]
    t = Bot.get("trn_" + tid)

    if not t or t["status"] != "registering":
        return

    # already joined check
    if any(p["id"] == user.id for p in t["players"]):
        return await callback_query.answer("Already in!")

    if len(t["players"]) >= t["max"]:
        return await callback_query.answer("Full!")

    t["players"].append({
        "id": user.id,
        "name": user.first_name
    })

    Bot.set("trn_" + tid, t, "json")

    pl = "\n".join(
        f"{i+1}. {cN(p['name'])}"
        for i, p in enumerate(t["players"])
    )

    await callback_query.message.edit_text(
        "╔══════════════════════╗\n"
        "       ⚔️ *TOURNAMENT*\n"
        "╚══════════════════════╝\n\n"
        f"👥 {len(t['players'])}/{t['max']}\n\n"
        f"{pl}\n\n"
        "🥇500 🥈200 🥉100"
        + foot,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f"🎮 Join ({len(t['players'])}/{t['max']})",
                    callback_data=f"trn_join {tid}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚀 Begin",
                    callback_data=f"trn_start {tid}"
                )
            ],
        ]),
        parse_mode="markdown"
    )

    await callback_query.answer("Joined!")

    return

# ═══ TOURNAMENT START ═══
if data.startswith("trn_start "):

    tid = data.split(" ")[1]
    t = Bot.get("trn_" + tid)

    if not t or t["status"] != "registering":
        return

    if user.id != t["creator"]:
        return await callback_query.answer("Host only!", show_alert=True)

    if len(t["players"]) < 2:
        return await callback_query.answer("Need 2+!", show_alert=True)

    import random

    pl = t["players"][:]

    # shuffle
    for i in range(len(pl) - 1, 0, -1):
        j = random.randint(0, i)
        pl[i], pl[j] = pl[j], pl[i]

    mt = []

    for i in range(0, len(pl), 2):

        if i + 1 < len(pl):

            import random
            mg = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))

            mt.append({
                "gid": mg,
                "p1": pl[i],
                "p2": pl[i + 1],
                "winner": None
            })

        else:

            mt.append({
                "gid": None,
                "p1": pl[i],
                "p2": None,
                "winner": pl[i]
            })

    t["status"] = "active"
    t["rounds"] = [mt]
    t["current_round"] = 0
    t["semifinal_losers"] = []

    Bot.set("trn_" + tid, t, "json")

    # notify players
    for p in t["players"]:

        await client.send_message(
            p["id"],
            "⚔️ *TOURNAMENT STARTED!*\n"
            f"🏆 {len(t['players'])} players!\n"
            "🥇500 🥈200 🥉100\n\n"
            "Head to the group!"
            + foot,
            parse_mode="markdown"
        )

    fm = None

    for m in mt:
        if m.get("p2") and m.get("gid"):
            fm = m
            break

    if fm:

        Bot.set(
            "game_" + fm["gid"],
            {
                "id": fm["gid"],
                "p1": fm["p1"]["id"],
                "p1_name": fm["p1"]["name"],
                "p2": fm["p2"]["id"],
                "p2_name": fm["p2"]["name"],
                "p1_msg": None,
                "p2_msg": None,
                "board": [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                "turn": fm["p1"]["id"],
                "status": "playing",
                "is_group": True,
                "group_cid": t["group_cid"],
                "group_mid": t["group_mid"],
                "type": "multi",
                "wager": 0,
                "tourney_id": tid,
            },
            "json"
        )

        Bot.runCommand("/render_board", {"gid": fm["gid"]})

        lk = gLink(t["group_cid"], t["group_mid"])

        await client.send_message(
            fm["p1"]["id"],
            f"🎮 *YOUR MATCH!*\nVs {cN(fm['p2']['name'])}\n🔗 [Play]({lk})",
            parse_mode="markdown"
        )

        await client.send_message(
            fm["p2"]["id"],
            f"🎮 *YOUR MATCH!*\nVs {cN(fm['p1']['name'])}\n🔗 [Play]({lk})",
            parse_mode="markdown"
        )

    return

# ═══ TOURNAMENT REMATCH ═══
if data.startswith("trn_rematch "):

    parts = data.split(" ")
    gid = parts[2]

    g = Bot.get("game_" + gid)
    if not g:
        return await callback_query.answer()

    g["board"] = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    g["status"] = "playing"
    g["winner"] = None
    g["turn"] = g["p1"]

    Bot.set("game_" + gid, g, "json")

    await client.run_command("/render_board", {"gid": gid})

    await callback_query.answer("Rematch!")
    return

# ═══ TOURNAMENT SPLIT ═══
if data.startswith("trn_split "):

    parts = data.split(" ")
    tid = parts[1]
    gid = parts[2]

    t = Bot.get("trn_" + tid)
    g = Bot.get("game_" + gid)

    if not t or not g:
        return

    cr = t["rounds"][t["current_round"]]

    me = None
    for m in cr:
        if m["gid"] == gid:
            me = m
            break

    if me:
        me["winner"] = {"id": "split", "name": "Split"}

        if "semifinal_losers" not in t:
            t["semifinal_losers"] = []

        t["semifinal_losers"].append(me["p1"])
        t["semifinal_losers"].append(me["p2"])

    Libs.ResourcesLib.anotherUserRes("nepcoins", g["p1"]).add(50)
    Libs.ResourcesLib.anotherUserRes("nepcoins", g["p2"]).add(50)

    Bot.set("trn_" + tid, t, "json")

    await client.edit_message_text(
        chat_id=t["group_cid"],
        message_id=t["group_mid"],
        text="🤝 *SPLIT!* Both left with 50 coins.\n⏳ Next match loading..." + foot,
        reply_markup=None,
        parse_mode="markdown"
    )

    await asyncio.sleep(3)

    await advanceTournament(client, tid, gid)

    return

# ═══ TOURNAMENT NEXT (FALLBACK) ═══
if data.startswith("trn_next "):

    parts = data.split(" ")
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

    g = Bot.get("game_" + gid)
    if not g or g["status"] != "playing":
        return

    # ═══ INLINE 60s IDLE AUTO-RESIGN ═══
    if g.get("is_inline") and g.get("last_move"):

        now = int(time.time())

        if now - g["last_move"] > 60:

            afkId = g["turn"]
            winnerId = g["p2"] if afkId == g["p1"] else g["p1"]

            g["status"] = "finished"
            g["winner"] = "resigned"
            g["resigner"] = afkId

            Libs.ResourcesLib.anotherUserRes("ttt_lose", afkId).add(1)

            if winnerId and winnerId != "bot":
                Libs.ResourcesLib.anotherUserRes("ttt_win", winnerId).add(1)

                tl = Bot.get("ttt_top_list") or {}
                tl[winnerId] = tl.get(winnerId, 0) + 1
                Bot.set("ttt_top_list", tl, "json")

            Bot.set("game_" + gid, g, "json")

            await client.run_command("/render_board", {"gid": gid})

            await callback_query.answer(
                "⏰ Time's up! Game auto-resigned after 60s.",
                show_alert=True
            )
            return

    if user.id != g["p1"] and user.id != g["p2"]:
        return await callback_query.answer("🚫 Spectator!", show_alert=True)

    if user.id != g["turn"]:
        return await callback_query.answer("⏳ Not your turn!", show_alert=True)

    if g["board"][idx] != " ":
        return await callback_query.answer("🚫 Taken!")

# Player move
g["board"][idx] = "X" if user.id == g["p1"] else "O"
g["last_move"] = int(time.time())

fr = chk(g["board"])

if fr:

    g["status"] = "finished"
    g["winner"] = fr

    if fr != "draw":

        wI = g["p1"] if fr == "X" else g["p2"]
        lI = g["p2"] if fr == "X" else g["p1"]

        if wI != "bot":

            tl = Bot.get("ttt_top_list") or {}
            tl[wI] = tl.get(wI, 0) + 1
            Bot.set("ttt_top_list", tl, "json")

            Libs.ResourcesLib.anotherUserRes("ttt_win", wI).add(1)

        if lI and lI != "bot":

            sh = Bot.get("shield_" + lI)

            if sh and sh > 0:
                Bot.set("shield_" + lI, sh - 1)
            else:
                Libs.ResourcesLib.anotherUserRes("ttt_lose", lI).add(1)

        if g.get("wager", 0) > 0 and wI != "bot":
            Libs.ResourcesLib.anotherUserRes("nepcoins", wI).add(g["wager"] * 2)

    else:

        if g.get("wager", 0) > 0 and not g.get("tourney_id"):

            Libs.ResourcesLib.anotherUserRes("nepcoins", g["p1"]).add(g["wager"])

            if g["p2"] != "bot":
                Libs.ResourcesLib.anotherUserRes("nepcoins", g["p2"]).add(g["wager"])

    Bot.set("game_" + gid, g, "json")

    await client.run_command("/render_board", {"gid": gid})

    if g.get("tourney_id"):
        await asyncio.sleep(3)
        await advanceTournament(client, g["tourney_id"], gid)

    await callback_query.answer()
    return

# Switch turn
g["turn"] = g["p2"] if g["turn"] == g["p1"] else g["p1"]

# AI move (renders ONCE with both moves)
if g["turn"] == "bot":

    m = aiMv(g)
    g["board"][m] = "O"

    ar = chk(g["board"])

    if ar:

        g["status"] = "finished"
        g["winner"] = ar

        if ar != "draw":

            sh = Bot.get("shield_" + g["p1"])

            if sh and sh > 0:
                Bot.set("shield_" + g["p1"], sh - 1)
            else:
                Libs.ResourcesLib.anotherUserRes("ttt_lose", g["p1"]).add(1)

        elif g.get("wager", 0) > 0:

            Libs.ResourcesLib.anotherUserRes("nepcoins", g["p1"]).add(g["wager"])

    g["turn"] = g["p1"]

Bot.set("game_" + gid, g, "json")

await client.run_command("/render_board", {"gid": gid})

await callback_query.answer()

# ═══ HELP COMMAND ═══
await client.send_message(
    chat_id=chat.id,
    text=
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
        "╔══════════════════════╗\n"
        "     👨‍💻 @nepcodexcc\n"
        "╚══════════════════════╝",
    parse_mode="markdown"
)

# ═══ INLINE QUERY HANDLER ═══

gid = Libs.random.randomString(8)

# Create a pending inline game
Bot.set("game_" + gid, {
    "id": gid,
    "p1": user.id,
    "p1_name": user.first_name,
    "p2": None,
    "p2_name": "???",
    "p1_msg": None,
    "p2_msg": None,
    "board": [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    "turn": user.id,
    "status": "inline_waiting",
    "is_inline": True,
    "inline_mid": None,
    "type": "multi",
    "wager": 0
}, "json")

results = [
    {
        "type": "article",
        "id": gid,
        "title": "🎮 Play Tic-Tac-Toe Here!",
        "description": "Send a game board — your friend can join instantly!",
        "input_message_content": {
            "message_text":
                "╔══════════════════════╗\n"
                "       🎮 *TIC-TAC-TOE*\n"
                "╚══════════════════════╝\n\n"
                "⚔️ *" + user.first_name + "* wants to battle!\n\n"
                "┌──── 🎮 ────┐\n"
                "│  · │ · │ ·\n"
                "│  · │ · │ ·\n"
                "│  · │ · │ ·\n"
                "└──────────────┘\n\n"
                "👇 Tap *Join* to play!\n\n"
                "╔══════════════════════╗\n"
                "     👨‍💻 @nepcodexcc\n"
                "╚══════════════════════╝",
            "parse_mode": "Markdown"
        },
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "🎮 Join & Play!", "callback_data": "ttt_iln_join " + gid}]
            ]
        }
    }
]

await client.answer_inline_query(
    inline_query_id=request.id,
    results=results,
    cache_time=0,
    is_personal=True
)

# ═══ JOIN GAME ═══

gid = options["gid"]
g = Bot.get("game_" + gid)

if not g or g["status"] != "waiting":
    return await client.send_message(chat.id, "🚫 Game unavailable.")

if g["p1"] == user.id:
    return await client.send_message(chat.id, "🚫 Wait for a friend!")

g["p2"] = user.id
g["p2_name"] = user.first_name
g["status"] = "playing"

res = await client.send_message(
    chat.id,
    "🎮 *Joining game...*",
    parse_mode="markdown"
)

if res:
    g["p2_msg"] = res.id
    Bot.set("game_" + gid, g, "json")
    await client.run_command("/render_board", {"gid": gid})

gid = options.get("gid")
g = Bot.get("game_" + gid)
if not g:
    return

import re

def cN(s):
    if not s:
        return "User"
    return re.sub(r"[_*`\[\]()]", " ", s).strip()

# Load skins
s1 = Bot.get("skin_" + str(g["p1"])) or {"x": "❌", "o": "⭕"}
s2 = Bot.get("skin_" + str(g["p2"])) if g.get("p2") and g.get("p2") != "bot" else {"x": "❌", "o": "⭕"}

xI = s1.get("x", "❌")
oI = s2.get("o", "⭕")

# Load board theme
bT = Bot.get("board_" + str(g["p1"])) or {"empty": "·"}

def gI(v):
    return xI if v == "X" else oI if v == "O" else bT.get("empty", "·")

b = g["board"]

gr = [
    [{"text": gI(b[i]), "callback_data": f"ttt_move {gid} {i}"} for i in [0,1,2]],
    [{"text": gI(b[i]), "callback_data": f"ttt_move {gid} {i}"} for i in [3,4,5]],
    [{"text": gI(b[i]), "callback_data": f"ttt_move {gid} {i}"} for i in [6,7,8]],
]

foot = "\n\n╔══════════════════════╗\n     👨‍💻 @nepcodexcc\n╚══════════════════════╝"

p1 = cN(g.get("p1_name"))
p2 = cN(g.get("p2_name"))

txt = ""

# Load titles
t1 = Bot.get("title_" + str(g["p1"]))
t2 = Bot.get("title_" + str(g["p2"])) if g.get("p2") and g.get("p2") != "bot" else None

if g.get("status") == "finished":

    if g.get("winner") == "draw":

        txt = (
            "╔══════════════════════╗\n"
            "       🤝 *DRAW GAME*\n"
            "╚══════════════════════╝\n\n"
            + xI + " " + p1 + " vs " + oI + " " + p2 + "\n"
            + "𝗡𝗼 𝘄𝗶𝗻𝗻𝗲𝗿 𝘁𝗵𝗶𝘀 𝘁𝗶𝗺𝗲!"
        )

        if g.get("wager", 0) > 0:
            txt += "\n💰 Coins refunded!"

        txt += foot

        if g.get("tourney_id"):
            gr.append([
                {"text": "🔄 Rematch", "callback_data": "trn_rematch " + g["tourney_id"] + " " + gid}
            ])
            gr.append([
                {"text": "🤝 Split & Leave", "callback_data": "trn_split " + g["tourney_id"] + " " + gid}
            ])
        elif g.get("is_inline"):
            gr.append([
                {"text": "🎮 Play Again", "callback_data": "ttt_iln_new " + gid}
            ])
        else:
            gr.append([
                {"text": "🔄 Rematch", "callback_data": "ttt_rematch " + gid},
                {"text": "🏠 Menu", "callback_data": "ttt_restart"}
            ])

    elif g.get("winner") == "resigned":

        wN = p2 if g.get("resigner") == g["p1"] else p1
        wT = t2 if g.get("resigner") == g["p1"] else t1

        txt = (
            "╔══════════════════════╗\n"
            "       🏳️ *FORFEIT*\n"
            "╚══════════════════════╝\n\n"
            "🏆 *" + wN + "*" + ((" " + wT) if wT else "") + "\n"
            "𝗢𝗽𝗽𝗼𝗻𝗲𝗻𝘁 𝗿𝗲𝘀𝗶𝗴𝗻𝗲𝗱 🏳️"
        )

        if g.get("wager", 0) > 0:
            txt += "\n\n💰 Won *" + str(g["wager"] * 2) + "* coins!"

        txt += foot

        if g.get("tourney_id"):
            txt += "\n\n⏳ _Next match loading..._"
        elif g.get("is_inline"):
            gr.append([
                {"text": "🎮 Play Again", "callback_data": "ttt_iln_new " + gid}
            ])
        else:
            gr.append([
                {"text": "🔄 Rematch", "callback_data": "ttt_rematch " + gid},
                {"text": "🏠 Menu", "callback_data": "ttt_restart"}
            ])

    else:

        wN = p1 if g.get("winner") == "X" else p2
        wT = t1 if g.get("winner") == "X" else t2

        txt = (
            "╔══════════════════════╗\n"
            "       🏆 *VICTORY!*\n"
            "╚══════════════════════╝\n\n"
            "🎉 *" + wN + "*" + ((" " + wT) if wT else "") + "\n"
            "𝗖𝗼𝗻𝗾𝘂𝗲𝗿𝗲𝗱 𝘁𝗵𝗲 𝗴𝗿𝗶𝗱! 👑"
        )

        if g.get("wager", 0) > 0:
            txt += "\n\n💰 Won *" + str(g["wager"] * 2) + "* coins!"

        txt += foot

        if g.get("tourney_id"):
            txt += "\n\n⏳ _Next match loading..._"
        elif g.get("is_inline"):
            gr.append([
                {"text": "🎮 Play Again", "callback_data": "ttt_iln_new " + gid}
            ])
        else:
            gr.append([
                {"text": "🔄 Rematch", "callback_data": "ttt_rematch " + gid},
                {"text": "🏠 Menu", "callback_data": "ttt_restart"}
            ])

elif g.get("status") == "waiting_acceptance":

    txt = "⚔️ *PENDING*\n" + p1 + " vs @" + g.get("target_username", "")
    if g.get("wager", 0) > 0:
        txt += "\n💰 Bet: " + str(g["wager"])
    txt += foot

    gr = [[{"text": "🤝 Accept", "callback_data": "ttt_acc " + gid}]]

elif g.get("status") == "waiting":

    txt = (
        "⏳ *WAITING FOR OPPONENT*\n\n"
        + xI + " " + p1 + " vs " + oI + " ???\n\n"
        + "📎 `https://t.me/" + bot.username + "?start=ttt_" + gid + "`"
        + foot
    )

    gr.append([{"text": "❌ Cancel", "callback_data": "ttt_cancel " + gid}])

else:

    mk = xI if g.get("turn") == g["p1"] else oI
    tN = p1 if g.get("turn") == g["p1"] else p2

    txt = (
        "╔══════════════════════╗\n"
        "       🎮 *GAME ON*\n"
        "╚══════════════════════╝\n\n"
        "┌──── ⚔️  ᴍᴀᴛᴄʜ ────┐\n"
        "│  " + xI + " " + p1 + "\n"
        "│  " + oI + " " + p2 + "\n"
        "└────────────────────────┘\n\n"
        + mk + " *" + tN + "'s Turn*"
    )

    if g.get("is_inline"):
        txt += "\n⏱ _60s per move or auto-resign_"

    if g.get("wager", 0) > 0:
        txt += "\n💰 Wager: *" + str(g["wager"]) + "*"

    if g.get("tourney_id"):
        txt += "\n⚔️ Tournament Match"

    txt += foot

    gr.append([{"text": "🏳️ Resign", "callback_data": "ttt_resign " + gid}])

# Send to correct chat
if g.get("is_inline") and g.get("inline_mid"):

    url = "https://api.telegram.org/bot" + bot.token + "/editMessageText"

    requests.post(url, json={
        "inline_message_id": g["inline_mid"],
        "text": txt,
        "reply_markup": json.dumps({"inline_keyboard": gr}),
        "parse_mode": "Markdown"
    })

elif g.get("is_group") and g.get("group_cid") and g.get("group_mid"):

    Api.editMessageText({
        "chat_id": g["group_cid"],
        "message_id": g["group_mid"],
        "text": txt,
        "reply_markup": {"inline_keyboard": gr},
        "parse_mode": "Markdown"
    })

else:

    for i, cid in enumerate([g.get("p1"), g.get("p2")]):

        mid = g.get("p1_msg") if i == 0 else g.get("p2_msg")

        if cid and mid and cid != "bot":

            Api.editMessageText({
                "chat_id": cid,
                "message_id": mid,
                "text": txt,
                "reply_markup": {"inline_keyboard": gr},
                "parse_mode": "Markdown"
            })

if chat.get("chat_type") == "private":
    Bot.sendMessage("❌ Use in a *Group*!", {"parse_mode": "Markdown"})
    return

tid = Libs.random.randomString(8)

t = {
    "id": tid,
    "creator": user.id,
    "creator_name": user.first_name,
    "players": [{"id": user.id, "name": user.first_name}],
    "max": 8,
    "status": "registering",
    "rounds": [],
    "current_round": 0,
    "group_cid": chat["id"],
    "group_mid": None,
    "semifinal_losers": []
}
res = await app.send_message(
    chat_id=chat["id"],
    text=
        "╔══════════════════════╗\n"
        "       ⚔️ *TOURNAMENT*\n"
        "╚══════════════════════╝\n\n"
        "🎮 Host: " + user.first_name + "\n"
        "👥 Players: 1/8\n\n"
        "1. " + user.first_name + "\n\n"
        "┌──── 🏆  ᴘʀɪᴢᴇs ────┐\n"
        "│  🥇 1st — 500 coins\n"
        "│  🥈 2nd — 200 coins\n"
        "│  🥉 3rd — 100 coins\n"
        "└────────────────────────┘\n\n"
        "╔══════════════════════╗\n"
        "     👨‍💻 SexiMadara\n"
        "╚══════════════════════╝",
    reply_markup=InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎮 Join Tournament",
                callback_data="trn_join " + tid
            )
        ],
        [
            InlineKeyboardButton(
                "🚀 Begin",
                callback_data="trn_start " + tid
            )
        ]
    ]),
    parse_mode=enums.ParseMode.MARKDOWN
)

if res:
    t["group_mid"] = res.id
    tournaments["trn_" + tid] = t


print("Bot Started!")
app.run()
