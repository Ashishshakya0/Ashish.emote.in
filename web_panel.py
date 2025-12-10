from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ashish-bot-panel-2024')

# -------------------- SIMPLE IN-MEMORY STORAGE --------------------
# No file needed - everything in memory
command_storage = {
    "commands": [],
    "last_id": 0,
    "stats": {"total": 0, "today": 0}
}

bot_status_storage = {
    "last_seen": "Never",
    "bot_uid": "Unknown",
    "status": "offline"
}

# -------------------- COMMAND MANAGER --------------------
class CommandManager:
    def __init__(self):
        self.storage = command_storage
    
    def save_command(self, team_code, emote_id, target_uid, user_ip):
        try:
            command_id = self.storage["last_id"] + 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Find emote name
            emote_name = "Unknown Emote"
            if emote_id == "909000001":
                emote_name = "Hello!"
            elif emote_id == "909033001":
                emote_name = "EVO M4A1 MAX"
            elif emote_id == "909000075":
                emote_name = "COBRA RISING"
            else:
                emote_name = f"Emote {emote_id}"
            
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
            
            self.storage["commands"].append(command)
            self.storage["last_id"] = command_id
            self.storage["stats"]["total"] += 1
            
            print(f"✅ Command #{command_id} saved: {team_code} -> {target_uid}")
            return command_id
            
        except Exception as e:
            print(f"❌ Save error: {e}")
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

        /* FORM STYLING */
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

        /* EMOTE CARDS */
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
            border: 2px solid #ff5500;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
        }

        .emote-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(255, 85, 0, 0.3);
        }

        .emote-icon {
            font-size: 2rem;
            color: #ffaa00;
            margin-bottom: 10px;
        }

        .emote-name {
            font-size: 1.2rem;
            color: white;
            margin-bottom: 10px;
        }

        .emote-id {
            background: rgba(255, 85, 0, 0.2);
            color: #ffaa00;
            padding: 5px 10px;
            border-radius: 15px;
            font-family: monospace;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }

        .send-btn {
            background: linear-gradient(135deg, #ff5500, #ff0000);
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
            <h2>⚡ Send Emotes Instantly | Termux Bot Integrated</h2>
        </div>

        <!-- TABS -->
        <div class="tabs">
            <button class="tab-btn active" onclick="openTab('send')">
                <i class="fas fa-paper-plane"></i> SEND EMOTE
            </button>
            <button class="tab-btn" onclick="openTab('status')">
                <i class="fas fa-chart-bar"></i> STATUS
            </button>
        </div>

        <!-- SEND EMOTE TAB -->
        <div id="send" class="tab-content active">
            <h3 style="color: var(--accent); text-align: center; margin-bottom: 20px;">
                <i class="fas fa-rocket"></i> INSTANT EMOTE SENDER
            </h3>
            
            <div class="input-form">
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE (Any 7 digits)</label>
                    <input type="text" id="team_code" placeholder="1234567" value="1234567">
                </div>
                <div class="input-group">
                    <label><i class="fas fa-user"></i> TARGET UID (Your UID)</label>
                    <input type="text" id="target_uid" placeholder="13706108657" value="13706108657">
                </div>
            </div>

            <h4 style="color: #ffaa00; text-align: center; margin: 20px 0;">
                <i class="fas fa-gun"></i> POPULAR EMOTES
            </h4>

            <div class="emote-grid">
                <div class="emote-card" onclick="sendEmote('909000001', 'Hello! Emote')">
                    <div class="emote-icon">
                        <i class="fas fa-hand"></i>
                    </div>
                    <div class="emote-name">👋 Hello!</div>
                    <div class="emote-id">ID: 909000001</div>
                    <button class="send-btn">
                        <i class="fas fa-paper-plane"></i> SEND
                    </button>
                </div>
                
                <div class="emote-card" onclick="sendEmote('909033001', 'EVO M4A1 MAX')">
                    <div class="emote-icon">
                        <i class="fas fa-gun"></i>
                    </div>
                    <div class="emote-name">🔥 EVO M4A1 MAX</div>
                    <div class="emote-id">ID: 909033001</div>
                    <button class="send-btn">
                        <i class="fas fa-paper-plane"></i> SEND
                    </button>
                </div>
                
                <div class="emote-card" onclick="sendEmote('909000075', 'COBRA RISING')">
                    <div class="emote-icon">
                        <i class="fas fa-fire"></i>
                    </div>
                    <div class="emote-name">🐍 COBRA RISING</div>
                    <div class="emote-id">ID: 909000075</div>
                    <button class="send-btn">
                        <i class="fas fa-paper-plane"></i> SEND
                    </button>
                </div>
                
                <div class="emote-card" onclick="sendCustomEmote()">
                    <div class="emote-icon">
                        <i class="fas fa-edit"></i>
                    </div>
                    <div class="emote-name">📝 CUSTOM EMOTE</div>
                    <div class="input-group" style="margin-top: 10px;">
                        <input type="text" id="custom_emote" placeholder="909000002" style="text-align: center;">
                    </div>
                    <button class="send-btn" onclick="sendCustomEmote()">
                        <i class="fas fa-paper-plane"></i> SEND CUSTOM
                    </button>
                </div>
            </div>
        </div>

        <!-- STATUS TAB -->
        <div id="status" class="tab-content">
            <h3 style="color: var(--accent); text-align: center; margin-bottom: 20px;">
                <i class="fas fa-chart-bar"></i> SYSTEM STATUS
            </h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px;">
                <div style="background: rgba(0,100,0,0.2); padding: 15px; border-radius: 10px; border: 1px solid #00ff00;">
                    <h4><i class="fas fa-server"></i> WEB PANEL</h4>
                    <p style="color: #00ff00;">🟢 ONLINE</p>
                    <p style="color: #aaa; font-size: 0.9rem;">Render.com</p>
                </div>
                
                <div style="background: rgba(255,165,0,0.2); padding: 15px; border-radius: 10px; border: 1px solid #ffa500;">
                    <h4><i class="fas fa-robot"></i> TERMUX BOT</h4>
                    <p id="botStatus" style="color: #ffa500;">⏳ CHECKING</p>
                    <p style="color: #aaa; font-size: 0.9rem;">Run on Termux</p>
                </div>
                
                <div style="background: rgba(0,100,255,0.2); padding: 15px; border-radius: 10px; border: 1px solid #00aaff;">
                    <h4><i class="fas fa-commands"></i> COMMANDS</h4>
                    <p id="queueCount" style="color: #00aaff;">0 pending</p>
                    <p style="color: #aaa; font-size: 0.9rem;">Total: <span id="totalCommands">0</span></p>
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
            
            <button class="btn" onclick="refreshStatus()" style="margin-top: 20px;">
                <i class="fas fa-sync-alt"></i> REFRESH STATUS
            </button>
        </div>
    </div>

    <!-- STATUS BAR -->
    <div class="status-bar">
        <div class="status-item">
            <i class="fas fa-circle" style="color: #00ff00;"></i>
            <span>Web Panel: ONLINE</span>
        </div>
        <div class="status-item">
            <i class="fas fa-robot"></i>
            <span>Termux Bot: <span id="botStatusBar">CHECKING</span></span>
        </div>
        <div class="status-item">
            <i class="fas fa-user"></i>
            <span>ASHISH</span>
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
            
            // Remove active class from buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Activate clicked button
            event.currentTarget.classList.add('active');
        }
        
        // Send emote
        function sendEmote(emoteId, emoteName) {
            const team = document.getElementById('team_code').value;
            const target = document.getElementById('target_uid').value;
            
            if (!team || !target) {
                showNotification('❌ Please enter Team Code and Target UID!', 'error');
                return;
            }
            
            sendCommand(team, emoteId, target, emoteName);
        }
        
        // Send custom emote
        function sendCustomEmote() {
            const team = document.getElementById('team_code').value;
            const target = document.getElementById('target_uid').value;
            const emote = document.getElementById('custom_emote').value;
            
            if (!emote) {
                showNotification('❌ Please enter Emote ID!', 'error');
                return;
            }
            
            sendCommand(team, emote, target, 'Custom Emote');
        }
        
        // Send command to server
        function sendCommand(team, emote, target, emoteName = '') {
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
                    showNotification(`✅ ${emoteName} sent! Command #${data.command_id}`, 'success');
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
                    document.getElementById('totalCommands').innerHTML = 
                        data.total_commands;
                    
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
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            refreshStatus();
            setInterval(refreshStatus, 5000);
        });
    </script>
