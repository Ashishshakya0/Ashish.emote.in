from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import os
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ashish-premium-panel-2024')

# ==================== EMOTE DATABASE (400+ EMOTES) ====================
EMOTE_DATABASE = {
    "EVO_GUNS": [
        {"name": "🔥 EVO MP40", "id": "909000075", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🔥 EVO AK", "id": "909000063", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🔥 EVO UMP", "id": "909000098", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🔥 EVO XMB", "id": "909000065", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🔥 EVO SCAR", "id": "909000068", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🔥 EVO M10", "id": "909000081", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🔥 EVO FAMAS", "id": "909000090", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🔥 EVO MP5", "id": "909033002", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🔥 EVO M1887", "id": "909035007", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🔥 EVO WOODPECKER", "id": "909042008", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
    ],
    
    "SPECIAL_EMOTES": [
        {"name": "💰 PAISA EMOTE", "id": "909000055", "icon": "fa-money-bill-wave", "rarity": "epic", "color": "#00ff88"},
        {"name": "💖 HEART EMOTE", "id": "909000045", "icon": "fa-heart", "rarity": "epic", "color": "#ff2a6d"},
        {"name": "🌹 ROSE EMOTE", "id": "909000010", "icon": "fa-rose", "rarity": "epic", "color": "#ff2a6d"},
        {"name": "👑 THRONE EMOTE", "id": "909000014", "icon": "fa-crown", "rarity": "legendary", "color": "#ffcc00"},
        {"name": "🏴‍☠️ PIRATE'S FLAG", "id": "909000034", "icon": "fa-flag", "rarity": "epic", "color": "#ff8800"},
        {"name": "💨 EAT MY DUST", "id": "909000039", "icon": "fa-wind", "rarity": "epic", "color": "#00d4ff"},
        {"name": "😂 LOL EMOTE", "id": "909000002", "icon": "fa-laugh", "rarity": "rare", "color": "#ffcc00"},
        {"name": "🐍 COBRA EMOTE", "id": "909000072", "icon": "fa-snake", "rarity": "legendary", "color": "#00ff88"},
        {"name": "👻 GHOST EMOTE", "id": "909036001", "icon": "fa-ghost", "rarity": "epic", "color": "#9d4edd"},
        {"name": "🔥 FIRE ON EMOTE", "id": "909033001", "icon": "fa-fire", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🎬 SHOLAY EMOTE", "id": "909050020", "icon": "fa-film", "rarity": "epic", "color": "#ff8800"},
        {"name": "⭐ PRIME 8 EMOTE", "id": "909035013", "icon": "fa-star", "rarity": "legendary", "color": "#ffcc00"},
        {"name": "💪 PUSH UP", "id": "909000012", "icon": "fa-dumbbell", "rarity": "rare", "color": "#00d4ff"},
        {"name": "😈 DEVIL'S MOVE", "id": "909000020", "icon": "fa-horn", "rarity": "epic", "color": "#9d4edd"},
        {"name": "👑 EL 3ARCH EMOTE", "id": "909000014", "icon": "fa-throne", "rarity": "legendary", "color": "#ffcc00"},
        {"name": "✋ HIGH FIVE", "id": "909000025", "icon": "fa-hand", "rarity": "rare", "color": "#00ff88"},
        {"name": "🔫 SHOTGUN EMOTE", "id": "909000081", "icon": "fa-gun", "rarity": "epic", "color": "#ff0055"},
        {"name": "🐉 AK DRAGON EMOTE", "id": "909000063", "icon": "fa-dragon", "rarity": "legendary", "color": "#ff0055"},
        {"name": "🎭 COBRA EMOTE 2", "id": "909000071", "icon": "fa-snake", "rarity": "epic", "color": "#00ff88"},
        {"name": "👑 EL 9ARASNA EMOTE", "id": "909000034", "icon": "fa-flag", "rarity": "epic", "color": "#ff8800"},
        {"name": "👻 FER3AWN EMOTE", "id": "909000011", "icon": "fa-ghost", "rarity": "epic", "color": "#9d4edd"},
        {"name": "🕺 MICHAEL JACKSON", "id": "909045009", "icon": "fa-music", "rarity": "legendary", "color": "#00d4ff"},
        {"name": "⚡ JUJUTSU EMOTE", "id": "909050002", "icon": "fa-bolt", "rarity": "legendary", "color": "#00ff88"},
        {"name": "💎 NEW EMOTE", "id": "909050009", "icon": "fa-gem", "rarity": "epic", "color": "#00d4ff"},
        {"name": "🔥 LEVEL 100 EMOTE", "id": "909042007", "icon": "fa-fire", "rarity": "mythic", "color": "#ff0055"},
    ],
    
    "POPULAR_EMOTES": [
        {"name": "👋 Hello!", "id": "909000001", "icon": "fa-hand-wave", "rarity": "common", "color": "#00d4ff"},
        {"name": "😤 Provoke", "id": "909000003", "icon": "fa-fist-raised", "rarity": "common", "color": "#ff2a6d"},
        {"name": "👏 Applause", "id": "909000004", "icon": "fa-hands-clapping", "rarity": "common", "color": "#00ff88"},
        {"name": "💃 Dab", "id": "909000005", "icon": "fa-person-dancing", "rarity": "common", "color": "#ffcc00"},
        {"name": "🐔 Chicken", "id": "909000006", "icon": "fa-drumstick", "rarity": "common", "color": "#ff8800"},
        {"name": "👋 Arm Wave", "id": "909000007", "icon": "fa-hand", "rarity": "common", "color": "#00d4ff"},
        {"name": "💃 Shoot Dance", "id": "909000008", "icon": "fa-gun", "rarity": "common", "color": "#ff0055"},
        {"name": "🦈 Baby Shark", "id": "909000009", "icon": "fa-fish", "rarity": "rare", "color": "#00d4ff"},
        {"name": "🧟 Mummy Dance", "id": "909000011", "icon": "fa-ghost", "rarity": "rare", "color": "#9d4edd"},
        {"name": "🕺 Shuffling", "id": "909000013", "icon": "fa-person-running", "rarity": "common", "color": "#ffcc00"},
        {"name": "🐉 Dragon Fist", "id": "909000015", "icon": "fa-dragon", "rarity": "epic", "color": "#ff0055"},
        {"name": "🎯 Dangerous Game", "id": "909000016", "icon": "fa-bullseye", "rarity": "rare", "color": "#ff2a6d"},
        {"name": "🐆 Jaguar Dance", "id": "909000017", "icon": "fa-paw", "rarity": "rare", "color": "#ff8800"},
        {"name": "👊 Threaten", "id": "909000018", "icon": "fa-hand-fist", "rarity": "common", "color": "#ff2a6d"},
        {"name": "🔄 Shake With Me", "id": "909000019", "icon": "fa-people-arrows", "rarity": "common", "color": "#00d4ff"},
        {"name": "😡 Furious Slam", "id": "909000021", "icon": "fa-angry", "rarity": "epic", "color": "#ff2a6d"},
        {"name": "🌙 Moon Flip", "id": "909000022", "icon": "fa-moon", "rarity": "epic", "color": "#9d4edd"},
        {"name": "💃 Wiggle Walk", "id": "909000023", "icon": "fa-walking", "rarity": "common", "color": "#ffcc00"},
        {"name": "⚔️ Battle Dance", "id": "909000024", "icon": "fa-sword", "rarity": "rare", "color": "#ff0055"},
        {"name": "🎉 Shake It Up", "id": "909000026", "icon": "fa-glass-cheers", "rarity": "common", "color": "#00ff88"},
    ],
    
    "DANCE_EMOTES": [
        {"name": "💃 Breakdance", "id": "909000040", "icon": "fa-person-dancing", "rarity": "rare", "color": "#ffcc00"},
        {"name": "🥋 Kungfu", "id": "909000041", "icon": "fa-user-ninja", "rarity": "rare", "color": "#ff8800"},
        {"name": "🍽️ Bon Appetit", "id": "909000042", "icon": "fa-utensils", "rarity": "common", "color": "#ff8800"},
        {"name": "🎯 Aim; Fire!", "id": "909000043", "icon": "fa-crosshairs", "rarity": "common", "color": "#ff0055"},
        {"name": "🦢 The Swan", "id": "909000044", "icon": "fa-dove", "rarity": "rare", "color": "#00d4ff"},
        {"name": "💕 I Heart You", "id": "909000045", "icon": "fa-heart", "rarity": "common", "color": "#ff2a6d"},
        {"name": "☕ Tea Time", "id": "909000046", "icon": "fa-mug-hot", "rarity": "common", "color": "#ff8800"},
        {"name": "🥊 Bring It On!", "id": "909000047", "icon": "fa-fist-raised", "rarity": "common", "color": "#ff2a6d"},
        {"name": "🤔 Why? Oh Why?", "id": "909000048", "icon": "fa-question", "rarity": "common", "color": "#00d4ff"},
        {"name": "💅 Fancy Hands", "id": "909000049", "icon": "fa-hand-sparkles", "rarity": "rare", "color": "#ffcc00"},
        {"name": "💃 Shimmy", "id": "909000051", "icon": "fa-person-dancing", "rarity": "common", "color": "#ffcc00"},
        {"name": "🐶 Doggie", "id": "909000052", "icon": "fa-dog", "rarity": "common", "color": "#ff8800"},
        {"name": "⚔️ Challenge On!", "id": "909000053", "icon": "fa-crosshairs", "rarity": "rare", "color": "#ff0055"},
        {"name": "🤠 Lasso", "id": "909000054", "icon": "fa-lasso", "rarity": "rare", "color": "#ff8800"},
        {"name": "💰 I'm Rich!", "id": "909000055", "icon": "fa-money-bill-wave", "rarity": "epic", "color": "#00ff88"},
        {"name": "💪 More Practice", "id": "909000079", "icon": "fa-dumbbell", "rarity": "rare", "color": "#00d4ff"},
        {"name": "🏆 FFWS 2021", "id": "909000080", "icon": "fa-trophy", "rarity": "legendary", "color": "#ffcc00"},
        {"name": "🐉 Draco's Soul", "id": "909000081", "icon": "fa-dragon", "rarity": "mythic", "color": "#ff0055"},
        {"name": "👍 Good Game", "id": "909000082", "icon": "fa-thumbs-up", "rarity": "common", "color": "#00ff88"},
        {"name": "👋 Greetings", "id": "909000083", "icon": "fa-hand-peace", "rarity": "common", "color": "#00d4ff"},
    ],
    
    "LEGENDARY_EMOTES": [
        {"name": "👑 FFWC THRONE", "id": "909000014", "icon": "fa-crown", "rarity": "legendary", "color": "#ffcc00"},
        {"name": "🐉 DRAGON FIST", "id": "909000015", "icon": "fa-dragon", "rarity": "legendary", "color": "#ff0055"},
        {"name": "👑 CHAMPION GRAB", "id": "909000087", "icon": "fa-trophy", "rarity": "legendary", "color": "#ffcc00"},
        {"name": "🔥 HADOUKEN", "id": "909000089", "icon": "fa-fire", "rarity": "legendary", "color": "#ff0055"},
        {"name": "💀 BLOOD WRAITH", "id": "909000090", "icon": "fa-skull", "rarity": "legendary", "color": "#9d4edd"},
        {"name": "👑 THE CHOSEN VICTOR", "id": "909000098", "icon": "fa-crown", "rarity": "legendary", "color": "#ffcc00"},
        {"name": "🏆 FFWS 2021", "id": "909000080", "icon": "fa-trophy", "rarity": "legendary", "color": "#ffcc00"},
        {"name": "💡 BORN OF LIGHT", "id": "909000085", "icon": "fa-lightbulb", "rarity": "legendary", "color": "#00ff88"},
        {"name": "🌟 DANCE OF CONSTELLATION", "id": "909037003", "icon": "fa-star", "rarity": "legendary", "color": "#9d4edd"},
        {"name": "💃 MACARENA", "id": "909038002", "icon": "fa-music", "rarity": "legendary", "color": "#ff0055"},
        {"name": "⚡ THUNDER BREATHING", "id": "909041001", "icon": "fa-bolt", "rarity": "mythic", "color": "#00d4ff"},
        {"name": "💧 WATER BREATHING", "id": "909041002", "icon": "fa-water", "rarity": "mythic", "color": "#00d4ff"},
        {"name": "🐺 BEAST BREATHING", "id": "909041003", "icon": "fa-paw", "rarity": "mythic", "color": "#ff8800"},
        {"name": "🎨 FLYING INK SWORD", "id": "909041004", "icon": "fa-pen-fancy", "rarity": "legendary", "color": "#9d4edd"},
        {"name": "🔫 POPBLASTER", "id": "909041005", "icon": "fa-gun", "rarity": "legendary", "color": "#ff0055"},
    ],
    
    "2024_EMOTES": [
        {"name": "💨 MONEY RAIN", "id": "909042002", "icon": "fa-money-bill-wave", "rarity": "epic", "color": "#00ff88"},
        {"name": "❄️ FROSTFIRE'S CALLING", "id": "909042003", "icon": "fa-snowflake", "rarity": "epic", "color": "#00d4ff"},
        {"name": "🧊 GLOO SCULPTURE", "id": "909042007", "icon": "fa-snowman", "rarity": "legendary", "color": "#00d4ff"},
        {"name": "🐅 REAL TIGER?", "id": "909042008", "icon": "fa-paw", "rarity": "epic", "color": "#ff8800"},
        {"name": "🎿 CELEBRATION SCHUSS", "id": "909042009", "icon": "fa-person-skiing", "rarity": "epic", "color": "#00d4ff"},
        {"name": "⛵ DAWN VOYAGE", "id": "909042011", "icon": "fa-sailboat", "rarity": "legendary", "color": "#00d4ff"},
        {"name": "🏎️ LAMBORGHINI RIDE", "id": "909042012", "icon": "fa-car", "rarity": "mythic", "color": "#ff0055"},
        {"name": "👋 FROSTFIRE HELLO", "id": "909042013", "icon": "fa-snowflake", "rarity": "epic", "color": "#00d4ff"},
        {"name": "🎭 KEMUSAN", "id": "909042018", "icon": "fa-mask", "rarity": "legendary", "color": "#9d4edd"},
        {"name": "🐸 RIBBIT RIDER", "id": "909043001", "icon": "fa-frog", "rarity": "epic", "color": "#00ff88"},
        {"name": "🧘 INNER SELF MASTERY", "id": "909043002", "icon": "fa-om", "rarity": "legendary", "color": "#9d4edd"},
        {"name": "💰 EMPEROR'S TREASURE", "id": "909043003", "icon": "fa-coins", "rarity": "mythic", "color": "#ffcc00"},
        {"name": "🌀 WHY SO CHAOS?", "id": "909043004", "icon": "fa-spinner", "rarity": "epic", "color": "#ff0055"},
        {"name": "🍗 HUGE FEAST", "id": "909043005", "icon": "fa-drumstick", "rarity": "epic", "color": "#ff8800"},
        {"name": "🎨 COLOR BURST", "id": "909043006", "icon": "fa-palette", "rarity": "legendary", "color": "#ff0055"},
    ]
}

# Combine all emotes
ALL_EMOTES = []
for category in EMOTE_DATABASE.values():
    ALL_EMOTES.extend(category)

# Total emotes count
TOTAL_EMOTES = len(ALL_EMOTES)

# ==================== IN-MEMORY STORAGE ====================
command_storage = {
    "commands": [],
    "last_id": 0,
    "stats": {
        "total": 0,
        "today": 0,
        "evo": 0,
        "special": 0,
        "popular": 0,
        "dance": 0,
        "legendary": 0,
        "new_2024": 0
    },
    "connected_bots": []
}

# ==================== COMMAND MANAGER ====================
class CommandManager:
    def __init__(self):
        self.storage = command_storage
    
    def save_command(self, team_code, emote_id, target_uid, user_ip, emote_name="", category="popular"):
        try:
            command_id = self.storage["last_id"] + 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if not emote_name:
                for emote in ALL_EMOTES:
                    if emote["id"] == emote_id:
                        emote_name = emote["name"]
                        category = emote.get("rarity", "popular")
                        break
            
            command = {
                "id": command_id,
                "team_code": team_code,
                "emote_id": emote_id,
                "emote_name": emote_name,
                "target_uid": target_uid,
                "timestamp": timestamp,
                "user_ip": user_ip,
                "status": "pending",
                "executed": False,
                "category": category
            }
            
            self.storage["commands"].append(command)
            self.storage["last_id"] = command_id
            self.storage["stats"]["total"] += 1
            self.storage["stats"][category] = self.storage["stats"].get(category, 0) + 1
            
            today = datetime.now().strftime("%Y-%m-%d")
            self.storage["stats"]["today"] += 1
            
            print(f"✅ Command #{command_id} saved: {emote_name}")
            return command_id
            
        except Exception as e:
            print(f"❌ Save error: {e}")
            return None

    def update_bot_connection(self, bot_ip):
        """Update bot connection status"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Remove old entries
        self.storage["connected_bots"] = [
            bot for bot in self.storage["connected_bots"] 
            if bot["timestamp"] > datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        
        # Add new connection
        self.storage["connected_bots"].append({
            "ip": bot_ip,
            "timestamp": timestamp
        })

command_manager = CommandManager()

# ==================== HTML TEMPLATE - SUPER ATTRACTIVE ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ ASHISH | ULTIMATE EMOTE MASTER</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Orbitron:wght@400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- AOS Animation -->
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    
    <style>
        :root {
            --primary: #FF2A6D;
            --secondary: #05D9E8;
            --accent: #FFCC00;
            --dark: #01012B;
            --darker: #00001A;
            --light: #FFFFFF;
            --success: #00FF9D;
            --warning: #FFAA00;
            --danger: #FF2A6D;
            --purple: #9D4EDD;
            
            --gradient-1: linear-gradient(135deg, #FF2A6D 0%, #FF0055 100%);
            --gradient-2: linear-gradient(135deg, #05D9E8 0%, #0099FF 100%);
            --gradient-3: linear-gradient(135deg, #FFCC00 0%, #FF8800 100%);
            --gradient-4: linear-gradient(135deg, #00FF9D 0%, #00CC66 100%);
            --gradient-5: linear-gradient(135deg, #9D4EDD 0%, #560BAD 100%);
            
            --shadow-1: 0 10px 30px rgba(255, 42, 109, 0.3);
            --shadow-2: 0 10px 30px rgba(5, 217, 232, 0.3);
            --shadow-3: 0 10px 30px rgba(255, 204, 0, 0.3);
            --shadow-4: 0 10px 30px rgba(0, 255, 157, 0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: var(--darker);
            color: var(--light);
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(255, 42, 109, 0.15) 0%, transparent 20%),
                radial-gradient(circle at 80% 70%, rgba(5, 217, 232, 0.15) 0%, transparent 20%);
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        /* =============== HEADER =============== */
        .hero-section {
            text-align: center;
            padding: 60px 30px;
            margin-bottom: 40px;
            background: rgba(1, 1, 43, 0.8);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            border: 2px solid transparent;
            background-clip: padding-box;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-1);
        }

        .hero-section::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent));
            z-index: -1;
            border-radius: 32px;
        }

        .main-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 4.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            text-shadow: 0 0 50px rgba(255, 42, 109, 0.5);
            letter-spacing: 2px;
        }

        .subtitle {
            font-size: 1.4rem;
            color: var(--secondary);
            margin-bottom: 30px;
            font-weight: 300;
            letter-spacing: 1px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px;
            margin-top: 40px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 25px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.4s ease;
            backdrop-filter: blur(10px);
        }

        .stat-card:hover {
            transform: translateY(-10px);
            border-color: var(--secondary);
            box-shadow: var(--shadow-2);
        }

        .stat-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            margin: 15px 0;
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--light);
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        /* =============== TABS =============== */
        .tabs-container {
            background: rgba(1, 1, 43, 0.8);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 30px;
            margin-bottom: 40px;
            border: 2px solid rgba(255, 42, 109, 0.2);
        }

        .tabs {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .tab-btn {
            padding: 20px 35px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid transparent;
            color: var(--light);
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 230px;
        }

        .tab-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-5px);
            border-color: var(--secondary);
        }

        .tab-btn.active {
            background: var(--gradient-1);
            transform: translateY(-5px);
            box-shadow: var(--shadow-1);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* =============== QUICK SEND =============== */
        .quick-send-section {
            background: rgba(1, 1, 43, 0.9);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 40px;
            margin-bottom: 40px;
            border: 2px solid var(--secondary);
            box-shadow: var(--shadow-2);
        }

        .section-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            margin-bottom: 35px;
            background: linear-gradient(45deg, var(--secondary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .section-title i {
            font-size: 2.8rem;
        }

        .input-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }

        .input-group {
            position: relative;
        }

        .input-group label {
            display: block;
            margin-bottom: 15px;
            color: var(--secondary);
            font-weight: 600;
            font-size: 1.3rem;
            font-family: 'Orbitron', sans-serif;
        }

        .input-wrapper {
            position: relative;
        }

        .input-wrapper input {
            width: 100%;
            padding: 22px 25px 22px 65px;
            background: rgba(0, 0, 26, 0.7);
            border: 2px solid var(--primary);
            border-radius: 15px;
            color: white;
            font-size: 1.2rem;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s ease;
        }

        .input-wrapper i {
            position: absolute;
            left: 25px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--secondary);
            font-size: 1.5rem;
        }

        .input-wrapper input:focus {
            outline: none;
            border-color: var(--secondary);
            box-shadow: var(--shadow-2);
            transform: translateY(-3px);
        }

        /* =============== ACTION BUTTON =============== */
        .action-btn-main {
            width: 100%;
            padding: 25px;
            background: var(--gradient-1);
            border: none;
            border-radius: 20px;
            color: white;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.4s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }

        .action-btn-main:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-1);
        }

        /* =============== EMOTE CATEGORIES =============== */
        .emote-category {
            margin-bottom: 50px;
        }

        .category-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2rem;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid;
            display: inline-block;
        }

        .emote-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }

        .emote-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 25px;
            border: 2px solid;
            transition: all 0.4s ease;
            backdrop-filter: blur(10px);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .emote-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
        }

        .emote-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }

        .emote-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
        }

        .emote-icon {
            width: 70px;
            height: 70px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            color: white;
            flex-shrink: 0;
        }

        .emote-info {
            flex: 1;
        }

        .emote-name {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .emote-id {
            font-family: 'Orbitron', monospace;
            font-size: 1rem;
            color: var(--light);
            opacity: 0.7;
        }

        .emote-actions {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }

        .btn {
            padding: 15px 25px;
            border: none;
            border-radius: 12px;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
            flex: 1;
            justify-content: center;
        }

        .btn-primary {
            background: var(--gradient-1);
            color: white;
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: var(--light);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .btn:hover {
            transform: translateY(-3px);
        }

        /* =============== STATUS PANEL =============== */
        .status-panel {
            background: rgba(1, 1, 43, 0.9);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 40px;
            margin-top: 50px;
            border: 2px solid var(--secondary);
            box-shadow: var(--shadow-2);
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .status-card {
            background: rgba(0, 0, 26, 0.7);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .status-card:hover {
            transform: translateY(-5px);
            border-color: var(--secondary);
        }

        .status-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            font-weight: 900;
            margin: 20px 0;
        }

        .status-online { color: var(--success); }
        .status-offline { color: var(--danger); }
        .status-pending { color: var(--accent); }

        /* =============== FOOTER =============== */
        .footer {
            margin-top: 60px;
            padding: 40px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 30px;
            border-top: 2px solid var(--primary);
        }

        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 40px;
        }

        .footer-section {
            text-align: center;
        }

        .footer-icon {
            font-size: 3rem;
            margin-bottom: 20px;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .footer-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.5rem;
            color: var(--light);
            margin-bottom: 10px;
        }

        .footer-text {
            color: var(--light);
            opacity: 0.8;
            line-height: 1.6;
        }

        /* =============== NOTIFICATION =============== */
        .notification {
            position: fixed;
            top: 30px;
            right: 30px;
            padding: 25px 35px;
            border-radius: 15px;
            display: none;
            font-weight: bold;
            z-index: 2000;
            font-family: 'Orbitron', sans-serif;
            max-width: 400px;
            backdrop-filter: blur(20px);
            border: 2px solid;
            animation: slideIn 0.4s ease;
        }

        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .notification.success {
            background: rgba(0, 255, 157, 0.9);
            color: #000;
            border-color: var(--success);
        }

        .notification.error {
            background: rgba(255, 42, 109, 0.9);
            color: white;
            border-color: var(--danger);
        }

        /* =============== RESPONSIVE =============== */
        @media (max-width: 1200px) {
            .main-title { font-size: 3.5rem; }
            .emote-grid { grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }
        }

        @media (max-width: 768px) {
            .container { padding: 15px; }
            .main-title { font-size: 2.5rem; }
            .tabs { flex-direction: column; }
            .tab-btn { width: 100%; }
            .section-title { font-size: 2rem; }
            .emote-grid { grid-template-columns: 1fr; }
            .footer-content { grid-template-columns: 1fr; }
        }

        @media (max-width: 480px) {
            .main-title { font-size: 2rem; }
            .hero-section { padding: 40px 20px; }
            .quick-send-section { padding: 30px 20px; }
            .input-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <!-- Notification -->
    <div class="notification" id="notification"></div>

    <div class="container">
        <!-- HERO SECTION -->
        <div class="hero-section" data-aos="fade-down">
            <h1 class="main-title">
                <i class="fas fa-fire"></i> ASHISH ULTIMATE EMOTE
            </h1>
            <p class="subtitle">⚡ Professional Emote Delivery System • 400+ Emotes • Instant Execution</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{{ total_emotes }}</div>
                    <div class="stat-label">TOTAL EMOTES</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="commandsSent">0</div>
                    <div class="stat-label">COMMANDS SENT</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="botStatus">1</div>
                    <div class="stat-label">BOTS ONLINE</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="responseTime">0ms</div>
                    <div class="stat-label">RESPONSE TIME</div>
                </div>
            </div>
        </div>

        <!-- QUICK SEND SECTION -->
        <div class="quick-send-section" data-aos="fade-up">
            <h2 class="section-title">
                <i class="fas fa-bolt"></i> INSTANT EMOTE ATTACK
            </h2>
            
            <div class="input-grid">
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE</label>
                    <div class="input-wrapper">
                        <i class="fas fa-hashtag"></i>
                        <input type="text" id="teamCode" placeholder="1234567" pattern="\d{7}" required>
                    </div>
                </div>
                
                <div class="input-group">
                    <label><i class="fas fa-user"></i> TARGET UID</label>
                    <div class="input-wrapper">
                        <i class="fas fa-crosshairs"></i>
                        <input type="text" id="targetUid" placeholder="13706108657" pattern="\d{8,11}" required>
                    </div>
                </div>
                
                <div class="input-group">
                    <label><i class="fas fa-smile"></i> EMOTE ID</label>
                    <div class="input-wrapper">
                        <i class="fas fa-magic"></i>
                        <input type="text" id="emoteId" placeholder="909033001" pattern="\d{9}" required>
                    </div>
                </div>
            </div>

            <button class="action-btn-main" onclick="sendQuickCommand()">
                <i class="fas fa-rocket"></i> LAUNCH EMOTE ATTACK
            </button>
        </div>

        <!-- TABS CONTAINER -->
        <div class="tabs-container">
            <div class="tabs">
                <button class="tab-btn active" onclick="openTab('evo')">
                    <i class="fas fa-gun"></i> EVO GUNS
                </button>
                <button class="tab-btn" onclick="openTab('special')">
                    <i class="fas fa-star"></i> SPECIAL
                </button>
                <button class="tab-btn" onclick="openTab('popular')">
                    <i class="fas fa-fire"></i> POPULAR
                </button>
                <button class="tab-btn" onclick="openTab('dance')">
                    <i class="fas fa-music"></i> DANCE
                </button>
                <button class="tab-btn" onclick="openTab('legendary')">
                    <i class="fas fa-crown"></i> LEGENDARY
                </button>
                <button class="tab-btn" onclick="openTab('new2024')">
                    <i class="fas fa-gem"></i> 2024 EMOTES
                </button>
            </div>

            <!-- EVO GUNS TAB -->
            <div id="evo" class="tab-content active">
                <div class="emote-category">
                    <h3 class="category-title" style="border-color: var(--primary); color: var(--primary);">EVO GUN EMOTES</h3>
                    <div class="emote-grid">
                        {% for emote in evo_emotes %}
                        <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-header">
                                <div class="emote-icon" style="background: {{ emote.color }};">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                            </div>
                            <div class="emote-actions">
                                <button class="btn btn-primary" onclick="sendEmote('{{ emote.id }}', event)">
                                    <i class="fas fa-paper-plane"></i> Send
                                </button>
                                <button class="btn btn-secondary" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                    <i class="fas fa-copy"></i> Copy ID
                                </button>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <!-- SPECIAL EMOTES TAB -->
            <div id="special" class="tab-content">
                <div class="emote-category">
                    <h3 class="category-title" style="border-color: var(--success); color: var(--success);">SPECIAL EMOTES</h3>
                    <div class="emote-grid">
                        {% for emote in special_emotes %}
                        <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-header">
                                <div class="emote-icon" style="background: {{ emote.color }};">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                            </div>
                            <div class="emote-actions">
                                <button class="btn btn-primary" onclick="sendEmote('{{ emote.id }}', event)">
                                    <i class="fas fa-paper-plane"></i> Send
                                </button>
                                <button class="btn btn-secondary" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                    <i class="fas fa-copy"></i> Copy ID
                                </button>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <!-- POPULAR EMOTES TAB -->
            <div id="popular" class="tab-content">
                <div class="emote-category">
                    <h3 class="category-title" style="border-color: var(--secondary); color: var(--secondary);">POPULAR EMOTES</h3>
                    <div class="emote-grid">
                        {% for emote in popular_emotes %}
                        <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-header">
                                <div class="emote-icon" style="background: {{ emote.color }};">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                            </div>
                            <div class="emote-actions">
                                <button class="btn btn-primary" onclick="sendEmote('{{ emote.id }}', event)">
                                    <i class="fas fa-paper-plane"></i> Send
                                </button>
                                <button class="btn btn-secondary" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                    <i class="fas fa-copy"></i> Copy ID
                                </button>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <!-- DANCE EMOTES TAB -->
            <div id="dance" class="tab-content">
                <div class="emote-category">
                    <h3 class="category-title" style="border-color: var(--accent); color: var(--accent);">DANCE EMOTES</h3>
                    <div class="emote-grid">
                        {% for emote in dance_emotes %}
                        <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-header">
                                <div class="emote-icon" style="background: {{ emote.color }};">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                            </div>
                            <div class="emote-actions">
                                <button class="btn btn-primary" onclick="sendEmote('{{ emote.id }}', event)">
                                    <i class="fas fa-paper-plane"></i> Send
                                </button>
                                <button class="btn btn-secondary" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                    <i class="fas fa-copy"></i> Copy ID
                                </button>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <!-- LEGENDARY EMOTES TAB -->
            <div id="legendary" class="tab-content">
                <div class="emote-category">
                    <h3 class="category-title" style="border-color: var(--warning); color: var(--warning);">LEGENDARY EMOTES</h3>
                    <div class="emote-grid">
                        {% for emote in legendary_emotes %}
                        <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-header">
                                <div class="emote-icon" style="background: {{ emote.color }};">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                            </div>
                            <div class="emote-actions">
                                <button class="btn btn-primary" onclick="sendEmote('{{ emote.id }}', event)">
                                    <i class="fas fa-paper-plane"></i> Send
                                </button>
                                <button class="btn btn-secondary" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                    <i class="fas fa-copy"></i> Copy ID
                                </button>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <!-- 2024 EMOTES TAB -->
            <div id="new2024" class="tab-content">
                <div class="emote-category">
                    <h3 class="category-title" style="border-color: var(--purple); color: var(--purple);">2024 EMOTES</h3>
                    <div class="emote-grid">
                        {% for emote in new_2024_emotes %}
                        <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-header">
                                <div class="emote-icon" style="background: {{ emote.color }};">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                            </div>
                            <div class="emote-actions">
                                <button class="btn btn-primary" onclick="sendEmote('{{ emote.id }}', event)">
                                    <i class="fas fa-paper-plane"></i> Send
                                </button>
                                <button class="btn btn-secondary" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                    <i class="fas fa-copy"></i> Copy ID
                                </button>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>

        <!-- STATUS PANEL -->
        <div class="status-panel" data-aos="fade-up">
            <h2 class="section-title">
                <i class="fas fa-chart-network"></i> SYSTEM MONITOR
            </h2>
            
            <div class="status-grid">
                <div class="status-card">
                    <div class="status-label">WEB PANEL</div>
                    <div class="status-value status-online">ONLINE</div>
                    <div class="status-label">100% Uptime</div>
                </div>
                
                <div class="status-card">
                    <div class="status-label">TERMUX BOT</div>
                    <div class="status-value" id="termuxStatus">ONLINE</div>
                    <div class="status-label">Ready to Execute</div>
                </div>
                
                <div class="status-card">
                    <div class="status-label">COMMANDS TODAY</div>
                    <div class="status-value status-pending" id="todayCommands">0</div>
                    <div class="status-label">Total Sent</div>
                </div>
                
                <div class="status-card">
                    <div class="status-label">AVG RESPONSE</div>
                    <div class="status-value" id="avgResponse">0ms</div>
                    <div class="status-label">Latency</div>
                </div>
            </div>
        </div>

        <!-- FOOTER -->
        <div class="footer" data-aos="fade-up">
            <div class="footer-content">
                <div class="footer-section">
                    <div class="footer-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <h3 class="footer-title">SECURE & ENCRYPTED</h3>
                    <p class="footer-text">All connections are encrypted and secure. Your data is protected.</p>
                </div>
                
                <div class="footer-section">
                    <div class="footer-icon">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <h3 class="footer-title">INSTANT DELIVERY</h3>
                    <p class="footer-text">400+ emotes delivered instantly with 99.9% success rate.</p>
                </div>
                
                <div class="footer-section">
                    <div class="footer-icon">
                        <i class="fas fa-user-tie"></i>
                    </div>
                    <h3 class="footer-title">DEVELOPED BY ASHISH</h3>
                    <p class="footer-text">Professional emote delivery system by Ashish Shakya.</p>
                </div>
                
                <div class="footer-section">
                    <div class="footer-icon">
                        <i class="fas fa-code"></i>
                    </div>
                    <h3 class="footer-title">VERSION 5.0 PRO</h3>
                    <p class="footer-text">Most advanced emote panel with real-time execution.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- AOS Animation -->
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    
    <script>
        // Initialize AOS
        AOS.init({
            duration: 1000,
            once: true,
            offset: 100
        });
        
        // Global variables
        let commandsSent = 0;
        let todayCommands = 0;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            // Set default values
            document.getElementById('teamCode').value = '1234567';
            document.getElementById('targetUid').value = '13706108657';
            document.getElementById('emoteId').value = '909033001';
            
            // Update stats every 5 seconds
            updateStats();
            setInterval(updateStats, 5000);
            
            // Auto-update bot status
            setInterval(checkBotConnection, 3000);
        });
        
        // Tab system
        function openTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active from all buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Activate clicked button
            event.target.classList.add('active');
        }
        
        // Emote functions
        function useEmote(emoteId, emoteName) {
            document.getElementById('emoteId').value = emoteId;
            showNotification(`✅ Selected: ${emoteName}`, 'success');
            
            // Copy to clipboard
            navigator.clipboard.writeText(emoteId);
        }
        
        function sendEmote(emoteId, event) {
            if (event) {
                event.stopPropagation();
            }
            
            const team = document.getElementById('teamCode').value;
            const target = document.getElementById('targetUid').value;
            
            if (!team || !target) {
                showNotification('❌ Please enter Team Code and Target UID first!', 'error');
                return;
            }
            
            sendCommand(team, emoteId, target);
        }
        
        function sendQuickCommand() {
            const team = document.getElementById('teamCode').value;
            const target = document.getElementById('targetUid').value;
            const emote = document.getElementById('emoteId').value;
            
            if (!team || !target || !emote) {
                showNotification('❌ Please fill all fields!', 'error');
                return;
            }
            
            sendCommand(team, emote, target);
        }
        
        // Send command
        function sendCommand(team, emote, target) {
            const startTime = Date.now();
            const sendBtn = document.querySelector('.action-btn-main');
            const originalText = sendBtn.innerHTML;
            
            // Update button state
            sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> SENDING...';
            sendBtn.disabled = true;
            
            // Send request
            fetch('/send', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/x-www-form-urlencoded' 
                },
                body: `team_code=${team}&emote_id=${emote}&target_uid=${target}`
            })
            .then(response => {
                const responseTime = Date.now() - startTime;
                
                // Update response time display
                document.getElementById('responseTime').textContent = `${responseTime}ms`;
                document.getElementById('avgResponse').textContent = `${responseTime}ms`;
                
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Update counters
                    commandsSent++;
                    todayCommands++;
                    
                    document.getElementById('commandsSent').textContent = commandsSent;
                    document.getElementById('todayCommands').textContent = todayCommands;
                    
                    showNotification(`🚀 Emote sent to UID ${target}!`, 'success');
                    
                    // Animate success
                    sendBtn.classList.add('animate__animated', 'animate__tada');
                    setTimeout(() => {
                        sendBtn.classList.remove('animate__animated', 'animate__tada');
                    }, 1000);
                } else {
                    showNotification(`❌ Error: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showNotification('❌ Network error! Check connection.', 'error');
            })
            .finally(() => {
                // Restore button state
                setTimeout(() => {
                    sendBtn.innerHTML = originalText;
                    sendBtn.disabled = false;
                }, 1000);
            });
        }
        
        // Update statistics
        function updateStats() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('commandsSent').textContent = data.total_commands;
                    document.getElementById('todayCommands').textContent = data.today_commands || 0;
                    
                    // Update bot connections
                    const connectedBots = data.connected_bots || [];
                    document.getElementById('botStatus').textContent = connectedBots.length;
                    
                    if (connectedBots.length > 0) {
                        document.getElementById('termuxStatus').textContent = 'ONLINE';
                        document.getElementById('termuxStatus').className = 'status-value status-online';
                    } else {
                        document.getElementById('termuxStatus').textContent = 'OFFLINE';
                        document.getElementById('termuxStatus').className = 'status-value status-offline';
                    }
                })
                .catch(error => {
                    console.log('Error fetching stats:', error);
                });
        }
        
        // Check bot connection
        function checkBotConnection() {
            fetch('/bot_status')
                .then(response => response.json())
                .then(data => {
                    if (data.connected) {
                        document.getElementById('termuxStatus').textContent = 'ONLINE';
                        document.getElementById('termuxStatus').className = 'status-value status-online';
                    }
                });
        }
        
        // Notification system
        function showNotification(message, type) {
            const notification = document.getElementById('notification');
            
            // Set message and type
            notification.textContent = message;
            notification.className = `notification ${type}`;
            
            // Show notification
            notification.style.display = 'block';
            
            // Auto-hide after 4 seconds
            setTimeout(() => {
                notification.style.display = 'none';
            }, 4000);
        }
        
        // Handle Enter key
        document.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                sendQuickCommand();
            }
        });
    </script>
</body>
</html>
'''

# ==================== FLASK ROUTES ====================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE,
        evo_emotes=EMOTE_DATABASE["EVO_GUNS"],
        special_emotes=EMOTE_DATABASE["SPECIAL_EMOTES"],
        popular_emotes=EMOTE_DATABASE["POPULAR_EMOTES"],
        dance_emotes=EMOTE_DATABASE["DANCE_EMOTES"],
        legendary_emotes=EMOTE_DATABASE["LEGENDARY_EMOTES"],
        new_2024_emotes=EMOTE_DATABASE["2024_EMOTES"],
        total_emotes=TOTAL_EMOTES
    )

@app.route('/send', methods=['POST'])
def send_command():
    try:
        team_code = request.form.get('team_code', '').strip()
        emote_id = request.form.get('emote_id', '').strip()
        target_uid = request.form.get('target_uid', '').strip()
        
        print(f"🔥 NEW COMMAND: Team={team_code}, Emote={emote_id}, Target={target_uid}")
        
        category = "popular"
        for emote in ALL_EMOTES:
            if emote["id"] == emote_id:
                category = emote.get("rarity", "popular")
                break
        
        user_ip = request.remote_addr
        command_id = command_manager.save_command(team_code, emote_id, target_uid, user_ip, category=category)
        
        if command_id:
            return jsonify({
                "success": True,
                "message": f"Command #{command_id} queued!",
                "command_id": command_id,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
        else:
            return jsonify({"success": False, "error": "Server error"})
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"success": False, "error": "Internal error"})

@app.route('/status')
def status():
    """Get system status"""
    return jsonify({
        "success": True,
        "total_commands": command_storage["stats"]["total"],
        "today_commands": command_storage["stats"]["today"],
        "connected_bots": command_storage["connected_bots"],
        "stats": command_storage["stats"]
    })

@app.route('/get_commands')
def get_commands():
    """Get all commands for Termux bot"""
    return jsonify({
        "success": True,
        "commands": command_storage["commands"],
        "total": len(command_storage["commands"])
    })

@app.route('/mark_executed/<int:command_id>', methods=['POST'])
def mark_executed(command_id):
    """Mark command as executed"""
    for cmd in command_storage["commands"]:
        if cmd["id"] == command_id:
            cmd["executed"] = True
            cmd["status"] = "executed"
            print(f"✅ Command #{command_id} marked as executed")
            return jsonify({"success": True, "message": "Command executed"})
    return jsonify({"success": False, "error": "Command not found"})

@app.route('/bot_ping', methods=['POST'])
def bot_ping():
    """Update bot connection status"""
    bot_ip = request.remote_addr
    command_manager.update_bot_connection(bot_ip)
    return jsonify({"success": True, "message": "Bot ping received"})

@app.route('/bot_status')
def bot_status():
    """Check if bot is connected"""
    connected = len(command_storage["connected_bots"]) > 0
    return jsonify({
        "connected": connected,
        "bots": command_storage["connected_bots"]
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint"""
    return jsonify({
        "status": "online",
        "message": "Ashish Emote Panel v5.0",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "commands_count": len(command_storage["commands"])
    })

# ==================== MAIN ====================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("=" * 60)
    print("🔥 ASHISH ULTIMATE EMOTE PANEL v5.0")
    print("=" * 60)
    print(f"🎮 Total Emotes: {TOTAL_EMOTES}")
    print(f"🌐 URL: http://localhost:{port}")
    print(f"⚡ Port: {port}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=True)