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

# Add more emotes dynamically
for i in range(21, 50):
    ALL_EMOTES.append({
        "name": f"Emote {i}",
        "id": f"909000{i:03d}",
        "category": "basic",
        "icon": "fas fa-star"
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

# -------------------- HTML TEMPLATE (FULL) --------------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 ASHISH EMOTE PANEL v3.0</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Animate.css -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    
    <style>
        :root {
            --primary: #ff0000;
            --secondary: #00ff00;
            --accent: #00ffff;
            --dark: #0a0a0a;
            --darker: #050505;
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
            background: var(--darker);
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 0, 0, 0.1) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 20%);
            animation: backgroundShift 20s infinite alternate;
        }

        @keyframes backgroundShift {
            0% { background-position: 0% 0%; }
            100% { background-position: 100% 100%; }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* HEADER WITH ANIMATION */
        .header {
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
            border-radius: 20px;
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid transparent;
            background-clip: padding-box;
            animation: borderGlow 3s infinite alternate;
        }

        @keyframes borderGlow {
            0% { border-color: rgba(255, 0, 0, 0.3); box-shadow: 0 0 30px rgba(255, 0, 0, 0.2); }
            100% { border-color: rgba(0, 255, 255, 0.3); box-shadow: 0 0 50px rgba(0, 255, 255, 0.3); }
        }

        .header::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: var(--gradient);
            z-index: -1;
            border-radius: 22px;
            animation: rotate 10s linear infinite;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .header h1 {
            font-size: 4rem;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-shadow: 0 0 50px rgba(255, 0, 255, 0.5);
            animation: textGlow 2s infinite alternate;
        }

        @keyframes textGlow {
            0% { text-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
            100% { text-shadow: 0 0 40px rgba(0, 255, 255, 0.7); }
        }

        .header h2 {
            color: var(--accent);
            font-size: 1.5rem;
            margin-bottom: 20px;
            animation: fadeInUp 1s;
        }

        /* TABS STYLING */
        .tabs {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            justify-content: center;
        }

        .tab-btn {
            padding: 15px 30px;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid transparent;
            color: white;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 10px;
            position: relative;
            overflow: hidden;
        }

        .tab-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }

        .tab-btn:hover::before {
            left: 100%;
        }

        .tab-btn:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 10px 25px rgba(255, 0, 0, 0.3);
        }

        .tab-btn.active {
            background: var(--gradient);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(255, 0, 0, 0.4);
            border-color: var(--accent);
        }

        .tab-content {
            display: none;
            background: rgba(20, 20, 20, 0.85);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .tab-content.active {
            display: block;
        }

        /* QUICK FORM STYLING */
        .quick-form {
            background: rgba(0, 0, 0, 0.5);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            border: 2px solid rgba(255, 0, 0, 0.3);
            animation: pulseBorder 2s infinite;
        }

        @keyframes pulseBorder {
            0%, 100% { border-color: rgba(255, 0, 0, 0.3); }
            50% { border-color: rgba(0, 255, 255, 0.5); }
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .input-group {
            position: relative;
        }

        .input-group label {
            display: block;
            margin-bottom: 8px;
            color: var(--accent);
            font-weight: 600;
            font-size: 1.1rem;
        }

        .input-group input {
            width: 100%;
            padding: 18px 20px;
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid var(--primary);
            border-radius: 12px;
            color: white;
            font-size: 16px;
            transition: all 0.3s ease;
            font-family: monospace;
        }

        .input-group input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.4);
            transform: scale(1.02);
        }

        .input-group i {
            position: absolute;
            right: 20px;
            top: 50px;
            color: var(--accent);
        }

        /* EVO GUNS GRID - SPECIAL STYLING */
        .section-title {
            color: var(--accent);
            margin: 30px 0 20px 0;
            font-size: 2rem;
            text-align: center;
            position: relative;
            padding-bottom: 15px;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--gradient);
            border-radius: 2px;
        }

        .evo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }

        .evo-card {
            background: rgba(0, 0, 0, 0.6);
            border-radius: 15px;
            padding: 25px;
            border: 2px solid transparent;
            background-clip: padding-box;
            position: relative;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: cardFloat 3s infinite ease-in-out;
        }

        @keyframes cardFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .evo-card:hover {
            transform: translateY(-15px) scale(1.05);
            box-shadow: 0 20px 40px rgba(255, 85, 0, 0.4);
        }

        .evo-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--evo-gradient);
        }

        .evo-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            color: #ff5500;
            text-align: center;
            animation: iconPulse 2s infinite;
        }

        @keyframes iconPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .evo-name {
            font-size: 1.4rem;
            color: #ffaa00;
            margin-bottom: 10px;
            text-align: center;
            font-weight: bold;
        }

        .evo-id {
            background: rgba(255, 85, 0, 0.2);
            color: #ffaa00;
            padding: 8px 15px;
            border-radius: 20px;
            font-family: monospace;
            font-size: 1rem;
            text-align: center;
            margin-bottom: 15px;
            border: 1px solid rgba(255, 85, 0, 0.5);
        }

        /* BUTTON STYLES */
        .btn {
            background: var(--gradient);
            color: white;
            border: none;
            padding: 20px 40px;
            border-radius: 15px;
            font-size: 1.3rem;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin: 30px 0;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .btn::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: rotate(45deg);
            transition: 0.5s;
        }

        .btn:hover::after {
            left: 100%;
        }

        .btn:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 35px rgba(255, 0, 0, 0.5);
        }

        .btn:active {
            transform: translateY(0) scale(0.98);
        }

        /* SPECIAL BUTTONS */
        .fire-btn {
            background: linear-gradient(135deg, #ff0000, #ff5500);
            animation: fireGlow 1.5s infinite alternate;
        }

        @keyframes fireGlow {
            from { box-shadow: 0 0 20px rgba(255, 0, 0, 0.5); }
            to { box-shadow: 0 0 40px rgba(255, 85, 0, 0.8); }
        }

        .ice-btn {
            background: linear-gradient(135deg, #00aaff, #00ffff);
            animation: iceGlow 1.5s infinite alternate;
        }

        @keyframes iceGlow {
            from { box-shadow: 0 0 20px rgba(0, 170, 255, 0.5); }
            to { box-shadow: 0 0 40px rgba(0, 255, 255, 0.8); }
        }

        /* STATUS BAR */
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
            border-top: 3px solid var(--primary);
            backdrop-filter: blur(10px);
            z-index: 1000;
            animation: slideUp 0.5s ease;
        }

        @keyframes slideUp {
            from { transform: translateY(100%); }
            to { transform: translateY(0); }
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00ff00;
            animation: pulse 2s infinite;
            box-shadow: 0 0 10px #00ff00;
        }

        @keyframes pulse {
            0%, 100% { 
                transform: scale(1);
                box-shadow: 0 0 10px #00ff00;
            }
            50% { 
                transform: scale(1.2);
                box-shadow: 0 0 20px #00ff00;
            }
        }

        /* NOTIFICATION */
        .notification {
            position: fixed;
            top: 30px;
            right: 30px;
            padding: 20px 30px;
            border-radius: 15px;
            display: none;
            font-weight: bold;
            z-index: 2000;
            animation: slideInRight 0.3s ease, fadeOut 0.3s ease 3.7s;
            max-width: 400px;
            backdrop-filter: blur(10px);
            border: 2px solid;
        }

        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes fadeOut {
            to { opacity: 0; }
        }

        .notification.success {
            background: linear-gradient(135deg, rgba(0, 255, 0, 0.9), rgba(0, 200, 0, 0.9));
            color: #000;
            border-color: #00ff00;
        }

        .notification.error {
            background: linear-gradient(135deg, rgba(255, 0, 0, 0.9), rgba(200, 0, 0, 0.9));
            color: white;
            border-color: #ff0000;
        }

        .notification.warning {
            background: linear-gradient(135deg, rgba(255, 255, 0, 0.9), rgba(200, 200, 0, 0.9));
            color: #000;
            border-color: #ffff00;
        }

        /* COMMANDS LIST */
        .commands-list {
            background: rgba(0, 0, 0, 0.6);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            max-height: 400px;
            overflow-y: auto;
            border: 2px solid rgba(0, 255, 255, 0.3);
        }

        .command-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            border-left: 5px solid var(--accent);
            animation: fadeInLeft 0.5s ease;
            transition: all 0.3s;
        }

        @keyframes fadeInLeft {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .command-item:hover {
            transform: translateX(10px);
            background: rgba(255, 255, 255, 0.1);
        }

        /* RESPONSIVE DESIGN */
        @media (max-width: 768px) {
            .header h1 { font-size: 2.5rem; }
            .evo-grid { grid-template-columns: 1fr; }
            .form-grid { grid-template-columns: 1fr; }
            .status-bar { flex-direction: column; gap: 15px; padding: 10px; }
            .tab-btn { padding: 12px 20px; font-size: 1rem; }
            .container { padding: 10px; }
        }

        /* LOADING ANIMATION */
        .loader {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 3000;
        }

        .spinner {
            width: 60px;
            height: 60px;
            border: 5px solid rgba(255, 0, 0, 0.3);
            border-top: 5px solid var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* SCROLLBAR STYLING */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--gradient);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary);
        }
    </style>
