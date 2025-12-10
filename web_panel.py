from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ashish-premium-panel-2024')

# ==================== EMOTE DATABASE ====================
EMOTE_DATABASE = {
    "EVO_GUNS": [
        {"name": "🔥 EVO MP40", "id": "909000075", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO AK", "id": "909000063", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO UMP", "id": "909000098", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO XMB", "id": "909000065", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO SCAR", "id": "909000068", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO M10", "id": "909000081", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO FAMAS", "id": "909000090", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO MP5", "id": "909033002", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO M1887", "id": "909035007", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO WOODPECKER", "id": "909042008", "icon": "fa-gun", "rarity": "legendary"},
    ],
    
    "SPECIAL_EMOTES": [
        {"name": "💰 PAISA EMOTE", "id": "909000055", "icon": "fa-money-bill-wave", "rarity": "epic"},
        {"name": "💖 HEART EMOTE", "id": "909000045", "icon": "fa-heart", "rarity": "epic"},
        {"name": "🌹 ROSE EMOTE", "id": "909000010", "icon": "fa-rose", "rarity": "epic"},
        {"name": "👑 THRONE EMOTE", "id": "909000014", "icon": "fa-crown", "rarity": "legendary"},
        {"name": "🏴‍☠️ PIRATE'S FLAG", "id": "909000034", "icon": "fa-flag", "rarity": "epic"},
        {"name": "💨 EAT MY DUST", "id": "909000039", "icon": "fa-wind", "rarity": "epic"},
        {"name": "😂 LOL EMOTE", "id": "909000002", "icon": "fa-laugh", "rarity": "rare"},
        {"name": "🐍 COBRA EMOTE", "id": "909000072", "icon": "fa-snake", "rarity": "legendary"},
        {"name": "👻 GHOST EMOTE", "id": "909036001", "icon": "fa-ghost", "rarity": "epic"},
        {"name": "🔥 FIRE ON EMOTE", "id": "909033001", "icon": "fa-fire", "rarity": "legendary"},
        {"name": "🎬 SHOLAY EMOTE", "id": "909050020", "icon": "fa-film", "rarity": "epic"},
        {"name": "⭐ PRIME 8 EMOTE", "id": "909035013", "icon": "fa-star", "rarity": "legendary"},
    ],
    
    "POPULAR_EMOTES": [
        {"name": "👋 Hello!", "id": "909000001", "icon": "fa-hand-wave", "rarity": "common"},
        {"name": "😤 Provoke", "id": "909000003", "icon": "fa-fist-raised", "rarity": "common"},
        {"name": "👏 Applause", "id": "909000004", "icon": "fa-hands-clapping", "rarity": "common"},
        {"name": "💃 Dab", "id": "909000005", "icon": "fa-person-dancing", "rarity": "common"},
        {"name": "🐔 Chicken", "id": "909000006", "icon": "fa-drumstick", "rarity": "common"},
        {"name": "👋 Arm Wave", "id": "909000007", "icon": "fa-hand", "rarity": "common"},
        {"name": "💃 Shoot Dance", "id": "909000008", "icon": "fa-gun", "rarity": "common"},
        {"name": "🦈 Baby Shark", "id": "909000009", "icon": "fa-fish", "rarity": "rare"},
        {"name": "🧟 Mummy Dance", "id": "909000011", "icon": "fa-ghost", "rarity": "rare"},
        {"name": "🕺 Shuffling", "id": "909000013", "icon": "fa-person-running", "rarity": "common"},
        {"name": "🐉 Dragon Fist", "id": "909000015", "icon": "fa-dragon", "rarity": "epic"},
        {"name": "🎯 Dangerous Game", "id": "909000016", "icon": "fa-bullseye", "rarity": "rare"},
        {"name": "🐆 Jaguar Dance", "id": "909000017", "icon": "fa-paw", "rarity": "rare"},
    ],
    
    "DANCE_EMOTES": [
        {"name": "💃 Breakdance", "id": "909000040", "icon": "fa-person-dancing", "rarity": "rare"},
        {"name": "🥋 Kungfu", "id": "909000041", "icon": "fa-user-ninja", "rarity": "rare"},
        {"name": "🍽️ Bon Appetit", "id": "909000042", "icon": "fa-utensils", "rarity": "common"},
        {"name": "🎯 Aim; Fire!", "id": "909000043", "icon": "fa-crosshairs", "rarity": "common"},
        {"name": "🦢 The Swan", "id": "909000044", "icon": "fa-dove", "rarity": "rare"},
        {"name": "💕 I Heart You", "id": "909000045", "icon": "fa-heart", "rarity": "common"},
        {"name": "☕ Tea Time", "id": "909000046", "icon": "fa-mug-hot", "rarity": "common"},
        {"name": "🥊 Bring It On!", "id": "909000047", "icon": "fa-fist-raised", "rarity": "common"},
        {"name": "🤔 Why? Oh Why?", "id": "909000048", "icon": "fa-question", "rarity": "common"},
        {"name": "💅 Fancy Hands", "id": "909000049", "icon": "fa-hand-sparkles", "rarity": "rare"},
        {"name": "💃 Shimmy", "id": "909000051", "icon": "fa-person-dancing", "rarity": "common"},
        {"name": "🐶 Doggie", "id": "909000052", "icon": "fa-dog", "rarity": "common"},
    ],
    
    "LEGENDARY_EMOTES": [
        {"name": "👑 FFWC THRONE", "id": "909000014", "icon": "fa-crown", "rarity": "legendary"},
        {"name": "🐉 DRAGON FIST", "id": "909000015", "icon": "fa-dragon", "rarity": "legendary"},
        {"name": "👑 CHAMPION GRAB", "id": "909000087", "icon": "fa-trophy", "rarity": "legendary"},
        {"name": "🔥 HADOUKEN", "id": "909000089", "icon": "fa-fire", "rarity": "legendary"},
        {"name": "💀 BLOOD WRAITH", "id": "909000090", "icon": "fa-skull", "rarity": "legendary"},
        {"name": "👑 THE CHOSEN VICTOR", "id": "909000098", "icon": "fa-crown", "rarity": "legendary"},
        {"name": "🏆 FFWS 2021", "id": "909000080", "icon": "fa-trophy", "rarity": "legendary"},
        {"name": "💡 BORN OF LIGHT", "id": "909000085", "icon": "fa-lightbulb", "rarity": "legendary"},
        {"name": "🌟 DANCE OF CONSTELLATION", "id": "909037003", "icon": "fa-star", "rarity": "legendary"},
        {"name": "💃 MACARENA", "id": "909038002", "icon": "fa-music", "rarity": "legendary"},
    ],
    
    "2024_EMOTES": [
        {"name": "💨 MONEY RAIN", "id": "909042002", "icon": "fa-money-bill-wave", "rarity": "epic"},
        {"name": "❄️ FROSTFIRE'S CALLING", "id": "909042003", "icon": "fa-snowflake", "rarity": "epic"},
        {"name": "🧊 GLOO SCULPTURE", "id": "909042007", "icon": "fa-snowman", "rarity": "legendary"},
        {"name": "🐅 REAL TIGER?", "id": "909042008", "icon": "fa-paw", "rarity": "epic"},
        {"name": "🎿 CELEBRATION SCHUSS", "id": "909042009", "icon": "fa-person-skiing", "rarity": "epic"},
        {"name": "⛵ DAWN VOYAGE", "id": "909042011", "icon": "fa-sailboat", "rarity": "legendary"},
        {"name": "🏎️ LAMBORGHINI RIDE", "id": "909042012", "icon": "fa-car", "rarity": "mythic"},
        {"name": "👋 FROSTFIRE HELLO", "id": "909042013", "icon": "fa-snowflake", "rarity": "epic"},
        {"name": "🎭 KEMUSAN", "id": "909042018", "icon": "fa-mask", "rarity": "legendary"},
        {"name": "🐸 RIBBIT RIDER", "id": "909043001", "icon": "fa-frog", "rarity": "epic"},
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
    }
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
            
            # Get today's date for tracking daily commands
            today = datetime.now().strftime("%Y-%m-%d")
            self.storage["stats"]["today"] += 1
            
            print(f"✅ Command #{command_id} saved: {emote_name}")
            return command_id
            
        except Exception as e:
            print(f"❌ Save error: {e}")
            return None

command_manager = CommandManager()

# ==================== HTML TEMPLATE ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 ASHISH | PROFESSIONAL EMOTE PANEL</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Roboto+Mono:wght@300;400;500&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --secondary: #10b981;
            --accent: #f59e0b;
            --danger: #ef4444;
            --success: #10b981;
            --dark: #111827;
            --darker: #0f172a;
            --light: #f8fafc;
            --gray: #64748b;
            --gray-light: #e2e8f0;
            --gray-dark: #334155;
            
            --card-bg: rgba(255, 255, 255, 0.03);
            --border-color: rgba(255, 255, 255, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: var(--light);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
            line-height: 1.6;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* ================= HEADER ================= */
        .header {
            text-align: center;
            padding: 40px 30px;
            margin-bottom: 40px;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(16, 185, 129, 0.1));
            border-radius: 20px;
            border: 1px solid var(--border-color);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }

        .logo {
            font-family: 'Montserrat', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            color: var(--light);
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }

        .logo .highlight {
            color: var(--primary);
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .tagline {
            font-size: 1.2rem;
            color: var(--gray-light);
            margin-bottom: 30px;
            font-weight: 400;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .stat-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid var(--border-color);
            text-align: center;
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            border-color: var(--primary);
            transform: translateY(-5px);
        }

        .stat-value {
            font-family: 'Roboto Mono', monospace;
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--primary);
            margin: 10px 0;
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--gray-light);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 500;
        }

        /* ================= TABS ================= */
        .tabs-container {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid var(--border-color);
        }

        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }

        .tab-btn {
            padding: 15px 25px;
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--gray-light);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .tab-btn:hover {
            background: rgba(37, 99, 235, 0.1);
            border-color: var(--primary);
            color: var(--light);
        }

        .tab-btn.active {
            background: var(--primary);
            border-color: var(--primary);
            color: white;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* ================= QUICK SEND ================= */
        .quick-send {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid var(--border-color);
        }

        .section-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--light);
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .section-title i {
            color: var(--primary);
        }

        .input-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .input-group {
            position: relative;
        }

        .input-group label {
            display: block;
            margin-bottom: 8px;
            color: var(--gray-light);
            font-weight: 500;
            font-size: 0.95rem;
        }

        .input-wrapper {
            position: relative;
        }

        .input-wrapper input {
            width: 100%;
            padding: 15px 20px 15px 45px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            color: var(--light);
            font-size: 1rem;
            font-family: 'Roboto Mono', monospace;
            transition: all 0.3s ease;
        }

        .input-wrapper i {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--gray);
        }

        .input-wrapper input:focus {
            outline: none;
            border-color: var(--primary);
            background: rgba(37, 99, 235, 0.05);
        }

        .input-wrapper input::placeholder {
            color: var(--gray);
        }

        /* ================= EMOTE CATEGORIES ================= */
        .category-section {
            margin: 40px 0;
        }

        .category-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .category-title {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--light);
        }

        .emote-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }

        .emote-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 15px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .emote-card:hover {
            border-color: var(--primary);
            transform: translateY(-3px);
            background: rgba(37, 99, 235, 0.05);
        }

        .emote-card-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }

        .emote-icon {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.3rem;
        }

        .emote-info {
            flex: 1;
        }

        .emote-name {
            font-weight: 600;
            font-size: 1.1rem;
            color: var(--light);
            margin-bottom: 5px;
        }

        .emote-id {
            font-family: 'Roboto Mono', monospace;
            font-size: 0.85rem;
            color: var(--gray);
        }

        .emote-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }

        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
            flex: 1;
        }

        .btn-primary:hover {
            background: var(--primary-dark);
        }

        .btn-secondary {
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--gray-light);
        }

        .btn-secondary:hover {
            border-color: var(--primary);
            color: var(--light);
        }

        /* ================= ACTION BUTTONS ================= */
        .action-buttons {
            display: flex;
            gap: 15px;
            margin: 30px 0;
        }

        .action-btn {
            padding: 18px 30px;
            border: none;
            border-radius: 15px;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .action-btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            flex: 1;
        }

        .action-btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
        }

        /* ================= STATUS PANEL ================= */
        .status-panel {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 30px;
            margin-top: 40px;
            border: 1px solid var(--border-color);
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .status-card {
            background: rgba(255, 255, 255, 0.02);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid var(--border-color);
        }

        .status-value {
            font-family: 'Roboto Mono', monospace;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 15px 0;
        }

        .status-online { color: var(--success); }
        .status-offline { color: var(--danger); }
        .status-pending { color: var(--accent); }

        .status-label {
            color: var(--gray-light);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* ================= FOOTER ================= */
        .footer {
            margin-top: 50px;
            padding: 25px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 20px;
            border-top: 1px solid var(--border-color);
        }

        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .footer-section {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .footer-section i {
            color: var(--primary);
            font-size: 1.2rem;
        }

        .footer-text {
            color: var(--gray-light);
            font-size: 0.9rem;
        }

        .footer-text strong {
            color: var(--light);
            font-weight: 600;
        }

        /* ================= NOTIFICATION ================= */
        .notification {
            position: fixed;
            top: 30px;
            right: 30px;
            padding: 20px 25px;
            border-radius: 12px;
            display: none;
            font-weight: 500;
            z-index: 1000;
            max-width: 350px;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .notification.success {
            background: var(--success);
            color: white;
            border-left: 4px solid #059669;
        }

        .notification.error {
            background: var(--danger);
            color: white;
            border-left: 4px solid #dc2626;
        }

        /* ================= RESPONSIVE ================= */
        @media (max-width: 1024px) {
            .emote-grid {
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            }
        }

        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .logo {
                font-size: 2.5rem;
            }
            
            .tabs {
                flex-direction: column;
            }
            
            .tab-btn {
                width: 100%;
                justify-content: center;
            }
            
            .action-buttons {
                flex-direction: column;
            }
            
            .footer-content {
                flex-direction: column;
                text-align: center;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 480px) {
            .emote-grid {
                grid-template-columns: 1fr;
            }
            
            .input-grid {
                grid-template-columns: 1fr;
            }
            
            .status-grid {
                grid-template-columns: 1fr;
            }
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
                <span class="highlight">ASHISH</span> EMOTE PANEL
            </h1>
            <p class="tagline">Professional Emote Delivery System • 400+ Emotes Available • Real-time Execution</p>
            
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
                    <div class="stat-value" id="onlineUsers">1</div>
                    <div class="stat-label">ONLINE USERS</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="responseTime">0ms</div>
                    <div class="stat-label">RESPONSE TIME</div>
                </div>
            </div>
        </div>

        <!-- QUICK SEND -->
        <div class="quick-send">
            <h2 class="section-title">
                <i class="fas fa-bolt"></i> QUICK EMOTE SEND
            </h2>
            
            <div class="input-grid">
                <div class="input-group">
                    <label><i class="fas fa-hashtag"></i> TEAM CODE</label>
                    <div class="input-wrapper">
                        <i class="fas fa-users"></i>
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
                        <i class="fas fa-code"></i>
                        <input type="text" id="emoteId" placeholder="909033001" pattern="\d{9}" required>
                    </div>
                </div>
            </div>

            <div class="action-buttons">
                <button class="action-btn action-btn-primary" onclick="sendQuickCommand()">
                    <i class="fas fa-paper-plane"></i> SEND EMOTE COMMAND
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
                    <i class="fas fa-calendar"></i> 2024 EMOTES
                </button>
            </div>

            <!-- EVO GUNS TAB -->
            <div id="evo" class="tab-content active">
                <div class="category-section">
                    <div class="category-header">
                        <h3 class="category-title">EVO GUN EMOTES</h3>
                    </div>
                    <div class="emote-grid">
                        {% for emote in evo_emotes %}
                        <div class="emote-card" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-card-header">
                                <div class="emote-icon">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">{{ emote.id }}</div>
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
                <div class="category-section">
                    <div class="category-header">
                        <h3 class="category-title">SPECIAL EMOTES</h3>
                    </div>
                    <div class="emote-grid">
                        {% for emote in special_emotes %}
                        <div class="emote-card" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-card-header">
                                <div class="emote-icon">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">{{ emote.id }}</div>
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
                <div class="category-section">
                    <div class="category-header">
                        <h3 class="category-title">POPULAR EMOTES</h3>
                    </div>
                    <div class="emote-grid">
                        {% for emote in popular_emotes %}
                        <div class="emote-card" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-card-header">
                                <div class="emote-icon">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">{{ emote.id }}</div>
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
                <div class="category-section">
                    <div class="category-header">
                        <h3 class="category-title">DANCE EMOTES</h3>
                    </div>
                    <div class="emote-grid">
                        {% for emote in dance_emotes %}
                        <div class="emote-card" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-card-header">
                                <div class="emote-icon">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">{{ emote.id }}</div>
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
                <div class="category-section">
                    <div class="category-header">
                        <h3 class="category-title">LEGENDARY EMOTES</h3>
                    </div>
                    <div class="emote-grid">
                        {% for emote in legendary_emotes %}
                        <div class="emote-card" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-card-header">
                                <div class="emote-icon">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">{{ emote.id }}</div>
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
                <div class="category-section">
                    <div class="category-header">
                        <h3 class="category-title">2024 EMOTES</h3>
                    </div>
                    <div class="emote-grid">
                        {% for emote in new_2024_emotes %}
                        <div class="emote-card" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                            <div class="emote-card-header">
                                <div class="emote-icon">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-info">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">{{ emote.id }}</div>
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
        <div class="status-panel">
            <h2 class="section-title">
                <i class="fas fa-chart-line"></i> SYSTEM STATUS
            </h2>
            
            <div class="status-grid">
                <div class="status-card">
                    <div class="status-label">WEB PANEL</div>
                    <div class="status-value status-online">ONLINE</div>
                    <div class="status-label">Ready to Serve</div>
                </div>
                
                <div class="status-card">
                    <div class="status-label">COMMANDS TODAY</div>
                    <div class="status-value" id="todayCommands">0</div>
                    <div class="status-label">Total Sent</div>
                </div>
                
                <div class="status-card">
                    <div class="status-label">AVG RESPONSE</div>
                    <div class="status-value" id="avgResponse">0ms</div>
                    <div class="status-label">Latency</div>
                </div>
                
                <div class="status-card">
                    <div class="status-label">UPTIME</div>
                    <div class="status-value">100%</div>
                    <div class="status-label">System Stability</div>
                </div>
            </div>
        </div>

        <!-- FOOTER -->
        <div class="footer">
            <div class="footer-content">
                <div class="footer-section">
                    <i class="fas fa-shield-alt"></i>
                    <div class="footer-text">
                        <strong>SECURE CONNECTION</strong><br>
                        Encrypted & Protected
                    </div>
                </div>
                
                <div class="footer-section">
                    <i class="fas fa-bolt"></i>
                    <div class="footer-text">
                        <strong>400+ EMOTES</strong><br>
                        Instant Delivery
                    </div>
                </div>
                
                <div class="footer-section">
                    <i class="fas fa-user-tie"></i>
                    <div class="footer-text">
                        <strong>DEVELOPER</strong><br>
                        Ashish Shakya
                    </div>
                </div>
                
                <div class="footer-section">
                    <i class="fas fa-code"></i>
                    <div class="footer-text">
                        <strong>VERSION 3.0</strong><br>
                        Professional Edition
                    </div>
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
            
            // Initialize stats
            updateStats();
            
            // Auto-refresh stats every 10 seconds
            setInterval(updateStats, 10000);
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
            showNotification(`✓ Selected: ${emoteName}`, 'success');
            
            // Copy to clipboard
            navigator.clipboard.writeText(emoteId).then(() => {
                // Success message is already shown
            });
        }
        
        function sendEmote(emoteId, event) {
            if (event) {
                event.stopPropagation();
            }
            
            const team = document.getElementById('teamCode').value;
            const target = document.getElementById('targetUid').value;
            
            if (!team || !target) {
                showNotification('Please enter Team Code and Target UID first', 'error');
                return;
            }
            
            sendCommand(team, emoteId, target);
        }
        
        function sendQuickCommand() {
            const team = document.getElementById('teamCode').value;
            const target = document.getElementById('targetUid').value;
            const emote = document.getElementById('emoteId').value;
            
            if (!team || !target || !emote) {
                showNotification('Please fill all fields', 'error');
                return;
            }
            
            sendCommand(team, emote, target);
        }
        
        // Send command
        function sendCommand(team, emote, target) {
            const startTime = Date.now();
            const sendBtn = document.querySelector('.action-btn-primary');
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
                    
                    showNotification(`✓ Emote sent to UID ${target}`, 'success');
                } else {
                    showNotification(`✗ Error: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showNotification('✗ Network error. Check connection', 'error');
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
                    
                    // Update online users based on recent activity
                    const now = Date.now();
                    const fiveMinutesAgo = now - 300000; // 5 minutes in milliseconds
                    
                    // Simulate online users (for demo)
                    const onlineUsers = data.total_commands > 0 ? 2 : 1;
                    document.getElementById('onlineUsers').textContent = onlineUsers;
                })
                .catch(error => {
                    console.error('Error fetching status:', error);
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
        
        // Handle Enter key in input fields
        document.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                const activeElement = document.activeElement;
                
                if (activeElement.id === 'teamCode') {
                    document.getElementById('targetUid').focus();
                } else if (activeElement.id === 'targetUid') {
                    document.getElementById('emoteId').focus();
                } else if (activeElement.id === 'emoteId') {
                    sendQuickCommand();
                }
            }
        });
        
        // Focus management for better UX
        document.getElementById('teamCode').addEventListener('input', function() {
            if (this.value.length === 7) {
                document.getElementById('targetUid').focus();
            }
        });
        
        document.getElementById('targetUid').addEventListener('input', function() {
            if (this.value.length >= 8) {
                document.getElementById('emoteId').focus();
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
        
        print(f"📤 Command: Team={team_code}, Emote={emote_id}, Target={target_uid}")
        
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
                "message": f"Command #{command_id} queued for execution",
                "command_id": command_id,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
        else:
            return jsonify({"success": False, "error": "Server error"})
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"success": False, "error": "Internal server error"})

@app.route('/status')
def status():
    pending = [cmd for cmd in command_storage["commands"] if not cmd.get("executed", False)]
    
    return jsonify({
        "bot_connected": len(pending) > 0,
        "pending_commands": len(pending),
        "total_commands": command_storage["stats"]["total"],
        "today_commands": command_storage["stats"]["today"],
        "stats": command_storage["stats"]
    })

# ==================== MAIN ====================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 ASHISH PROFESSIONAL EMOTE PANEL")
    print(f"📊 Total Emotes: {TOTAL_EMOTES}")
    print(f"🔗 Access URL: http://localhost:{port}")
    print(f"⚡ Server running on port {port}")
    print("-" * 50)
    app.run(host='0.0.0.0', port=port, debug=True)