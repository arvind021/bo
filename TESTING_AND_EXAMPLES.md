# 🧪 Testing & Examples - Ultimate Telegram Game

## 📋 Testing Checklist

### Bot Setup Testing
- [ ] Token सही है
- [ ] Internet connection ठीक है
- [ ] `python-telegram-bot` installed है
- [ ] Bot को @BotFather से allow किया है

### Feature Testing
- [ ] `/start` - Welcome message दिखता है
- [ ] `/play` - Difficulty buttons दिखते हैं
- [ ] Easy riddle - खेल सकते हो
- [ ] Medium riddle - खेल सकते हो
- [ ] Hard riddle - खेल सकते हो
- [ ] Hints - काम कर रहे हैं (2 hints)
- [ ] `/stats` - Stats दिखते हैं
- [ ] `/challenge` - Daily challenge आता है
- [ ] `/leaderboard` - Top 10 दिखता है
- [ ] `/achievements` - Badges दिखती हैं
- [ ] `/help` - Help message आता है
- [ ] `/quit` - Game quit हो जाता है

### Database Testing
- [ ] Database file create होती है
- [ ] User data save होता है
- [ ] Score update होते हैं
- [ ] History track होती है

---

## 🎮 Example Game Play

### Scenario 1: नया User, Easy Level

```
1. User: /start
   Bot: 🎮 ULTIMATE RIDDLE GAME में स्वागत है!
        /play दबाइए और शुरू करें
   
2. User: /play
   Bot: 🎯 Difficulty चुनें:
        🥚 Easy (10 pts)
        🔥 Medium (20 pts)
        💎 Hard (30 pts)
   
3. User: (Easy button दबाता है)
   Bot: ❓ Riddle
        मैं एक शहर हूँ जो नदी पर बसा हूँ। मेरे पास ताज महल है।
        
        Options:
        □ दिल्ली
        □ आगरा
        □ वाराणसी
        □ कोलकाता
        
        💡 Hint लें

4. User: (आगरा दबाता है)
   Bot: ✅ बिल्कुल सही! 🎉
        
        सही जवाब: आगरा
        आपको 10 points मिले! ⭐
        
        📊 आपके Stats:
        🏆 Total Score: 10 points
        ✅ Riddles Solved: 1
        🎖️ Level: BEGINNER
        
        🎯 नई Achievement Unlock हुई!
        ✨ 🎮 पहला खेल

5. Bot: ▶️ अगला Riddle?
```

### Scenario 2: Hint लेना

```
1. User: /play → Medium चुनता है
   
2. Bot: ❓ Riddle
        मैं दिन में हजार बार खुलता और बंद होता हूँ।
        
        Points: 20

3. User: (💡 Hint button दबाता है)
   Bot: 💡 Hint: यह आपके चेहरे पर है
   
4. User: (अभी भी नहीं समझा, फिर से Hint)
   Bot: 💡 Hint: आप इससे देखते हो
   
5. User: (आँख दबाता है)
   Bot: ✅ सही जवाब!
```

### Scenario 3: गलत जवाब

```
1. User: Hard riddle खेलता है
   
2. Riddle: मेरे पास शहर हैं लेकिन मकान नहीं।
   
3. User: (गलत option चुनता है)
   Bot: ❌ गलत जवाब! 😢
        
        सही जवाब: नक्शा
        आप ने चुना: किताब
        
        इस बार कोई points नहीं।

4. User: अगला riddle खेलता है
```

### Scenario 4: Daily Challenge

```
1. User: /challenge
   Bot: 📅 आज का Daily Challenge ⏳ अभी बाकी है
        
        मैं जितना बड़ा हूँ, उतना कम दिखाई देता हूँ।
        
        💰 Regular Points: 20
        🎁 +50 Bonus Points!

2. User: (सही answer दबाता है)
   Bot: ✅ सही!
        
        Regular Points: 20
        Daily Bonus: 50
        Total: 70 points आज!
```

---

## 📊 Advanced Customization Examples

### Example 1: नए Riddles जोड़ें

```python
# File में RIDDLES list को find करें (line ~55)

RIDDLES = [
    # Existing riddles...
    
    # नया riddle यहाँ add करें:
    {
        "id": 13,
        "difficulty": "easy",
        "question": "मेरे पास मुँह है पर बोल नहीं सकता। मैं क्या हूँ?",
        "options": ["कुआँ", "नदी", "नाला", "सड़क"],
        "answer": "कुआँ",
        "points": 10,
        "hints": [
            "मैं जमीन में गहरा होता हूँ",
            "पानी निकालने के लिए इस्तेमाल होता हूँ"
        ]
    },
]
```

### Example 2: नई Achievement Add करें

```python
# ACHIEVEMENTS dictionary में add करें (line ~150)

ACHIEVEMENTS = {
    # Existing achievements...
    
    # नई achievement:
    "riddle_collector": {
        "name": "📚 Riddle Collector",
        "description": "30 riddles हल करो",
        "points": 100
    },
    
    "speed_demon": {
        "name": "⚡ Speed Demon", 
        "description": "5 riddles 2 minutes में solve करो",
        "points": 75
    },
}
```

फिर `check_achievements` function में add करें:

```python
def check_achievements(user_id):
    # ... existing code ...
    
    if solved >= 30 and "riddle_collector" not in achievements:
        achievements.append("riddle_collector")
        new_achievements.append("riddle_collector")
    
    # ... more checks ...
```

### Example 3: New Difficulty Level Add करें

