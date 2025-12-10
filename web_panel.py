from flask import Flask, render_template_string, request, jsonify
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

# ==================== EMOTE DATABASE ====================
EMOTE_DATABASE = {
    "EVO_GUNS": [
        {"name": "🔥 EVO MP40", "id": "909000075", "icon": "fa-gun", "color": "#00D4FF"},
        {"name": "🔥 EVO AK", "id": "909000063", "icon": "fa-gun", "color": "#00D4FF"},
        {"name": "🔥 EVO UMP", "id": "909000098", "icon": "fa-gun", "color": "#00D4FF"},
    ],
    "SPECIAL_EMOTES": [
        {"name": "💰 PAISA EMOTE", "id": "909000055", "icon": "fa-money-bill-wave", "color": "#FFCC00"},
        {"name": "💖 HEART EMOTE", "id": "909000045", "icon": "fa-heart", "color": "#FF2A6D"},
    ]
}

ALL_EMOTES = []
for category in EMOTE_DATABASE.values():
    ALL_EMOTES.extend(category)

TOTAL_EMOTES = len(ALL_EMOTES)

# ==================== STORAGE ====================
storage = {
    "commands": [],
    "last_id": 0,
    "stats": {"total": 0, "today": 0},
    "last_bot_ping": None
}

# ==================== HTML TEMPLATE ====================
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 ASHISH EMOTE PANEL</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%);
            color: white;
            font-family: 'Montserrat', sans-serif;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 40px;
            background: rgba(0, 212, 255, 0.1);
            border-radius: 20px;
            margin-bottom: 30px;
            border: 2px solid #00D4FF;
        }
        .logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            background: linear-gradient(45deg, #00D4FF, #FF0055);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .input-group {
            margin: 20px 0;
        }
        .input-group label {
            display: block;
            margin-bottom: 8px;
            color: #00D4FF;
            font-weight: 600;
        }
        .input-group input {
            width: 100%;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border: 2px solid #00D4FF;
            border-radius: 10px;
            color: white;
            font-size: 1.1rem;
        }
        .btn {
            background: linear-gradient(45deg, #00D4FF, #FF0055);
            color: white;
            border: none;
            padding: 18px 30px;
            border-radius: 10px;
            font-size: 1.2rem;
            font-weight: 700;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
        }
        .emote-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
        }
        .emote-card {
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
            border: 2px solid;
            transition: 0.3s;
        }
        .emote-card:hover {
            transform: translateY(-5px);
        }
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 10px;
            display: none;
            font-weight: bold;
        }
        .success { background: #00FF88; color: #000; }
        .error { background: #FF2A6D; color: white; }
    </style>
</head>
<body>
    <div class="notification" id="notification"></div>
    <div class="container">
        <div class="header">
            <h1 class="logo">🔥 ASHISH EMOTE PANEL</h1>
            <p>⚡ Professional Emote Delivery System</p>
        </div>
        
        <div class="input-group">
            <label>Team Code</label>
            <input type="text" id="teamCode" placeholder="1234567" value="1234567">
        </div>
        
        <div class="input-group">
            <label>Target UID</label>
            <input type="text" id="targetUid" placeholder="13706108657" value="13706108657">
        </div>
        
        <div class="input-group">
            <label>Emote ID</label>
            <input type="text" id="emoteId" placeholder="909033001" value="909033001">
        </div>
        
        <button class="btn" onclick="sendCommand()">
            <i class="fas fa-rocket"></i> SEND EMOTE
        </button>
        
        <h2 style="margin: 40px 0 20px 0; color: #00D4FF;">Available Emotes</h2>
        <div class="emote-grid">
            {% for emote in all_emotes %}
            <div class="emote-card" style="border-color: {{ emote.color }};" onclick="selectEmote('{{ emote.id }}', '{{ emote.name }}')">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="width: 50px; height: 50px; border-radius: 10px; background: {{ emote.color }}; display: flex; align-items: center; justify-content: center;">
                        <i class="fas {{ emote.icon }}" style="color: white; font-size: 1.5rem;"></i>
                    </div>
                    <div>
                        <div style="font-weight: 700; font-size: 1.2rem;">{{ emote.name }}</div>
                        <div style="color: #aaa; font-family: monospace;">{{ emote.id }}</div>
                    </div>
                </div>
                <button style="margin-top: 15px; padding: 10px; background: {{ emote.color }}; border: none; border-radius: 8px; color: white; width: 100%;" 
                        onclick="sendEmote('{{ emote.id }}')">
                    <i class="fas fa-paper-plane"></i> Send
                </button>
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
        function selectEmote(id, name) {
            document.getElementById('emoteId').value = id;
            showNotification('✅ Selected: ' + name, 'success');
        }
        
        function sendEmote(emoteId) {
            const team = document.getElementById('teamCode').value;
            const target = document.getElementById('targetUid').value;
            
            if (!team || !target) {
                showNotification('❌ Enter Team Code and Target UID', 'error');
                return;
            }
            
            sendCommandToServer(team, emoteId, target);
        }
        
        function sendCommand() {
            const team = document.getElementById('teamCode').value;
            const target = document.getElementById('targetUid').value;
            const emote = document.getElementById('emoteId').value;
            
            if (!team || !target || !emote) {
                showNotification('❌ Fill all fields', 'error');
                return;
            }
            
            sendCommandToServer(team, emote, target);
        }
        
        function sendCommandToServer(team, emote, target) {
            const btn = document.querySelector('.btn');
            const original = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> SENDING...';
            btn.disabled = true;
            
            fetch('/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: 'team_code=' + team + '&emote_id=' + emote + '&target_uid=' + target
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    showNotification('🚀 Emote sent successfully!', 'success');
                } else {
                    showNotification('❌ Error: ' + data.error, 'error');
                }
            })
            .catch(() => {
                showNotification('❌ Network error', 'error');
            })
            .finally(() => {
                setTimeout(() => {
                    btn.innerHTML = original;
                    btn.disabled = false;
                }, 1000);
            });
        }
        
        function showNotification(message, type) {
            const notif = document.getElementById('notification');
            notif.textContent = message;
            notif.className = 'notification ' + type;
            notif.style.display = 'block';
            setTimeout(() => {
                notif.style.display = 'none';
            }, 3000);
        }
    </script>