</head>
<body>
    <!-- LOADING OVERLAY -->
    <div class="loader" id="loader">
        <div class="spinner"></div>
        <p style="margin-top: 20px; color: var(--accent); text-align: center;">Sending Command...</p>
    </div>

    <div class="container">
        <!-- HEADER -->
        <div class="header animate__animated animate__fadeInDown">
            <h1><i class="fas fa-fire"></i> ASHISH EMOTE PANEL v3.0</h1>
            <h2>⚡ Premium Emote Sending System | Termux Bot Integration</h2>
            <p style="color: #aaa; max-width: 800px; margin: 0 auto; line-height: 1.6;">
                Send any emote to any player instantly! EVO Guns, Special Emotes, and more...
                Commands are queued and executed automatically by Termux TCP Bot.
            </p>
        </div>

        <!-- TABS -->
        <div class="tabs">
            <button class="tab-btn active" onclick="openTab('quick')">
                <i class="fas fa-bolt"></i> QUICK SEND
            </button>
            <button class="tab-btn" onclick="openTab('evo')">
                <i class="fas fa-gun"></i> EVO GUNS
            </button>
            <button class="tab-btn" onclick="openTab('emotes')">
                <i class="fas fa-gamepad"></i> ALL EMOTES
            </button>
            <button class="tab-btn" onclick="openTab('status')">
                <i class="fas fa-chart-bar"></i> STATUS
            </button>
        </div>

        <!-- QUICK SEND TAB -->
        <div id="quick" class="tab-content active">
            <div class="quick-form">
                <h3 class="section-title"><i class="fas fa-rocket"></i> INSTANT EMOTE ATTACK</h3>
                
                <div class="form-grid">
                    <div class="input-group">
                        <label><i class="fas fa-users"></i> TEAM CODE</label>
                        <input type="text" id="team_code" placeholder="Enter 7-digit team code" 
                               pattern="\d{7}" maxlength="7" required>
                        <i class="fas fa-hashtag"></i>
                    </div>
                    
                    <div class="input-group">
                        <label><i class="fas fa-user"></i> TARGET UID</label>
                        <input type="text" id="target_uid" placeholder="Enter target UID (8-11 digits)" 
                               pattern="\d{8,11}" required>
                        <i class="fas fa-crosshairs"></i>
                    </div>
                    
                    <div class="input-group">
                        <label><i class="fas fa-smile"></i> EMOTE ID</label>
                        <input type="text" id="emote_id" placeholder="909033001" 
                               pattern="\d{9}" required>
                        <i class="fas fa-magic"></i>
                    </div>
                </div>
                
                <button class="btn fire-btn" onclick="sendQuickCommand()">
                    <i class="fas fa-paper-plane"></i> LAUNCH EMOTE ATTACK
                </button>
                
                <div style="text-align: center; margin-top: 20px;">
                    <p style="color: #aaa; font-size: 0.9rem;">
                        <i class="fas fa-info-circle"></i> Command will be sent to Termux bot for execution
                    </p>
                </div>
            </div>
            
            <!-- POPULAR EMOTES -->
            <h3 class="section-title"><i class="fas fa-star"></i> POPULAR EMOTES</h3>
            <div class="evo-grid">
                <div class="evo-card" onclick="usePopularEmote('909033001', 'EVO M4A1 MAX')">
                    <div class="evo-icon"><i class="fas fa-gun"></i></div>
                    <div class="evo-name">EVO M4A1 MAX</div>
                    <div class="evo-id">ID: 909033001</div>
                    <div style="text-align: center; color: #aaa; font-size: 0.9rem;">
                        <i class="fas fa-bolt"></i> INSTANT SEND
                    </div>
                </div>
                
                <div class="evo-card" onclick="usePopularEmote('909000075', 'COBRA RISING')">
                    <div class="evo-icon"><i class="fas fa-fire"></i></div>
                    <div class="evo-name">COBRA RISING</div>
                    <div class="evo-id">ID: 909000075</div>
                    <div style="text-align: center; color: #aaa; font-size: 0.9rem;">
                        <i class="fas fa-fire"></i> SPECIAL EMOTE
                    </div>
                </div>
                
                <div class="evo-card" onclick="usePopularEmote('909000001', 'HELLO!')">
                    <div class="evo-icon"><i class="fas fa-hand"></i></div>
                    <div class="evo-name">HELLO!</div>
                    <div class="evo-id">ID: 909000001</div>
                    <div style="text-align: center; color: #aaa; font-size: 0.9rem;">
                        <i class="fas fa-waving-hand"></i> BASIC EMOTE
                    </div>
                </div>
            </div>
        </div>

        <!-- EVO GUNS TAB -->
        <div id="evo" class="tab-content">
            <h3 class="section-title"><i class="fas fa-gun"></i> EVO GUN EMOTE COLLECTION</h3>
            <p style="text-align: center; color: #aaa; margin-bottom: 30px;">
                Select any EVO Gun emote to send instantly. These are the most powerful emotes!
            </p>
            
            <div class="form-grid" style="margin-bottom: 30px;">
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE</label>
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
                    <div class="evo-icon"><i class="{{ emote.icon }}"></i></div>
                    <div class="evo-name">{{ emote.name }}</div>
                    <div class="evo-id">ID: {{ emote.id }}</div>
                    <div style="text-align: center; margin-top: 10px;">
                        <button class="send-btn" style="background: var(--evo-gradient); padding: 8px 20px; border-radius: 20px; border: none; color: white; cursor: pointer;">
                            <i class="fas fa-paper-plane"></i> SEND
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- ALL EMOTES TAB -->
        <div id="emotes" class="tab-content">
            <h3 class="section-title"><i class="fas fa-gamepad"></i> COMPLETE EMOTE LIBRARY</h3>
            
            <div style="text-align: center; margin-bottom: 30px;">
                <input type="text" id="searchInput" placeholder="🔍 Search emotes by name or ID..." 
                       style="width: 80%; padding: 15px; border-radius: 25px; border: 2px solid var(--primary); background: rgba(0,0,0,0.5); color: white; font-size: 1.1rem;"
                       onkeyup="searchEmotes()">
            </div>
            
            <div class="evo-grid" id="allEmotesContainer">
                <!-- All emotes will be loaded here -->
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <button class="btn ice-btn" onclick="loadMoreEmotes()">
                    <i class="fas fa-sync"></i> LOAD MORE EMOTES
                </button>
            </div>
        </div>

        <!-- STATUS TAB -->
        <div id="status" class="tab-content">
            <h3 class="section-title"><i class="fas fa-chart-bar"></i> SYSTEM STATUS & STATISTICS</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
                <div style="background: linear-gradient(135deg, rgba(0,100,0,0.3), rgba(0,50,0,0.3)); padding: 25px; border-radius: 15px; border: 2px solid #00ff00;">
                    <h4><i class="fas fa-server"></i> WEB PANEL STATUS</h4>
                    <p style="color: #00ff00; font-size: 2rem; margin: 10px 0;">🟢 ONLINE</p>
                    <p style="color: #aaa;">Render.com Hosting</p>
                </div>
                
                <div style="background: linear-gradient(135deg, rgba(255,165,0,0.3), rgba(200,100,0,0.3)); padding: 25px; border-radius: 15px; border: 2px solid #ffa500;">
                    <h4><i class="fas fa-robot"></i> TERMUX BOT</h4>
                    <p id="botStatus" style="color: #ffa500; font-size: 2rem; margin: 10px 0;">⏳ CHECKING...</p>
                    <p style="color: #aaa;">Run bot on Termux</p>
                </div>
                
                <div style="background: linear-gradient(135deg, rgba(0,100,255,0.3), rgba(0,50,200,0.3)); padding: 25px; border-radius: 15px; border: 2px solid #00aaff;">
                    <h4><i class="fas fa-commands"></i> COMMANDS QUEUE</h4>
                    <p id="queueCount" style="color: #00aaff; font-size: 2rem; margin: 10px 0;">0</p>
                    <p style="color: #aaa;">Pending commands</p>
                </div>
            </div>
            
            <h4 style="margin: 30px 0 20px 0;"><i class="fas fa-history"></i> RECENT COMMANDS</h4>
            <div class="commands-list" id="commandsList">
                <!-- Commands will be loaded here -->
            </div>
            
            <button class="btn" onclick="refreshStatus()" style="margin-top: 20px;">
                <i class="fas fa-sync-alt"></i> REFRESH STATUS
            </button>
        </div>
    </div>

    <!-- STATUS BAR -->
    <div class="status-bar">
        <div class="status-item">
            <div class="status-dot"></div>
            <span>Panel: <span style="color: #00ff00;">ONLINE</span></span>
        </div>
        <div class="status-item">
            <i class="fas fa-robot"></i>
            <span>Bot: <span id="botStatusBar" style="color: #ffa500;">CHECKING</span></span>
        </div>
        <div class="status-item">
            <i class="fas fa-paper-plane"></i>
            <span>Commands: <span id="totalCommands">0</span></span>
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
        let allEmotes = [];
        let currentPage = 0;
        const itemsPerPage = 12;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            // Load emotes from server
            fetch('/get_emotes')
                .then(r => r.json())
                .then(data => {
                    allEmotes = data.emotes;
                    displayAllEmotes();
                });
            
            // Initial status check
            refreshStatus();
            
            // Auto-refresh every 3 seconds
            setInterval(refreshStatus, 3000);
            
            // Auto-refresh commands list every 5 seconds
            setInterval(loadCommands, 5000);
        });
        
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
            
            // Animate tab change
            document.getElementById(tabName).style.animation = 'none';
            setTimeout(() => {
                document.getElementById(tabName).style.animation = 'fadeIn 0.5s ease';
            }, 10);
        }
        
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
        
        function showLoader(show = true) {
            document.getElementById('loader').style.display = show ? 'block' : 'none';
        }
        
        function sendQuickCommand() {
            const team = document.getElementById('team_code').value;
            const target = document.getElementById('target_uid').value;
            const emote = document.getElementById('emote_id').value;
            
            if (!team || !target || !emote) {
                showNotification('❌ Please fill all fields!', 'error');
                return;
            }
            
            if (!/^\d{7}$/.test(team)) {
                showNotification('❌ Team Code must be 7 digits!', 'error');
                return;
            }
            
            sendCommand(team, emote, target);
        }
        
        function usePopularEmote(emoteId, emoteName) {
            document.getElementById('emote_id').value = emoteId;
            showNotification(`✅ ${emoteName} selected! Enter Team Code & Target UID`, 'success');
            document.getElementById('team_code').focus();
        }
        
        function sendEvoEmote(emoteId, emoteName) {
            const team = document.getElementById('evo_team').value;
            const target = document.getElementById('evo_target').value;
            
            if (!team || !target) {
                showNotification('❌ Please enter Team Code and Target UID first!', 'error');
                return;
            }
            
            sendCommand(team, emoteId, target, emoteName);
        }
        
        function sendCommand(team, emote, target, emoteName = '') {
            showLoader(true);
            
            fetch('/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `team_code=${team}&emote_id=${emote}&target_uid=${target}`
            })
            .then(response => response.json())
            .then(data => {
                showLoader(false);
                
                if (data.success) {
                    showNotification(`✅ Command #${data.command_id} saved successfully!`, 'success');
                    refreshStatus();
                    
                    // Animate success
                    document.querySelector('.btn').classList.add('animate__animated', 'animate__tada');
                    setTimeout(() => {
                        document.querySelector('.btn').classList.remove('animate__animated', 'animate__tada');
                    }, 1000);
                } else {
                    showNotification(`❌ Error: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showLoader(false);
                showNotification('❌ Network error! Check your connection.', 'error');
            });
        }
        
        function displayAllEmotes() {
            const container = document.getElementById('allEmotesContainer');
            container.innerHTML = '';
            
            const start = currentPage * itemsPerPage;
            const end = start + itemsPerPage;
            const pageEmotes = allEmotes.slice(start, end);
            
            pageEmotes.forEach(emote => {
                const card = document.createElement('div');
                card.className = 'evo-card';
                card.innerHTML = `
                    <div class="evo-icon"><i class="${emote.icon}"></i></div>
                    <div class="evo-name">${emote.name}</div>
                    <div class="evo-id">ID: ${emote.id}</div>
                    <div style="text-align: center; margin-top: 10px;">
                        <button class="send-btn" onclick="useEmoteInQuick('${emote.id}', '${emote.name}')" 
                                style="background: var(--basic-gradient); padding: 8px 20px; border-radius: 20px; border: none; color: white; cursor: pointer;">
                            <i class="fas fa-paper-plane"></i> USE
                        </button>
                    </div>
                `;
                container.appendChild(card);
            });
        }
        
        function useEmoteInQuick(emoteId, emoteName) {
            // Switch to quick tab
            openTab('quick');
            document.getElementById('emote_id').value = emoteId;
            showNotification(`🎭 ${emoteName} selected!`, 'success');
        }
        
        function searchEmotes() {
            const search = document.getElementById('searchInput').value.toLowerCase();
            const container = document.getElementById('allEmotesContainer');
            
            if (!search) {
                currentPage = 0;
                displayAllEmotes();
                return;
            }
            
            const filtered = allEmotes.filter(emote => 
                emote.name.toLowerCase().includes(search) || 
                emote.id.includes(search)
            );
            
            container.innerHTML = '';
            filtered.forEach(emote => {
                const card = document.createElement('div');
                card.className = 'evo-card';
                card.innerHTML = `
                    <div class="evo-icon"><i class="${emote.icon}"></i></div>
                    <div class="evo-name">${emote.name}</div>
                    <div class="evo-id">ID: ${emote.id}</div>
                    <div style="text-align: center; margin-top: 10px;">
                        <button class="send-btn" onclick="useEmoteInQuick('${emote.id}', '${emote.name}')" 
                                style="background: var(--basic-gradient); padding: 8px 20px; border-radius: 20px; border: none; color: white; cursor: pointer;">
                            <i class="fas fa-paper-plane"></i> USE
                        </button>
                    </div>
                `;
                container.appendChild(card);
            });
        }
        
        function loadMoreEmotes() {
            currentPage++;
            displayAllEmotes();
            showNotification(`📚 Loaded page ${currentPage + 1} of emotes`, 'success');
        }
        
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
                    document.getElementById('queueCount').innerHTML = data.pending_commands;
                    document.getElementById('totalCommands').innerHTML = data.pending_commands;
                    
                    // Load commands
                    loadCommands();
                })
                .catch(() => {
                    document.getElementById('botStatus').innerHTML = '❌ ERROR';
                    document.getElementById('botStatus').style.color = '#ff0000';
                });
        }
        
        function loadCommands() {
            const commandsList = document.getElementById('commandsList');
            
            fetch('/get_commands')
                .then(r => r.json())
                .then(data => {
                    commandsList.innerHTML = '';
                    
                    if (data.commands.length === 0) {
                        commandsList.innerHTML = '<p style="text-align: center; color: #aaa; padding: 20px;">No commands yet. Send your first emote!</p>';
                        return;
                    }
                    
                    data.commands.forEach(cmd => {
                        const item = document.createElement('div');
                        item.className = 'command-item';
                        item.innerHTML = `
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <strong style="color: var(--accent);">#${cmd.id}</strong>
                                <span style="color: #aaa; font-size: 0.9rem;">${cmd.timestamp}</span>
                            </div>
                            <div style="margin-bottom: 5px;">
                                <span style="color: #ffaa00;">${cmd.emote_name}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                                <span>Team: <span style="color: #00ff00;">${cmd.team_code}</span></span>
                                <span>Target: <span style="color: #00aaff;">${cmd.target_uid}</span></span>
                            </div>
                            <div style="margin-top: 5px; text-align: right;">
                                <span style="color: ${cmd.status === 'executed' ? '#00ff00' : '#ffff00'}">
                                    ${cmd.status === 'executed' ? '✅ EXECUTED' : '⏳ PENDING'}
                                </span>
                            </div>
                        `;
                        commandsList.appendChild(item);
                    });
                });
        }
        
        // Add some random animations
        setInterval(() => {
            const cards = document.querySelectorAll('.evo-card');
            if (cards.length > 0) {
                const randomCard = cards[Math.floor(Math.random() * cards.length)];
                randomCard.classList.add('animate__animated', 'animate__pulse');
                setTimeout(() => {
                    randomCard.classList.remove('animate__animated', 'animate__pulse');
                }, 1000);
            }
        }, 3000);
    </script>
</body>
</html>
'''

# -------------------- FLASK ROUTES --------------------
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, 
                                  evo_emotes=EVO_GUN_EMOTES,
                                  basic_emotes=BASIC_EMOTES,
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

@app.route('/get_emotes')
def get_emotes():
    return jsonify({"emotes": ALL_EMOTES})

@app.route('/status')
def status():
    try:
        with open("commands.json", 'r') as f:
            data = json.load(f)
        
        pending = [cmd for cmd in data["commands"] if not cmd.get("executed", False)]
        
        return jsonify({
            "bot_connected": len(pending) > 0,
            "pending_commands": len(pending),
            "total_commands": data.get("stats", {}).get("total", 0),
            "recent_commands": data["commands"][-10:] if data["commands"] else []
        })
    except:
        return jsonify({
            "bot_connected": False,
            "pending_commands": 0,
            "total_commands": 0,
            "recent_commands": []
        })

@app.route('/get_commands')
def get_commands():
    try:
        with open("commands.json", 'r') as f:
            data = json.load(f)
        
        # Return last 20 commands
        commands = data["commands"][-20:] if data["commands"] else []
        return jsonify({"commands": commands})
    except:
        return jsonify({"commands": []})

# -------------------- MAIN --------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