```python
# अगर 4th level add करना हो (EXTREME)

# RIDDLES में riddles add करें:
{
    "id": 20,
    "difficulty": "extreme",  # नया difficulty
    "question": "बहुत मुश्किल सवाल...",
    "options": ["opt1", "opt2", "opt3", "opt4"],
    "answer": "opt1",
    "points": 50,  # ज्यादा points
    "hints": ["hint1", "hint2"]
}

# Play command में difficulty buttons add करें:
buttons = [
    [InlineKeyboardButton("🥚 Easy (10 pts)", callback_data="difficulty_easy")],
    [InlineKeyboardButton("🔥 Medium (20 pts)", callback_data="difficulty_medium")],
    [InlineKeyboardButton("💎 Hard (30 pts)", callback_data="difficulty_hard")],
    [InlineKeyboardButton("🌪️ Extreme (50 pts)", callback_data="difficulty_extreme")],  # नया
]
```

---

## 🔍 Database Inspection

### SQLite में data देखने के लिए:

```bash
# SQLite shell खोलें
sqlite3 ultimate_riddle_game.db

# सभी tables देखें
.tables

# Users देखें
SELECT * FROM users;

# Game history देखें
SELECT * FROM game_history LIMIT 10;

# Daily challenges देखें
SELECT * FROM daily_challenges;

# Exit करें
.exit
```

### Example Queries:

```sql
-- Top 5 scorers
SELECT username, total_score FROM users ORDER BY total_score DESC LIMIT 5;

-- कितने riddles solved हुए
SELECT user_id, COUNT(*) as total FROM game_history WHERE is_correct = 1 GROUP BY user_id;

-- Most popular riddle
SELECT riddle_id, COUNT(*) as plays FROM game_history GROUP BY riddle_id ORDER BY plays DESC;

-- Hints का analysis
SELECT user_id, AVG(hints_used) as avg_hints FROM game_history GROUP BY user_id;

-- Daily challenge stats
SELECT challenge_date, COUNT(*) as completed FROM daily_challenges WHERE is_completed = 1 GROUP BY challenge_date;
```

---

## 🎯 Performance Optimization

### 1. Database Indexing

```python
def init_database():
    # ... existing code ...
    
    # Speed up queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON game_history(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_score ON users(total_score)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_riddle_id ON game_history(riddle_id)")
    
    conn.commit()
```

### 2. Caching

```python
# User stats को cache करें (optional)
user_stats_cache = {}
cache_expiry = {}

def get_user_stats_cached(user_id):
    import time
    
    # अगर cache fresh है तो return करो
    if user_id in user_stats_cache:
        if time.time() - cache_expiry.get(user_id, 0) < 60:  # 60 sec cache
            return user_stats_cache[user_id]
    
    # नहीं तो database से fetch करो
    stats = get_user_stats(user_id)
    user_stats_cache[user_id] = stats
    cache_expiry[user_id] = time.time()
    
    return stats
```

---

## 📱 UI/UX Improvements

### Add ये emojis:

```python
# Level emojis
level_emoji = {
    "beginner": "🥚",
    "intermediate": "🔥",
    "advanced": "⚡",
    "pro": "👑"
}

# Status emojis
status_emoji = {
    "correct": "✅",
    "wrong": "❌",
    "hint": "💡",
    "complete": "🎉"
}

# Medals
medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

# Stars
stars = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
```

---

## 🔐 Security Tips

### 1. Rate Limiting (spam से बचने के लिए)

```python
from telegram.ext import ContextTypes
from datetime import datetime, timedelta

user_commands = {}

async def rate_limit_check(user_id, max_commands=5, time_window=60):
    now = datetime.now()
    
    if user_id not in user_commands:
        user_commands[user_id] = []
    
    # पुरानी entries remove करो
    user_commands[user_id] = [
        t for t in user_commands[user_id] 
        if now - t < timedelta(seconds=time_window)
    ]
    
    if len(user_commands[user_id]) >= max_commands:
        return False  # Rate limit exceeded
    
    user_commands[user_id].append(now)
    return True  # OK
```

### 2. Input Validation

```python
def sanitize_input(text, max_length=100):
    """User input को safe बनाएं"""
    if not text or len(text) > max_length:
        return None
    return text.strip()
```

---

## 📈 Monitoring & Analytics

### Simple Analytics

```python
def get_game_analytics():
    """Game के stats return करें"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(total_score) FROM users")
    total_points = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM game_history WHERE is_correct = 1")
    total_correct = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM game_history")
    total_games = cursor.fetchone()[0]
    
    accuracy = (total_correct / total_games * 100) if total_games > 0 else 0
    
    conn.close()
    
    return {
        "total_users": total_users,
        "total_points": total_points,
        "total_games": total_games,
        "accuracy": accuracy
    }
```

---

## 🚀 Deployment Checklist

```
Before Deploying:
- [ ] Token set correctly
- [ ] Database tested
- [ ] All commands tested
- [ ] Error handling in place
- [ ] Rate limiting added
- [ ] Backup plan ready
- [ ] Monitoring set up

Deployment:
- [ ] Server configured
- [ ] Python installed
- [ ] Dependencies installed
- [ ] Bot running on screen/supervisor
- [ ] Logs being saved
- [ ] Backups scheduled

Post-Deployment:
- [ ] Monitor logs daily
- [ ] Backup database regularly
- [ ] User feedback collect करो
- [ ] New features plan करो
```

---

## 🎉 Success Metrics

```
Track करने के लिए:
📊 Active Users: कितने लोग रोज खेलते हैं
🏆 Avg Score: औसत score कितना है
⏰ Avg Session: कितने समय खेलते हैं
💾 Database Size: कितना बड़ा हो गया है
🎯 Achievement Rate: कितने achievements unlock हो रहे हैं
```

---

**Made with ❤️ by Claude**

Happy Testing & Customizing! 🚀