</body>
</html>
'''

# ==================== ROUTES ====================
@app.route('/')
def home():
    return render_template_string(HTML, all_emotes=ALL_EMOTES)

@app.route('/send', methods=['POST'])
def send_command():
    try:
        team = request.form.get('team_code', '').strip()
        emote = request.form.get('emote_id', '').strip()
        target = request.form.get('target_uid', '').strip()
        
        print(f"✅ Command received: Team={team}, Emote={emote}, Target={target}")
        
        storage["last_id"] += 1
        command = {
            "id": storage["last_id"],
            "team_code": team,
            "emote_id": emote,
            "target_uid": target,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "status": "pending"
        }
        storage["commands"].append(command)
        storage["stats"]["total"] += 1
        storage["stats"]["today"] += 1
        
        return jsonify({
            "success": True,
            "message": f"Command #{storage['last_id']} received",
            "command_id": storage["last_id"]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/get_commands')
def get_commands():
    pending = [c for c in storage["commands"] if c.get("status") == "pending"]
    return jsonify({
        "success": True,
        "commands": pending,
        "total": len(pending)
    })

@app.route('/mark_executed/<int:command_id>', methods=['POST'])
def mark_executed(command_id):
    for cmd in storage["commands"]:
        if cmd["id"] == command_id:
            cmd["status"] = "executed"
            return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/bot_ping', methods=['POST'])
def bot_ping():
    storage["last_bot_ping"] = datetime.now()
    return jsonify({"success": True, "message": "Ping received"})

@app.route('/status')
def status():
    return jsonify({
        "success": True,
        "total_commands": storage["stats"]["total"],
        "today_commands": storage["stats"]["today"],
        "last_bot_ping": storage["last_bot_ping"].isoformat() if storage["last_bot_ping"] else None
    })

@app.route('/ping')
def ping():
    return jsonify({
        "status": "online",
        "message": "Ashish Emote Panel",
        "time": datetime.now().strftime("%H:%M:%S"),
        "total_emotes": TOTAL_EMOTES
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/test')
def test():
    return jsonify({"message": "Server is working!"})

# ==================== MAIN ====================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🔥 ASHISH EMOTE PANEL STARTING...")
    print(f"🌐 Port: {port}")
    print(f"🎮 Emotes: {TOTAL_EMOTES}")
    print("✅ Endpoints: /, /send, /ping, /status, /get_commands, /bot_ping")
    app.run(host='0.0.0.0', port=port, debug=False)
