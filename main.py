from flask import Flask, render_template_string, request, jsonify, session
import os
import re
import json
import time
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ashish-bot-panel-secret-2024')

# -------------------- EMOTE DATABASE --------------------
EMOTES = [
    # Basic Emotes
    {"name": "Hello!", "id": "909000001"},
    {"name": "LOL", "id": "909000002"},
    {"name": "Provoke", "id": "909000003"},
    {"name": "Applause", "id": "909000004"},
    {"name": "Dab", "id": "909000005"},
    {"name": "Chicken", "id": "909000006"},
    {"name": "Arm Wave", "id": "909000007"},
    {"name": "Shoot Dance", "id": "909000008"},
    {"name": "Baby Shark", "id": "909000009"},
    {"name": "Flowers of Love", "id": "909000010"},
    {"name": "Mummy Dance", "id": "909000011"},
    {"name": "Push-up", "id": "909000012"},
    {"name": "Shuffling", "id": "909000013"},
    {"name": "FFWC Throne", "id": "909000014"},
    {"name": "Dragon Fist", "id": "909000015"},
    {"name": "Dangerous Game", "id": "909000016"},
    {"name": "Jaguar Dance", "id": "909000017"},
    {"name": "Threaten", "id": "909000018"},
    {"name": "Shake With Me", "id": "909000019"},
    {"name": "Devil's Move", "id": "909000020"},
    
    # EVO Gun Emotes
    {"name": "EVO M4A1 MAX", "id": "909033001"},
    {"name": "EVO AK47 MAX", "id": "909000063"},
    {"name": "EVO SHOTGUN MAX", "id": "909035007"},
    {"name": "EVO SCAR MAX", "id": "909000068"},
    {"name": "EVO XMB MAX", "id": "909000085"},
    {"name": "EVO G18 MAX", "id": "909038012"},
    {"name": "EVO MP40 MAX", "id": "909040010"},
    {"name": "EVO FAMAS MAX", "id": "909000090"},
    {"name": "EVO UMP MAX", "id": "909000098"},
    {"name": "EVO WOODPECKER MAX", "id": "909042008"},
    {"name": "EVO GROZA MAX", "id": "909041005"},
    {"name": "EVO THOMPSON MAX", "id": "909038010"},
    {"name": "EVO PARAFAL MAX", "id": "909045001"},
    {"name": "EVO P90 MAX", "id": "909049010"},
    {"name": "EVO M60 MAX", "id": "909051003"},
    {"name": "COBRA RISING", "id": "909000075"},
    
    # Legendary Emotes
    {"name": "Dragon Slayer", "id": "909050001"},
    {"name": "Phoenix Rise", "id": "909050002"},
    {"name": "Titan Smash", "id": "909050003"},
    {"name": "Valkyrie Wings", "id": "909050004"},
    {"name": "Samurai Strike", "id": "909050005"},
    {"name": "Ninja Vanish", "id": "909050006"},
    {"name": "Wizard Spell", "id": "909050007"},
    {"name": "Knight Honor", "id": "909050008"},
    {"name": "Assassin Stealth", "id": "909050009"},
    {"name": "Berserker Rage", "id": "909050010"},
]

# Add more emotes
for i in range(100, 200):
    EMOTES.append({"name": f"Emote {i}", "id": f"909000{i}"})