</body>
</html>
'''

# -------------------- FLASK ROUTES --------------------
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send', methods=['POST'])
def send_command():
    """Save command - NO FILE VALIDATION"""
    try:
        team_code = request.form.get('team_code', '').strip()
        emote_id = request.form.get('emote_id', '').strip()
        target_uid = request.form.get('target_uid', '').strip()
        
        print(f"📥 Received command: Team={team_code}, Emote={emote_id}, Target={target_uid}")
        
        user_ip = request.remote_addr
        command_id = command_manager.save_command(team_code, emote_id, target_uid, user_ip)
        
        if command_id:
            return jsonify({
                "success": True,
                "message": f"Command #{command_id} saved successfully!",
                "command_id": command_id,
                "note": "Termux bot will execute this command"
            })
        else:
            return jsonify({"success": False, "error": "Server error - try again"})
            
    except Exception as e:
        print(f"❌ Route error: {e}")
        return jsonify({"success": False, "error": "Internal server error"})

@app.route('/status')
def status():
    """System status"""
    pending = [cmd for cmd in command_storage["commands"] if not cmd.get("executed", False)]
    
    return jsonify({
        "bot_connected": len(pending) > 0,
        "pending_commands": len(pending),
        "total_commands": command_storage["stats"]["total"],
        "recent_commands": command_storage["commands"][-10:] if command_storage["commands"] else []
    })

@app.route('/get_commands')
def get_commands():
    """Get all commands"""
    return jsonify({"commands": command_storage["commands"]})

@app.route('/mark_executed/<int:command_id>', methods=['POST'])
def mark_executed(command_id):
    """Mark command as executed"""
    try:
        for cmd in command_storage["commands"]:
            if cmd["id"] == command_id:
                cmd["executed"] = True
                cmd["status"] = "executed"
                print(f"✅ Command #{command_id} marked as executed")
                return jsonify({"success": True})
        
        return jsonify({"success": False, "error": "Command not found"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# -------------------- MAIN --------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Starting Ashish Emote Panel on port {port}")
    print(f"✅ In-memory storage active")
    print(f"✅ No file dependencies")
    app.run(host='0.0.0.0', port=port, debug=False)
