"""
🎮 ULTIMATE TELEGRAM RIDDLE GAME 🎮
Professional Grade - with Hints, Difficulty Levels, Achievements, Daily Challenges
Database: SQLite | Language: Python | Framework: python-telegram-bot
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler
import random
import sqlite3
from datetime import datetime, timedelta
import json

# ============================================================================
# DATABASE SETUP
# ============================================================================

DB_FILE = "ultimate_riddle_game.db"

def init_database():
    """Database को initialize करें"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            total_score INTEGER DEFAULT 0,
            riddles_solved INTEGER DEFAULT 0,
            hints_used INTEGER DEFAULT 0,
            last_played TEXT,
            level TEXT DEFAULT 'beginner',
            streak INTEGER DEFAULT 0,
            achievements TEXT DEFAULT '[]'
        )
    """)
    
    # Game History
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            riddle_id INTEGER,
            difficulty TEXT,
            answer TEXT,
            is_correct BOOLEAN,
            points_earned INTEGER,
            hints_used INTEGER DEFAULT 0,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Daily Challenges
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            challenge_date TEXT,
            riddle_id INTEGER,
            is_completed BOOLEAN DEFAULT FALSE,
            bonus_points INTEGER DEFAULT 50,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    conn.commit()
    conn.close()

# ============================================================================
# COMPREHENSIVE RIDDLES DATABASE
# ============================================================================

RIDDLES = [
    # BEGINNER (Easy)
    {
        "id": 1,
        "difficulty": "easy",
        "question": "मैं एक शहर हूँ जो नदी पर बसा हूँ। मेरे पास ताज महल है।",
        "options": ["दिल्ली", "आगरा", "वाराणसी", "कोलकाता"],
        "answer": "आगरा",
        "points": 10,
        "hints": ["यह शहर उत्तर प्रदेश में है", "ताज महल यहाँ है"]
    },
    {
        "id": 2,
        "difficulty": "easy",
        "question": "मेरे पास कोई पैर नहीं लेकिन मैं चल सकता हूँ।",
        "options": ["नदी", "हवा", "बादल", "रेत"],
        "answer": "नदी",
        "points": 10,
        "hints": ["यह जल से बना है", "यह बहता है"]
    },
    {
        "id": 3,
        "difficulty": "easy",
        "question": "मैं हर दिन आता हूँ लेकिन कभी नहीं आया था।",
        "options": ["सूरज", "बारिश", "हवा", "रात"],
        "answer": "सूरज",
        "points": 10,
        "hints": ["यह आकाश में है", "यह गर्मी देता है"]
    },
    {
        "id": 4,
        "difficulty": "easy",
        "question": "मेरे पास हाथ हैं लेकिन मैं नहीं पकड़ सकता।",
        "options": ["घड़ी", "घंटा", "नदी", "दीवार"],
        "answer": "घड़ी",
        "points": 10,
        "hints": ["मैं समय दिखाता हूँ", "मेरे दो हाथ हैं"]
    },
    
    # MEDIUM (Normal)
    {
        "id": 5,
        "difficulty": "medium",
        "question": "मैं दिन में हजार बार खुलता और बंद होता हूँ।",
        "options": ["दरवाजा", "आँख", "मुँह", "किताब"],
        "answer": "आँख",
        "points": 20,
        "hints": ["यह आपके चेहरे पर है", "आप इससे देखते हो"]
    },
    {
        "id": 6,
        "difficulty": "medium",
        "question": "मैं जितना बड़ा हूँ, उतना कम दिखाई देता हूँ।",
        "options": ["धुआँ", "अंधकार", "कुआँ", "सुरंग"],
        "answer": "अंधकार",
        "points": 20,
        "hints": ["रात में मैं होता हूँ", "मुझे प्रकाश से डर लगता है"]
    },
    {
        "id": 7,
        "difficulty": "medium",
        "question": "मैं आकाश में हूँ लेकिन मेरा कोई शरीर नहीं है।",
        "options": ["बादल", "तारा", "इंद्रधनुष", "परछाई"],
        "answer": "इंद्रधनुष",
        "points": 20,
        "hints": ["बारिश के बाद दिखता हूँ", "मेरे सात रंग हैं"]
    },
    {
        "id": 8,
        "difficulty": "medium",
        "question": "मैं खाना नहीं खाता पर आग जरूर खाता हूँ।",
        "options": ["घड़ी", "मोमबत्ती", "दीपक", "आईना"],
        "answer": "मोमबत्ती",
        "points": 20,
        "hints": ["मैं रात में उपयोगी हूँ", "मुझे जलाया जाता है"]
    },
    
    # HARD (Difficult)
    {
        "id": 9,
        "difficulty": "hard",
        "question": "मेरे पास शहर हैं लेकिन मकान नहीं। मेरे पास पानी है लेकिन मछली नहीं।",
        "options": ["नक्शा", "आईना", "किताब", "तस्वीर"],
        "answer": "नक्शा",
        "points": 30,
        "hints": ["मैं कागज पर होता हूँ", "मैं दिशाएँ दिखाता हूँ"]
    },
    {
        "id": 10,
        "difficulty": "hard",
        "question": "मैं जितना ज्यादा सूखा हूँ, उतना ही ज्यादा गीला होता हूँ।",
        "options": ["कपड़ा", "साबुन", "तौलिया", "कपास"],
        "answer": "तौलिया",
        "points": 30,
        "hints": ["नहाते समय इस्तेमाल होता हूँ", "मैं नमी सोखता हूँ"]
    },
    {
        "id": 11,
        "difficulty": "hard",
        "question": "मैं हर जगह हूँ लेकिन मुझे कभी नहीं देखा जा सकता। मैं सब कुछ के साथ हूँ।",
        "options": ["हवा", "प्रकाश", "परछाई", "समय"],
        "answer": "परछाई",
        "points": 30,
        "hints": ["सूरज की जरूरत है", "मेरा आकार बदलता है"]
    },
    {
        "id": 12,
        "difficulty": "hard",
        "question": "मेरे बिना आप खा सकते हैं लेकिन स्वाद नहीं ले सकते।",
        "options": ["नमक", "मिर्च", "जीभ", "दाँत"],
        "answer": "जीभ",
        "points": 30,
        "hints": ["यह आपके मुँह में है", "स्वाद के लिए जरूरी है"]
    }
]

# ============================================================================
# ACHIEVEMENTS SYSTEM
# ============================================================================

ACHIEVEMENTS = {
    "first_game": {"name": "🎮 पहला खेल", "description": "अपना पहला riddle खेलो", "points": 10},
    "perfect_streak_5": {"name": "⭐ 5 के लिए Perfect", "description": "5 riddles लगातार सही करो", "points": 50},
    "hint_master": {"name": "💡 Hint Master", "description": "10 hints का उपयोग करो", "points": 25},
    "difficulty_easy": {"name": "🥚 Easy Master", "description": "सभी Easy riddles हल करो", "points": 30},
    "difficulty_medium": {"name": "🔥 Medium Master", "description": "सभी Medium riddles हल करो", "points": 60},
    "difficulty_hard": {"name": "💎 Hard Master", "description": "सभी Hard riddles हल करो", "points": 100},
    "score_500": {"name": "💰 500 points", "description": "500 points हासिल करो", "points": 50},
    "daily_challenge": {"name": "📅 Daily Champion", "description": "7 दिन के Daily Challenges पूरे करो", "points": 75},
}

# ============================================================================
# DATABASE HELPER FUNCTIONS
# ============================================================================

def get_or_create_user(user_id, username):
    """User को create/update करें"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute(
            "INSERT INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username)
        )
        conn.commit()
    
    conn.close()

