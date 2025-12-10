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
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Orbitron:wght@400;500;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary: #6d28d9;
            --primary-dark: #5b21b6;
            --secondary: #0ea5e9;
            --accent: #f97316;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --dark: #0f172a;
            --darker: #020617;
            --light: #f8fafc;
            --gray: #64748b;
            --gray-dark: #334155;
            
            --evo: #ec4899;
            --special: #8b5cf6;
            --basic: #10b981;
            --legendary: #f59e0b;
            --mythic: linear-gradient(135deg, #ec4899, #8b5cf6, #0ea5e9);
            
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            
            --radius: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 100%);
            color: var(--light);
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            line-height: 1.6;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }

        /* ================= HEADER ================= */
        .header {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(2, 6, 23, 0.9) 100%);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-xl);
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: var(--shadow-xl);
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
            background: var(--mythic);
            z-index: 1;
        }

        .logo-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 20px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .logo-icon {
            background: var(--mythic);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 0 20px rgba(236, 72, 153, 0.3);
        }

        .logo-text {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--secondary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .version-badge {
            background: var(--accent);
            color: white;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tagline {
            text-align: center;
            color: var(--secondary);
            font-size: 1.2rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--radius-lg);
            padding: 24px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            border-color: var(--secondary);
            box-shadow: var(--shadow-lg);
        }

        .stat-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--secondary);
        }

        .stat-label {
            color: var(--gray);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* ================= QUICK SEND ================= */
        .quick-send-section {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(2, 6, 23, 0.9) 100%);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-xl);
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: var(--shadow-xl);
        }

        .section-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 15px;
            color: var(--light);
        }

        .section-title i {
            color: var(--accent);
            font-size: 24px;
        }

        .input-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin-bottom: 30px;
        }

        .form-group {
            position: relative;
        }

        .form-label {
            display: block;
            margin-bottom: 10px;
            font-weight: 500;
            color: var(--light);
            font-size: 0.95rem;
        }

        .form-control {
            width: 100%;
            padding: 16px 20px 16px 50px;
            background: rgba(255, 255, 255, 0.07);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: var(--radius);
            color: var(--light);
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--secondary);
            background: rgba(255, 255, 255, 0.1);
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
        }

        .form-icon {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--gray);
            font-size: 18px;
        }

        .btn {
            padding: 16px 32px;
            border: none;
            border-radius: var(--radius);
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white;
            width: 100%;
            font-size: 1.1rem;
            padding: 18px;
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
        }

        /* ================= TABS ================= */
        .tabs-section {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(2, 6, 23, 0.9) 100%);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-xl);
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: var(--shadow-xl);
        }

        .tabs-header {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .tab-btn {
            padding: 15px 30px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid transparent;
            border-radius: var(--radius);
            color: var(--light);
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .tab-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }

        .tab-btn.active {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            border-color: var(--secondary);
            box-shadow: var(--shadow);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* ================= EMOTE CARDS ================= */
        .emote-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .emote-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--radius);
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .emote-card:hover {
            transform: translateY(-5px);
            border-color: var(--secondary);
            box-shadow: var(--shadow-lg);
        }

        .emote-icon {
            width: 60px;
            height: 60px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            flex-shrink: 0;
        }

        .evo .emote-icon { background: rgba(236, 72, 153, 0.2); color: var(--evo); }
        .special .emote-icon { background: rgba(139, 92, 246, 0.2); color: var(--special); }
        .basic .emote-icon { background: rgba(16, 185, 129, 0.2); color: var(--basic); }
        .legendary .emote-icon { background: rgba(245, 158, 11, 0.2); color: var(--legendary); }

        .emote-info {
            flex: 1;
            min-width: 0;
        }

        .emote-name {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 4px;
            color: var(--light);
        }

        .emote-id {
            font-family: monospace;
            font-size: 0.9rem;
            color: var(--gray);
        }

        .emote-action {
            display: flex;
            gap: 10px;
        }

        .btn-sm {
            padding: 8px 16px;
            font-size: 0.9rem;
            border-radius: 8px;
        }

        .btn-select {
            background: rgba(255, 255, 255, 0.1);
            color: var(--light);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .btn-select:hover {
            background: rgba(255, 255, 255, 0.15);
        }

        .btn-send {
            background: var(--secondary);
            color: white;
        }

        .btn-send:hover {
            background: #0284c7;
        }

        /* ================= STATUS PANEL ================= */
        .status-section {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(2, 6, 23, 0.9) 100%);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-xl);
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: var(--shadow-xl);
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .status-item {
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--radius);
            padding: 24px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .status-label {
            color: var(--gray);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }

        .status-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 700;
        }

        .online { color: var(--success); }
        .offline { color: var(--danger); }
        .pending { color: var(--warning); }

        .commands-history {
            background: rgba(255, 255, 255, 0.05);
            border-radius: var(--radius);
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .history-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--light);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .command-item {
            background: rgba(255, 255, 255, 0.03);
            border-radius: var(--radius);
            padding: 16px;
            margin-bottom: 12px;
            border-left: 4px solid var(--secondary);
        }

        .command-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .command-id {
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            color: var(--secondary);
        }

        .command-time {
            color: var(--gray);
            font-size: 0.9rem;
        }

        .command-details {
            color: var(--light);
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .command-status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 500;
            margin-top: 8px;
        }

        .status-executed { background: rgba(16, 185, 129, 0.2); color: var(--success); }
        .status-pending { background: rgba(245, 158, 11, 0.2); color: var(--warning); }

        /* ================= FOOTER ================= */
        .footer {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(2, 6, 23, 0.9) 100%);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-xl);
            padding: 30px 40px;
            margin-top: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
        }

        .footer-item {
            display: flex;
            align-items: center;
            gap: 12px;
            color: var(--gray);
        }

        .footer-item i {
            color: var(--secondary);
            font-size: 18px;
        }

        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--success);
        }

        /* ================= NOTIFICATION ================= */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            border-radius: var(--radius);
            display: none;
            align-items: center;
            gap: 12px;
            z-index: 1000;
            max-width: 400px;
            box-shadow: var(--shadow-xl);
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .notification.success {
            background: var(--success);
            color: white;
        }

        .notification.error {
            background: var(--danger);
            color: white;
        }

        .notification i {
            font-size: 20px;
        }

        /* ================= RESPONSIVE ================= */
        @media (max-width: 1200px) {
            .container { padding: 15px; }
            .header, .quick-send-section, .tabs-section, .status-section { padding: 30px; }
        }

        @media (max-width: 768px) {
            .logo-text { font-size: 2rem; }
            .logo-icon { width: 50px; height: 50px; font-size: 20px; }
            .section-title { font-size: 1.5rem; }
            .input-grid { grid-template-columns: 1fr; }
            .tabs-header { justify-content: center; }
            .tab-btn { flex: 1; justify-content: center; min-width: 140px; }
            .emote-grid { grid-template-columns: 1fr; }
            .footer-grid { grid-template-columns: 1fr; text-align: center; }
            .footer-item { justify-content: center; }
        }

        @media (max-width: 480px) {
            .header, .quick-send-section, .tabs-section, .status-section { padding: 20px; }
            .logo-container { flex-direction: column; align-items: center; }
            .logo { flex-direction: column; text-align: center; }
            .section-title { font-size: 1.3rem; }
            .stat-value { font-size: 2rem; }
            .btn { padding: 14px 24px; }
        }
    </style>
