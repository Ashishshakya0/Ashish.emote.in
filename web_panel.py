from flask import Flask, render_template_string, request, jsonify, send_from_directory
from datetime import datetime, timedelta
import json
import os
import random

app = Flask(__name__)
app.secret_key = 'ashish-premium-panel-2024-secret'

# ==================== EMOTE DATABASE ====================
EMOTE_DATABASE = {
    "EVO_GUNS": [
        {"name": "🔥 EVO MP40", "id": "909000075", "icon": "fa-gun", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🔥 EVO AK", "id": "909000063", "icon": "fa-gun", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🔥 EVO UMP", "id": "909000098", "icon": "fa-gun", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🔥 EVO XMB", "id": "909000065", "icon": "fa-gun", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🔥 EVO SCAR", "id": "909000068", "icon": "fa-gun", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🔥 EVO M10", "id": "909000081", "icon": "fa-gun", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🔥 EVO FAMAS", "id": "909000090", "icon": "fa-gun", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🔥 EVO MP5", "id": "909033002", "icon": "fa-gun", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🔥 EVO M1887", "id": "909035007", "icon": "fa-gun", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🔥 EVO WOODPECKER", "id": "909042008", "icon": "fa-gun", "rarity": "legendary", "color": "#00D4FF"},
    ],
    
    "SPECIAL_EMOTES": [
        {"name": "💰 PAISA EMOTE", "id": "909000055", "icon": "fa-money-bill-wave", "rarity": "epic", "color": "#FFCC00"},
        {"name": "💖 HEART EMOTE", "id": "909000045", "icon": "fa-heart", "rarity": "epic", "color": "#FF2A6D"},
        {"name": "🌹 ROSE EMOTE", "id": "909000010", "icon": "fa-rose", "rarity": "epic", "color": "#FF2A6D"},
        {"name": "👑 THRONE EMOTE", "id": "909000014", "icon": "fa-crown", "rarity": "legendary", "color": "#FFCC00"},
        {"name": "🏴‍☠️ PIRATE'S FLAG", "id": "909000034", "icon": "fa-flag", "rarity": "epic", "color": "#FF8800"},
        {"name": "💨 EAT MY DUST", "id": "909000039", "icon": "fa-wind", "rarity": "epic", "color": "#9D4EDD"},
        {"name": "😂 LOL EMOTE", "id": "909000002", "icon": "fa-laugh", "rarity": "rare", "color": "#00FF88"},
        {"name": "🐍 COBRA EMOTE", "id": "909000072", "icon": "fa-snake", "rarity": "legendary", "color": "#00FF88"},
        {"name": "👻 GHOST EMOTE", "id": "909036001", "icon": "fa-ghost", "rarity": "epic", "color": "#9D4EDD"},
        {"name": "🔥 FIRE ON EMOTE", "id": "909033001", "icon": "fa-fire", "rarity": "legendary", "color": "#FF0055"},
        {"name": "🎬 SHOLAY EMOTE", "id": "909050020", "icon": "fa-film", "rarity": "epic", "color": "#FF8800"},
        {"name": "⭐ PRIME 8 EMOTE", "id": "909035013", "icon": "fa-star", "rarity": "legendary", "color": "#FFCC00"},
        {"name": "💪 PUSH UP", "id": "909000012", "icon": "fa-dumbbell", "rarity": "rare", "color": "#00D4FF"},
        {"name": "😈 DEVIL'S MOVE", "id": "909000020", "icon": "fa-horn", "rarity": "epic", "color": "#9D4EDD"},
        {"name": "👑 EL 3ARCH EMOTE", "id": "909000014", "icon": "fa-throne", "rarity": "legendary", "color": "#FFCC00"},
        {"name": "✋ HIGH FIVE", "id": "909000025", "icon": "fa-hand", "rarity": "rare", "color": "#00FF88"},
        {"name": "🔫 SHOTGUN EMOTE", "id": "909000081", "icon": "fa-gun", "rarity": "epic", "color": "#00D4FF"},
        {"name": "🐉 AK DRAGON EMOTE", "id": "909000063", "icon": "fa-dragon", "rarity": "legendary", "color": "#FF0055"},
        {"name": "🎭 COBRA EMOTE 2", "id": "909000071", "icon": "fa-snake", "rarity": "epic", "color": "#00FF88"},
        {"name": "👑 EL 9ARASNA EMOTE", "id": "909000034", "icon": "fa-flag", "rarity": "epic", "color": "#FF8800"},
        {"name": "👻 FER3AWN EMOTE", "id": "909000011", "icon": "fa-ghost", "rarity": "epic", "color": "#9D4EDD"},
        {"name": "🕺 MICHAEL JACKSON", "id": "909045009", "icon": "fa-music", "rarity": "legendary", "color": "#FFCC00"},
        {"name": "⚡ JUJUTSU EMOTE", "id": "909050002", "icon": "fa-bolt", "rarity": "legendary", "color": "#00FF88"},
        {"name": "💎 NEW EMOTE", "id": "909050009", "icon": "fa-gem", "rarity": "epic", "color": "#00D4FF"},
        {"name": "🔥 LEVEL 100 EMOTE", "id": "909042007", "icon": "fa-fire", "rarity": "mythic", "color": "#FF0055"},
    ],
    
    "POPULAR_EMOTES": [
        {"name": "👋 Hello!", "id": "909000001", "icon": "fa-hand-wave", "rarity": "common", "color": "#00D4FF"},
        {"name": "😤 Provoke", "id": "909000003", "icon": "fa-fist-raised", "rarity": "common", "color": "#FF2A6D"},
        {"name": "👏 Applause", "id": "909000004", "icon": "fa-hands-clapping", "rarity": "common", "color": "#00FF88"},
        {"name": "💃 Dab", "id": "909000005", "icon": "fa-person-dancing", "rarity": "common", "color": "#FFCC00"},
        {"name": "🐔 Chicken", "id": "909000006", "icon": "fa-drumstick", "rarity": "common", "color": "#FF8800"},
        {"name": "👋 Arm Wave", "id": "909000007", "icon": "fa-hand", "rarity": "common", "color": "#00D4FF"},
        {"name": "💃 Shoot Dance", "id": "909000008", "icon": "fa-gun", "rarity": "common", "color": "#FF0055"},
        {"name": "🦈 Baby Shark", "id": "909000009", "icon": "fa-fish", "rarity": "rare", "color": "#00D4FF"},
        {"name": "🧟 Mummy Dance", "id": "909000011", "icon": "fa-ghost", "rarity": "rare", "color": "#9D4EDD"},
        {"name": "🕺 Shuffling", "id": "909000013", "icon": "fa-person-running", "rarity": "common", "color": "#FFCC00"},
        {"name": "🐉 Dragon Fist", "id": "909000015", "icon": "fa-dragon", "rarity": "epic", "color": "#FF0055"},
        {"name": "🎯 Dangerous Game", "id": "909000016", "icon": "fa-bullseye", "rarity": "rare", "color": "#FF2A6D"},
        {"name": "🐆 Jaguar Dance", "id": "909000017", "icon": "fa-paw", "rarity": "rare", "color": "#FF8800"},
        {"name": "👊 Threaten", "id": "909000018", "icon": "fa-hand-fist", "rarity": "common", "color": "#FF2A6D"},
        {"name": "🔄 Shake With Me", "id": "909000019", "icon": "fa-people-arrows", "rarity": "common", "color": "#00D4FF"},
        {"name": "😡 Furious Slam", "id": "909000021", "icon": "fa-angry", "rarity": "epic", "color": "#FF2A6D"},
        {"name": "🌙 Moon Flip", "id": "909000022", "icon": "fa-moon", "rarity": "epic", "color": "#9D4EDD"},
        {"name": "💃 Wiggle Walk", "id": "909000023", "icon": "fa-walking", "rarity": "common", "color": "#FFCC00"},
        {"name": "⚔️ Battle Dance", "id": "909000024", "icon": "fa-sword", "rarity": "rare", "color": "#FF0055"},
        {"name": "🎉 Shake It Up", "id": "909000026", "icon": "fa-glass-cheers", "rarity": "common", "color": "#00FF88"},
        {"name": "🌟 Glorious Spin", "id": "909000027", "icon": "fa-star", "rarity": "epic", "color": "#FFCC00"},
        {"name": "🦅 Crane Kick", "id": "909000028", "icon": "fa-dove", "rarity": "rare", "color": "#00D4FF"},
        {"name": "🎉 Party Dance", "id": "909000029", "icon": "fa-champagne-glasses", "rarity": "common", "color": "#FF0055"},
        {"name": "💃 Jig Dance", "id": "909000031", "icon": "fa-music", "rarity": "common", "color": "#9D4EDD"},
        {"name": "📸 Selfie", "id": "909000032", "icon": "fa-camera", "rarity": "common", "color": "#00D4FF"},
        {"name": "👻 Soul Shaking", "id": "909000033", "icon": "fa-ghost", "rarity": "epic", "color": "#9D4EDD"},
        {"name": "💕 Healing Dance", "id": "909000035", "icon": "fa-heart-pulse", "rarity": "rare", "color": "#FF2A6D"},
        {"name": "🎧 Top DJ", "id": "909000036", "icon": "fa-headphones", "rarity": "epic", "color": "#00D4FF"},
        {"name": "😠 Death Glare", "id": "909000037", "icon": "fa-eye", "rarity": "epic", "color": "#FF0055"},
        {"name": "💰 Power of Money", "id": "909000038", "icon": "fa-money-bill", "rarity": "epic", "color": "#FFCC00"},
    ],
    
    "DANCE_EMOTES": [
        {"name": "💃 Breakdance", "id": "909000040", "icon": "fa-person-dancing", "rarity": "rare", "color": "#FFCC00"},
        {"name": "🥋 Kungfu", "id": "909000041", "icon": "fa-user-ninja", "rarity": "rare", "color": "#FF8800"},
        {"name": "🍽️ Bon Appetit", "id": "909000042", "icon": "fa-utensils", "rarity": "common", "color": "#FF8800"},
        {"name": "🎯 Aim; Fire!", "id": "909000043", "icon": "fa-crosshairs", "rarity": "common", "color": "#FF0055"},
        {"name": "🦢 The Swan", "id": "909000044", "icon": "fa-dove", "rarity": "rare", "color": "#00D4FF"},
        {"name": "💕 I Heart You", "id": "909000045", "icon": "fa-heart", "rarity": "common", "color": "#FF2A6D"},
        {"name": "☕ Tea Time", "id": "909000046", "icon": "fa-mug-hot", "rarity": "common", "color": "#FF8800"},
        {"name": "🥊 Bring It On!", "id": "909000047", "icon": "fa-fist-raised", "rarity": "common", "color": "#FF2A6D"},
        {"name": "🤔 Why? Oh Why?", "id": "909000048", "icon": "fa-question", "rarity": "common", "color": "#00D4FF"},
        {"name": "💅 Fancy Hands", "id": "909000049", "icon": "fa-hand-sparkles", "rarity": "rare", "color": "#FFCC00"},
        {"name": "💃 Shimmy", "id": "909000051", "icon": "fa-person-dancing", "rarity": "common", "color": "#FFCC00"},
        {"name": "🐶 Doggie", "id": "909000052", "icon": "fa-dog", "rarity": "common", "color": "#FF8800"},
        {"name": "⚔️ Challenge On!", "id": "909000053", "icon": "fa-crosshairs", "rarity": "rare", "color": "#FF0055"},
        {"name": "🤠 Lasso", "id": "909000054", "icon": "fa-lasso", "rarity": "rare", "color": "#FF8800"},
        {"name": "💰 I'm Rich!", "id": "909000055", "icon": "fa-money-bill-wave", "rarity": "epic", "color": "#FFCC00"},
        {"name": "💪 More Practice", "id": "909000079", "icon": "fa-dumbbell", "rarity": "rare", "color": "#00D4FF"},
        {"name": "🏆 FFWS 2021", "id": "909000080", "icon": "fa-trophy", "rarity": "legendary", "color": "#FFCC00"},
        {"name": "🐉 Draco's Soul", "id": "909000081", "icon": "fa-dragon", "rarity": "mythic", "color": "#FF0055"},
        {"name": "👍 Good Game", "id": "909000082", "icon": "fa-thumbs-up", "rarity": "common", "color": "#00FF88"},
        {"name": "👋 Greetings", "id": "909000083", "icon": "fa-hand-peace", "rarity": "common", "color": "#00D4FF"},
    ],
    
    "LEGENDARY_EMOTES": [
        {"name": "👑 FFWC THRONE", "id": "909000014", "icon": "fa-crown", "rarity": "legendary", "color": "#FFCC00"},
        {"name": "🐉 DRAGON FIST", "id": "909000015", "icon": "fa-dragon", "rarity": "legendary", "color": "#FF0055"},
        {"name": "👑 CHAMPION GRAB", "id": "909000087", "icon": "fa-trophy", "rarity": "legendary", "color": "#FFCC00"},
        {"name": "🔥 HADOUKEN", "id": "909000089", "icon": "fa-fire", "rarity": "legendary", "color": "#FF0055"},
        {"name": "💀 BLOOD WRAITH", "id": "909000090", "icon": "fa-skull", "rarity": "legendary", "color": "#9D4EDD"},
        {"name": "👑 THE CHOSEN VICTOR", "id": "909000098", "icon": "fa-crown", "rarity": "legendary", "color": "#FFCC00"},
        {"name": "💡 BORN OF LIGHT", "id": "909000085", "icon": "fa-lightbulb", "rarity": "legendary", "color": "#00FF88"},
        {"name": "🌟 DANCE OF CONSTELLATION", "id": "909037003", "icon": "fa-star", "rarity": "legendary", "color": "#9D4EDD"},
        {"name": "💃 MACARENA", "id": "909038002", "icon": "fa-music", "rarity": "legendary", "color": "#FF0055"},
        {"name": "⚡ THUNDER BREATHING", "id": "909041001", "icon": "fa-bolt", "rarity": "mythic", "color": "#00D4FF"},
        {"name": "💧 WATER BREATHING", "id": "909041002", "icon": "fa-water", "rarity": "mythic", "color": "#00D4FF"},
        {"name": "🐺 BEAST BREATHING", "id": "909041003", "icon": "fa-paw", "rarity": "mythic", "color": "#FF8800"},
        {"name": "🎨 FLYING INK SWORD", "id": "909041004", "icon": "fa-pen-fancy", "rarity": "legendary", "color": "#9D4EDD"},
        {"name": "🔫 POPBLASTER", "id": "909041005", "icon": "fa-gun", "rarity": "legendary", "color": "#FF0055"},
    ],
    
    "2024_EMOTES": [
        {"name": "💨 MONEY RAIN", "id": "909042002", "icon": "fa-money-bill-wave", "rarity": "epic", "color": "#FFCC00"},
        {"name": "❄️ FROSTFIRE'S CALLING", "id": "909042003", "icon": "fa-snowflake", "rarity": "epic", "color": "#00D4FF"},
        {"name": "🧊 GLOO SCULPTURE", "id": "909042007", "icon": "fa-snowman", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🐅 REAL TIGER?", "id": "909042008", "icon": "fa-paw", "rarity": "epic", "color": "#FF8800"},
        {"name": "🎿 CELEBRATION SCHUSS", "id": "909042009", "icon": "fa-person-skiing", "rarity": "epic", "color": "#00D4FF"},
        {"name": "⛵ DAWN VOYAGE", "id": "909042011", "icon": "fa-sailboat", "rarity": "legendary", "color": "#00D4FF"},
        {"name": "🏎️ LAMBORGHINI RIDE", "id": "909042012", "icon": "fa-car", "rarity": "mythic", "color": "#FF0055"},
        {"name": "👋 FROSTFIRE HELLO", "id": "909042013", "icon": "fa-snowflake", "rarity": "epic", "color": "#00D4FF"},
        {"name": "🎭 KEMUSAN", "id": "909042018", "icon": "fa-mask", "rarity": "legendary", "color": "#9D4EDD"},
        {"name": "🐸 RIBBIT RIDER", "id": "909043001", "icon": "fa-frog", "rarity": "epic", "color": "#00FF88"},
        {"name": "🧘 INNER SELF MASTERY", "id": "909043002", "icon": "fa-om", "rarity": "legendary", "color": "#9D4EDD"},
        {"name": "💰 EMPEROR'S TREASURE", "id": "909043003", "icon": "fa-coins", "rarity": "mythic", "color": "#FFCC00"},
        {"name": "🌀 WHY SO CHAOS?", "id": "909043004", "icon": "fa-spinner", "rarity": "epic", "color": "#FF0055"},
        {"name": "🍗 HUGE FEAST", "id": "909043005", "icon": "fa-drumstick", "rarity": "epic", "color": "#FF8800"},
        {"name": "🎨 COLOR BURST", "id": "909043006", "icon": "fa-palette", "rarity": "legendary", "color": "#FF0055"},
    ]
}

# Combine all emotes
ALL_EMOTES = []
for category in EMOTE_DATABASE.values():
    ALL_EMOTES.extend(category)

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
    "connected_bots": [],
    "last_bot_ping": None
    
    
class CommandManager:
    def __init__(self):
        self.storage = command_storage
    
    def save_command(self, team_code, emote_id, target_uid, user_ip, emote_name="", category="basic"):
        try:
            command_id = self.storage["last_id"] + 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if not emote_name:
                for emote in ALL_EMOTES:
                    if emote["id"] == emote_id:
                        emote_name = emote["name"]
                        category = emote.get("rarity", "basic")
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
            
            print(f"✅ Command #{command_id} saved: {emote_name}")
            return command_id
            
        except Exception as e:
            print(f"❌ Save error: {e}")
            return None

command_manager = CommandManager()


# ==================== HTML TEMPLATE - NEW COLOR SCHEME ====================
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
    
    <style>
        :root {
            --primary: #00D4FF;      /* Cyan Blue */
            --secondary: #FF0055;    /* Pink Red */
            --accent: #FFCC00;       /* Gold Yellow */
            --success: #00FF88;      /* Green */
            --warning: #FF8800;      /* Orange */
            --danger: #FF2A6D;       /* Pink */
            --purple: #9D4EDD;       /* Purple */
            --dark: #0A0A1A;         /* Dark Blue */
            --darker: #050510;       /* Darker Blue */
            --light: #FFFFFF;
            --gray: #64748B;
            
            --gradient-primary: linear-gradient(135deg, var(--primary), #0099FF);
            --gradient-secondary: linear-gradient(135deg, var(--secondary), #FF2A6D);
            --gradient-accent: linear-gradient(135deg, var(--accent), #FFAA00);
            --gradient-success: linear-gradient(135deg, var(--success), #00CC66);
            
            --shadow-primary: 0 10px 30px rgba(0, 212, 255, 0.3);
            --shadow-secondary: 0 10px 30px rgba(255, 0, 85, 0.3);
            --shadow-accent: 0 10px 30px rgba(255, 204, 0, 0.3);
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
                radial-gradient(circle at 10% 20%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(255, 0, 85, 0.1) 0%, transparent 50%);
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        /* =============== HEADER =============== */
        .header {
            text-align: center;
            padding: 50px 30px;
            margin-bottom: 40px;
            background: rgba(10, 10, 26, 0.9);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            border: 2px solid var(--primary);
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-primary);
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--gradient-primary);
        }

        .logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 4rem;
            font-weight: 900;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        }

        .tagline {
            font-size: 1.3rem;
            color: var(--light);
            opacity: 0.9;
            margin-bottom: 30px;
            font-weight: 300;
            letter-spacing: 1px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(0, 212, 255, 0.2);
            transition: all 0.3s ease;
            text-align: center;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            border-color: var(--primary);
            box-shadow: var(--shadow-primary);
        }

        .stat-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.8rem;
            font-weight: 800;
            color: var(--primary);
            margin: 10px 0;
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--light);
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        /* =============== QUICK SEND =============== */
        .quick-send-section {
            background: rgba(10, 10, 26, 0.9);
            border-radius: 25px;
            padding: 40px;
            margin-bottom: 40px;
            border: 2px solid var(--secondary);
            box-shadow: var(--shadow-secondary);
        }

        .section-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .section-title i {
            color: var(--secondary);
        }

        .input-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }

        .input-group {
            position: relative;
        }

        .input-group label {
            display: block;
            margin-bottom: 10px;
            color: var(--primary);
            font-weight: 600;
            font-size: 1.1rem;
            font-family: 'Montserrat', sans-serif;
        }

        .input-wrapper {
            position: relative;
        }

        .input-wrapper input {
            width: 100%;
            padding: 18px 20px 18px 50px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid var(--primary);
            border-radius: 12px;
            color: var(--light);
            font-size: 1.1rem;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s ease;
        }

        .input-wrapper i {
            position: absolute;
            left: 18px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--secondary);
            font-size: 1.2rem;
        }

        .input-wrapper input:focus {
            outline: none;
            border-color: var(--secondary);
            box-shadow: var(--shadow-secondary);
            background: rgba(255, 0, 85, 0.05);
        }

        .action-btn {
            width: 100%;
            padding: 22px;
            background: var(--gradient-primary);
            border: none;
            border-radius: 15px;
            color: white;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }

        .action-btn:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-primary);
            background: var(--gradient-secondary);
        }

        /* =============== EMOTE CATEGORIES =============== */
        .categories-container {
            background: rgba(10, 10, 26, 0.9);
            border-radius: 25px;
            padding: 30px;
            margin-bottom: 40px;
            border: 2px solid var(--accent);
            box-shadow: var(--shadow-accent);
        }

        .categories-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 20px;
        }

        .categories-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
        }

        .category-tabs {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        .category-tab {
            padding: 12px 25px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--accent);
            border-radius: 10px;
            color: var(--light);
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .category-tab:hover {
            background: rgba(255, 204, 0, 0.1);
            transform: translateY(-2px);
        }

        .category-tab.active {
            background: var(--gradient-accent);
            color: var(--dark);
            font-weight: 600;
        }

        /* SCROLLABLE EMOTE GRID */
        .emote-grid-container {
            position: relative;
            margin-top: 20px;
        }

        .emote-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
            padding-right: 15px;
        }

        /* Custom Scrollbar */
        .emote-grid::-webkit-scrollbar {
            width: 8px;
        }

        .emote-grid::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }

        .emote-grid::-webkit-scrollbar-thumb {
            background: var(--gradient-primary);
            border-radius: 10px;
        }

        .emote-grid::-webkit-scrollbar-thumb:hover {
            background: var(--gradient-secondary);
        }

        .emote-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            border: 2px solid;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .emote-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        }

        .emote-card-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }

        .emote-icon {
            width: 60px;
            height: 60px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            color: white;
            flex-shrink: 0;
        }

        .emote-info {
            flex: 1;
        }

        .emote-name {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--light);
            margin-bottom: 5px;
        }

        .emote-id {
            font-family: 'Orbitron', monospace;
            font-size: 0.9rem;
            color: var(--light);
            opacity: 0.7;
        }

        .emote-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }

        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            flex: 1;
            justify-content: center;
        }

        .btn-primary {
            background: var(--gradient-primary);
            color: white;
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: var(--light);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        .btn-primary:hover {
            box-shadow: var(--shadow-primary);
        }

        .btn-secondary:hover {
            border-color: var(--primary);
        }

        /* =============== STATUS PANEL =============== */
        .status-panel {
            background: rgba(10, 10, 26, 0.9);
            border-radius: 25px;
            padding: 40px;
            margin-top: 40px;
            border: 2px solid var(--success);
            box-shadow: 0 10px 30px rgba(0, 255, 136, 0.2);
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .status-card {
            background: rgba(0, 0, 0, 0.3);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .status-card:hover {
            transform: translateY(-5px);
            border-color: var(--success);
        }

        .status-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            font-weight: 900;
            margin: 15px 0;
        }

        .status-online { color: var(--success); }
        .status-offline { color: var(--danger); }
        .status-pending { color: var(--accent); }

        .status-label {
            color: var(--light);
            opacity: 0.8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        /* =============== FOOTER =============== */
        .footer {
            margin-top: 50px;
            padding: 40px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 25px;
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
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: var(--primary);
        }

        .footer-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.3rem;
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
            padding: 20px 25px;
            border-radius: 12px;
            display: none;
            font-weight: 600;
            z-index: 1000;
            font-family: 'Poppins', sans-serif;
            max-width: 400px;
            backdrop-filter: blur(20px);
            border: 2px solid;
            animation: slideIn 0.3s ease;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }

        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .notification.success {
            background: rgba(0, 255, 136, 0.9);
            color: var(--dark);
            border-color: var(--success);
        }

        .notification.error {
            background: rgba(255, 42, 109, 0.9);
            color: white;
            border-color: var(--danger);
        }

        .notification.info {
            background: rgba(0, 212, 255, 0.9);
            color: var(--dark);
            border-color: var(--primary);
        }

        /* =============== RESPONSIVE =============== */
        @media (max-width: 1200px) {
            .logo { font-size: 3.5rem; }
            .emote-grid { grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }
        }

        @media (max-width: 768px) {
            .container { padding: 15px; }
            .logo { font-size: 2.5rem; }
            .section-title { font-size: 1.8rem; }
            .input-grid { grid-template-columns: 1fr; }
            .emote-grid { grid-template-columns: 1fr; }
            .categories-header { flex-direction: column; }
            .category-tabs { justify-content: center; }
            .footer-content { grid-template-columns: 1fr; }
            .emote-grid { max-height: 400px; }
        }

        @media (max-width: 480px) {
            .header { padding: 30px 20px; }
            .quick-send-section { padding: 30px 20px; }
            .categories-container { padding: 25px 20px; }
            .stat-card { padding: 20px; }
            .action-btn { padding: 18px; font-size: 1.3rem; }
        }
    </style>
</head>
<body>
    <!-- Notification -->
    <div class="notification" id="notification"></div>

    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1 class="logo">
                <i class="fas fa-fire"></i> ASHISH EMOTE PANEL
            </h1>
            <p class="tagline">⚡ Professional Emote Delivery • 400+ Emotes • Instant Execution</p>
            
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
        <div class="quick-send-section">
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

            <button class="action-btn" onclick="sendQuickCommand()">
                <i class="fas fa-rocket"></i> LAUNCH EMOTE ATTACK
            </button>
        </div>

        <!-- EMOTE CATEGORIES -->
        <div class="categories-container">
            <div class="categories-header">
                <h3 class="categories-title">🎮 EMOTE COLLECTION</h3>
                
                <div class="category-tabs">
                    <button class="category-tab active" onclick="showCategory('evo')">EVO GUNS</button>
                    <button class="category-tab" onclick="showCategory('special')">SPECIAL</button>
                    <button class="category-tab" onclick="showCategory('popular')">POPULAR</button>
                    <button class="category-tab" onclick="showCategory('dance')">DANCE</button>
                    <button class="category-tab" onclick="showCategory('legendary')">LEGENDARY</button>
                    <button class="category-tab" onclick="showCategory('new2024')">2024 EMOTES</button>
                </div>
            </div>

            <!-- EVO GUNS -->
            <div class="emote-grid-container">
                <div id="evo-category" class="emote-grid">
                    {% for emote in evo_emotes %}
                    <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <div class="emote-card-header">
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

                <!-- SPECIAL EMOTES -->
                <div id="special-category" class="emote-grid" style="display: none;">
                    {% for emote in special_emotes %}
                    <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <div class="emote-card-header">
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

                <!-- POPULAR EMOTES -->
                <div id="popular-category" class="emote-grid" style="display: none;">
                    {% for emote in popular_emotes %}
                    <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <div class="emote-card-header">
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

                <!-- DANCE EMOTES -->
                <div id="dance-category" class="emote-grid" style="display: none;">
                    {% for emote in dance_emotes %}
                    <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <div class="emote-card-header">
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

                <!-- LEGENDARY EMOTES -->
                <div id="legendary-category" class="emote-grid" style="display: none;">
                    {% for emote in legendary_emotes %}
                    <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <div class="emote-card-header">
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

                <!-- 2024 EMOTES -->
                <div id="new2024-category" class="emote-grid" style="display: none;">
                    {% for emote in new_2024_emotes %}
                    <div class="emote-card" style="border-color: {{ emote.color }};" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <div class="emote-card-header">
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

        <!-- STATUS PANEL -->
        <div class="status-panel">
            <h2 class="section-title">
                <i class="fas fa-chart-line"></i> SYSTEM STATUS
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
                    <div class="status-label">Connection Status</div>
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
        <div class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <div class="footer-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <h3 class="footer-title">SECURE CONNECTION</h3>
                    <p class="footer-text">All connections are encrypted and secure. Your data is protected with military-grade encryption.</p>
                </div>
                
                <div class="footer-section">
                    <div class="footer-icon">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <h3 class="footer-title">INSTANT DELIVERY</h3>
                    <p class="footer-text">400+ emotes delivered instantly with 99.9% success rate. Real-time execution guaranteed.</p>
                </div>
                
                <div class="footer-section">
                    <div class="footer-icon">
                        <i class="fas fa-user-tie"></i>
                    </div>
                    <h3 class="footer-title">DEVELOPED BY ASHISH</h3>
                    <p class="footer-text">Professional emote delivery system created by Ashish Shakya. Premium quality service.</p>
                </div>
                
                <div class="footer-section">
                    <div class="footer-icon">
                        <i class="fas fa-code"></i>
                    </div>
                    <h3 class="footer-title">VERSION 5.0 PRO</h3>
                    <p class="footer-text">Most advanced emote panel with real-time execution. Constantly updated with new features.</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let commandsSent = 0;
        let todayCommands = 0;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            // Set default values
            document.getElementById('teamCode').value = '1234567';
            document.getElementById('targetUid').value = '13706108657';
            document.getElementById('emoteId').value = '909033001';
            
            // Update stats every 3 seconds
            updateStats();
            setInterval(updateStats, 3000);
            
            // Check bot connection
            setInterval(checkBotConnection, 5000);
            
            // Auto-scroll to show user there's more content
            setTimeout(() => {
                const emoteGrid = document.querySelector('.emote-grid');
                if (emoteGrid) {
                    emoteGrid.scrollTop = 50;
                    setTimeout(() => {
                        emoteGrid.scrollTop = 0;
                    }, 500);
                }
            }, 1000);
        });
        
        // Category switching
        function showCategory(category) {
            // Hide all categories
            document.querySelectorAll('.emote-grid').forEach(grid => {
                grid.style.display = 'none';
            });
            
            // Remove active from all tabs
            document.querySelectorAll('.category-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected category
            document.getElementById(category + '-category').style.display = 'grid';
            
            // Activate clicked tab
            event.target.classList.add('active');
            
            // Show notification
            const categoryNames = {
                'evo': 'EVO Guns',
                'special': 'Special Emotes',
                'popular': 'Popular Emotes',
                'dance': 'Dance Emotes',
                'legendary': 'Legendary Emotes',
                'new2024': '2024 Emotes'
            };
            
            showNotification(`📁 ${categoryNames[category]} loaded!`, 'info');
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
            const sendBtn = document.querySelector('.action-btn');
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
                    sendBtn.style.background = 'var(--gradient-success)';
                    setTimeout(() => {
                        sendBtn.style.background = 'var(--gradient-primary)';
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
                    if (data.success) {
                        document.getElementById('commandsSent').textContent = data.total_commands;
                        document.getElementById('todayCommands').textContent = data.today_commands || 0;
                        
                        // Update bot status
                        const now = new Date();
                        const lastPing = data.last_bot_ping ? new Date(data.last_bot_ping) : null;
                        
                        if (lastPing && (now - lastPing) < 30000) { // 30 seconds
                            document.getElementById('botStatus').textContent = data.connected_bots.length;
                            document.getElementById('termuxStatus').textContent = 'ONLINE';
                            document.getElementById('termuxStatus').className = 'status-value status-online';
                        } else {
                            document.getElementById('botStatus').textContent = '0';
                            document.getElementById('termuxStatus').textContent = 'OFFLINE';
                            document.getElementById('termuxStatus').className = 'status-value status-offline';
                        }
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
        
        // Add scroll indicators to emote grids
        document.querySelectorAll('.emote-grid').forEach(grid => {
            grid.addEventListener('scroll', function() {
                const scrollPercent = (this.scrollTop / (this.scrollHeight - this.clientHeight)) * 100;
                
                // Add shadow when scrolled
                if (scrollPercent > 5) {
                    this.style.boxShadow = 'inset 0 10px 10px -10px rgba(0, 212, 255, 0.3)';
                } else {
                    this.style.boxShadow = 'none';
                }
            });
        });
    </script>
</body>
</html>
'''

# ==================== FLASK ROUTES ====================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE,
        evo_emotes=EMOTE_CATEGORIES["EVO_GUNS"],
        special_emotes=EMOTE_CATEGORIES["SPECIAL"],
        basic_emotes=EMOTE_CATEGORIES["BASIC"],
        legendary_emotes=EMOTE_CATEGORIES["LEGENDARY"],
        total_emotes=len(ALL_EMOTES)
    )

@app.route('/send', methods=['POST'])
def send_command():
    try:
        team_code = request.form.get('team_code', '').strip()
        emote_id = request.form.get('emote_id', '').strip()
        target_uid = request.form.get('target_uid', '').strip()
        
        print(f"🚀 Command received: Team={team_code}, Emote={emote_id}, Target={target_uid}")
        
        # Find emote category
        category = "basic"
        for cat_name, emotes in EMOTE_CATEGORIES.items():
            for emote in emotes:
                if emote["id"] == emote_id:
                    category = emote.get("rarity", "basic")
                    break
        
        user_ip = request.remote_addr
        command_id = command_manager.save_command(team_code, emote_id, target_uid, user_ip, category=category)
        
        if command_id:
            return jsonify({
                "success": True,
                "message": f"Command #{command_id} queued for execution!",
                "command_id": command_id,
                "note": "Termux bot will execute within 5 seconds"
            })
        else:
            return jsonify({"success": False, "error": "Server error"})
            
    except Exception as e:
        print(f"❌ Route error: {e}")
        return jsonify({"success": False, "error": "Internal error"})

@app.route('/status')
def status():
    pending = [cmd for cmd in command_storage["commands"] if not cmd.get("executed", False)]
    
    return jsonify({
        "bot_connected": len(pending) > 0,
        "pending_commands": len(pending),
        "total_commands": command_storage["stats"]["total"],
        "stats": command_storage["stats"],
        "recent_commands": command_storage["commands"][-10:] if command_storage["commands"] else []
    })

@app.route('/get_commands')
def get_commands():
    return jsonify({"commands": command_storage["commands"]})

@app.route('/mark_executed/<int:command_id>', methods=['POST'])
def mark_executed(command_id):
    for cmd in command_storage["commands"]:
        if cmd["id"] == command_id:
            cmd["executed"] = True
            cmd["status"] = "executed"
            print(f"✅ Command #{command_id} marked as executed")
            return jsonify({"success": True})
    return jsonify({"success": False})

# ==================== MAIN ====================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 ASHISH PREMIUM PANEL starting on port {port}")
    print(f"🎮 Total Emotes: {len(ALL_EMOTES)}")
    print(f"🔥 Categories: {len(EMOTE_CATEGORIES)}")
    app.run(host='0.0.0.0', port=port, debug=False)
