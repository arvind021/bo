# 🎮 ULTIMATE TELEGRAM RIDDLE GAME

## 📋 Overview

यह एक **Professional Grade का Telegram Game** है जिसमें सभी modern features हैं:

```
✨ 12 Handcrafted Riddles (3 Difficulty Levels)
✨ Smart Hints System (2 hints per riddle)
✨ 4-Level Progression System
✨ Achievement/Badge System
✨ Daily Challenges with Bonus Points
✨ Persistent Database (SQLite)
✨ Leaderboard & Rankings
✨ Advanced User Statistics
✨ Beautiful UI/UX
```

---

## 🚀 Quick Start (5 मिनट में Setup)

### Step 1: Token लें
```bash
# Telegram में @BotFather को message करें
/newbot
# Bot का नाम दें: "Ultimate Riddle Game"
# Username दें: "ultimate_riddle_game_bot"
# Token copy करें
```

### Step 2: Install करें
```bash
pip install python-telegram-bot
```

### Step 3: Token डालें
File को edit करें - line number 571:
```python
TOKEN = "123456:ABCdef-ghIJKLmnoPQRSTUVwxyz"
```

### Step 4: Run करें
```bash
python ultimate_telegram_game.py
```

**Output:**
```
╔════════════════════════════════════════╗
║  🎮 ULTIMATE RIDDLE GAME - शुरू हुआ! 🎮  ║
╚════════════════════════════════════════╝
```

---

## 🎮 Game Features

### 1️⃣ **3 Difficulty Levels**

```
🥚 EASY (10 points each)
   - सरल प्रश्न
   - शुरुआती के लिए perfect
   - 4 riddles

🔥 MEDIUM (20 points each)
   - थोड़ा चुनौतीपूर्ण
   - Intermediate players के लिए
   - 4 riddles

💎 HARD (30 points each)
   - बहुत मुश्किल
   - Advanced players के लिए
   - 4 riddles
```

### 2️⃣ **Smart Hints System**

```
💡 हर riddle में 2 hints
💡 बुद्धिमानी से choose करें
💡 Hints डालने से points नहीं कटते
💡 अगर 2 hints use हो जाएं तो और नहीं मिलते
```

### 3️⃣ **4-Level Progression**

```
🥚 BEGINNER (0-99 points)
   - शुरुआत करें

🔥 INTERMEDIATE (100-249 points)
   - सीखते रहें

⚡ ADVANCED (250-499 points)
   - Expert बन रहे हो

👑 PRO (500+ points)
   - Master level!
```

### 4️⃣ **Achievement System**

```
🎮 पहला खेल
   - अपना पहला riddle खेलो

⭐ 5 के लिए Perfect
   - 5 riddles लगातार सही करो

💡 Hint Master
   - 10 hints use करो

🥚 Easy Master
   - सभी Easy riddles हल करो

🔥 Medium Master
   - सभी Medium riddles हल करो

💎 Hard Master
   - सभी Hard riddles हल करो

💰 500 points
   - 500 points हासिल करो

📅 Daily Champion
   - 7 दिन के Daily Challenges पूरे करो
```

### 5️⃣ **Daily Challenges**

```
📅 हर दिन 1 special riddle
🎁 Bonus +50 points
🔄 अलग-अलग difficulty हर दिन
🏆 Streak बनाएं
```

### 6️⃣ **Persistent Leaderboard**

```
🏅 Top 10 players दिखाई देते हैं
🥇 🥈 🥉 medals के साथ
📊 Level के साथ
⏰ Lifetime stats
```

---

## 📱 Available Commands

| Command | काम | Description |
|---------|------|------------|
| `/start` | Game intro | स्वागत message दिखाता है |
| `/play` | शुरू करें | Difficulty चुनें और खेलें |
| `/challenge` | Daily riddle | आज का special challenge |
| `/stats` | Mera Score | अपने statistics देखें |
| `/achievements` | Badges | अपनी achievements देखें |
| `/leaderboard` | Top Players | Top 10 scorers देखें |
| `/help` | Help | पूरी guide दिखाता है |
| `/quit` | खेल छोड़ें | Game को quit करें |

---

## 🗄️ Database Structure

### Users Table
```sql
user_id (PRIMARY KEY)      - Telegram user ID
username                   - User का नाम
total_score               - कुल points
riddles_solved            - हल किए गए riddles
hints_used                - इस्तेमाल किए गए hints
last_played               - आखिरी बार खेला कब
level                     - Current level
streak                    - Consecutive correct answers
achievements              - Unlock किए गए badges (JSON)
```

### Game History Table
```sql
id                        - Unique ID
user_id (FOREIGN KEY)     - कौन खेल रहा है
riddle_id                 - कौन सा riddle
difficulty                - Easy/Medium/Hard
answer                    - दिया गया जवाब
is_correct                - सही है?
points_earned             - कितने points मिले
hints_used                - कितने hints use किए
played_at                 - कब खेला
```

### Daily Challenges Table
```sql
id                        - Unique ID
user_id (FOREIGN KEY)     - किसका challenge
challenge_date            - किस दिन का
riddle_id                 - कौन सा riddle
is_completed              - पूरा किया?
bonus_points              - Extra points
completed_at              - कब पूरा किया
```

---

## 🎯 How Game Works (Step-by-Step)

