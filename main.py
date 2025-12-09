from flask import Flask, render_template_string, request, jsonify
import os
import re
import json
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ashish-bot-panel-2024')

# -------------------- EMOTE DATABASE --------------------
EVO_GUN_EMOTES = [
    {"name": "🔥 EVO M4A1 MAX", "id": "909033001", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO AK47 MAX", "id": "909000063", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO SHOTGUN MAX", "id": "909035007", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO SCAR MAX", "id": "909000068", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO XMB MAX", "id": "909000085", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO G18 MAX", "id": "909038012", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO MP40 MAX", "id": "909040010", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO FAMAS MAX", "id": "909000090", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO UMP MAX", "id": "909000098", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO WOODPECKER MAX", "id": "909042008", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO GROZA MAX", "id": "909041005", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO THOMPSON MAX", "id": "909038010", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO PARAFAL MAX", "id": "909045001", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO P90 MAX", "id": "909049010", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🔥 EVO M60 MAX", "id": "909051003", "category": "evo", "icon": "fas fa-gun"},
    {"name": "🐍 COBRA RISING", "id": "909000075", "category": "special", "icon": "fas fa-fire"},
    {"name": "👻 DRACO'S SOUL", "id": "909000081", "category": "special", "icon": "fas fa-ghost"},
    {"name": "💀 BLOOD WRAITH", "id": "909000090", "category": "special", "icon": "fas fa-skull"},
]

BASIC_EMOTES = [
    {"name": "👋 Hello!", "id": "909000001", "category": "basic", "icon": "fas fa-hand"},
    {"name": "😂 LOL", "id": "909000002", "category": "basic", "icon": "fas fa-laugh"},
    {"name": "😤 Provoke", "id": "909000003", "category": "basic", "icon": "fas fa-fist-raised"},
    {"name": "👏 Applause", "id": "909000004", "category": "basic", "icon": "fas fa-hands-clapping"},
    {"name": "💃 Dab", "id": "909000005", "category": "basic", "icon": "fas fa-person-dancing"},
    {"name": "🐔 Chicken", "id": "909000006", "category": "basic", "icon": "fas fa-drumstick"},
    {"name": "👋 Arm Wave", "id": "909000007", "category": "basic", "icon": "fas fa-hand-wave"},
    {"name": "💃 Shoot Dance", "id": "909000008", "category": "basic", "icon": "fas fa-gun"},
    {"name": "🦈 Baby Shark", "id": "909000009", "category": "basic", "icon": "fas fa-fish"},
    {"name": "🌹 Flowers of Love", "id": "909000010", "category": "basic", "icon": "fas fa-heart"},
    {"name": "🧟 Mummy Dance", "id": "909000011", "category": "basic", "icon": "fas fa-ghost"},
    {"name": "💪 Push-up", "id": "909000012", "category": "basic", "icon": "fas fa-dumbbell"},
    {"name": "🕺 Shuffling", "id": "909000013", "category": "basic", "icon": "fas fa-person-running"},
    {"name": "👑 FFWC Throne", "id": "909000014", "category": "basic", "icon": "fas fa-crown"},
    {"name": "🐉 Dragon Fist", "id": "909000015", "category": "basic", "icon": "fas fa-dragon"},
    {"name": "🎯 Dangerous Game", "id": "909000016", "category": "basic", "icon": "fas fa-bullseye"},
    {"name": "🐆 Jaguar Dance", "id": "909000017", "category": "basic", "icon": "fas fa-paw"},
    {"name": "👊 Threaten", "id": "909000018", "category": "basic", "icon": "fas fa-hand-fist"},
    {"name": "🔄 Shake With Me", "id": "909000019", "category": "basic", "icon": "fas fa-people-arrows"},
    {"name": "😈 Devil's Move", "id": "909000020", "category": "basic", "icon": "fas fa-horn"},
]