def get_user_stats(user_id):
    """User के stats return करें"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT total_score, riddles_solved, hints_used, level, streak, achievements 
        FROM users WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "score": result[0],
            "riddles_solved": result[1],
            "hints_used": result[2],
            "level": result[3],
            "streak": result[4],
            "achievements": json.loads(result[5]) if result[5] else []
        }
    return None

def save_game_result(user_id, riddle_id, difficulty, answer, is_correct, points, hints_used=0):
    """Game result save करें और achievements check करें"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO game_history 
           (user_id, riddle_id, difficulty, answer, is_correct, points_earned, hints_used) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, riddle_id, difficulty, answer, is_correct, points, hints_used)
    )
    
    if is_correct:
        cursor.execute(
            "UPDATE users SET total_score = total_score + ?, riddles_solved = riddles_solved + 1 WHERE user_id = ?",
            (points, user_id)
        )
    
    cursor.execute(
        "UPDATE users SET hints_used = hints_used + ? WHERE user_id = ?",
        (hints_used, user_id)
    )
    
    # Update level based on score
    cursor.execute("SELECT total_score FROM users WHERE user_id = ?", (user_id,))
    total_score = cursor.fetchone()[0]
    
    if total_score >= 500:
        level = "pro"
    elif total_score >= 250:
        level = "advanced"
    elif total_score >= 100:
        level = "intermediate"
    else:
        level = "beginner"
    
    cursor.execute("UPDATE users SET level = ? WHERE user_id = ?", (level, user_id))
    
    conn.commit()
    conn.close()
    
    # Check achievements
    check_achievements(user_id)

