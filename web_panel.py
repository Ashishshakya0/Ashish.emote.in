from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ashish-premium-panel-2024')

# ==================== PREMIUM EMOTE DATABASE ====================
EMOTE_CATEGORIES = {
    "EVO_GUNS": [
        {"name": "🔥 EVO M4A1 MAX", "id": "909033001", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO AK47 MAX", "id": "909000063", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO SHOTGUN MAX", "id": "909035007", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO SCAR MAX", "id": "909000068", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO XMB MAX", "id": "909000085", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO G18 MAX", "id": "909038012", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO MP40 MAX", "id": "909040010", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO FAMAS MAX", "id": "909000090", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO UMP MAX", "id": "909000098", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO WOODPECKER MAX", "id": "909042008", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO GROZA MAX", "id": "909041005", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO THOMPSON MAX", "id": "909038010", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO PARAFAL MAX", "id": "909045001", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO P90 MAX", "id": "909049010", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO M60 MAX", "id": "909051003", "icon": "fa-gun", "rarity": "legendary"},
    ],
    
    "SPECIAL": [
        {"name": "🐍 COBRA RISING", "id": "909000075", "icon": "fa-fire", "rarity": "mythic"},
        {"name": "👻 DRACO'S SOUL", "id": "909000081", "icon": "fa-ghost", "rarity": "mythic"},
        {"name": "💀 BLOOD WRAITH", "id": "909000090", "icon": "fa-skull", "rarity": "mythic"},
        {"name": "🦅 FFWS 2021", "id": "909000080", "icon": "fa-trophy", "rarity": "legendary"},
        {"name": "👍 GOOD GAME", "id": "909000082", "icon": "fa-thumbs-up", "rarity": "rare"},
        {"name": "👋 GREETINGS", "id": "909000083", "icon": "fa-hand-peace", "rarity": "rare"},
        {"name": "🚶 THE WALKER", "id": "909000084", "icon": "fa-walking", "rarity": "epic"},
        {"name": "💡 BORN OF LIGHT", "id": "909000085", "icon": "fa-lightbulb", "rarity": "legendary"},
        {"name": "⚡ MYTHOS FOUR", "id": "909000086", "icon": "fa-bolt", "rarity": "epic"},
        {"name": "🏆 CHAMPION GRAB", "id": "909000087", "icon": "fa-trophy", "rarity": "legendary"},
        {"name": "❄️ WIN AND CHILL", "id": "909000088", "icon": "fa-snowflake", "rarity": "epic"},
        {"name": "🔥 HADOUKEN", "id": "909000089", "icon": "fa-fire", "rarity": "mythic"},
        {"name": "👹 BIG SMASH", "id": "909000091", "icon": "fa-fist-raised", "rarity": "epic"},
        {"name": "💃 FANCY STEPS", "id": "909000092", "icon": "fa-shoe-prints", "rarity": "rare"},
        {"name": "🎮 ALL IN CONTROL", "id": "909000093", "icon": "fa-gamepad", "rarity": "epic"},
        {"name": "🔧 DEBUGGING", "id": "909000094", "icon": "fa-screwdriver-wrench", "rarity": "rare"},
        {"name": "👋 WAGGOR WAVE", "id": "909000095", "icon": "fa-hand-wave", "rarity": "rare"},
        {"name": "🎸 CRAZY GUITAR", "id": "909000096", "icon": "fa-guitar", "rarity": "epic"},
        {"name": "✨ POOF", "id": "909000097", "icon": "fa-wand-sparkles", "rarity": "rare"},
        {"name": "👑 THE CHOSEN VICTOR", "id": "909000098", "icon": "fa-crown", "rarity": "legendary"},
        {"name": "⚔️ CHALLENGER", "id": "909000099", "icon": "fa-crosshairs", "rarity": "epic"},
    ],
    
    "BASIC": [
        {"name": "👋 HELLO!", "id": "909000001", "icon": "fa-hand", "rarity": "common"},
        {"name": "😂 LOL", "id": "909000002", "icon": "fa-laugh", "rarity": "common"},
        {"name": "😤 PROVOKE", "id": "909000003", "icon": "fa-fist-raised", "rarity": "common"},
        {"name": "👏 APPLAUSE", "id": "909000004", "icon": "fa-hands-clapping", "rarity": "common"},
        {"name": "💃 DAB", "id": "909000005", "icon": "fa-person-dancing", "rarity": "common"},
        {"name": "🐔 CHICKEN", "id": "909000006", "icon": "fa-drumstick", "rarity": "common"},
        {"name": "👋 ARM WAVE", "id": "909000007", "icon": "fa-hand-wave", "rarity": "common"},
        {"name": "💃 SHOOT DANCE", "id": "909000008", "icon": "fa-gun", "rarity": "common"},
        {"name": "🦈 BABY SHARK", "id": "909000009", "icon": "fa-fish", "rarity": "rare"},
        {"name": "🌹 FLOWERS OF LOVE", "id": "909000010", "icon": "fa-heart", "rarity": "rare"},
        {"name": "🧟 MUMMY DANCE", "id": "909000011", "icon": "fa-ghost", "rarity": "rare"},
        {"name": "💪 PUSH-UP", "id": "909000012", "icon": "fa-dumbbell", "rarity": "common"},
        {"name": "🕺 SHUFFLING", "id": "909000013", "icon": "fa-person-running", "rarity": "common"},
        {"name": "👑 FFWC THRONE", "id": "909000014", "icon": "fa-crown", "rarity": "epic"},
        {"name": "🐉 DRAGON FIST", "id": "909000015", "icon": "fa-dragon", "rarity": "epic"},
        {"name": "🎯 DANGEROUS GAME", "id": "909000016", "icon": "fa-bullseye", "rarity": "rare"},
        {"name": "🐆 JAGUAR DANCE", "id": "909000017", "icon": "fa-paw", "rarity": "rare"},
        {"name": "👊 THREATEN", "id": "909000018", "icon": "fa-hand-fist", "rarity": "common"},
        {"name": "🔄 SHAKE WITH ME", "id": "909000019", "icon": "fa-people-arrows", "rarity": "common"},
        {"name": "😈 DEVIL'S MOVE", "id": "909000020", "icon": "fa-horn", "rarity": "epic"},
    ],
    
    "LEGENDARY": [
        {"name": "🐉 DRAGON SLAYER", "id": "909050001", "icon": "fa-dragon", "rarity": "mythic"},
        {"name": "🔥 PHOENIX RISE", "id": "909050002", "icon": "fa-fire", "rarity": "mythic"},
        {"name": "👹 TITAN SMASH", "id": "909050003", "icon": "fa-fist-raised", "rarity": "mythic"},
        {"name": "👼 VALKYRIE WINGS", "id": "909050004", "icon": "fa-dove", "rarity": "mythic"},
        {"name": "🗡️ SAMURAI STRIKE", "id": "909050005", "icon": "fa-sword", "rarity": "mythic"},
        {"name": "🥷 NINJA VANISH", "id": "909050006", "icon": "fa-user-ninja", "rarity": "mythic"},
        {"name": "🧙 WIZARD SPELL", "id": "909050007", "icon": "fa-hat-wizard", "rarity": "mythic"},
        {"name": "🛡️ KNIGHT HONOR", "id": "909050008", "icon": "fa-shield", "rarity": "mythic"},
        {"name": "🗡️ ASSASSIN STEALTH", "id": "909050009", "icon": "fa-user-secret", "rarity": "mythic"},
        {"name": "😡 BERSERKER RAGE", "id": "909050010", "icon": "fa-angry", "rarity": "mythic"},
    ]
}