# Combine all emotes
ALL_EMOTES = EVO_GUN_EMOTES + BASIC_EMOTES

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
            
            # Update today's count
            today = datetime.now().strftime("%Y-%m-%d")
            if "daily_stats" not in data:
                data["daily_stats"] = {}
            if today not in data["daily_stats"]:
                data["daily_stats"][today] = 0
            data["daily_stats"][today] += 1
            
            with open(self.commands_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return command_id
        except Exception as e:
            print(f"Error saving command: {e}")
            return None

command_manager = CommandManager()

# -------------------- HTML TEMPLATE (SIMPLIFIED) --------------------
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
            max-width: 1200px;
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

        /* EVO GUNS SECTION */
        .section-title {
            color: var(--accent);
            margin: 20px 0;
            font-size: 1.8rem;
            text-align: center;
        }

        .evo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .evo-card {
            background: rgba(0, 0, 0, 0.6);
            border-radius: 12px;
            padding: 20px;
            border: 2px solid #ff5500;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
        }

        .evo-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(255, 85, 0, 0.3);
            background: rgba(255, 85, 0, 0.1);
        }

        .evo-icon {
            font-size: 2rem;
            color: #ffaa00;
            margin-bottom: 10px;
        }

        .evo-name {
            font-size: 1.2rem;
            color: #ffcc00;
            margin-bottom: 10px;
        }

        .evo-id {
            background: rgba(255, 85, 0, 0.2);
            color: #ffaa00;
            padding: 5px 10px;
            border-radius: 15px;
            font-family: monospace;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }

        .send-btn {
            background: var(--evo-gradient);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            font-weight: bold;
            transition: all 0.3s;
        }

        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255, 85, 0, 0.4);
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

        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .evo-grid { grid-template-columns: 1fr; }
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
            <h2>⚡ EVO Gun Emotes | Termux Bot Integration</h2>
        </div>

        <!-- TABS -->
        <div class="tabs">
            <button class="tab-btn active" onclick="openTab('evo')">
                <i class="fas fa-gun"></i> EVO GUNS
            </button>
            <button class="tab-btn" onclick="openTab('basic')">
                <i class="fas fa-gamepad"></i> BASIC EMOTES
            </button>
            <button class="tab-btn" onclick="openTab('status')">
                <i class="fas fa-chart-bar"></i> STATUS
            </button>
        </div>

        <!-- EVO GUNS TAB -->
        <div id="evo" class="tab-content active">
            <h3 class="section-title"><i class="fas fa-gun"></i> EVO GUN EMOTES</h3>
            
            <div class="input-form">
                <h4 style="color: var(--accent); margin-bottom: 15px; text-align: center;">
                    <i class="fas fa-cog"></i> ENTER DETAILS
                </h4>
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE (7 digits)</label>
                    <input type="text" id="evo_team" placeholder="1234567" pattern="\d{7}">
                </div>
                <div class="input-group">
                    <label><i class="fas fa-user"></i> TARGET UID</label>
                    <input type="text" id="evo_target" placeholder="4255057762" pattern="\d{8,11}">
                </div>
            </div>

            <div class="evo-grid">
                {% for emote in evo_emotes %}
                <div class="evo-card" onclick="sendEvoEmote('{{ emote.id }}', '{{ emote.name }}')">
                    <div class="evo-icon">
                        <i class="{{ emote.icon }}"></i>
                    </div>
                    <div class="evo-name">{{ emote.name }}</div>
                    <div class="evo-id">ID: {{ emote.id }}</div>
                    <button class="send-btn">
                        <i class="fas fa-paper-plane"></i> SEND EMOTE
                    </button>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- BASIC EMOTES TAB -->
        <div id="basic" class="tab-content">
            <h3 class="section-title"><i class="fas fa-gamepad"></i> BASIC EMOTES</h3>
            
            <div class="input-form">
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE</label>
                    <input type="text" id="basic_team" placeholder="1234567" pattern="\d{7}">
                </div>
                <div class="input-group">
                    <label><i class="fas fa-user"></i> TARGET UID</label>
                    <input type="text" id="basic_target" placeholder="4255057762" pattern="\d{8,11}">
                </div>
            </div>

            <div class="evo-grid">
                {% for emote in basic_emotes %}
                <div class="evo-card" onclick="sendBasicEmote('{{ emote.id }}', '{{ emote.name }}')">
                    <div class="evo-icon">
                        <i class="{{ emote.icon }}"></i>
                    </div>
                    <div class="evo-name">{{ emote.name }}</div>
                    <div class="evo-id">ID: {{ emote.id }}</div>
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
            <i class="fas fa-user"></i>
            <span>ASHISH</span>
        </div>
        <div class="status-item">
            <i class="fab fa-instagram"></i>
            <span>@ashish.shakya0001</span>
        </div>
    </div>

    <!-- NOTIFICATION -->
    <div class="notification" id="notification"></div>

    <script>
        // Tab switching
        function openTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remov