def check_achievements(user_id):
    """Achievements को check और update करें"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT total_score, riddles_solved, hints_used, achievements FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if not result:
        return
    
    score, solved, hints, achievements_str = result
    achievements = json.loads(achievements_str) if achievements_str else []
    
    # New achievements to unlock
    new_achievements = []
    
    if solved >= 1 and "first_game" not in achievements:
        achievements.append("first_game")
        new_achievements.append("first_game")
    
    if score >= 500 and "score_500" not in achievements:
        achievements.append("score_500")
        new_achievements.append("score_500")
    
    if hints >= 10 and "hint_master" not in achievements:
        achievements.append("hint_master")
        new_achievements.append("hint_master")
    
    # Save updated achievements
    cursor.execute(
        "UPDATE users SET achievements = ? WHERE user_id = ?",
        (json.dumps(achievements), user_id)
    )
    
    conn.commit()
    conn.close()
    
    return new_achievements

def get_leaderboard(limit=10):
    """Top scorers return करें"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT username, total_score, riddles_solved, level FROM users ORDER BY total_score DESC LIMIT ?",
        (limit,)
    )
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_daily_challenge(user_id):
    """आज का daily challenge return करें"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute(
        "SELECT riddle_id, is_completed FROM daily_challenges WHERE user_id = ? AND challenge_date = ?",
        (user_id, today)
    )
    result = cursor.fetchone()
    
    if not result:
        # नया daily challenge बनाएं
        riddle_id = random.choice([r["id"] for r in RIDDLES])
        cursor.execute(
            "INSERT INTO daily_challenges (user_id, challenge_date, riddle_id) VALUES (?, ?, ?)",
            (user_id, today, riddle_id)
        )
        conn.commit()
        result = (riddle_id, False)
    
    conn.close()
    return result

# ============================================================================
# BOT COMMAND HANDLERS
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Game शुरू करें"""
    user_id = update.effective_user.id
    username = update.effective_user.first_name or "Player"
    
    get_or_create_user(user_id, username)
    
    welcome_text = """
╔══════════════════════════════════════╗
║    🎮 ULTIMATE RIDDLE GAME 🎮       ║
║  खेलो, सीखो, और जीतो!              ║
╚══════════════════════════════════════╝

🔥 **Features:**
🎯 3 Difficulty Levels (Easy, Medium, Hard)
💡 Smart Hints System
🏆 Achievements & Badges
📊 Leaderboard
📅 Daily Challenges
🎪 Rewards & Points

📋 **Commands:**
/play - खेलना शुरू करें
/challenge - आज का Challenge
/stats - अपने Stats देखें
/leaderboard - Top Players
/achievements - Achievements
/help - सहायता
/quit - खेल छोड़ें

👉 /play दबाइए और शुरू करें! 🚀
    """
    
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Difficulty level चुनने के लिए पूछें"""
    user_id = update.effective_user.id
    get_or_create_user(user_id, update.effective_user.first_name)
    
    buttons = [
        [InlineKeyboardButton("🥚 Easy (10 pts)", callback_data="difficulty_easy")],
        [InlineKeyboardButton("🔥 Medium (20 pts)", callback_data="difficulty_medium")],
        [InlineKeyboardButton("💎 Hard (30 pts)", callback_data="difficulty_hard")],
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text(
        "🎯 **Difficulty चुनें:**\n\n"
        "🥚 Easy - शुरुआती के लिए\n"
        "🔥 Medium - थोड़ा challenging\n"
        "💎 Hard - बहुत मुश्किल",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_difficulty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Difficulty चुनने के बाद riddle दिखाएं"""
    query = update.callback_query
    user_id = query.from_user.id
    
    difficulty = query.data.replace("difficulty_", "")
    
    # इसी difficulty के riddles ढूंढें
    available_riddles = [r for r in RIDDLES if r["difficulty"] == difficulty]
    
    if not available_riddles:
        await query.answer("❌ इस difficulty के riddles नहीं मिले!")
        return
    
    riddle = random.choice(available_riddles)
    
    # Session में store करें
    context.user_data["current_riddle"] = riddle
    context.user_data["difficulty"] = difficulty
    context.user_data["hints_remaining"] = 2  # 2 hints दे सकते हैं
    
    # Buttons बनाएं
    buttons = []
    for option in riddle["options"]:
        buttons.append([InlineKeyboardButton(option, callback_data=f"answer_{riddle['id']}_{option}")])
    
    buttons.append([InlineKeyboardButton("💡 Hint लें", callback_data=f"hint_{riddle['id']}")])
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    difficulty_emoji = {"easy": "🥚", "medium": "🔥", "hard": "💎"}
    
    question_text = f"""
{difficulty_emoji.get(difficulty, "❓")} **Riddle**

{riddle['question']}

💰 **Points: {riddle['points']}**
💡 **Hints बाकी: {context.user_data['hints_remaining']}**
    """
    
    await query.edit_message_text(question_text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Answer को process करें"""
    query = update.callback_query
    user_id = query.from_user.id
    
    # Parse callback data
    data_parts = query.data.replace("answer_", "").split("_")
    riddle_id = int(data_parts[0])
    selected_answer = "_".join(data_parts[1:])
    
    # Current riddle को ढूंढें
    riddle = context.user_data.get("current_riddle")
    
    if not riddle:
        await query.answer("❌ पहले /play दबाइए!")
        return
    
    correct_answer = riddle["answer"]
    is_correct = selected_answer == correct_answer
    difficulty = context.user_data.get("difficulty", "easy")
    hints_used = 2 - context.user_data.get("hints_remaining", 2)
    
    # Result को save करें
    points = riddle["points"] if is_correct else 0
    save_game_result(user_id, riddle_id, difficulty, selected_answer, is_correct, points, hints_used)
    
    stats = get_user_stats(user_id)
    new_achievements = check_achievements(user_id)
    
    if is_correct:
        result_text = f"""
✅ **बिल्कुल सही!** 🎉

सही जवाब: **{correct_answer}**
आपको **{riddle['points']} points** मिले! ⭐

📊 **आपके Stats:**
🏆 Total Score: {stats['score']} points
✅ Riddles Solved: {stats['riddles_solved']}
🎖️ Level: {stats['level'].upper()}

"""
        if new_achievements:
            result_text += "🎯 **नई Achievement Unlock हुई!**\n"
            for ach in new_achievements:
                if ach in ACHIEVEMENTS:
                    result_text += f"✨ {ACHIEVEMENTS[ach]['name']}\n"
        
        await query.answer("✅ सही जवाब! बधाई!")
    else:
        result_text = f"""
❌ **गलत जवाब!** 😢

सही जवाब: **{correct_answer}**
आप ने चुना: **{selected_answer}**

इस बार कोई points नहीं। 😔

📊 **आपके Stats:**
🏆 Total Score: {stats['score']} points
✅ Riddles Solved: {stats['riddles_solved']}
🎖️ Level: {stats['level'].upper()}
        """
        await query.answer("❌ गलत!")
    
    await query.edit_message_text(result_text, parse_mode="Markdown")
    
    # अगला riddle का बटन
    buttons = [[InlineKeyboardButton("▶️ अगला Riddle", callback_data="next_riddle")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.reply_text("अगले riddle के लिए तैयार हैं?", reply_markup=reply_markup)

async def handle_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hint दिखाएं"""
    query = update.callback_query
    
    riddle = context.user_data.get("current_riddle")
    hints_remaining = context.user_data.get("hints_remaining", 0)
    
    if not riddle:
        await query.answer("❌ कोई riddle नहीं है!")
        return
    
    if hints_remaining <= 0:
        await query.answer("❌ आपके सभी hints खत्म हो गए!")
        return
    
    # Hint दिखाएं
    hint_index = 2 - hints_remaining
    if hint_index < len(riddle["hints"]):
        hint_text = riddle["hints"][hint_index]
        context.user_data["hints_remaining"] -= 1
        
        await query.answer(f"💡 Hint: {hint_text}", show_alert=True)
    else:
        await query.answer("❌ और कोई hint नहीं है!")

async def next_riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """अगला riddle दिखाएं"""
    query = update.callback_query
    await query.answer()
    await play(query, context)

async def daily_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """आज का Daily Challenge दिखाएं"""
    user_id = update.effective_user.id
    get_or_create_user(user_id, update.effective_user.first_name)
    
    riddle_id, is_completed = get_daily_challenge(user_id)
    riddle = next((r for r in RIDDLES if r["id"] == riddle_id), None)
    
    if not riddle:
        await update.message.reply_text("❌ Daily Challenge नहीं मिला!")
        return
    
    status = "✅ पूरा किया!" if is_completed else "⏳ अभी बाकी है"
    bonus = "🎁 +50 Bonus Points!" if not is_completed else ""
    
    buttons = []
    for option in riddle["options"]:
        buttons.append([InlineKeyboardButton(option, callback_data=f"daily_{riddle['id']}_{option}")])
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    challenge_text = f"""
📅 **आज का Daily Challenge** {status}

{riddle['question']}

💰 Regular Points: {riddle['points']}
🎁 {bonus}
    """
    
    await update.message.reply_text(challenge_text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User के stats दिखाएं"""
    user_id = update.effective_user.id
    username = update.effective_user.first_name
    
    stats = get_user_stats(user_id)
    
    if not stats:
        await update.message.reply_text("पहले /play दबाकर game खेलिए!")
        return
    
    level_emoji = {
        "beginner": "🥚",
        "intermediate": "🔥",
        "advanced": "⚡",
        "pro": "👑"
    }
    
    stats_text = f"""
📊 **{username} के Stats** 📊

🏆 Total Score: {stats['score']} points
✅ Riddles Solved: {stats['riddles_solved']}
💡 Hints Used: {stats['hints_used']}
🎖️ Level: {level_emoji.get(stats['level'], '🎯')} {stats['level'].upper()}
🔥 Streak: {stats['streak']} riddles

📚 Achievements Unlocked: {len(stats['achievements'])}
    """
    
    await update.message.reply_text(stats_text, parse_mode="Markdown")

async def show_achievements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Achievements दिखाएं"""
    user_id = update.effective_user.id
    stats = get_user_stats(user_id)
    
    if not stats:
        await update.message.reply_text("पहले /play दबाकर game खेलिए!")
        return
    
    unlocked = stats["achievements"]
    
    achievements_text = "🏅 **Achievements** 🏅\n\n"
    
    for ach_key, ach_data in ACHIEVEMENTS.items():
        if ach_key in unlocked:
            achievements_text += f"✅ {ach_data['name']} - {ach_data['description']}\n"
        else:
            achievements_text += f"🔒 {ach_data['name']} - {ach_data['description']}\n"
    
    await update.message.reply_text(achievements_text, parse_mode="Markdown")

async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Leaderboard दिखाएं"""
    leaderboard = get_leaderboard(10)
    
    if not leaderboard:
        await update.message.reply_text("अभी leaderboard empty है। /play दबाइए!")
        return
    
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    leaderboard_text = "🏅 **Top 10 Players** 🏅\n\n"
    
    for idx, (username, score, solved, level) in enumerate(leaderboard):
        leaderboard_text += f"{medals[idx]} **{username}** - {score} pts ({solved} riddles) [{level.upper()}]\n"
    
    await update.message.reply_text(leaderboard_text, parse_mode="Markdown")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """मदद दिखाएं"""
    help_text = """
📚 **Help Guide** 📚

🎮 **कैसे खेलें:**
1. /play दबाइए
2. Difficulty चुनें (Easy/Medium/Hard)
3. Riddle को समझिए
4. सही option चुनिए
5. Points जीतिए!

💡 **Hints:**
- हर riddle के 2 hints हैं
- बुद्धिमानी से इस्तेमाल करें
- Hints का कोई फायदा नहीं होता

🏆 **Points System:**
🥚 Easy: 10 points
🔥 Medium: 20 points
💎 Hard: 30 points

📅 **Daily Challenge:**
- हर दिन 1 special riddle
- Bonus +50 points
- /challenge दबाइए

🎯 **Levels:**
🥚 Beginner: 0-99 points
🔥 Intermediate: 100-249 points
⚡ Advanced: 250-499 points
👑 Pro: 500+ points

❓ **Commands:**
/play - खेलना शुरू करें
/challenge - Daily Challenge
/stats - अपने stats
/leaderboard - Top players
/achievements - Badges
/help - यह message

Happy Gaming! 🚀
    """
    
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def quit_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Game छोड़ें"""
    user_id = update.effective_user.id
    stats = get_user_stats(user_id)
    
    if stats:
        quit_text = f"""
👋 **Thanks for Playing!**

🏆 Your Final Score: {stats['score']} points
✅ Riddles Solved: {stats['riddles_solved']}
🎖️ Level: {stats['level'].upper()}

दोबारा खेलने के लिए /play दबाइए! 🎮
        """
        await update.message.reply_text(quit_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("आपने अभी game नहीं खेली है।")

# ============================================================================
# MAIN BOT SETUP
# ============================================================================

def main():
    """Bot को शुरू करें"""
    init_database()
    
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
    
    application = Application.builder().token(TOKEN).build()
    
    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("challenge", daily_challenge))
    application.add_handler(CommandHandler("stats", show_stats))
    application.add_handler(CommandHandler("achievements", show_achievements))
    application.add_handler(CommandHandler("leaderboard", show_leaderboard))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("quit", quit_game))
    
    # Callback Handlers
    application.add_handler(CallbackQueryHandler(handle_difficulty, pattern=r"^difficulty_"))
    application.add_handler(CallbackQueryHandler(handle_answer, pattern=r"^answer_"))
    application.add_handler(CallbackQueryHandler(handle_hint, pattern=r"^hint_"))
    application.add_handler(CallbackQueryHandler(next_riddle, pattern="^next_riddle$"))
    
    print("""
╔════════════════════════════════════════╗
║  🎮 ULTIMATE RIDDLE GAME - शुरू हुआ! 🎮  ║
║                                        ║
║  Database: riddle_game.db              ║
║  Total Riddles: 12                     ║
║  Features: Hints, Achievements, Daily  ║
║                                        ║
║  Telegram में bot search करें          ║
║  /start दबाइए और खेलना शुरू करें      ║
╚════════════════════════════════════════╝
    """)
    
    application.run_polling()

if __name__ == "__main__":
    main()