```
1. User /start करता है
   ↓
2. Bot intro दिखाता है + commands
   ↓
3. User /play दबाता है
   ↓
4. Bot difficulty levels दिखाता है
   - Easy (🥚)
   - Medium (🔥)
   - Hard (💎)
   ↓
5. User difficulty चुनता है
   ↓
6. Bot random riddle दिखाता है
   - Question
   - 4 options
   - Hint button
   - Points info
   ↓
7. User answer चुनता है
   - या
   - Hint लेता है (2 hints available)
   ↓
8. Bot result दिखाता है
   ✅ सही → Points + achievement check
   ❌ गलत → सही जवाब बताता है
   ↓
9. User stats update होते हैं
   - Score बढ़ता है
   - Level बदलता है
   - Achievements unlock होती हैं
   ↓
10. "अगला Riddle?" button दिखता है
    ↓
11. Process दोहराता है
```

---

## 📊 Points Calculation

```
Easy Riddle:
- बिना hint: 10 points
- 1 hint के साथ: 10 points
- 2 hints के साथ: 10 points
(Points hints use करने से नहीं कटते)

Medium Riddle:
- Without hint: 20 points
- With hints: 20 points

Hard Riddle:
- Without hint: 30 points
- With hints: 30 points

Daily Challenge Bonus:
- Regular points (10/20/30)
- + 50 BONUS points
- (अगर same दिन में complete करो)
```

---

## 🔧 Customization Guide

### अपने Riddles Add करें

```python
RIDDLES = [
    {
        "id": 13,                              # नया ID
        "difficulty": "easy",                   # या "medium" या "hard"
        "question": "आपका नया सवाल यहाँ...",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "answer": "Option 1",                  # सही जवाब
        "points": 10,                          # Easy=10, Medium=20, Hard=30
        "hints": [
            "पहला hint यहाँ",
            "दूसरा hint यहाँ"
        ]
    },
]
```

### Achievements Add करें

```python
ACHIEVEMENTS = {
    "my_achievement": {
        "name": "🎯 Achievement Name",
        "description": "क्या करना है achievement unlock करने के लिए",
        "points": 50  # bonus points
    },
}
```

### Database Files

```
ultimate_riddle_game.db
├── users table
├── game_history table
└── daily_challenges table
```

Database को delete करने से सभी data clear हो जाता है।

---

## 🐛 Troubleshooting

### ❌ Bot respond नहीं कर रहा?

1. Token सही है?
   ```bash
   # @BotFather में check करें
   /getme
   ```

2. Internet connection ठीक है?
   ```bash
   ping google.com
   ```

3. Bot को /start से allow किया?

### ❌ "ModuleNotFoundError" error?

```bash
pip install --upgrade python-telegram-bot
```

### ❌ Database locked?

```bash
# Database file को delete करें
rm ultimate_riddle_game.db

# फिर से run करें
python ultimate_telegram_game.py
```

### ❌ Bot अचानक बंद हुआ?

```bash
# Logs के साथ run करें
python ultimate_telegram_game.py --verbose

# या screen में run करें (persist करने के लिए)
screen -S game
python ultimate_telegram_game.py
# Ctrl+A, फिर D (detach करने के लिए)
```

---

## 📈 Performance Tips

1. **Database को regularly backup करें**
   ```bash
   cp ultimate_riddle_game.db ultimate_riddle_game_backup.db
   ```

2. **Leaderboard को optimize करें**
   - Database में index add करें (advanced)

3. **User sessions को manage करें**
   - Context में ही रखें (already done)

4. **Long-running bot के लिए**
   ```bash
   pip install supervisor
   # या
   screen -S telegram_game
   nohup python ultimate_telegram_game.py &
   ```

---

## 🌐 Server पर Deploy करें

### Replit पर:
1. Code को Replit में paste करें
2. Environment variables में TOKEN set करें
3. Run करें!

### Heroku पर:
1. Procfile बनाएं: `worker: python ultimate_telegram_game.py`
2. requirements.txt: `python-telegram-bot`
3. `git push heroku main`

### AWS/GCP पर:
1. EC2/Compute Instance setup करें
2. Python install करें
3. Bot को run करें (screen/systemd के साथ)

---

## 🎉 Game Statistics Example

```
एक player के लिए:

📊 Stats:
🏆 Total Score: 845 points
✅ Riddles Solved: 42
💡 Hints Used: 8
🎖️ Level: Advanced (⚡)
🔥 Streak: 5 consecutive correct

🏅 Achievements Unlocked:
✅ First Game
✅ 5 for Perfect
✅ Medium Master
✅ 500 Points
✅ 7 Achievements total

📅 Daily Challenge:
✅ Completed today (+50 bonus)
🎁 Weekly streak: 4 days
```

---

## 🎓 Learning Resources

- **Telegram Bot Docs**: https://core.telegram.org/bots
- **Python Telegram Bot**: https://python-telegram-bot.readthedocs.io/
- **SQLite**: https://www.sqlite.org/docs.html

---

## 📞 Support

अगर कोई issue है:

1. **Token check करें** - BotFather में /getme
2. **Internet check करें** - Connectivity verify करें
3. **Logs देखें** - Terminal output में error
4. **Database reset करें** - DB file delete करके restart

---

## 🎉 You're Ready!

```
✅ Code ready
✅ Features built
✅ Database set up
✅ Ready to deploy

अब /start दबाइए और खेलना शुरू करें! 🚀
```

**Made with ❤️ by Claude**

Happy Gaming! 🎮🎉