# Combine all emotes
ALL_EMOTES = []
for category in EMOTE_CATEGORIES.values():
    ALL_EMOTES.extend(category)

# ==================== IN-MEMORY STORAGE ====================
command_storage = {
    "commands": [],
    "last_id": 0,
    "stats": {
        "total": 0,
        "today": 0,
        "evo": 0,
        "special": 0,
        "basic": 0,
        "legendary": 0
    }
}

# ==================== COMMAND MANAGER ====================
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

# ==================== PROFESSIONAL HTML TEMPLATE ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 ASHISH | PREMIUM EMOTE PANEL</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap" rel="stylesheet">
    
    <!-- Animate.css -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    
    <style>
        :root {
            --primary: #ff2a6d;
            --secondary: #05d9e8;
            --accent: #d1f7ff;
            --dark: #01012b;
            --darker: #00001a;
            --evo-gradient: linear-gradient(135deg, #ff2a6d 0%, #ff8a00 100%);
            --special-gradient: linear-gradient(135deg, #05d9e8 0%, #005678 100%);
            --basic-gradient: linear-gradient(135deg, #9d4edd 0%, #560bad 100%);
            --legendary-gradient: linear-gradient(135deg, #ffd166 0%, #ff9e00 100%);
            --mythic-gradient: linear-gradient(135deg, #ff2a6d 0%, #9d4edd 50%, #05d9e8 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: var(--darker);
            color: var(--accent);
            font-family: 'Exo 2', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 42, 109, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(5, 217, 232, 0.1) 0%, transparent 20%);
            animation: backgroundPulse 20s infinite alternate;
        }

        @keyframes backgroundPulse {
            0% { background-position: 0% 0%; }
            100% { background-position: 100% 100%; }
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        /* ================= HEADER ================= */
        .header {
            text-align: center;
            padding: 40px 30px;
            margin-bottom: 40px;
            background: rgba(1, 1, 43, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 2px solid transparent;
            background-clip: padding-box;
            position: relative;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(255, 42, 109, 0.2);
            animation: headerGlow 3s infinite alternate;
        }

        @keyframes headerGlow {
            0% { 
                border-color: rgba(255, 42, 109, 0.3);
                box-shadow: 0 15px 35px rgba(255, 42, 109, 0.2);
            }
            100% { 
                border-color: rgba(5, 217, 232, 0.4);
                box-shadow: 0 15px 40px rgba(5, 217, 232, 0.3);
            }
        }

        .header::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: var(--mythic-gradient);
            z-index: -1;
            border-radius: 22px;
            animation: rotate 10s linear infinite;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 4.5rem;
            font-weight: 900;
            background: var(--mythic-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-shadow: 0 0 50px rgba(255, 42, 109, 0.5);
            animation: textGlow 2s infinite alternate;
        }

        @keyframes textGlow {
            0% { text-shadow: 0 0 30px rgba(255, 42, 109, 0.5); }
            100% { text-shadow: 0 0 60px rgba(5, 217, 232, 0.7); }
        }

        .tagline {
            font-size: 1.4rem;
            color: var(--secondary);
            margin-bottom: 20px;
            font-weight: 300;
            letter-spacing: 2px;
        }

        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .stat-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px 25px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 150px;
        }

        .stat-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--secondary);
            font-family: 'Orbitron', sans-serif;
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--accent);
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* ================= TABS ================= */
        .tabs-container {
            background: rgba(1, 1, 43, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 30px;
            border: 2px solid rgba(255, 42, 109, 0.2);
        }

        .tabs {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .tab-btn {
            padding: 18px 30px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid transparent;
            color: var(--accent);
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
            overflow: hidden;
            min-width: 200px;
            justify-content: center;
        }

        .tab-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: 0.6s;
        }

        .tab-btn:hover::before {
            left: 100%;
        }

        .tab-btn:hover {
            transform: translateY(-8px) scale(1.05);
            box-shadow: 0 15px 30px rgba(255, 42, 109, 0.3);
        }

        .tab-btn.active {
            background: var(--mythic-gradient);
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(255, 42, 109, 0.4);
            border-color: var(--secondary);
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.6s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .tab-content.active {
            display: block;
        }

        /* ================= QUICK SEND ================= */
        .quick-send-card {
            background: rgba(1, 1, 43, 0.9);
            border-radius: 20px;
            padding: 35px;
            margin-bottom: 30px;
            border: 2px solid var(--secondary);
            box-shadow: 0 10px 30px rgba(5, 217, 232, 0.2);
            position: relative;
            overflow: hidden;
        }

        .quick-send-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--mythic-gradient);
        }

        .section-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2rem;
            margin-bottom: 25px;
            color: var(--secondary);
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .section-title i {
            font-size: 2.5rem;
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
            margin-bottom: 12px;
            color: var(--secondary);
            font-weight: 600;
            font-size: 1.2rem;
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 1px;
        }

        .input-wrapper {
            position: relative;
        }

        .input-wrapper input {
            width: 100%;
            padding: 20px 25px;
            background: rgba(0, 0, 26, 0.7);
            border: 2px solid var(--primary);
            border-radius: 15px;
            color: white;
            font-size: 1.1rem;
            font-family: 'Exo 2', sans-serif;
            transition: all 0.3s ease;
            padding-left: 60px;
        }

        .input-wrapper i {
            position: absolute;
            left: 25px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--secondary);
            font-size: 1.3rem;
            z-index: 2;
        }

        .input-wrapper input:focus {
            outline: none;
            border-color: var(--secondary);
            box-shadow: 0 0 30px rgba(5, 217, 232, 0.4);
            transform: translateY(-3px);
        }

        /* ================= EMOTE GRIDS ================= */
        .emote-grids {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }

        .category-card {
            background: rgba(1, 1, 43, 0.9);
            border-radius: 20px;
            padding: 30px;
            border: 2px solid;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .category-card.evo { border-color: #ff2a6d; }
        .category-card.special { border-color: #05d9e8; }
        .category-card.basic { border-color: #9d4edd; }
        .category-card.legendary { border-color: #ffd166; }

        .category-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
        }
        .category-card.evo::before { background: var(--evo-gradient); }
        .category-card.special::before { background: var(--special-gradient); }
        .category-card.basic::before { background: var(--basic-gradient); }
        .category-card.legendary::before { background: var(--legendary-gradient); }

        .category-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }

        .category-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
        }

        .category-icon {
            font-size: 2.5rem;
            width: 70px;
            height: 70px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .evo .category-icon { background: var(--evo-gradient); }
        .special .category-icon { background: var(--special-gradient); }
        .basic .category-icon { background: var(--basic-gradient); }
        .legendary .category-icon { background: var(--legendary-gradient); }

        .category-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
        }
        .evo .category-title { color: #ff2a6d; }
        .special .category-title { color: #05d9e8; }
        .basic .category-title { color: #9d4edd; }
        .legendary .category-title { color: #ffd166; }

        .emote-list {
            display: grid;
            gap: 15px;
            max-height: 400px;
            overflow-y: auto;
            padding-right: 10px;
        }

        .emote-list::-webkit-scrollbar {
            width: 8px;
        }

        .emote-list::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }

        .emote-list::-webkit-scrollbar-thumb {
            background: var(--secondary);
            border-radius: 10px;
        }

        .emote-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 18px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid transparent;
        }

        .emote-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(10px);
            border-color: var(--secondary);
        }

        .emote-icon {
            font-size: 1.8rem;
            width: 50px;
            height: 50px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .evo .emote-icon { background: rgba(255, 42, 109, 0.2); color: #ff2a6d; }
        .special .emote-icon { background: rgba(5, 217, 232, 0.2); color: #05d9e8; }
        .basic .emote-icon { background: rgba(157, 78, 221, 0.2); color: #9d4edd; }
        .legendary .emote-icon { background: rgba(255, 209, 102, 0.2); color: #ffd166; }

        .emote-details {
            flex: 1;
        }

        .emote-name {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 5px;
        }

        .emote-id {
            font-family: monospace;
            font-size: 0.9rem;
            color: var(--accent);
            opacity: 0.7;
        }

        .emote-send-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9rem;
            letter-spacing: 1px;
        }
        .evo .emote-send-btn { background: var(--evo-gradient); color: white; }
        .special .emote-send-btn { background: var(--special-gradient); color: white; }
        .basic .emote-send-btn { background: var(--basic-gradient); color: white; }
        .legendary .emote-send-btn { background: var(--legendary-gradient); color: #000; }

        .emote-send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        /* ================= BUTTONS ================= */
        .action-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }

        .action-btn {
            padding: 25px;
            border: none;
            border-radius: 15px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.4s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            position: relative;
            overflow: hidden;
            letter-spacing: 2px;
        }

        .action-btn::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: rotate(45deg);
            transition: 0.6s;
        }

        .action-btn:hover::after {
            left: 100%;
        }

        .action-btn:hover {
            transform: translateY(-10px) scale(1.05);
        }

        .send-all-btn {
            background: var(--mythic-gradient);
            color: white;
            grid-column: 1 / -1;
            padding: 30px;
            font-size: 1.5rem;
        }

        .send-all-btn:hover {
            box-shadow: 0 20px 40px rgba(255, 42, 109, 0.4);
        }

        .test-btn {
            background: var(--special-gradient);
            color: white;
        }

        .clear-btn {
            background: rgba(255, 42, 109, 0.2);
            color: #ff2a6d;
            border: 2px solid #ff2a6d;
        }

        /* ================= STATUS PANEL ================= */
        .status-panel {
            background: rgba(1, 1, 43, 0.9);
            border-radius: 20px;
            padding: 30px;
            margin-top: 40px;
            border: 2px solid var(--secondary);
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .status-card {
            background: rgba(0, 0, 26, 0.7);
            padding: 25px;
            border-radius: 15px;
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
            font-size: 3rem;
            font-weight: 900;
            margin: 15px 0;
        }

        .status-online { color: #00ff9d; }
        .status-offline { color: #ff2a6d; }
        .status-pending { color: #ffd166; }

        .status-label {
            color: var(--accent);
            opacity: 0.8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .commands-history {
            background: rgba(0, 0, 26, 0.7);
            border-radius: 15px;
            padding: 25px;
            max-height: 400px;
            overflow-y: auto;
            margin-top: 20px;
        }

        .command-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 5px solid var(--secondary);
            animation: slideIn 0.5s ease;
            transition: all 0.3s ease;
        }

        .command-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(10px);
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        /* ================= FOOTER ================= */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(1, 1, 43, 0.95);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-top: 2px solid var(--primary);
            display: flex;
            justify-content: space-around;
            align-items: center;
            z-index: 1000;
        }

        .footer-item {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1rem;
        }

        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00ff9d;
            box-shadow: 0 0 10px #00ff9d;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { 
                transform: scale(1);
                box-shadow: 0 0 10px #00ff9d;
            }
            50% { 
                transform: scale(1.2);
                box-shadow: 0 0 20px #00ff9d;
            }
        }

        /* ================= NOTIFICATION ================= */
        .notification {
            position: fixed;
            top: 30px;
            right: 30px;
            padding: 25px 35px;
            border-radius: 15px;
            display: none;
            font-weight: bold;
            z-index: 2000;
            animation: slideInRight 0.4s ease, fadeOut 0.4s ease 3.6s;
            max-width: 400px;
            backdrop-filter: blur(10px);
            border: 2px solid;
            font-family: 'Orbitron', sans-serif;
        }

        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes fadeOut {
            to { opacity: 0; }
        }

        .notification.success {
            background: linear-gradient(135deg, rgba(0, 255, 157, 0.9), rgba(0, 200, 120, 0.9));
            color: #000;
            border-color: #00ff9d;
        }

        .notification.error {
            background: linear-gradient(135deg, rgba(255, 42, 109, 0.9), rgba(200, 30, 80, 0.9));
            color: white;
            border-color: #ff2a6d;
        }

        /* ================= RESPONSIVE ================= */
        @media (max-width: 1200px) {
            .emote-grids { grid-template-columns: 1fr; }
            .input-grid { grid-template-columns: 1fr; }
        }

        @media (max-width: 768px) {
            .logo { font-size: 3rem; }
            .tabs { flex-direction: column; }
            .tab-btn { min-width: 100%; }
            .footer { flex-direction: column; gap: 15px; }
            .stats-bar { gap: 15px; }
            .stat-item { min-width: 120px; padding: 12px 20px; }
            .stat-value { font-size: 1.8rem; }
        }

        @media (max-width: 480px) {
            .container { padding: 10px; }
            .header { padding: 25px 15px; }
            .quick-send-card { padding: 20px; }
            .category-card { padding: 20px; }
            .action-buttons { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <!-- NOTIFICATION -->
    <div class="notification" id="notification"></div>

    <div class="container">
        <!-- HEADER -->
        <div class="header animate__animated animate__fadeInDown">
            <div class="logo">
                <i class="fas fa-fire"></i> ASHISH EMOTE PANEL PRO
            </div>
            <div class="tagline">⚡ PREMIUM EMOTE DELIVERY SYSTEM | TERMUX TCP INTEGRATION</div>
            
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-value" id="totalEmotes">{{ total_emotes }}</div>
                    <div class="stat-label">TOTAL EMOTES</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="totalCommands">0</div>
                    <div class="stat-label">COMMANDS SENT</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="botStatusValue">ONLINE</div>
                    <div class="stat-label">BOT STATUS</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="responseTime">0ms</div>
                    <div class="stat-label">RESPONSE TIME</div>
                </div>
            </div>
        </div>

        <!-- QUICK SEND CARD -->
        <div class="quick-send-card animate__animated animate__fadeInUp">
            <h2 class="section-title">
                <i class="fas fa-bolt"></i> INSTANT EMOTE ATTACK
            </h2>
            
            <div class="input-grid">
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE</label>
                    <div class="input-wrapper">
                        <i class="fas fa-hashtag"></i>
                        <input type="text" id="teamCode" placeholder="Enter 7-digit team code" 
                               pattern="\d{7}" maxlength="7" required>
                    </div>
                </div>
                
                <div class="input-group">
                    <label><i class="fas fa-user"></i> TARGET UID</label>
                    <div class="input-wrapper">
                        <i class="fas fa-crosshairs"></i>
                        <input type="text" id="targetUid" placeholder="Enter target UID (8-11 digits)" 
                               pattern="\d{8,11}" required>
                    </div>
                </div>
                
                <div class="input-group">
                    <label><i class="fas fa-smile"></i> EMOTE ID</label>
                    <div class="input-wrapper">
                        <i class="fas fa-magic"></i>
                        <input type="text" id="emoteId" placeholder="909033001" 
                               pattern="\d{9}" required>
                    </div>
                </div>
            </div>

            <div class="action-buttons">
                <button class="action-btn send-all-btn" onclick="sendQuickCommand()">
                    <i class="fas fa-rocket"></i> LAUNCH EMOTE ATTACK
                </button>
            </div>
        </div>

        <!-- TABS CONTAINER -->
        <div class="tabs-container">
            <div class="tabs">
                <button class="tab-btn active" onclick="openTab('evo')">
                    <i class="fas fa-gun"></i> EVO GUNS
                </button>
                <button class="tab-btn" onclick="openTab('special')">
                    <i class="fas fa-star"></i> SPECIAL EMOTES
                </button>
                <button class="tab-btn" onclick="openTab('basic')">
                    <i class="fas fa-gamepad"></i> BASIC EMOTES
                </button>
                <button class="tab-btn" onclick="openTab('legendary')">
                    <i class="fas fa-crown"></i> LEGENDARY
                </button>
                <button class="tab-btn" onclick="openTab('status')">
                    <i class="fas fa-chart-network"></i> STATUS
                </button>
            </div>

            <!-- EVO GUNS TAB -->
            <div id="evo" class="tab-content active">
                <div class="emote-grids">
                    <div class="category-card evo">
                        <div class="category-header">
                            <div class="category-icon">
                                <i class="fas fa-gun"></i>
                            </div>
                            <h3 class="category-title">EVO GUN EMOTES</h3>
                        </div>
                        
                        <div class="emote-list">
                            {% for emote in evo_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}', event)">
                                    <i class="fas fa-paper-plane"></i> SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- SPECIAL EMOTES TAB -->
            <div id="special" class="tab-content">
                <div class="emote-grids">
                    <div class="category-card special">
                        <div class="category-header">
                            <div class="category-icon">
                                <i class="fas fa-star"></i>
                            </div>
                            <h3 class="category-title">SPECIAL EMOTES</h3>
                        </div>
                        
                        <div class="emote-list">
                            {% for emote in special_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}', event)">
                                    <i class="fas fa-paper-plane"></i> SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- BASIC EMOTES TAB -->
            <div id="basic" class="tab-content">
                <div class="emote-grids">
                    <div class="category-card basic">
                        <div class="category-header">
                            <div class="category-icon">
                                <i class="fas fa-gamepad"></i>
                            </div>
                            <h3 class="category-title">BASIC EMOTES</h3>
                        </div>
                        
                        <div class="emote-list">
                            {% for emote in basic_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}', event)">
                                    <i class="fas fa-paper-plane"></i> SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- LEGENDARY EMOTES TAB -->
            <div id="legendary" class="tab-content">
                <div class="emote-grids">
                    <div class="category-card legendary">
                        <div class="category-header">
                            <div class="category-icon">
                                <i class="fas fa-crown"></i>
                            </div>
                            <h3 class="category-title">LEGENDARY EMOTES</h3>
                        </div>
                        
                        <div class="emote-list">
                            {% for emote in legendary_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}', event)">
                                    <i class="fas fa-paper-plane"></i> SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- STATUS TAB -->
            <div id="status" class="tab-content">
                <div class="status-panel">
                    <h2 class="section-title">
                        <i class="fas fa-chart-network"></i> SYSTEM STATUS
                    </h2>
                    
                    <div class="status-grid">
                        <div class="status-card">
                            <div class="status-label">WEB PANEL</div>
                            <div class="status-value status-online">ONLINE</div>
                            <div class="status-label">Render.com</div>
                        </div>
                        
                        <div class="status-card">
                            <div class="status-label">TERMUX BOT</div>
                            <div class="status-value" id="botStatusDisplay">CHECKING</div>
                            <div class="status-label" id="lastSeen">Last: Checking...</div>
                        </div>
                        
                        <div class="status-card">
                            <div class="status-label">COMMANDS QUEUE</div>
                            <div class="status-value status-pending" id="queueCount">0</div>
                            <div class="status-label">Pending Execution</div>
                        </div>
                        
                        <div class="status-card">
                            <div class="status-label">RESPONSE TIME</div>
                            <div class="status-value" id="pingTime">0ms</div>
                            <div class="status-label">Server Latency</div>
                        </div>
                    </div>
                    
                    <h3 style="color: var(--secondary); margin: 30px 0 15px 0;">
                        <i class="fas fa-history"></i> RECENT COMMANDS
                    </h3>
                    
                    <div class="commands-history" id="commandsHistory">
                        <p style="text-align: center; color: var(--accent); opacity: 0.6;">
                            No commands yet. Send your first emote!
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <div class="footer">
        <div class="footer-item">
            <div class="status-indicator"></div>
            <span>PANEL: <span style="color: #00ff9d;">OPERATIONAL</span></span>
        </div>
        <div class="footer-item">
            <i class="fas fa-robot"></i>
            <span>BOT: <span id="footerBotStatus" style="color: #ffd166;">CONNECTING</span></span>
        </div>
        <div class="footer-item">
            <i class="fas fa-user-ninja"></i>
            <span>DEVELOPER: ASHISH</span>
        </div>
        <div class="footer-item">
            <i class="fab fa-instagram"></i>
            <span>@ashish.shakya0001</span>
        </div>
        <div class="footer-item">
            <i class="fas fa-bolt"></i>
            <span>VERSION: PRO 3.0</span>
        </div>
    </div>

    <script>
        // ================= CONFIGURATION =================
        const WEB_URL = window.location.origin;
        let commandCount = 0;
        let botConnected = false;
        
        // ================= INITIALIZE =================
        document.addEventListener('DOMContentLoaded', function() {
            updateStats();
            checkBotStatus();
            loadCommandsHistory();
            
            // Auto-refresh every 5 seconds
            setInterval(checkBotStatus, 5000);
            setInterval(loadCommandsHistory, 3000);
            setInterval(updateStats, 10000);
            
            // Set default values for testing
            document.getElementById('teamCode').value = '1234567';
            document.getElementById('targetUid').value = '13706108657';
            document.getElementById('emoteId').value = '909033001';
        });
        
        // ================= TAB SYSTEM =================
        function openTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active from buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            document.querySelector(`[onclick="openTab('${tabName}')"]`).classList.add('active');
            
            // Add animation
            document.getElementById(tabName).classList.add('animate__animated', 'animate__fadeIn');
            setTimeout(() => {
                document.getElementById(tabName).classList.remove('animate__animated', 'animate__fadeIn');
            }, 1000);
        }
        
        // ================= EMOTE FUNCTIONS =================
        function useEmote(emoteId, emoteName) {
            document.getElementById('emoteId').value = emoteId;
            showNotification(`✅ ${emoteName} selected! Enter Team Code & Target UID`, 'success');
            document.getElementById('teamCode').focus();
        }
        
        function sendEmote(emoteId, emoteName, event) {
            if (event) event.stopPropagation();
            
            const team = document.getElementById('teamCode').value;
            const target = document.getElementById('targetUid').value;
            
            if (!team || !target) {
                showNotification('❌ Please enter Team Code and Target UID first!', 'error');
                return;
            }
            
            sendCommand(team, emoteId, target, emoteName);
        }
        
        function sendQuickCommand() {
            const team = document.getElementById('teamCode').value;
            const target = document.getElementById('targetUid').value;
            const emote = document.getElementById('emoteId').value;
            
            if (!team || !target || !emote) {
                showNotification('❌ Please fill all fields!', 'error');
                return;
            }
            
            sendCommand(team, emote, target, 'Custom Emote');
        }
        
        // ================= COMMAND SENDING =================
        function sendCommand(team, emote, target, emoteName) {
            const startTime = Date.now();
            
            // Validate
            if (!/^\d{7}$/.test(team)) {
                showNotification('❌ Team Code must be 7 digits!', 'error');
                return;
            }
            
            if (!/^\d{8,11}$/.test(target)) {
                showNotification('❌ Target UID must be 8-11 digits!', 'error');
                return;
            }
            
            if (!/^\d{9}$/.test(emote)) {
                showNotification('❌ Emote ID must be 9 digits!', 'error');
                return;
            }
            
            // Show sending animation
            const sendBtn = event?.target || document.querySelector('.send-all-btn');
            const originalText = sendBtn.innerHTML;
            sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> SENDING...';
            sendBtn.disabled = true;
            
            // Send to server
            fetch('/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `team_code=${team}&emote_id=${emote}&target_uid=${target}`
            })
            .then(response => {
                const responseTime = Date.now() - startTime;
                document.getElementById('responseTime').textContent = `${responseTime}ms`;
                document.getElementById('pingTime').textContent = `${responseTime}ms`;
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    commandCount++;
                    updateStats();
                    showNotification(`🚀 ${emoteName} sent to UID ${target}!`, 'success');
                    loadCommandsHistory();
                    
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
                setTimeout(() => {
                    sendBtn.innerHTML = originalText;
                    sendBtn.disabled = false;
                }, 1000);
            });
        }
        
        // ================= STATUS FUNCTIONS =================
        function checkBotStatus() {
            fetch('/status')
                .then(r => r.json())
                .then(data => {
                    const botStatus = document.getElementById('botStatusDisplay');
                    const footerBotStatus = document.getElementById('footerBotStatus');
                    const botStatusValue = document.getElementById('botStatusValue');
                    
                    if (data.bot_connected) {
                        botStatus.innerHTML = '🟢 ONLINE';
                        botStatus.style.color = '#00ff9d';
                        footerBotStatus.innerHTML = 'ONLINE';
                        footerBotStatus.style.color = '#00ff9d';
                        botStatusValue.innerHTML = 'ONLINE';
                        botConnected = true;
                    } else {
                        botStatus.innerHTML = '🔴 OFFLINE';
                        botStatus.style.color = '#ff2a6d';
                        footerBotStatus.innerHTML = 'OFFLINE';
                        footerBotStatus.style.color = '#ff2a6d';
                        botStatusValue.innerHTML = 'OFFLINE';
                        botConnected = false;
                    }
                    
                    // Update queue count
                    document.getElementById('queueCount').innerHTML = data.pending_commands;
                })
                .catch(() => {
                    document.getElementById('botStatusDisplay').innerHTML = '❌ ERROR';
                    document.getElementById('botStatusDisplay').style.color = '#ff2a6d';
                });
        }
        
        function loadCommandsHistory() {
            const historyContainer = document.getElementById('commandsHistory');
            
            fetch('/get_commands')
                .then(r => r.json())
                .then(data => {
                    const commands = data.commands || [];
                    
                    if (commands.length === 0) {
                        historyContainer.innerHTML = `
                            <p style="text-align: center; color: var(--accent); opacity: 0.6;">
                                No commands yet. Send your first emote!
                            </p>`;
                        return;
                    }
                    
                    // Show last 8 commands
                    const recent = commands.slice(-8).reverse();
                    let html = '';
                    
                    recent.forEach(cmd => {
                        const time = cmd.timestamp.split(' ')[1];
                        const statusColor = cmd.status === 'executed' ? '#00ff9d' : '#ffd166';
                        const statusIcon = cmd.status === 'executed' ? 'fa-check' : 'fa-clock';
                        
                        html += `
                        <div class="command-item">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                <strong style="color: var(--secondary);">#${cmd.id} • ${cmd.emote_name}</strong>
                                <span style="color: var(--accent); opacity: 0.7;">${time}</span>
                            </div>
                            <div style="margin-bottom: 5px;">
                                Team: <span style="color: #ff2a6d;">${cmd.team_code}</span> • 
                                Target: <span style="color: #05d9e8;">${cmd.target_uid}</span>
                            </div>
                            <div style="text-align: right;">
                                <span style="color: ${statusColor};">
                                    <i class="fas ${statusIcon}"></i> ${cmd.status.toUpperCase()}
                                </span>
                            </div>
                        </div>`;
                    });
                    
                    historyContainer.innerHTML = html;
                });
        }
        
        function updateStats() {
            document.getElementById('totalCommands').textContent = commandCount;
            
            // Update response time
            const start = Date.now();
            fetch('/status', { method: 'HEAD' })
                .then(() => {
                    const time = Date.now() - start;
                    document.getElementById('responseTime').textContent = `${time}ms`;
                });
        }
        
        // ================= NOTIFICATION =================
        function showNotification(message, type = 'success') {
            const notif = document.getElementById('notification');
            notif.textContent = message;
            notif.className = `notification ${type}`;
            notif.style.display = 'block';
            
            // Auto hide after 4 seconds
            setTimeout(() => {
                notif.style.display = 'none';
            }, 4000);
        }
        
        // ================= ANIMATIONS =================
        setInterval(() => {
            // Random emote animation
            const emoteItems = document.querySelectorAll('.emote-item');
            if (emoteItems.length > 0) {
                const randomItem = emoteItems[Math.floor(Math.random() * emoteItems.length)];
                randomItem.classList.add('animate__animated', 'animate__pulse');
                setTimeout(() => {
                    randomItem.classList.remove('animate__animated', 'animate__pulse');
                }, 1000);
            }
        }, 3000);
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