</head>
<body>
    <!-- NOTIFICATION -->
    <div class="notification" id="notification">
        <i class="fas fa-check-circle"></i>
        <span id="notification-message"></span>
    </div>

    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <div class="logo-container">
                <div class="logo">
                    <div class="logo-icon">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <div>
                        <div class="logo-text">ASHISH EMOTE PANEL</div>
                        <div class="tagline">⚡ Premium Emote Delivery System | Termux TCP Integration</div>
                    </div>
                </div>
                <div class="version-badge">
                    <i class="fas fa-star"></i>
                    PRO 3.0
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value" id="totalEmotes">{{ total_emotes }}</div>
                    <div class="stat-label">TOTAL EMOTES</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="totalCommands">0</div>
                    <div class="stat-label">COMMANDS SENT</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="botStatus">ONLINE</div>
                    <div class="stat-label">BOT STATUS</div>
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
                <div class="form-group">
                    <label class="form-label"><i class="fas fa-users"></i> TEAM CODE</label>
                    <div class="input-wrapper">
                        <i class="fas fa-hashtag form-icon"></i>
                        <input type="text" class="form-control" id="teamCode" 
                               placeholder="Enter 7-digit team code" pattern="\d{7}" maxlength="7" required
                               value="1234567">
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label"><i class="fas fa-user"></i> TARGET UID</label>
                    <div class="input-wrapper">
                        <i class="fas fa-crosshairs form-icon"></i>
                        <input type="text" class="form-control" id="targetUid" 
                               placeholder="Enter target UID (8-11 digits)" pattern="\d{8,11}" required
                               value="13706108657">
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label"><i class="fas fa-smile"></i> EMOTE ID</label>
                    <div class="input-wrapper">
                        <i class="fas fa-magic form-icon"></i>
                        <input type="text" class="form-control" id="emoteId" 
                               placeholder="909033001" pattern="\d{9}" required
                               value="909033001">
                    </div>
                </div>
            </div>

            <button class="btn btn-primary" onclick="sendQuickCommand()">
                <i class="fas fa-rocket"></i> LAUNCH EMOTE ATTACK
            </button>
        </div>

        <!-- TABS SECTION -->
        <div class="tabs-section">
            <div class="tabs-header">
                <button class="tab-btn active" onclick="openTab('evo')">
                    <i class="fas fa-gun"></i> EVO GUNS
                </button>
                <button class="tab-btn" onclick="openTab('special')">
                    <i class="fas fa-star"></i> SPECIAL
                </button>
                <button class="tab-btn" onclick="openTab('basic')">
                    <i class="fas fa-gamepad"></i> BASIC
                </button>
                <button class="tab-btn" onclick="openTab('legendary')">
                    <i class="fas fa-crown"></i> LEGENDARY
                </button>
                <button class="tab-btn" onclick="openTab('status')">
                    <i class="fas fa-chart-bar"></i> STATUS
                </button>
            </div>

            <!-- EVO GUNS TAB -->
            <div id="evo" class="tab-content active">
                <div class="emote-grid">
                    {% for emote in evo_emotes %}
                    <div class="emote-card evo">
                        <div class="emote-icon">
                            <i class="fas {{ emote.icon }}"></i>
                        </div>
                        <div class="emote-info">
                            <div class="emote-name">{{ emote.name }}</div>
                            <div class="emote-id">ID: {{ emote.id }}</div>
                        </div>
                        <div class="emote-action">
                            <button class="btn btn-sm btn-select" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <i class="fas fa-mouse-pointer"></i>
                            </button>
                            <button class="btn btn-sm btn-send" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}', event)">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- SPECIAL EMOTES TAB -->
            <div id="special" class="tab-content">
                <div class="emote-grid">
                    {% for emote in special_emotes %}
                    <div class="emote-card special">
                        <div class="emote-icon">
                            <i class="fas {{ emote.icon }}"></i>
                        </div>
                        <div class="emote-info">
                            <div class="emote-name">{{ emote.name }}</div>
                            <div class="emote-id">ID: {{ emote.id }}</div>
                        </div>
                        <div class="emote-action">
                            <button class="btn btn-sm btn-select" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <i class="fas fa-mouse-pointer"></i>
                            </button>
                            <button class="btn btn-sm btn-send" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}', event)">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- BASIC EMOTES TAB -->
            <div id="basic" class="tab-content">
                <div class="emote-grid">
                    {% for emote in basic_emotes %}
                    <div class="emote-card basic">
                        <div class="emote-icon">
                            <i class="fas {{ emote.icon }}"></i>
                        </div>
                        <div class="emote-info">
                            <div class="emote-name">{{ emote.name }}</div>
                            <div class="emote-id">ID: {{ emote.id }}</div>
                        </div>
                        <div class="emote-action">
                            <button class="btn btn-sm btn-select" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <i class="fas fa-mouse-pointer"></i>
                            </button>
                            <button class="btn btn-sm btn-send" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}', event)">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- LEGENDARY EMOTES TAB -->
            <div id="legendary" class="tab-content">
                <div class="emote-grid">
                    {% for emote in legendary_emotes %}
                    <div class="emote-card legendary">
                        <div class="emote-icon">
                            <i class="fas {{ emote.icon }}"></i>
                        </div>
                        <div class="emote-info">
                            <div class="emote-name">{{ emote.name }}</div>
                            <div class="emote-id">ID: {{ emote.id }}</div>
                        </div>
                        <div class="emote-action">
                            <button class="btn btn-sm btn-select" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <i class="fas fa-mouse-pointer"></i>
                            </button>
                            <button class="btn btn-sm btn-send" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}', event)">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- STATUS TAB -->
            <div id="status" class="tab-content">
                <div class="status-section">
                    <h2 class="section-title">
                        <i class="fas fa-chart-bar"></i> SYSTEM STATUS
                    </h2>
                    
                    <div class="status-grid">
                        <div class="status-item">
                            <div class="status-label">WEB PANEL</div>
                            <div class="status-value online">ONLINE</div>
                        </div>
                        
                        <div class="status-item">
                            <div class="status-label">TERMUX BOT</div>
                            <div class="status-value" id="botStatusDisplay">ONLINE</div>
                        </div>
                        
                        <div class="status-item">
                            <div class="status-label">QUEUED COMMANDS</div>
                            <div class="status-value pending" id="queueCount">0</div>
                        </div>
                        
                        <div class="status-item">
                            <div class="status-label">RESPONSE TIME</div>
                            <div class="status-value" id="pingTime">0ms</div>
                        </div>
                    </div>
                    
                    <div class="commands-history">
                        <h3 class="history-title">
                            <i class="fas fa-history"></i> RECENT COMMANDS
                        </h3>
                        
                        <div id="commandsHistory">
                            <div style="text-align: center; color: var(--gray); padding: 40px;">
                                <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: 20px;"></i>
                                <p>No commands yet. Send your first emote!</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- FOOTER -->
        <div class="footer">
            <div class="footer-grid">
                <div class="footer-item">
                    <div class="status-indicator"></div>
                    <span>PANEL STATUS: <strong style="color: var(--success);">ONLINE</strong></span>
                </div>
                <div class="footer-item">
                    <i class="fas fa-robot"></i>
                    <span>BOT: <strong id="footerBotStatus" style="color: var(--warning);">CONNECTING</strong></span>
                </div>
                <div class="footer-item">
                    <i class="fas fa-user-ninja"></i>
                    <span>DEVELOPER: <strong>ASHISH</strong></span>
                </div>
                <div class="footer-item">
                    <i class="fab fa-instagram"></i>
                    <span>@ashish.shakya0001</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ================= CONFIGURATION =================
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
        }
        
        // ================= EMOTE FUNCTIONS =================
        function useEmote(emoteId, emoteName) {
            document.getElementById('emoteId').value = emoteId;
            showNotification(`✅ ${emoteName} selected! Enter Team Code & Target UID`);
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
            const sendBtn = document.querySelector('.btn-primary');
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
                    showNotification(`🚀 ${emoteName} sent to UID ${target}!`);
                    loadCommandsHistory();
                    
                    // Reset form
                    document.getElementById('teamCode').value = '1234567';
                    document.getElementById('targetUid').value = '13706108657';
                    document.getElementById('emoteId').value = emote;
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
                    const mainBotStatus = document.getElementById('botStatus');
                    
                    if (data.bot_connected) {
                        botStatus.innerHTML = '🟢 ONLINE';
                        botStatus.className = 'status-value online';
                        footerBotStatus.innerHTML = 'ONLINE';
                        footerBotStatus.style.color = '#10b981';
                        mainBotStatus.innerHTML = 'ONLINE';
                        mainBotStatus.style.color = '#10b981';
                        botConnected = true;
                    } else {
                        botStatus.innerHTML = '🔴 OFFLINE';
                        botStatus.className = 'status-value offline';
                        footerBotStatus.innerHTML = 'OFFLINE';
                        footerBotStatus.style.color = '#ef4444';
                        mainBotStatus.innerHTML = 'OFFLINE';
                        mainBotStatus.style.color = '#ef4444';
                        botConnected = false;
                    }
                    
                    // Update queue count
                    document.getElementById('queueCount').innerHTML = data.pending_commands;
                })
                .catch(() => {
                    document.getElementById('botStatusDisplay').innerHTML = '❌ ERROR';
                    document.getElementById('botStatusDisplay').className = 'status-value offline';
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
                            <div style="text-align: center; color: var(--gray); padding: 40px;">
                                <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: 20px;"></i>
                                <p>No commands yet. Send your first emote!</p>
                            </div>`;
                        return;
                    }
                    
                    // Show last 10 commands
                    const recent = commands.slice(-10).reverse();
                    let html = '';
                    
                    recent.forEach(cmd => {
                        const time = cmd.timestamp.split(' ')[1];
                        const statusClass = cmd.status === 'executed' ? 'status-executed' : 'status-pending';
                        const statusText = cmd.status === 'executed' ? 'EXECUTED' : 'PENDING';
                        
                        html += `
                        <div class="command-item">
                            <div class="command-header">
                                <div class="command-id">#${cmd.id} • ${cmd.emote_name}</div>
                                <div class="command-time">${time}</div>
                            </div>
                            <div class="command-details">
                                Team: <strong style="color: var(--secondary);">${cmd.team_code}</strong> • 
                                Target: <strong style="color: var(--accent);">${cmd.target_uid}</strong>
                            </div>
                            <div class="command-status ${statusClass}">${statusText}</div>
                        </div>`;
                    });
                    
                    historyContainer.innerHTML = html;
                });
        }
        
        function updateStats() {
            document.getElementById('totalCommands').textContent = commandCount;
        }
        
        // ================= NOTIFICATION =================
        function showNotification(message, type = 'success') {
            const notif = document.getElementById('notification');
            const notifMsg = document.getElementById('notification-message');
            
            notifMsg.textContent = message;
            notif.className = `notification ${type}`;
            notif.style.display = 'flex';
            
            // Set icon based on type
            const icon = notif.querySelector('i');
            if (type === 'error') {
                icon.className = 'fas fa-exclamation-circle';
            } else {
                icon.className = 'fas fa-check-circle';
            }
            
            // Auto hide after 4 seconds
            setTimeout(() => {
                notif.style.display = 'none';
            }, 4000);
        }
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