# -------------------- COMMAND MANAGER --------------------
class CommandManager:
    def __init__(self):
        self.commands_file = "commands.json"
        self.initialize_file()
    
    def initialize_file(self):
        """Initialize commands file"""
        if not os.path.exists(self.commands_file):
            with open(self.commands_file, 'w') as f:
                json.dump({"commands": [], "last_id": 0}, f)
    
    def save_command(self, team_code, emote_id, target_uid, user_ip):
        """Save command to JSON file"""
        try:
            with open(self.commands_file, 'r') as f:
                data = json.load(f)
            
            command_id = data["last_id"] + 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            command = {
                "id": command_id,
                "team_code": team_code,
                "emote_id": emote_id,
                "target_uid": target_uid,
                "timestamp": timestamp,
                "user_ip": user_ip,
                "status": "pending",
                "executed": False
            }
            
            data["commands"].append(command)
            data["last_id"] = command_id
            
            with open(self.commands_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return command_id
        except Exception as e:
            print(f"Error saving command: {e}")
            return None
    
    def get_pending_commands(self):
        """Get all pending commands"""
        try:
            with open(self.commands_file, 'r') as f:
                data = json.load(f)
            
            pending = [cmd for cmd in data["commands"] if not cmd.get("executed", False)]
            return pending[:10]  # Return only last 10
        except:
            return []
    
    def mark_executed(self, command_id):
        """Mark command as executed"""
        try:
            with open(self.commands_file, 'r') as f:
                data = json.load(f)
            
            for cmd in data["commands"]:
                if cmd["id"] == command_id:
                    cmd["executed"] = True
                    cmd["status"] = "executed"
                    break
            
            with open(self.commands_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except:
            return False

command_manager = CommandManager()

# -------------------- HTML TEMPLATE --------------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 ASHISH EMOTE PANEL v2.0</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #ff0000;
            --secondary: #00ff00;
            --accent: #00ffff;
            --dark: #0a0a0a;
            --gradient: linear-gradient(135deg, #ff0000 0%, #ff00ff 50%, #00ffff 100%);
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
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 0, 0, 0.05) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(0, 255, 255, 0.05) 0%, transparent 20%);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            padding: 30px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
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
        }

        .tab-content.active {
            display: block;
            animation: fadeIn 0.5s;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .input-group {
            margin-bottom: 20px;
        }

        .input-group label {
            display: block;
            margin-bottom: 8px;
            color: var(--accent);
            font-weight: 600;
        }

        .input-group input {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid var(--primary);
            border-radius: 10px;
            color: white;
            font-size: 16px;
            transition: all 0.3s;
        }

        .input-group input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        }

        .btn {
            background: var(--gradient);
            color: white;
            border: none;
            padding: 18px;
            border-radius: 10px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin: 20px 0;
            transition: all 0.3s;
            letter-spacing: 1px;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(255, 0, 0, 0.4);
        }

        .evo-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .evo-btn {
            background: linear-gradient(135deg, #ff0000, #ff5500);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
            text-align: center;
        }

        .evo-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(255, 0, 0, 0.3);
        }

        .emotes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .emote-card {
            background: rgba(30, 30, 30, 0.8);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s;
        }

        .emote-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            border-color: var(--primary);
        }

        .emote-name {
            color: #ffcc00;
            font-size: 1.2rem;
            margin-bottom: 10px;
        }

        .emote-id {
            color: var(--accent);
            background: rgba(0, 0, 0, 0.5);
            padding: 8px 12px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-family: monospace;
        }

        .send-btn {
            background: linear-gradient(135deg, #00ff00, #00cc00);
            color: #000;
            border: none;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            font-weight: bold;
            transition: all 0.3s;
        }

        .send-btn:hover {
            background: linear-gradient(135deg, #00ff88, #00ff00);
        }

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
            z-index: 1000;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #00ff00;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 20px;
            border-radius: 10px;
            display: none;
            font-weight: bold;
            z-index: 2000;
            animation: slideIn 0.3s;
            max-width: 400px;
        }

        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .notification.success {
            background: linear-gradient(135deg, #00ff00, #00cc00);
            color: #000;
        }

        .notification.error {
            background: linear-gradient(135deg, #ff0000, #cc0000);
            color: white;
        }

        .commands-list {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            max-height: 300px;
            overflow-y: auto;
        }

        .command-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid var(--accent);
        }

        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .evo-buttons { grid-template-columns: 1fr; }
            .emotes-grid { grid-template-columns: 1fr; }
            .status-bar { flex-direction: column; gap: 10px; }
            .tabs { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-fire"></i> ASHISH EMOTE PANEL v2.0</h1>
            <h2>⚡ Web Control Panel | Termux TCP Bot Integration</h2>
            <p style="color: #aaa; margin-top: 10px;">Send emotes remotely to Free Fire via Termux bot</p>
        </div>

        <div class="tabs">
            <button class="tab-btn active" onclick="openTab('quick')">
                <i class="fas fa-bolt"></i> QUICK EMOTE
            </button>
            <button class="tab-btn" onclick="openTab('evo')">
                <i class="fas fa-gun"></i> EVO GUNS
            </button>
            <button class="tab-btn" onclick="openTab('all')">
                <i class="fas fa-gamepad"></i> ALL EMOTES
            </button>
            <button class="tab-btn" onclick="openTab('status')">
                <i class="fas fa-chart-bar"></i> STATUS
            </button>
        </div>

        <!-- QUICK EMOTE TAB -->
        <div id="quick" class="tab-content active">
            <h3><i class="fas fa-rocket"></i> QUICK EMOTE ATTACK</h3>
            <p style="color: #aaa; margin-bottom: 20px;">Send emote to any player instantly</p>
            
            <form id="quickForm">
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE (7 digits)</label>
                    <input type="text" id="team_code" placeholder="1234567" pattern="\d{7}" required>
                </div>
                
                <div class="input-group">
                    <label><i class="fas fa-user"></i> TARGET UID</label>
                    <input type="text" id="target_uid" placeholder="4255057762" pattern="\d{8,11}" required>
                </div>
                
                <div class="input-group">
                    <label><i class="fas fa-smile"></i> EMOTE ID</label>
                    <input type="text" id="emote_id" placeholder="909033001" pattern="\d{9}" required>
                    <small style="color: #aaa;">Example: 909033001 (EVO M4A1)</small>
                </div>
                
                <button type="submit" class="btn">
                    <i class="fas fa-paper-plane"></i> SEND EMOTE VIA TERMUX BOT
                </button>
            </form>
            
            <div class="evo-buttons">
                <button class="evo-btn" onclick="setEmote('909033001')">
                    <i class="fas fa-gun"></i> M4A1 MAX
                </button>
                <button class="evo-btn" onclick="setEmote('909035007')">
                    <i class="fas fa-gun"></i> SHOTGUN MAX
                </button>
                <button class="evo-btn" onclick="setEmote('909000063')">
                    <i class="fas fa-gun"></i> AK47 MAX
                </button>
                <button class="evo-btn" onclick="setEmote('909000075')">
                    <i class="fas fa-fire"></i> COBRA RISING
                </button>
            </div>
        </div>

        <!-- EVO GUNS TAB -->
        <div id="evo" class="tab-content">
            <h3><i class="fas fa-gun"></i> EVO GUN EMOTE COLLECTION</h3>
            <p style="color: #aaa; margin-bottom: 20px;">Select EVO gun emote to send</p>
            
            <div class="input-group">
                <label><i class="fas fa-users"></i> TEAM CODE</label>
                <input type="text" id="evo_team" placeholder="1234567" pattern="\d{7}">
            </div>
            
            <div class="input-group">
                <label><i class="fas fa-user"></i> TARGET UID</label>
                <input type="text" id="evo_target" placeholder="4255057762" pattern="\d{8,11}">
            </div>
            
            <div class="evo-buttons">
                <!-- EVO Guns Grid -->
                <button class="evo-btn" onclick="sendEvo('909033001', 'M4A1 MAX')">
                    <i class="fas fa-gun"></i> M4A1 MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909000063', 'AK47 MAX')">
                    <i class="fas fa-gun"></i> AK47 MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909035007', 'SHOTGUN MAX')">
                    <i class="fas fa-gun"></i> SHOTGUN MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909000068', 'SCAR MAX')">
                    <i class="fas fa-gun"></i> SCAR MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909038012', 'G18 MAX')">
                    <i class="fas fa-gun"></i> G18 MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909040010', 'MP40 MAX')">
                    <i class="fas fa-gun"></i> MP40 MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909042008', 'WOODPECKER MAX')">
                    <i class="fas fa-gun"></i> WOODPECKER MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909041005', 'GROZA MAX')">
                    <i class="fas fa-gun"></i> GROZA MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909038010', 'THOMPSON MAX')">
                    <i class="fas fa-gun"></i> THOMPSON MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909045001', 'PARAFAL MAX')">
                    <i class="fas fa-gun"></i> PARAFAL MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909049010', 'P90 MAX')">
                    <i class="fas fa-gun"></i> P90 MAX
                </button>
                <button class="evo-btn" onclick="sendEvo('909051003', 'M60 MAX')">
                    <i class="fas fa-gun"></i> M60 MAX
                </button>
            </div>
        </div>

        <!-- ALL EMOTES TAB -->
        <div id="all" class="tab-content">
            <h3><i class="fas fa-gamepad"></i> ALL EMOTES ({{ total_emotes }} Total)</h3>
            <div class="input-group">
                <input type="text" id="searchEmote" placeholder="Search emotes by name or ID..." 
                       onkeyup="searchEmotes()">
            </div>
            
            <div class="emotes-grid" id="emotesContainer">
                <!-- Emotes will be loaded here -->
            </div>
            
            <div style="text-align: center; margin-top: 20px;">
                <button class="btn" onclick="loadMoreEmotes()">
                    <i class="fas fa-sync"></i> LOAD MORE EMOTES
                </button>
            </div>
        </div>

        <!-- STATUS TAB -->
        <div id="status" class="tab-content">
            <h3><i class="fas fa-chart-bar"></i> SYSTEM STATUS</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                <div style="background: rgba(0,100,0,0.2); padding: 20px; border-radius: 10px; border: 1px solid #00ff00;">
                    <h4><i class="fas fa-server"></i> WEB PANEL</h4>
                    <p style="color: #00ff00;">🟢 ONLINE</p>
                    <p>Render.com</p>
                </div>
                
                <div style="background: rgba(255,165,0,0.2); padding: 20px; border-radius: 10px; border: 1px solid #ffa500;">
                    <h4><i class="fas fa-robot"></i> TERMUX BOT</h4>
                    <p id="botStatus" style="color: #ffa500;">⏳ WAITING FOR CONNECTION</p>
                    <p>Run bot on Termux</p>
                </div>
                
                <div style="background: rgba(0,100,255,0.2); padding: 20px; border-radius: 10px; border: 1px solid #00aaff;">
                    <h4><i class="fas fa-commands"></i> COMMANDS QUEUE</h4>
                    <p id="queueCount" style="color: #00aaff;">0 pending</p>
                    <p>Commands waiting</p>
                </div>
            </div>
            
            <h4 style="margin-top: 30px;"><i class="fas fa-history"></i> RECENT COMMANDS</h4>
            <div class="commands-list" id="commandsList">
                <!-- Commands will be loaded here -->
            </div>
            
            <button class="btn" onclick="refreshStatus()" style="margin-top: 20px;">
                <i class="fas fa-sync-alt"></i> REFRESH STATUS
            </button>
        </div>
    </div>

    <div class="status-bar">
        <div class="status-item">
            <div class="status-dot"></div>
            <span>Web Panel: <span style="color: #00ff00;">ONLINE</span></span>
        </div>
        <div class="status-item">
            <i class="fas fa-robot"></i>
            <span>Termux Bot: <span id="botStatusBar">NOT CONNECTED</span></span>
        </div>
        <div class="status-item">
            <i class="fas fa-user"></i>
            <span>Developer: ASHISH</span>
        </div>
        <div class="status-item">
            <i class="fab fa-instagram"></i>
            <span>@ashish.shakya0001</span>
        </div>
    </div>

    <div class="notification" id="notification"></div>

    <script>
        let currentEmotesPage = 0;
        const emotesPerPage = 20;
        let allEmotes = [];
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadEmotes();
            refreshStatus();
            setInterval(refreshStatus, 5000); // Refresh every 5 seconds
        });
        
        function openTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active class from all buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Activate button
            event.currentTarget.classList.add('active');
        }
        
        function setEmote(emoteId) {
            document.getElementById('emote_id').value = emoteId;
            showNotification(`✅ Emote ID set to ${emoteId}`, 'success');
        }
        
        function sendEvo(emoteId, emoteName) {
            const team = document.getElementById('evo_team').value;
            const target = document.getElementById('evo_target').value;
            
            if (!team || !target) {
                showNotification('❌ Please enter Team Code and Target UID first!', 'error');
                return;
            }
            
            sendCommand(team, emoteId, target, emoteName);
        }
        
        // Quick Form Submission
        document.getElementById('quickForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const team = document.getElementById('team_code').value;
            const target = document.getElementById('target_uid').value;
            const emote = document.getElementById('emote_id').value;
            
            sendCommand(team, emote, target, 'Custom Emote');
        });
        
        function sendCommand(team, emote, target, emoteName) {
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
            
            // Send to server
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
                    showNotification(`✅ Command sent to Termux bot!`, 'success');
                    refreshStatus();
                } else {
                    showNotification(`❌ Error: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                showNotification('❌ Network error!', 'error');
            });
        }
        
        function loadEmotes() {
            fetch('/get_emotes')
                .then(r => r.json())
                .then(data => {
                    allEmotes = data.emotes;
                    displayEmotes();
                });
        }
        
        function displayEmotes() {
            const container = document.getElementById('emotesContainer');
            container.innerHTML = '';
            
            const start = currentEmotesPage * emotesPerPage;
            const end = start + emotesPerPage;
            const pageEmotes = allEmotes.slice(start, end);
            
            pageEmotes.forEach(emote => {
                const card = document.createElement('div');
                card.className = 'emote-card';
                card.innerHTML = `
                    <div class="emote-name">
                        <i class="fas fa-play-circle"></i> ${emote.name}
                    </div>
                    <div class="emote-id">ID: ${emote.id}</div>
                    <button class="send-btn" onclick="useEmote('${emote.id}', '${emote.name}')">
                        <i class="fas fa-paper-plane"></i> USE EMOTE
                    </button>
                `;
                container.appendChild(card);
            });
        }
        
        function useEmote(emoteId, emoteName) {
            // Switch to quick tab and set values
            document.querySelector('.tab-btn.active').classList.remove('active');
            document.querySelector('.tab-content.active').classList.remove('active');
            
            document.querySelector('[onclick="openTab(\'quick\')"]').classList.add('active');
            document.getElementById('quick').classList.add('active');
            
            // Set emote ID
            document.getElementById('emote_id').value = emoteId;
            document.getElementById('emote_id').focus();
            
            showNotification(`🎭 ${emoteName} selected! Enter Team Code and Target UID`, 'success');
        }
        
        function loadMoreEmotes() {
            currentEmotesPage++;
            displayEmotes();
        }
        
        function searchEmotes() {
            const search = document.getElementById('searchEmote').value.toLowerCase();
            const container = document.getElementById('emotesContainer');
            
            if (!search) {
                currentEmotesPage = 0;
                displayEmotes();
                return;
            }
            
            const filtered = allEmotes.filter(emote => 
                emote.name.toLowerCase().includes(search) || 
                emote.id.includes(search)
            );
            
            container.innerHTML = '';
            filtered.slice(0, 50).forEach(emote => {
                const card = document.createElement('div');
                card.className = 'emote-card';
                card.innerHTML = `
                    <div class="emote-name">
                        <i class="fas fa-play-circle"></i> ${emote.name}
                    </div>
                    <div class="emote-id">ID: ${emote.id}</div>
                    <button class="send-btn" onclick="useEmote('${emote.id}', '${emote.name}')">
                        <i class="fas fa-paper-plane"></i> USE EMOTE
                    </button>
                `;
                container.appendChild(card);
            });
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
                    document.getElementById('queueCount').innerHTML = 
                        `${data.pending_commands} pending`;
                    
                    // Update commands list
                    const commandsList = document.getElementById('commandsList');
                    commandsList.innerHTML = '';
                    
                    data.recent_commands.forEach(cmd => {
                        const item = document.createElement('div');
                        item.className = 'command-item';
                        item.innerHTML = `
                            <div><strong>#${cmd.id}</strong> | ${cmd.timestamp}</div>
                            <div>Team: ${cmd.team_code} | Emote: ${cmd.emote_id}</div>
                            <div>Target: ${cmd.target_uid} | Status: <span style="color: ${cmd.status === 'executed' ? '#00ff00' : '#ffff00'}">${cmd.status}</span></div>
                        `;
                        commandsList.appendChild(item);
                    });
                });
        }
        
        function showNotification(message, type) {
            const notif = document.getElementById('notification');
            notif.textContent = message;
            notif.className = `notification ${type}`;
            notif.style.display = 'block';
            
            setTimeout(() => {
                notif.style.display = 'none';
            }, 4000);
        }
    </script>
</body>
</html>
'''

# -------------------- FLASK ROUTES --------------------
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, total_emotes=len(EMOTES))

@app.route('/send', methods=['POST'])
def send_command():
    try:
        team_code = request.form.get('team_code', '').strip()
        emote_id = request.form.get('emote_id', '').strip()
        target_uid = request.form.get('target_uid', '').strip()
        
        # Validation
        if not re.match(r'^\d{7}$', team_code):
            return jsonify({"success": False, "error": "Team code must be 7 digits"})
        
        if not re.match(r'^\d{8,11}$', target_uid):
            return jsonify({"success": False, "error": "Target UID must be 8-11 digits"})
        
        if not re.match(r'^\d{9}$', emote_id):
            return jsonify({"success": False, "error": "Emote ID must be 9 digits"})
        
        # Save command
        user_ip = request.remote_addr
        command_id = command_manager.save_command(team_code, emote_id, target_uid, user_ip)
        
        if command_id:
            return jsonify({
                "success": True,
                "message": f"Command #{command_id} saved successfully!",
                "command_id": command_id,
                "note": "Command will be executed when Termux bot is running"
            })
        else:
            return jsonify({"success": False, "error": "Failed to save command"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/get_emotes')
def get_emotes():
    return jsonify({"emotes": EMOTES})

@app.route('/status')
def status():
    pending = command_manager.get_pending_commands()
    
    # Simulate bot connection status
    # In real setup, you would check if bot is connected
    bot_connected = len(pending) > 0  # Simple check
    
    return jsonify({
        "bot_connected": bot_connected,
        "pending_commands": len(pending),
        "recent_commands": pending[:10],
        "web_panel": "online",
        "total_emotes": len(EMOTES)
    })

@app.route('/get_commands')
def get_commands():
    """For Termux bot to fetch commands"""
    pending = command_manager.get_pending_commands()
    return jsonify({"commands": pending})

@app.route('/mark_executed/<int:command_id>', methods=['POST'])
def mark_executed(command_id):
    """For Termux bot to mark command as executed"""
    success = command_manager.mark_executed(command_id)
    return jsonify({"success": success})

# -------------------- MAIN --------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
