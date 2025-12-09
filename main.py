
from flask import Flask, render_template_string, request, jsonify
import os
import re
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ashish-bot-panel-2024')

# -------------------- COMPLETE EMOTE DATABASE --------------------
ALL_EMOTES = [
    # Basic Emotes (1-50)
    {"name": "Hello!", "id": "909000001", "category": "basic", "icon": "fa-hand"},
    {"name": "LOL", "id": "909000002", "category": "basic", "icon": "fa-laugh"},
    {"name": "Provoke", "id": "909000003", "category": "basic", "icon": "fa-fist-raised"},
    {"name": "Applause", "id": "909000004", "category": "basic", "icon": "fa-hands-clapping"},
    {"name": "Dab", "id": "909000005", "category": "basic", "icon": "fa-person-dancing"},
    {"name": "Chicken", "id": "909000006", "category": "basic", "icon": "fa-drumstick"},
    {"name": "Arm Wave", "id": "909000007", "category": "basic", "icon": "fa-hand-wave"},
    {"name": "Shoot Dance", "id": "909000008", "category": "basic", "icon": "fa-gun"},
    {"name": "Baby Shark", "id": "909000009", "category": "basic", "icon": "fa-fish"},
    {"name": "Flowers of Love", "id": "909000010", "category": "basic", "icon": "fa-heart"},
    {"name": "Mummy Dance", "id": "909000011", "category": "basic", "icon": "fa-ghost"},
    {"name": "Push-up", "id": "909000012", "category": "basic", "icon": "fa-dumbbell"},
    {"name": "Shuffling", "id": "909000013", "category": "basic", "icon": "fa-person-running"},
    {"name": "FFWC Throne", "id": "909000014", "category": "basic", "icon": "fa-crown"},
    {"name": "Dragon Fist", "id": "909000015", "category": "basic", "icon": "fa-dragon"},
    {"name": "Dangerous Game", "id": "909000016", "category": "basic", "icon": "fa-bullseye"},
    {"name": "Jaguar Dance", "id": "909000017", "category": "basic", "icon": "fa-paw"},
    {"name": "Threaten", "id": "909000018", "category": "basic", "icon": "fa-hand-fist"},
    {"name": "Shake With Me", "id": "909000019", "category": "basic", "icon": "fa-people-arrows"},
    {"name": "Devil's Move", "id": "909000020", "category": "basic", "icon": "fa-horn"},
    {"name": "Furious Slam", "id": "909000021", "category": "basic", "icon": "fa-hammer"},
    {"name": "Moon Flip", "id": "909000022", "category": "basic", "icon": "fa-moon"},
    {"name": "Wiggle Walk", "id": "909000023", "category": "basic", "icon": "fa-walking"},
    {"name": "Battle Dance", "id": "909000024", "category": "basic", "icon": "fa-helmet-battle"},
    {"name": "High Five", "id": "909000025", "category": "basic", "icon": "fa-hand-spock"},
    {"name": "Shake It Up", "id": "909000026", "category": "basic", "icon": "fa-music"},
    {"name": "Glorious Spin", "id": "909000027", "category": "basic", "icon": "fa-sync"},
    {"name": "Crane Kick", "id": "909000028", "category": "basic", "icon": "fa-shoe-prints"},
    {"name": "Party Dance", "id": "909000029", "category": "basic", "icon": "fa-champagne-glasses"},
    {"name": "Jig Dance", "id": "909000031", "category": "basic", "icon": "fa-music"},
    {"name": "Selfie", "id": "909000032", "category": "basic", "icon": "fa-camera"},
    {"name": "Soul Shaking", "id": "909000033", "category": "basic", "icon": "fa-ghost"},
    {"name": "Pirate's Flag", "id": "909000034", "category": "basic", "icon": "fa-flag"},
    {"name": "Healing Dance", "id": "909000035", "category": "basic", "icon": "fa-heart-pulse"},
    {"name": "Top DJ", "id": "909000036", "category": "basic", "icon": "fa-headphones"},
    {"name": "Death Glare", "id": "909000037", "category": "basic", "icon": "fa-eye"},
    {"name": "Power of Money", "id": "909000038", "category": "basic", "icon": "fa-money-bill"},
    {"name": "Eat My Dust", "id": "909000039", "category": "basic", "icon": "fa-wind"},
    {"name": "Breakdance", "id": "909000040", "category": "basic", "icon": "fa-user-ninja"},
    {"name": "Kungfu", "id": "909000041", "category": "basic", "icon": "fa-user-ninja"},
    {"name": "Bon Appetit", "id": "909000042", "category": "basic", "icon": "fa-utensils"},
    {"name": "Aim; Fire!", "id": "909000043", "category": "basic", "icon": "fa-crosshairs"},
    {"name": "The Swan", "id": "909000044", "category": "basic", "icon": "fa-dove"},
    {"name": "I Heart You", "id": "909000045", "category": "basic", "icon": "fa-heart"},
    {"name": "Tea Time", "id": "909000046", "category": "basic", "icon": "fa-mug-hot"},
    {"name": "Bring It On!", "id": "909000047", "category": "basic", "icon": "fa-trophy"},
    {"name": "Why? Oh Why?", "id": "909000048", "category": "basic", "icon": "fa-question"},
    {"name": "Fancy Hands", "id": "909000049", "category": "basic", "icon": "fa-hand-sparkles"},
    {"name": "Shimmy", "id": "909000051", "category": "basic", "icon": "fa-person-dancing"},
    
    # EVO Gun Emotes
    {"name": "🔥 EVO M4A1 MAX", "id": "909033001", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO AK47 MAX", "id": "909000063", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO SHOTGUN MAX", "id": "909035007", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO SCAR MAX", "id": "909000068", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO XMB MAX", "id": "909000085", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO G18 MAX", "id": "909038012", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO MP40 MAX", "id": "909040010", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO FAMAS MAX", "id": "909000090", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO UMP MAX", "id": "909000098", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO WOODPECKER MAX", "id": "909042008", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO GROZA MAX", "id": "909041005", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO THOMPSON MAX", "id": "909038010", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO PARAFAL MAX", "id": "909045001", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO P90 MAX", "id": "909049010", "category": "evo", "icon": "fa-gun"},
    {"name": "🔥 EVO M60 MAX", "id": "909051003", "category": "evo", "icon": "fa-gun"},
    
    # Special Emotes
    {"name": "🐍 COBRA RISING", "id": "909000075", "category": "special", "icon": "fa-fire"},
    {"name": "👻 DRACO'S SOUL", "id": "909000081", "category": "special", "icon": "fa-ghost"},
    {"name": "💀 BLOOD WRAITH", "id": "909000090", "category": "special", "icon": "fa-skull"},
    {"name": "🦅 FFWS 2021", "id": "909000080", "category": "special", "icon": "fa-trophy"},
    {"name": "👍 Good Game", "id": "909000082", "category": "special", "icon": "fa-thumbs-up"},
    {"name": "👋 Greetings", "id": "909000083", "category": "special", "icon": "fa-hand-peace"},
    {"name": "🚶 The Walker", "id": "909000084", "category": "special", "icon": "fa-walking"},
    {"name": "💡 Born of Light", "id": "909000085", "category": "special", "icon": "fa-lightbulb"},
    {"name": "⚡ Mythos Four", "id": "909000086", "category": "special", "icon": "fa-bolt"},
    {"name": "🏆 Champion Grab", "id": "909000087", "category": "special", "icon": "fa-trophy"},
    {"name": "❄️ Win and Chill", "id": "909000088", "category": "special", "icon": "fa-snowflake"},
    {"name": "🔥 Hadouken", "id": "909000089", "category": "special", "icon": "fa-fire"},
    {"name": "👹 Big Smash", "id": "909000091", "category": "special", "icon": "fa-fist-raised"},
    {"name": "💃 Fancy Steps", "id": "909000092", "category": "special", "icon": "fa-shoe-prints"},
    {"name": "🎮 All In Control", "id": "909000093", "category": "special", "icon": "fa-gamepad"},
    {"name": "🔧 Debugging", "id": "909000094", "category": "special", "icon": "fa-screwdriver-wrench"},
    {"name": "👋 Waggor Wave", "id": "909000095", "category": "special", "icon": "fa-hand-wave"},
    {"name": "🎸 Crazy Guitar", "id": "909000096", "category": "special", "icon": "fa-guitar"},
    {"name": "✨ Poof", "id": "909000097", "category": "special", "icon": "fa-wand-sparkles"},
    {"name": "👑 The Chosen Victor", "id": "909000098", "category": "special", "icon": "fa-crown"},
    {"name": "⚔️ Challenger", "id": "909000099", "category": "special", "icon": "fa-crosshairs"},
    
    # More Emotes (100-150)
    {"name": "🏆 Victory Pose", "id": "909000100", "category": "special", "icon": "fa-trophy"},
    {"name": "😄 Laughing", "id": "909000101", "category": "basic", "icon": "fa-laugh"},
    {"name": "😢 Crying", "id": "909000102", "category": "basic", "icon": "fa-sad-cry"},
    {"name": "😠 Angry", "id": "909000103", "category": "basic", "icon": "fa-angry"},
    {"name": "😲 Surprised", "id": "909000104", "category": "basic", "icon": "fa-surprise"},
    {"name": "💃 Dancing", "id": "909000105", "category": "basic", "icon": "fa-music"},
    {"name": "😴 Sleeping", "id": "909000106", "category": "basic", "icon": "fa-bed"},
    {"name": "🍔 Eating", "id": "909000107", "category": "basic", "icon": "fa-hamburger"},
    {"name": "🥤 Drinking", "id": "909000108", "category": "basic", "icon": "fa-mug-hot"},
    {"name": "👏 Clapping", "id": "909000109", "category": "basic", "icon": "fa-hands-clapping"},
    {"name": "👋 Waving", "id": "909000110", "category": "basic", "icon": "fa-hand-wave"},
    {"name": "👉 Pointing", "id": "909000111", "category": "basic", "icon": "fa-hand-point-right"},
    {"name": "👍 Thumbs Up", "id": "909000112", "category": "basic", "icon": "fa-thumbs-up"},
    {"name": "👎 Thumbs Down", "id": "909000113", "category": "basic", "icon": "fa-thumbs-down"},
    {"name": "👌 OK Sign", "id": "909000114", "category": "basic", "icon": "fa-hand-ok"},
    {"name": "✌️ Peace Sign", "id": "909000115", "category": "basic", "icon": "fa-hand-peace"},
    {"name": "🤘 Rock On", "id": "909000116", "category": "basic", "icon": "fa-hand-rock"},
    {"name": "🤦 Facepalm", "id": "909000117", "category": "basic", "icon": "fa-face-palm"},
    {"name": "🤷 Shrug", "id": "909000118", "category": "basic", "icon": "fa-person-shrugging"},
    {"name": "🙇 Bow", "id": "909000119", "category": "basic", "icon": "fa-person-bow"},
    {"name": "🎖️ Salute", "id": "909000120", "category": "basic", "icon": "fa-hand-salute"},
    
    # Legendary Emotes
    {"name": "🐉 Dragon Slayer", "id": "909050001", "category": "legendary", "icon": "fa-dragon"},
    {"name": "🔥 Phoenix Rise", "id": "909050002", "category": "legendary", "icon": "fa-fire"},
    {"name": "👹 Titan Smash", "id": "909050003", "category": "legendary", "icon": "fa-fist-raised"},
    {"name": "👼 Valkyrie Wings", "id": "909050004", "category": "legendary", "icon": "fa-dove"},
    {"name": "🗡️ Samurai Strike", "id": "909050005", "category": "legendary", "icon": "fa-sword"},
    {"name": "🥷 Ninja Vanish", "id": "909050006", "category": "legendary", "icon": "fa-user-ninja"},
    {"name": "🧙 Wizard Spell", "id": "909050007", "category": "legendary", "icon": "fa-hat-wizard"},
    {"name": "🛡️ Knight Honor", "id": "909050008", "category": "legendary", "icon": "fa-shield"},
    {"name": "🗡️ Assassin Stealth", "id": "909050009", "category": "legendary", "icon": "fa-user-secret"},
    {"name": "😡 Berserker Rage", "id": "909050010", "category": "legendary", "icon": "fa-angry"},
]

# Add more emotes (1000-1100)
for i in range(1000, 1101):
    ALL_EMOTES.append({
        "name": f"Emote {i}",
        "id": f"9090{i:04d}",
        "category": "special",
        "icon": "fa-star"
    })

# -------------------- COMMAND MANAGER --------------------
class CommandManager:
    def __init__(self):
        self.commands_file = "commands.json"
        self.initialize_file()
    
    def initialize_file(self):
        if not os.path.exists(self.commands_file):
            with open(self.commands_file, 'w') as f:
                json.dump({"commands": [], "last_id": 0, "stats": {"total": 0, "today": 0}}, f)
    
    def save_command(self, team_code, emote_id, target_uid, user_ip):
        try:
            with open(self.commands_file, 'r') as f:
                data = json.load(f)
            
            command_id = data["last_id"] + 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Find emote name
            emote_name = "Unknown"
            for emote in ALL_EMOTES:
                if emote["id"] == emote_id:
                    emote_name = emote["name"]
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
                "executed": False
            }
            
            data["commands"].append(command)
            data["last_id"] = command_id
            data["stats"]["total"] += 1
            
            with open(self.commands_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return command_id
        except Exception as e:
            print(f"Error saving command: {e}")
            return None

command_manager = CommandManager()

# -------------------- HTML TEMPLATE --------------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 ASHISH EMOTE PANEL</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --primary: #ff0000;
            --secondary: #00ff00;
            --accent: #00ffff;
            --dark: #0a0a0a;
            --gradient: linear-gradient(135deg, #ff0000 0%, #ff00ff 50%, #00ffff 100%);
            --evo-gradient: linear-gradient(135deg, #ff5500 0%, #ff0000 100%);
            --special-gradient: linear-gradient(135deg, #00ff88 0%, #00aaff 100%);
            --basic-gradient: linear-gradient(135deg, #aa00ff 0%, #5500ff 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: var(--dark);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            padding: 30px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            border: 2px solid var(--primary);
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(255, 0, 0, 0.2);
        }

        .header h1 {
            font-size: 3rem;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .header h2 {
            color: var(--accent);
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .tab-btn {
            padding: 12px 24px;
            background: rgba(255, 0, 0, 0.2);
            border: 1px solid var(--primary);
            color: white;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            flex: 1;
            min-width: 150px;
            text-align: center;
            font-weight: bold;
        }

        .tab-btn.active {
            background: var(--gradient);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 0, 0, 0.3);
        }

        .tab-content {
            display: none;
            background: rgba(20, 20, 20, 0.8);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
            animation: fadeIn 0.5s;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .tab-content.active {
            display: block;
        }

        /* INPUT FORM */
        .input-form {
            background: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            border: 2px solid rgba(255, 0, 0, 0.3);
        }

        .input-group {
            margin-bottom: 15px;
        }

        .input-group label {
            display: block;
            margin-bottom: 5px;
            color: var(--accent);
            font-weight: bold;
        }

        .input-group input {
            width: 100%;
            padding: 12px;
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid var(--primary);
            border-radius: 8px;
            color: white;
            font-size: 16px;
        }

        /* EMOTE GRID */
        .section-title {
            color: var(--accent);
            margin: 20px 0;
            font-size: 1.8rem;
            text-align: center;
        }

        .emote-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .emote-card {
            background: rgba(0, 0, 0, 0.6);
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
        }

        .emote-card.evo { border: 2px solid #ff5500; }
        .emote-card.special { border: 2px solid #00ff88; }
        .emote-card.basic { border: 2px solid #aa00ff; }
        .emote-card.legendary { border: 2px solid #ffaa00; }

        .emote-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(255, 255, 255, 0.1);
        }

        .emote-icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        .emote-card.evo .emote-icon { color: #ff5500; }
        .emote-card.special .emote-icon { color: #00ff88; }
        .emote-card.basic .emote-icon { color: #aa00ff; }
        .emote-card.legendary .emote-icon { color: #ffaa00; }

        .emote-name {
            font-size: 1.2rem;
            margin-bottom: 10px;
            color: white;
        }

        .emote-id {
            background: rgba(255, 255, 255, 0.1);
            color: #aaa;
            padding: 5px 10px;
            border-radius: 15px;
            font-family: monospace;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }

        .send-btn {
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            font-weight: bold;
            transition: all 0.3s;
        }
        .emote-card.evo .send-btn { background: var(--evo-gradient); }
        .emote-card.special .send-btn { background: var(--special-gradient); }
        .emote-card.basic .send-btn { background: var(--basic-gradient); }
        .emote-card.legendary .send-btn { background: linear-gradient(135deg, #ffaa00, #ff5500); }

        .send-btn:hover {
            transform: scale(1.05);
        }

        /* BUTTON */
        .btn {
            background: var(--gradient);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 10px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin: 20px 0;
            transition: all 0.3s;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(255, 0, 0, 0.4);
        }

        /* STATUS */
        .status-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(10, 10, 10, 0.95);
            padding: 15px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-top: 2px solid var(--primary);
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 10px;
            display: none;
            font-weight: bold;
            z-index: 1000;
            animation: slideIn 0.3s;
        }

        @keyframes slideIn {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
        }

        .notification.success {
            background: linear-gradient(135deg, #00ff00, #00cc00);
            color: #000;
        }

        .notification.error {
            background: linear-gradient(135deg, #ff0000, #cc0000);
            color: white;
        }

        /* SEARCH */
        .search-box {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid var(--primary);
            border-radius: 10px;
            color: white;
            font-size: 16px;
            margin-bottom: 20px;
        }

        /* RESPONSIVE */
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .emote-grid { grid-template-columns: 1fr; }
            .status-bar { flex-direction: column; gap: 10px; }
            .tab-btn { min-width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1><i class="fas fa-fire"></i> ASHISH EMOTE PANEL</h1>
            <h2>⚡ All Emotes Collection | Total: {{ total_emotes }} Emotes</h2>
        </div>

        <!-- TABS -->
        <div class="tabs">
            <button class="tab-btn active" onclick="openTab('all')">
                <i class="fas fa-th-large"></i> ALL EMOTES
            </button>
            <button class="tab-btn" onclick="openTab('evo')">
                <i class="fas fa-gun"></i> EVO GUNS
            </button>
            <button class="tab-btn" onclick="openTab('special')">
                <i class="fas fa-star"></i> SPECIAL
            </button>
            <button class="tab-btn" onclick="openTab('status')">
                <i class="fas fa-chart-bar"></i> STATUS
            </button>
        </div>

        <!-- ALL EMOTES TAB -->
        <div id="all" class="tab-content active">
            <h3 class="section-title"><i class="fas fa-th-large"></i> ALL EMOTES ({{ total_emotes }})</h3>
            
            <input type="text" class="search-box" id="searchAll" placeholder="🔍 Search all emotes..." onkeyup="searchAllEmotes()">
            
            <div class="input-form">
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE (7 digits)</label>
                    <input type="text" id="all_team" placeholder="1234567" pattern="\d{7}">
                </div>
                <div class="input-group">
                    <label><i class="fas fa-user"></i> TARGET UID</label>
                    <input type="text" id="all_target" placeholder="4255057762" pattern="\d{8,11}">
                </div>
            </div>

            <div class="emote-grid" id="allEmotesContainer">
                <!-- All emotes will be loaded here -->
            </div>
            
            <button class="btn" onclick="loadMore()">
                <i class="fas fa-sync"></i> LOAD MORE EMOTES
            </button>
        </div>

        <!-- EVO GUNS TAB -->
        <div id="evo" class="tab-content">
            <h3 class="section-title"><i class="fas fa-gun"></i> EVO GUN EMOTES</h3>
            
            <div class="input-form">
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE</label>
                    <input type="text" id="evo_team" placeholder="1234567" pattern="\d{7}">
                </div>
                <div class="input-group">
                    <label><i class="fas fa-user"></i> TARGET UID</label>
                    <input type="text" id="evo_target" placeholder="4255057762" pattern="\d{8,11}">
                </div>
            </div>

            <div class="emote-grid" id="evoEmotesContainer">
                {% for emote in emotes if emote.category == 'evo' %}
                <div class="emote-card evo" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}', 'evo')">
                    <div class="emote-icon">
                        <i class="fas {{ emote.icon }}"></i>
                    </div>
                    <div class="emote-name">{{ emote.name }}</div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <button class="send-btn">
                        <i class="fas fa-paper-plane"></i> SEND
                    </button>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- SPECIAL EMOTES TAB -->
        <div id="special" class="tab-content">
            <h3 class="section-title"><i class="fas fa-star"></i> SPECIAL EMOTES</h3>
            
            <div class="input-form">
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE</label>
                    <input type="text" id="special_team" placeholder="1234567" pattern="\d{7}">
                </div>
                <div class="input-group">
                    <label><i class="fas fa-user"></i> TARGET UID</label>
                    <input type="text" id="special_target" placeholder="4255057762" pattern="\d{8,11}">
                </div>
            </div>

            <div class="emote-grid" id="specialEmotesContainer">
                {% for emote in emotes if emote.category == 'special' %}
                <div class="emote-card special" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}', 'special')">
                    <div class="emote-icon">
                        <i class="fas {{ emote.icon }}"></i>
                    </div>
                    <div class="emote-name">{{ emote.name }}</div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <button class="send-btn">
                        <i class="fas fa-paper-plane"></i> SEND
                    </button>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- STATUS TAB -->
        <div id="status" class="tab-content">
            <h3 class="section-title"><i class="fas fa-chart-bar"></i> SYSTEM STATUS</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px;">
                <div style="background: rgba(0,100,0,0.2); padding: 15px; border-radius: 10px; border: 1px solid #00ff00;">
                    <h4><i class="fas fa-server"></i> WEB PANEL</h4>
                    <p style="color: #00ff00;">🟢 ONLINE</p>
                </div>
                
                <div style="background: rgba(255,165,0,0.2); padding: 15px; border-radius: 10px; border: 1px solid #ffa500;">
                    <h4><i class="fas fa-robot"></i> TERMUX BOT</h4>
                    <p id="botStatus" style="color: #ffa500;">⏳ CHECKING</p>
                </div>
                
                <div style="background: rgba(0,100,255,0.2); padding: 15px; border-radius: 10px; border: 1px solid #00aaff;">
                    <h4><i class="fas fa-commands"></i> COMMANDS</h4>
                    <p id="queueCount" style="color: #00aaff;">0 pending</p>
                </div>
                
                <div style="background: rgba(170,0,255,0.2); padding: 15px; border-radius: 10px; border: 1px solid #aa00ff;">
                    <h4><i class="fas fa-gamepad"></i> TOTAL EMOTES</h4>
                    <p style="color: #aa00ff;">{{ total_emotes }}</p>
                </div>
            </div>
            
            <h4 style="margin: 20px 0 10px 0;"><i class="fas fa-history"></i> RECENT COMMANDS</h4>
            <div id="commandsList" style="
                background: rgba(0,0,0,0.5);
                border-radius: 10px;
                padding: 15px;
                max-height: 300px;
                overflow-y: auto;
            ">
                <p style="text-align: center; color: #aaa;">No commands yet</p>
            </div>
        </div>
    </div>

    <!-- STATUS BAR -->
    <div class="status-bar">
        <div class="status-item">
            <i class="fas fa-circle" style="color: #00ff00;"></i>
            <span>Panel: ONLINE</span>
        </div>
        <div class="status-item">
            <i class="fas fa-robot"></i>
            <span>Bot: <span id="botStatusBar">CHECKING</span></span>
        </div>
        <div class="status-item">
            <i class="fas fa-gamepad"></i>
            <span>Emotes: {{ total_emotes }}</span>
        </div>
        <div class="status-item">
            <i class="fas fa-user"></i>
            <span>ASHISH</span>
        </div>
    </div>

    <!-- NOTIFICATION -->
    <div class="notification" id="notification"></div>

    <script>
        let allEmotesData = {{ emotes|tojson }};
        let currentPage = 0;
        const itemsPerPage = 24;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            displayAllEmotes();
            refreshStatus();
            setInterval(refreshStatus, 5000);
        });
        
        // Tab switching
        function openTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active class from buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Activate clicked button
            event.currentTarget.classList.add('active');
        }
        
        // Display all emotes
        function displayAllEmotes() {
            const container = document.getElementById('allEmotesContainer');
            container.innerHTML = '';
            
            const start = currentPage * itemsPerPage;
            const end = start + itemsPerPage;
            const pageEmotes = allEmotesData.slice(start, end);
            
            pageEmotes.forEach(emote => {
                const card = document.createElement('div');
                card.className = `emote-card ${emote.category}`;
                card.innerHTML = `
                    <div class="emote-icon">
                        <i class="fas ${emote.icon}"></i>
                    </div>
                    <div class="emote-name">${emote.name}</div>
                    <div class="emote-id">ID: ${emote.id}</div>
                    <button class="send-btn" onclick="sendEmoteFromAll('${emote.id}', '${emote.name}', '${emote.category}')">
                        <i class="fas fa-paper-plane"></i> SEND
                    </button>
                `;
                container.appendChild(card);
            });
        }
        
        // Load more emotes
        function loadMore() {
            currentPage++;
            displayAllEmotes();
            showNotification(`Loaded page ${currentPage + 1}`, 'success');
        }
        
        // Search emotes
        function searchAllEmotes() {
            const search = document.getElementById('searchAll').value.toLowerCase();
            const container = document.getElementById('allEmotesContainer');
            
            if (!search) {
                currentPage = 0;
                displayAllEmotes();
                return;
            }
            
            const filtered = allEmotesData.filter(emote => 
                emote.name.toLowerCase().includes(search) || 
                emote.id.includes(search)
            );
            
            container.innerHTML = '';
            filtered.forEach(emote => {
                const card = document.createElement('div');
                card.className = `emote-card ${emote.category}`;
                card.innerHTML = `
                    <div class="emote-icon">
                        <i class="fas ${emote.icon}"></i>
                    </div>
                    <div class="emote-name">${emote.name}</div>
                    <div class="emote-id">ID: ${emote.id}</div>
                    <button class="send-btn" onclick="sendEmoteFromAll('${emote.id}', '${emote.name}', '${emote.category}')">
                        <i class="fas fa-paper-plane"></i> SEND
                    </button>
                `;
                container.appendChild(card);
            });
        }
        
        // Send emote from All tab
        function sendEmoteFromAll(emoteId, emoteName, category) {
            let team, target;
            
            if (category === 'evo') {
                team = document.getElementById('evo_team').value;
                target = document.getElementById('evo_target').value;
            } else if (category === 'special') {
                team = document.getElementById('special_team').value;
                target = document.getElementById('special_target').value;
            } else {
                team = document.getElementById('all_team').value;
                target = document.getElementById('all_target').value;
            }
            
            if (!team || !target) {
                showNotification('❌ Please enter Team Code and Target UID first!', 'error');
                return;
            }
            
            sendCommand(team, emoteId, target, emoteName);
        }
        
        // Send emote from specific tab
        function sendEmote(emoteId, emoteName, category) {
            let team, target;
            
            if (category === 'evo') {
                team = document.getElementById('evo_team').value;
                target = document.getElementById('evo_target').value;
            } else if (category === 'special') {
                team = document.getElementById('special_team').value;
                target = document.getElementById('special_target').value;
            } else {
                team = document.getElementById('all_team').value;
                target = document.getElementById('all_target').value;
            }
            
            if (!team || !target) {
                showNotification('❌ Please enter Team Code and Target UID first!', 'error');
                return;
            }
            
            sendCommand(team, emoteId, target, emoteName);
        }
        
        // Send command to server
        function sendCommand(team, emote, target, emoteName = '') {
            // Validation
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
            
            showNotification('📤 Sending command...', 'success');
            
            fetch('/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `team_code=${team}&emote_id=${emote}&target_uid=${target}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification(`✅ ${emoteName} sent to UID ${target}!`, 'success');
                    refreshStatus();
                } else {
                    showNotification(`❌ Error: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showNotification('❌ Network error!', 'error');
            });
        }
        
        // Show notification
        function showNotification(message, type = 'success') {
            const notif = document.getElementById('notification');
            notif.textContent = message;
            notif.className = `notification ${type}`;
            notif.style.display = 'block';
            
            setTimeout(() => {
                notif.style.display = 'none';
            }, 3000);
        }
        
        // Refresh status
        function refreshStatus() {
            fetch('/status')
                .then(r => r.json())
                .then(data => {
                    // Update bot status
                    const botStatus = document.getElementById('botStatus');
                    const botStatusBar = document.getElementById('botStatusBar');
                    
                    if (data.bot_connected) {
                        botStatus.innerHTML = '🟢 CONNECTED';
                        botStatus.style.color = '#00ff00';
                        botStatusBar.innerHTML = 'CONNECTED';
                        botStatusBar.style.color = '#00ff00';
                    } else {
                        botStatus.innerHTML = '🔴 NOT CONNECTED';
                        botStatus.style.color = '#ff0000';
                        botStatusBar.innerHTML = 'NOT CONNECTED';
                        botStatusBar.style.color = '#ff0000';
                    }
                    
                    // Update queue count
                    document.getElementById('queueCount').innerHTML = 
                        `${data.pending_commands} pending`;
                    
                    // Load commands
                    loadCommands();
                });
        }
        
        // Load commands
        function loadCommands() {
            const commandsList = document.getElementById('commandsList');
            
            fetch('/get_commands')
                .then(r => r.json())
                .then(data => {
                    commandsList.innerHTML = '';
                    
                    if (data.commands.length === 0) {
                        commandsList.innerHTML = '<p style="text-align: center; color: #aaa;">No commands yet</p>';
                        return;
                    }
                    
                    // Show last 5 commands
                    const recent = data.commands.slice(-5).reverse();
                    
                    recent.forEach(cmd => {
                        const item = document.createElement('div');
                        item.style.cssText = `
                            background: rgba(255,255,255,0.05);
                            padding: 10px;
                            margin-bottom: 8px;
                            border-radius: 8px;
                            border-left: 4px solid #00ffff;
                            font-size: 0.9rem;
                        `;
                        item.innerHTML = `
                            <div><strong>#${cmd.id}</strong> | ${cmd.timestamp.split(' ')[1]}</div>
                            <div>${cmd.emote_name}</div>
                            <div>Team: ${cmd.team_code} | Target: ${cmd.target_uid}</div>
                            <div style="color: ${cmd.status === 'executed' ? '#00ff00' : '#ffff00'}">
                                ${cmd.status === 'executed' ? '✅ EXECUTED' : '⏳ PENDING'}
                            </div>
                        `;
                        commandsList.appendChild(item);
                    });
                });
        }
    </script>
</body>
</html>
'''

# -------------------- FLASK ROUTES --------------------
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, 
                                  emotes=ALL_EMOTES,
                                  total_emotes=len(ALL_EMOTES))

@app.route('/send', methods=['POST'])
def send_command():
    try:
        team_code = request.form.get('team_code', '').strip()
        emote_id = request.form.get('emote_id', '').strip()
        target_uid = request.form.get('target_uid', '').strip()
        
        if not re.match(r'^\d{7}$', team_code):
            return jsonify({"success": False, "error": "Team code must be 7 digits"})
        
        if not re.match(r'^\d{8,11}$', target_uid):
            return jsonify({"success": False, "error": "Target UID must be 8-11 digits"})
        
        if not re.match(r'^\d{9}$', emote_id):
            return jsonify({"success": False, "error": "Emote ID must be 9 digits"})
        
        user_ip = request.remote_addr
        command_id = command_manager.save_command(team_code, emote_id, target_uid, user_ip)
        
        if command_id:
            return jsonify({
                "success": True,
                "message": f"Command #{command_id} saved!",
                "command_id": command_id
            })
        else:
            return jsonify({"success": False, "error": "Failed to save command"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/status')
def status():
    try:
        with open("commands.json", 'r') as f:
            data = json.load(f)
        
        pending = [cmd for cmd in data["commands"] if not cmd.get("executed", False)]
        
        return jsonify({
            "bot_connected": len(pending) > 0,
            "pending_commands": len(pending),
            "total_commands": data.get("stats", {}).get("total", 0)
        })
    except:
        return jsonify({
            "bot_connected": False,
            "pending_commands": 0,
            "total_commands": 0
        })

@app.route('/get_commands')
def get_commands():
    try:
        with open("commands.json", 'r') as f:
            data = json.load(f)
        
        # Return all commands
        return jsonify({"commands": data["commands"]})
    except:
        return jsonify({"commands": []})

# -------------------- MAIN --------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
