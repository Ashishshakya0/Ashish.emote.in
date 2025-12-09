import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp, asyncio, random, subprocess
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import *; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2
from cfonts import render, say
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import re

# EMOTES BY ASHISH 
# FIXED BY WINTER ❄️ 
# MODIFIED BY ASHISH 

# Try to import Flask (for web panel)
try:
    from flask import Flask, render_template_string, request, jsonify
    FLASK_AVAILABLE = True
    print("✅ Flask loaded successfully")
except ImportError:
    FLASK_AVAILABLE = False
    print("⚠️ Flask not available, web panel disabled")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# Variables
#------------------------------------------#
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
server2 = "ind"
key1 = "Xr_Kanha"  # optional, chaho to hata bhi sakte ho
key2 = "Xr_Kanha"  # Added missing key2
# owner protection (change to your own uid)
#----------------------------#

# Initialize Flask app if available
if FLASK_AVAILABLE:
    app = Flask(__name__)
else:
    app = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMANDS_FILE = os.path.join(BASE_DIR, "commands.txt")

EMOTES = [
    # Basic Emotes (909000001-909000150)
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
    {"name": "Furious Slam", "id": "909000021"},
    {"name": "Moon Flip", "id": "909000022"},
    {"name": "Wiggle Walk", "id": "909000023"},
    {"name": "Battle Dance", "id": "909000024"},
    {"name": "High Five", "id": "909000025"},
    {"name": "Shake It Up", "id": "909000026"},
    {"name": "Glorious Spin", "id": "909000027"},
    {"name": "Crane Kick", "id": "909000028"},
    {"name": "Party Dance", "id": "909000029"},
    {"name": "Jig Dance", "id": "909000031"},
    {"name": "Selfie", "id": "909000032"},
    {"name": "Soul Shaking", "id": "909000033"},
    {"name": "Pirate's Flag", "id": "909000034"},
    {"name": "Healing Dance", "id": "909000035"},
    {"name": "Top DJ", "id": "909000036"},
    {"name": "Death Glare", "id": "909000037"},
    {"name": "Power of Money", "id": "909000038"},
    {"name": "Eat My Dust", "id": "909000039"},
    {"name": "Breakdance", "id": "909000040"},
    {"name": "Kungfu", "id": "909000041"},
    {"name": "Bon Appetit", "id": "909000042"},
    {"name": "Aim; Fire!", "id": "909000043"},
    {"name": "The Swan", "id": "909000044"},
    {"name": "I Heart You", "id": "909000045"},
    {"name": "Tea Time", "id": "909000046"},
    {"name": "Bring It On!", "id": "909000047"},
    {"name": "Why? Oh Why?", "id": "909000048"},
    {"name": "Fancy Hands", "id": "909000049"},
    {"name": "Shimmy", "id": "909000051"},
    {"name": "Doggie", "id": "909000052"},
    {"name": "Challenge On!", "id": "909000053"},
    {"name": "Lasso", "id": "909000054"},
    {"name": "I'm Rich!", "id": "909000055"},
    {"name": "More Practice", "id": "909000079"},
    {"name": "FFWS 2021", "id": "909000080"},
    {"name": "Draco's Soul", "id": "909000081"},
    {"name": "Good Game", "id": "909000082"},
    {"name": "Greetings", "id": "909000083"},
    {"name": "The Walker", "id": "909000084"},
    {"name": "Born of Light", "id": "909000085"},
    {"name": "Mythos Four", "id": "909000086"},
    {"name": "Champion Grab", "id": "909000087"},
    {"name": "Win and Chill", "id": "909000088"},
    {"name": "Hadouken", "id": "909000089"},
    {"name": "Blood Wraith", "id": "909000090"},
    {"name": "Big Smash", "id": "909000091"},
    {"name": "Fancy Steps", "id": "909000092"},
    {"name": "All In Control", "id": "909000093"},
    {"name": "Debugging", "id": "909000094"},
    {"name": "Waggor Wave", "id": "909000095"},
    {"name": "Crazy Guitar", "id": "909000096"},
    {"name": "Poof", "id": "909000097"},
    {"name": "The Chosen Victor", "id": "909000098"},
    {"name": "Challenger", "id": "909000099"},
    
    # Special Emotes
    {"name": "Cobra Rising", "id": "909000075"},
    {"name": "Ak Max", "id": "909000063"},
    {"name": "Shotgun Max", "id": "909035007"},
    {"name": "Scar Max", "id": "909000068"},
    {"name": "XMB Max", "id": "909000085"},
    {"name": "G18 Max", "id": "909038012"},
    {"name": "MP40 Max", "id": "909040010"},
    {"name": "Famas Max", "id": "909000090"},
    {"name": "UMP Max", "id": "909000098"},
    {"name": "Woodpecker Max", "id": "909042008"},
    {"name": "Groza Max", "id": "909041005"},
    {"name": "M4A1 Max", "id": "909033001"},
    {"name": "Thompson Max", "id": "909038010"},
    {"name": "Parafal Max", "id": "909045001"},
    {"name": "P90 Max", "id": "909049010"},
    {"name": "M60 Max", "id": "909051003"},
    
    # Additional Popular Emotes
    {"name": "Fireborn", "id": "909033001"},
    {"name": "Golden Feather", "id": "909033002"},
    {"name": "Come and Dance", "id": "909033003"},
    {"name": "Drop Kick", "id": "909033004"},
    {"name": "Sit Down!", "id": "909033005"},
    {"name": "BOOYAH Sparks", "id": "909033006"},
    {"name": "The FFWS Dance", "id": "909033007"},
    {"name": "Easy Peasy", "id": "909033008"},
    {"name": "Winner Throw", "id": "909033009"},
    {"name": "Weight of Victory", "id": "909033010"},
]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>🔥 ASHISH EMOTE PANEL</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial; }
        body { background: #000; color: #fff; min-height: 100vh; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: #111; border-radius: 10px; padding: 20px; border: 2px solid #ff0000; }
        .header { text-align: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #ff0000; }
        .header h1 { color: #ff0000; font-size: 2.5rem; margin-bottom: 10px; }
        .header h2 { color: #00ff00; font-size: 1.2rem; }
        .section { margin: 20px 0; padding: 20px; background: #222; border-radius: 10px; }
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; margin-bottom: 8px; color: #00ffff; font-weight: bold; }
        .input-group input { width: 100%; padding: 12px; background: #000; border: 2px solid #00ff00; border-radius: 5px; color: white; font-size: 16px; }
        .btn { background: #ff0000; color: white; border: none; padding: 15px; border-radius: 5px; font-size: 1.1rem; cursor: pointer; width: 100%; margin: 20px 0; }
        .btn:hover { background: #ff4444; }
        .emotes-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }
        .emote-card { background: #333; border-radius: 10px; padding: 15px; border: 1px solid #ff0000; }
        .emote-name { color: #ffcc00; font-size: 1.2rem; margin-bottom: 10px; }
        .emote-id { color: #00ffff; background: #000; padding: 8px; border-radius: 5px; margin-bottom: 15px; }
        .send-btn { background: #00ff00; color: #000; border: none; padding: 12px; border-radius: 5px; cursor: pointer; width: 100%; font-weight: bold; }
        .send-btn:hover { background: #00ff88; }
        .status-bar { position: fixed; bottom: 0; left: 0; right: 0; background: #111; padding: 10px; display: flex; justify-content: space-between; border-top: 2px solid #ff0000; }
        .notification { position: fixed; top: 20px; right: 20px; background: #00ff00; color: #000; padding: 15px; border-radius: 5px; display: none; font-weight: bold; }
        .notification.error { background: #ff0000; color: white; }
        @media (max-width: 768px) {
            .container { padding: 15px; margin: 10px; }
            .emotes-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 ASHISH EMOTE PANEL</h1>
            <h2>Fast Emote Sending System</h2>
        </div>
        
        <form id="mainForm" method="POST">
            <div class="section">
                <h3>TEAM INFORMATION</h3>
                <div class="input-group">
                    <label>TEAM CODE (7 digits)</label>
                    <input type="text" name="team_code" placeholder="Enter 7-digit team code" required 
                           pattern="[0-9]{7}" title="7 digit team code">
                </div>
            </div>
            
            <div class="section">
                <h3>PLAYER UIDs</h3>
                <div class="input-group">
                    <label>UID 1 (YOUR UID) - Required</label>
                    <input type="text" name="uid1" placeholder="Enter your UID (8-11 digits)" required 
                           pattern="[0-9]{8,11}" title="8-11 digits">
                </div>
                <div class="input-group">
                    <label>UID 2 (Optional)</label>
                    <input type="text" name="uid2" placeholder="Friend's UID" pattern="[0-9]{8,11}">
                </div>
                <div class="input-group">
                    <label>UID 3 (Optional)</label>
                    <input type="text" name="uid3" placeholder="Friend's UID" pattern="[0-9]{8,11}">
                </div>
                <div class="input-group">
                    <label>UID 4 (Optional)</label>
                    <input type="text" name="uid4" placeholder="Friend's UID" pattern="[0-9]{8,11}">
                </div>
            </div>
            
            <button type="submit" class="btn">SHOW EMOTES</button>
        </form>
        
        {% if show_emotes %}
        <div class="section">
            <h3>SELECT EMOTE</h3>
            <div class="emotes-grid">
                {% for emote in emotes %}
                <div class="emote-card">
                    <div class="emote-name">{{ emote.name }}</div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <form method="POST" action="/send" class="send-form">
                        <input type="hidden" name="team_code" value="{{ team_code }}">
                        <input type="hidden" name="emote_id" value="{{ emote.id }}">
                        <input type="hidden" name="uid1" value="{{ uid1 }}">
                        <input type="hidden" name="uid2" value="{{ uid2 }}">
                        <input type="hidden" name="uid3" value="{{ uid3 }}">
                        <input type="hidden" name="uid4" value="{{ uid4 }}">
                        <button type="submit" class="send-btn">SEND EMOTE</button>
                    </form>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
    
    <div class="status-bar">
        <div>Status: <span id="status">READY</span></div>
        <div>Commands Sent: <span id="count">0</span></div>
        <div>User: ASHISH</div>
    </div>
    
    <div class="notification" id="notification"></div>
    
    <script>
        let commandCount = 0;
        
        function showNotification(message, type = 'success') {
            const notif = document.getElementById('notification');
            notif.textContent = message;
            notif.className = 'notification ' + (type === 'error' ? 'error' : '');
            notif.style.display = 'block';
            
            setTimeout(() => {
                notif.style.display = 'none';
            }, 3000);
        }
        
        function updateStatus() {
            document.getElementById('count').textContent = commandCount;
        }
        
        document.querySelectorAll('.send-form').forEach(form => {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                const button = this.querySelector('.send-btn');
                const originalText = button.textContent;
                
                button.textContent = 'SENDING...';
                button.disabled = true;
                
                fetch('/send', {
                    method: 'POST',
                    body: formData
                })
                .then(r => r.json())
                .then(data => {
                    if(data.success) {
                        commandCount++;
                        updateStatus();
                        showNotification('✅ Emote sent successfully!');
                    } else {
                        showNotification('❌ ' + data.error, 'error');
                    }
                })
                .catch(() => {
                    showNotification('❌ Network error', 'error');
                })
                .finally(() => {
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 1000);
                });
            });
        });
        
        document.getElementById('mainForm').addEventListener('submit', function(e) {
            const teamCode = this.querySelector('[name="team_code"]').value;
            const uid1 = this.querySelector('[name="uid1"]').value;
            
            if(!/^\d{7}$/.test(teamCode)) {
                showNotification('❌ Team code must be 7 digits!', 'error');
                e.preventDefault();
                return false;
            }
            
            if(!/^\d{8,11}$/.test(uid1)) {
                showNotification('❌ UID must be 8-11 digits!', 'error');
                e.preventDefault();
                return false;
            }
        });
        
        updateStatus();
    </script>
</body>
</html>
'''

class BotManager:
    def __init__(self):
        self.commands_sent = 0
    
    def send_command(self, command):
        """Send command to bot via commands.txt"""
        try:
            parts = command.split()
            if len(parts) < 4:
                return False
            
            team_code = parts[1]
            if not re.match(r'^\d{7}$', team_code):
                return False
            
            uid = parts[3]
            if not re.match(r'^\d{8,11}$', uid):
                return False
            
            # Write command to file
            with open(COMMANDS_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{command}\n")
                f.flush()
            
            print(f"✅ Web Command saved: {command}")
            self.commands_sent += 1
            return True
            
        except Exception as e:
            print(f"❌ Web Error: {e}")
            return False

bot_manager = BotManager()

# Flask Routes (only if Flask is available)
if FLASK_AVAILABLE and app:
    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            team_code = request.form['team_code']
            uid1 = request.form['uid1']
            uid2 = request.form.get('uid2', '')
            uid3 = request.form.get('uid3', '')
            uid4 = request.form.get('uid4', '')
            
            # Validate
            if not re.match(r'^\d{7}$', team_code):
                return render_template_string(HTML, show_emotes=False)
            
            if not re.match(r'^\d{8,11}$', uid1):
                return render_template_string(HTML, show_emotes=False)
            
            return render_template_string(HTML,
                show_emotes=True,
                emotes=EMOTES,
                team_code=team_code,
                uid1=uid1, uid2=uid2, uid3=uid3, uid4=uid4
            )
        return render_template_string(HTML, show_emotes=False)

    @app.route('/send', methods=['POST'])
    def send_command():
        try:
            team_code = request.form['team_code']
            emote_id = request.form['emote_id']
            uid1 = request.form['uid1']
            
            # Validate
            if not re.match(r'^\d{7}$', team_code):
                return jsonify({"success": False, "error": "Invalid team code"})
            
            if not re.match(r'^\d{8,11}$', uid1):
                return jsonify({"success": False, "error": "Invalid UID"})
            
            if not re.match(r'^\d{9}$', emote_id):
                return jsonify({"success": False, "error": "Invalid emote ID"})
            
            # Collect UIDs
            uids = [uid1]
            for i in range(2, 5):
                uid = request.form.get(f'uid{i}', '').strip()
                if uid and re.match(r'^\d{8,11}$', uid):
                    uids.append(uid)
            
            # Send commands
            sent = 0
            for uid in uids:
                command = f"/quick {team_code} {emote_id} {uid}"
                if bot_manager.send_command(command):
                    sent += 1
            
            if sent > 0:
                return jsonify({
                    "success": True,
                    "message": f"Sent to {sent} player(s)"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to send commands"
                })
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            })

    @app.route('/status')
    def status():
        return jsonify({
            "commands_sent": bot_manager.commands_sent,
            "status": "Online"
        })

####################################
# ORIGINAL BOT FUNCTIONS (मुख्य TCP कोड)
####################################

#Clan-info-by-clan-id
def Get_clan_info(clan_id):
    try:
        url = f"https://get-clan-info.vercel.app/get_clan_info?clan_id={clan_id}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            msg = f""" 
[11EAFD][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
▶▶▶▶GUILD DETAILS◀◀◀◀
Achievements: {data['achievements']}\n\n
Balance : {fix_num(data['balance'])}\n\n
Clan Name : {data['clan_name']}\n\n
Expire Time : {fix_num(data['guild_details']['expire_time'])}\n\n
Members Online : {fix_num(data['guild_details']['members_online'])}\n\n
Regional : {data['guild_details']['regional']}\n\n
Reward Time : {fix_num(data['guild_details']['reward_time'])}\n\n
Total Members : {fix_num(data['guild_details']['total_members'])}\n\n
ID : {fix_num(data['id'])}\n\n
Last Active : {fix_num(data['last_active'])}\n\n
Level : {fix_num(data['level'])}\n\n
Rank : {fix_num(data['rank'])}\n\n
Region : {data['region']}\n\n
Score : {fix_num(data['score'])}\n\n
Timestamp1 : {fix_num(data['timestamp1'])}\n\n
Timestamp2 : {fix_num(data['timestamp2'])}\n\n
Welcome Message: {data['welcome_message']}\n\n
XP: {fix_num(data['xp'])}\n\n
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
[FFB300][b][c]MADE BY Ashish 
            """
            return msg
        else:
            msg = """
[11EAFD][b][c]
°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
Failed to get info, please try again later!!

°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
[FFB300][b][c]MADE BY Ashish
            """
            return msg
    except:
        pass
#GET INFO BY PLAYER ID
def get_player_info(player_id):
    url = f"https://like2.vercel.app/player-info?uid={player_id}&server={server2}&key={key2}"
    response = requests.get(url)
    print(response)    
    if response.status_code == 200:
        try:
            r = response.json()
            return {
                "Account Booyah Pass": f"{r.get('booyah_pass_level', 'N/A')}",
                "Account Create": f"{r.get('createAt', 'N/A')}",
                "Account Level": f"{r.get('level', 'N/A')}",
                "Account Likes": f" {r.get('likes', 'N/A')}",
                "Name": f"{r.get('nickname', 'N/A')}",
                "UID": f" {r.get('accountId', 'N/A')}",
                "Account Region": f"{r.get('region', 'N/A')}",
                }
        except ValueError as e:
            pass
            return {
                "error": "Invalid JSON response"
            }
    else:
        pass
        return {
            "error": f"Failed to fetch data: {response.status_code}"
        }
#CHAT WITH AI
def get_writer_from_type(chat_type):
    global whisper_writer, clan_writer, team_writer, chat_writer

    if chat_type == "GUILD":      # Clan chat
        return clan_writer
    elif chat_type == "PRI":      # Private whisper
        return whisper_writer
    elif chat_type == "SQUAD":    # Team / squad chat
        return team_writer
    else:
        return whisper_writer     # Default
        
        
def talk_with_ai(question):
    url = f"https://gemini-api-api-v2.vercel.app/prince/api/v1/ask?key=prince&ask={question}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        msg = data["message"]["content"]
        return msg
    else:
        return "An error occurred while connecting to the server."
#SPAM REQUESTS
def make_fields(idroom, idplayer):

    fields = {
        1: 78,
        2: {
            1: int(idroom),
            2: "[FF0000]FFWLXD BOT",
            4: 330,
            5: 6000,
            6: 201,
            10: 1,
            11: int(idplayer),
            12: 1,
            13: {
                1: 11,
                2: 13502539260,
                3: 9999
            },
            15: {
                1: 1,
                2: 32768
            },
            16: 32768,
            18: {
                1: 13502539260,
                2: 8,
                3: "DATA"
            }
        }
    }

    return fields
def spam_requests(player_id):
    # This URL now correctly points to the Flask app you provided
    url = f"https://like2.vercel.app/send_requests?uid={player_id}&server={server2}&key={key2}"
    try:
        res = requests.get(url, timeout=20) # Added a timeout
        if res.status_code == 200:
            data = res.json()
            # Return a more descriptive message based on the API's JSON response
            return f"API Status: Success [{data.get('success_count', 0)}] Failed [{data.get('failed_count', 0)}]"
        else:
            # Return the error status from the API
            return f"API Error: Status {res.status_code}"
    except requests.exceptions.RequestException as e:
        # Handle cases where the API isn't running or is unreachable
        print(f"Could not connect to spam API: {e}")
        return "Failed to connect to spam API."
####################################

# ** NEW INFO FUNCTION using the new API **
def newinfo(uid):
    # Base URL without parameters
    url = "https://like2.vercel.app/player-info"
    # Parameters dictionary - this is the robust way to do it
    params = {
        'uid': uid,
        'server': server2,  # Hardcoded to bd as requested
        'key': key2
    }
    try:
        # Pass the parameters to requests.get()
        response = requests.get(url, params=params, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Check if the expected data structure is in the response
            if "basicInfo" in data:
                return {"status": "ok", "data": data}
            else:
                # The API returned 200, but the data is not what we expect (e.g., error message in JSON)
                return {"status": "error", "message": data.get("error", "Invalid ID or data not found.")}
        else:
            # The API returned an error status code (e.g., 404, 500)
            try:
                # Try to get a specific error message from the API's response
                error_msg = response.json().get('error', f"API returned status {response.status_code}")
                return {"status": "error", "message": error_msg}
            except ValueError:
                # If the error response is not JSON
                return {"status": "error", "message": f"API returned status {response.status_code}"}

    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., timeout, no connection)
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except ValueError: 
        # Handle cases where the response is not valid JSON
        return {"status": "error", "message": "Invalid JSON response from API."}

	
#ADDING-100-LIKES-IN-24H
def send_likes(uid):
    try:
        likes_api_response = requests.get(
             f"https://like-api-kanha.vercel.app/like?uid={uid}&server_name={server2}&key={key1}",
             timeout=15
             )
      
      
        if likes_api_response.status_code != 200:
            return f"""
[C][B][FF0000]━━━━━+
[FFFFFF]Like API Error!
Status Code: {likes_api_response.status_code}
Please check if the uid is correct.
━━━━━
"""

        api_json_response = likes_api_response.json()

        player_name = api_json_response.get('PlayerNickname', 'Unknown')
        likes_before = api_json_response.get('LikesbeforeCommand', 0)
        likes_after = api_json_response.get('LikesafterCommand', 0)
        likes_added = api_json_response.get('LikesGivenByAPI', 0)
        status = api_json_response.get('status', 0)

        if status == 1 and likes_added > 0:
            # ✅ Success
            return f"""
[C][B][11EAFD]‎━━━━━━━━━━━━
[FFFFFF]Likes Status:

[00FF00]Likes Sent Successfully!

[FFFFFF]Player Name : [00FF00]{player_name}  
[FFFFFF]Likes Added : [00FF00]{likes_added}  
[FFFFFF]Likes Before : [00FF00]{likes_before}  
[FFFFFF]Likes After : [00FF00]{likes_after}  
[C][B][11EAFD]‎━━━━━━━━━━━━
[C][B][FFB300]Follow_instagram: [FFFFFF]Ashish.shakya0001 [00FF00]!!
"""
        elif status == 2 or likes_before == likes_after:
            # 🚫 Already claimed / Maxed
            return f"""
[C][B][FF0000]━━━━━━━━━━━━

[FFFFFF]No Likes Sent!

[FF0000]B_S_D_K KAL TRY KRNA AB..

[FFFFFF]Player Name : [FF0000]{player_name}  
[FFFFFF]Likes Before : [FF0000]{likes_before}  
[FFFFFF]Likes After : [FF0000]{likes_after}  
[C][B][FF0000]━━━━━━━━━━━━
"""
        else:
            # ❓ Unexpected case
            return f"""
[C][B][FF0000]━━━━━━━━━━━━
[FFFFFF]Unexpected Response!
Something went wrong.

Please try again or contact support.
━━━━━━━━━━━━
"""

    except requests.exceptions.RequestException:
        return """
[C][B][FF0000]━━━━━
[FFFFFF]Like API Connection Failed!
Is the API server (app.py) running?
━━━━━
"""
    except Exception as e:
        return f"""
[C][B][FF0000]━━━━━
[FFFFFF]An unexpected error occurred:
[FF0000]{str(e)}
━━━━━
"""
####################################
#CHECK ACCOUNT IS BANNED

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB51"}

# ---- Random Colores ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)
            
async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    """Safely send message with retry mechanism"""
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            print(f"Message sent successfully on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"Failed to send message (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)  # Wait before retry
    return False
    

async def ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region):
    """Join team, authenticate chat, perform emote, and leave automatically"""
    try:
        # Step 1: Join the team
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        print(f"🤖 Joined team: {team_code}")
        
        # Wait for team data and chat authentication
        await asyncio.sleep(1.5)  # Increased to ensure proper connection
        
        # Step 2: The bot needs to be detected in the team and authenticate chat
        # This happens automatically in TcPOnLine, but we need to wait for it
        
        # Step 3: Perform emote to target UID
        emote_packet = await Emote_k(int(target_uid), int(emote_id), key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
        print(f"🎭 Performed emote {emote_id} to UID {target_uid}")
        
        # Wait for emote to register
        await asyncio.sleep(0.5)
        
        # Step 4: Leave the team
        leave_packet = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        print(f"🚪 Left team: {team_code}")
        
        return True, f"Quick emote attack completed! Sent emote to UID {target_uid}"
        
    except Exception as e:
        return False, f"Quick emote attack failed: {str(e)}"
        

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.118.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0OUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT) ; await online_writer.drain()
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)' 

import threading
import time

def run_sync_spam(invoker_self, target_player_id, notify_uid=None):
    try:
        sent_count = 0
        max_iterations = 50  # चाहो तो 8000 कर सकते हो

        for i in range(max_iterations):
            try:
                # Packet बनाना
                if invoker_self:
                    packet = invoker_self.request_skwad(target_player_id)
                else:
                    packet = request_skwad(target_player_id)

                socket_client.send(packet)
                sent_count += 1

                # हर 10 request पर message
                if notify_uid and sent_count % 10 == 0:
                    msg = f"[C][B][00FF00]✅ {sent_count} requests sent to {target_player_id}"
                    try:
                        if invoker_self:
                            clients.send(invoker_self.GenResponsMsg(msg, notify_uid))
                        else:
                            clients.send(GenResponsMsg(msg, notify_uid))
                    except Exception as e:
                        print(f"Status msg error: {e}")

                time.sleep(0.1)

            except Exception as inner_e:
                print(f"[run_sync_spam] inner loop error: {inner_e}")
                time.sleep(0.5)
                continue

        # Done message
        if notify_uid:
            msg = f"[C][B][1E90FF]🚀 Done sending {sent_count} invites to {target_player_id}"
            if invoker_self:
                clients.send(invoker_self.GenResponsMsg(msg, notify_uid))
            else:
                clients.send(GenResponsMsg(msg, notify_uid))

    except Exception as outer_e:
        print(f"[run_sync_spam] unexpected error: {outer_e}")
    
async def jnl_ghost(player_id, secret_code, key, iv):

    idroom = secret_code
    idplayer = player_id

    fields = make_fields(idroom, idplayer)

    packet = (await CrEaTe_ProTo(fields)).hex()
    enc_packet = await EnC_PacKeT(packet, key, iv)

    header_length = len(enc_packet) // 2
    header_length_final = await DecodE_HeX(header_length)

    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + enc_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + enc_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + enc_packet
    else:
        final_packet = "0515000000" + header_length_final + enc_packet

    return bytes.fromhex(final_packet)

async def custom_invite(player_id, room_id, key, iv):
    fields = make_custom_fields(room_id, player_id)

    proto = (await CrEaTe_ProTo(fields)).hex()
    enc = await EnC_PacKeT(proto, key, iv)

    hl = await DecodE_HeX(len(enc) // 2)
    final_packet = "0515000000"[:10-len(hl)] + hl + enc

    return bytes.fromhex(final_packet)           
           
async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer, region
    
    # Define region
    region = "ind"
    
    print(f"🔌 Connecting to Online: {ip}:{port}")
    
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            
            print(f"✅ TCP Online Connected!")
            
            while True:
                # 1. FIRST check web commands
                try:
                    if os.path.exists(COMMANDS_FILE):
                        with open(COMMANDS_FILE, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                        
                        if content:
                            print(f"📥 Found web command: {content}")
                            
                            if content.startswith("/quick"):
                                parts = content.split()
                                if len(parts) >= 4:
                                    team_code = parts[1]
                                    emote_id = parts[2]
                                    target_uid = parts[3]
                                    
                                    print(f"🚀 Executing: Team={team_code}, Emote={emote_id}, Target={target_uid}")
                                    
                                    # Execute command
                                    try:
                                        success, result = await ultra_quick_emote_attack(
                                            team_code, emote_id, target_uid, key, iv, region
                                        )
                                        
                                        if success:
                                            print(f"✅ Web command successful!")
                                        else:
                                            print(f"❌ Web command failed: {result}")
                                            
                                    except Exception as e:
                                        print(f"❌ Attack error: {e}")
                                    
                                    # Clear file AFTER execution
                                    with open(COMMANDS_FILE, 'w', encoding='utf-8') as f:
                                        f.write("")
                                    
                except Exception as e:
                    print(f"⚠️ Command check error: {e}")
                
                # 2. THEN check TCP data (with timeout)
                try:
                    data2 = await asyncio.wait_for(reader.read(9999), timeout=0.5)
                    if not data2:
                        print("❌ Server disconnected")
                        break
                    
                    # Process TCP data (your existing code)
                    if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                        try:
                            packet = await DeCode_PackEt(data2.hex()[10:])
                            packet_data = json.loads(packet)
                            OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet_data)

                            JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', JoinCHaT)

                            message = f'[B][C]{get_random_color()}\n- WeLComE To Emote Bot! '
                            P = await SEndMsG(0, message, OwNer_UiD, OwNer_UiD, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                        except Exception as e:
                            # Optional: print for debugging
                            # print(f"TCP data error: {e}")
                            pass
                            
                except asyncio.TimeoutError:
                    # This is normal - no TCP data, continue checking commands
                    continue
                except Exception as e:
                    print(f"⚠️ TCP read error: {e}")
                    break
                    
                # Small delay to prevent CPU overload
                await asyncio.sleep(0.1)

            online_writer.close()
            await online_writer.wait_closed()
            online_writer = None
            print("❌ TCP Online disconnected")

        except Exception as e:
            print(f"❌ TCP Online connection error: {e}")
            online_writer = None
        
        print(f"🔄 Reconnecting in {reconnect_delay} seconds...")
        await asyncio.sleep(reconnect_delay)
                            
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                
                if data.hex().startswith("120000"):

                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                    except:
                        response = None


                    if response:
                        if inPuTMsG.startswith(("/5")):
                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                message = f"[B][C]{get_random_color()}\n\nAccepT My Invitation FasT\n\n"
                                P = await SEndMsG(response.Data.chat_type , message , uid , chat_id , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                                PAc = await OpEnSq(key , iv,region)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , PAc)
                                C = await cHSq(5, uid ,key, iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , C)
                                V = await SEnd_InV(5 , uid , key , iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , V)
                                E = await ExiT(None , key , iv)
                                await asyncio.sleep(3)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , E)
                            except:
                                print('msg in squad')
                                
                              # QUICK EMOTE ATTACK COMMAND - FIXED
                        if inPuTMsG.strip().startswith('/quick'):
                            print('Processing quick emote attack command')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /quick (team_code) [emote_id] [target_uid]\n\n[FFFFFF]Examples:\n[00FF00]/quick ABC123[FFFFFF] - Join, send Rings emote, leave\n[00FF00]/ghostquick ABC123[FFFFFF] - Ghost join, send emote, leave\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
        
                                # Set default values
                                emote_id = parts[0]
                                target_uid = str(response.Data.uid)  # Default: Sender's UID
        
                                # Parse optional parameters
                                if len(parts) >= 3:
                                    emote_id = parts[2]
                                if len(parts) >= 4:
                                    target_uid = parts[3]
        
                                # Determine target name for message
                                if target_uid == str(response.Data.uid):
                                    target_name = "Yourself"
                                else:
                                    target_name = f"UID {target_uid}"
        
                                initial_message = f"[B][C][FFFF00]⚡ QUICK EMOTE ATTACK!\n\n[FFFFFF]🎯 Team: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Target: [00FF00]{target_name}\n[FFFFFF]⏱️ Estimated: [00FF00]2 seconds\n\n[FFFF00]Executing sequence...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
                                try:
                                    # Try regular method first
                                    success, result = await ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region)
            
                                    if success:
                                        success_message = f"[B][C][00FF00]✅ QUICK ATTACK SUCCESS!\n\n[FFFFFF]🏷️ Team: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Target: [00FF00]{target_name}\n\n[00FF00]Bot joined → emoted → left! ✅\n"
                                    else:
                                        success_message = f"[B][C][FF0000]❌ Regular attack failed: {result}\n"
                                    
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    print("failed:", str(e))
                                    
                        if inPuTMsG.strip().startswith('/gali '):
                            print('Processing /gali command')

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! Usage:\n"
                                        "/gali <name>\n"
                                        "Example: /gali hater"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    name = parts[1].strip()

                                    messages = [
                                        "{Name} TƐRI SƐXY BHEN KI CHXT ME ME L0DA DAAL KAR RAAT BHAR JOR JOR SE CH0DUNGA",
                                        "{Name} MADHERXHOD TƐRI MÁÁ KI KALI G4ND MƐ LÀND MARU",
                                        "{Name} TƐRI BHƐN KI TIGHT CHXT KO 5G KI SPEED SE CHÒD DU",
                                        "{Name} TƐRI BEHEN KI CHXT ME L4ND MARU",
                                        "{Name} TƐRI MÁÁ KI CHXT 360 BAR",
                                        "{Name} TƐRI BƐHƐN KI CHXT 720 BAR",
                                        "{Name} BEHEN KE L0DE",
                                        "{Name} MADARCHXD",
                                        "{Name} BETE TƐRA BAAP HUN ME",
                                        "{Name} G4NDU APNE BAAP KO H8 DEGA",
                                        "{Name} KI MÀÀ KI CHXT PER NIGHT 4000",
                                        "{Name} KI BƐHƐN KI CHXT PER NIGHT 8000",
                                        "{Name} R4NDI KE BACHHƐ APNE BAP KO H8 DEGA",
                                        "INDIA KA NO-1 G4NDU {Name}",
                                        "{Name} CHAPAL CH0R",
                                        "{Name} TƐRI MÀÀ KO GB ROAD PE BETHA KE CHXDUNGA",
                                        "{Name} BETA JHULA JHUL APNE BAAP KO MAT BHUL"
            ]

                                    # Send each message one by one with random color
                                    for msg in messages:
                                        colored_message = f"[B][C]{get_random_color()} {msg.replace('{Name}', name.upper())}"
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                        if inPuTMsG.startswith("/invite"):
                            try:
                                parts = inPuTMsG.strip().split()

                                if len(parts) < 2:
                                    msg = "Usage:\n/invite <player_id>"
                                    P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    player_id = parts[1].strip()

                                    # छोटा शॉर्टकोड बदलने के लिए
                                    if "***" in player_id:
                                        player_id = player_id.replace("***", "106")

                                    # Valid ID check
                                    if not player_id.isdigit():
                                        msg = "[C][B][FF0000]❌ Invalid ID. Use /invite [player_id]"
                                        P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    else:
                                        # 🧩 Thread Start (self check)
                                        try:
                                            # अगर self defined है (class के अंदर)
                                            threading.Thread(
                                                target=run_sync_spam,
                                                args=(self, player_id, uid),
                                                daemon=True
                                            ).start()
                                        except NameError:
                                            # अगर self defined नहीं है (class के बाहर)
                                            threading.Thread(
                                                target=run_sync_spam,
                                                args=(None, player_id, uid),
                                                daemon=True
                                            ).start()

                                        # 🚀 Start message
                                        msg = f"[C][B][1E90FF]🚀 Started invite spam to {player_id}"
                                        P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                            except Exception as e:
                                msg = f"[C][B][FF0000]❌ Error in /invite command: {e}"
                                print(f"DEBUG /invite error: {e}")
                                P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
        
                        if inPuTMsG.startswith("/like/"):
                            try:
                                uid_like = inPuTMsG.split("/like/")[1]
                                result = send_likes(uid_like)
                                msg = str(result).replace("[C]", "").replace("[B]", "").replace("[FFFFFF]", "").replace("[FF0000]", "")
                                msg = msg[:340]  # message 340 characters se zyada na ho
                                print("DEBUG LIKE RESPONSE:", result)
                                P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except Exception as e:
                                msg = f"[C][B][FF0000]Error while sending likes: {e}"
                                P = await SEndMsG(response.Data.chat_type, msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                           
                        if inPuTMsG.startswith("/code"):
                            try:
                              p = inPuTMsG.split()
                              if len(p) < 2:
                                 await SEndPacKeT(whisper_writer, online_writer, 'ChaT',
                                     await SEndMsG(response.Data.chat_type, "Usage: /code <room_id>", uid, chat_id, key, iv))
                              else:
                                room_id = int(p[1])
                                pkt = await custom_invite(uid, room_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', pkt)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT',
                                await SEndMsG(response.Data.chat_type, f"[C][00FF00]✅ Custom invite → {room_id}", uid, chat_id, key, iv))
                            except Exception as e:
                              print("CODE ERROR:", e)
        
                               # /lag <teamcode> [count]
                               #------------------------------------
                        if inPuTMsG.startswith("/lag"):
                            try:
                                parts = inPuTMsG.strip().split()
                                team_code = parts[1] if len(parts) > 1 else ""
                                requested_count = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 1000  # default 50 cycles

                                if not team_code:
                                 print("⚠️ Missing team code for /lag command.")
                                else:
                                 count = max(1, min(requested_count, 10000))  # cap at 500 to stay safe
                                 print(f"DEBUG /lag: Starting join-leave loop on team {team_code} ({count}x)")
 
                                 for i in range(count):
                                    try:
                                        # JOIN team
                                      EM = await GenJoinSquadsPacket(team_code, key, iv)
                                      await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)

                                         # small delay between join and leave
                                      await asyncio.sleep(0.01)

                                          # LEAVE team
                                      leave = await ExiT(uid, key, iv)
                                      await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave)
      
                                   #   print(f"[{i+1}/{count}] cycle done ✅")

                                      await asyncio.sleep(0.01)  # short delay to avoid flood
                                    except Exception as inner_e:
                                      print("Lag loop error:", inner_e)

                                 print(f"DEBUG /lag: Finished {count} cycles on team {team_code}")

                            except Exception as e:
                                print("ERROR in /lag:", e)
                             
                             
                        if inPuTMsG.startswith('/x/'):
                            CodE = inPuTMsG.split('/x/')[1]
                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')

                                # 🟢 Join squad packet send
                                EM = await GenJoinSquadsPacket(CodE , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)

                                # 💬 Guild message (FF style + proper spaces)
                                uid = response.Data.uid
                                chat_id = response.Data.Chat_ID
                                guild_message = (
                                    '\n'
                                    '   [B][C][FFBB00]   Follow On Instagram   \n'
                                    '\n'
                                    '   [B][C]   ╭─╮   \n'
                                    '       ︱◯֯︱★ɪɴꜱᴛᴀ★┊[FF00FF] ✓   \n'
                                    '   ╰─   \n'
                                    '\n'
                                    '   [00FFFF]   Ashish.shakya001   \n'
                                    '\n'
                                )

                                # 📨 Send guild message (visible in guild)
                                Gmsg = await SEndMsG('Guild', guild_message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , Gmsg)

                            except Exception as e:
                                print('msg in squad', e)

                        if inPuTMsG.startswith('leave'):
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)

                        if inPuTMsG.strip().startswith('/s'):
                            EM = await FS(key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)

                        if inPuTMsG.strip().startswith('@a'):

                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                message = f"[B][C]{get_random_color()}\n\nCommand Available OnLy In SQuaD ! \n\n"
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                            except:
                                print('msg in squad')

                                parts = inPuTMsG.strip().split()
                                print(response.Data.chat_type, uid, chat_id)
                                message = f'[B][C]{get_random_color()}\nACITVE TarGeT -> {xMsGFixinG(uid)}\n'

                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)

                                uid2 = uid3 = uid4 = uid5 = None
                                s = False

                                try:
                                    uid = int(parts[1])
                                    uid2 = int(parts[2])
                                    uid3 = int(parts[3])
                                    uid4 = int(parts[4])
                                    uid5 = int(parts[5])
                                    idT = int(parts[5])

                                except ValueError as ve:
                                    print("ValueError:", ve)
                                    s = True

                                except Exception:
                                    idT = len(parts) - 1
                                    idT = int(parts[idT])
                                    print(idT)
                                    print(uid)

                                if not s:
                                    try:
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                                        H = await Emote_k(uid, idT, key, iv,region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)

                                        if uid2:
                                            H = await Emote_k(uid2, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if uid3:
                                            H = await Emote_k(uid3, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if uid4:
                                            H = await Emote_k(uid4, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if uid5:
                                            H = await Emote_k(uid5, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        

                                    except Exception as e:
                                        pass


                        if inPuTMsG in ("hi" , "hello" , "fen" , "help"):
                            uid = response.Data.uid
                            chat_id = response.Data.Chat_ID
                            message = '[C][B][00FFFF]━━━━━━━━━━━━\n[ffd319][B]☂︎Add 100 Likes\n[FFFFFF]/like/(uid)\n[ffd319][b]❄︎Join Bot In Group\n[FFFFFF][b]/x/(teamcode)\n[ffd319][b]❀To Perform AnyEmote\n[FFFFFF][b]@a (uid) (emote) code)\n[ffd319]⚡Make 5 Player Group:\n[FFFFFF]❄️/5 \n[B][C][FF00FF] ʟᴀɢ ɢʀᴏᴜᴘ \n 	[FF0000] /lag teamcod \n[ffd319][b][c]🎵Make leave Bot \n[FFFFFF][b][c]©️ leave\n[00FF7F][B]!!admin Commond!!\n[ffd319][b]To Stop The Bot\n[FFFFFF][b]/stop\n[ffd319][b]To Mute Bot\n[FFFFFF][b]/mute (time)\n[C][B][FFB300]OWNER: ASHISH BHAI \n[00FFFF]━━━━━━━━━━━━\n[00FF00]\n[00ff00][B]⚓ Developer by Ashish shakya ⚓                            '
                            P = await SEndMsG(response.Data.chat_type , message , uid , chat_id , key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                        response = None
                            
            whisper_writer.close() ; await whisper_writer.wait_closed() ; whisper_writer = None
                    
                    	
                    	
        except Exception as e: print(f"ErroR {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)

async def MaiiiinE():
    Uid, Pw = '4255057762', '7F4D576695F378518609792E12BEDED4E469A47C85CCA458EA8C87E20984B112'

    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id or not access_token: 
        print("❌ Invalid account")
        return None
    
    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: 
        print("❌ Account banned or not registered")
        return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
    if not LoGinDaTa: 
        print("❌ Error getting login data")
        return None
    
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP, OnLineporT = OnLinePorTs.split(":")
    ChaTiP, ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    
    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
    ready_event = asyncio.Event()
    
    print("=" * 50)
    print(f"🤖 BOT: {acc_name}")
    print(f"📍 UID: {TarGeT}")
    print(f"🌐 Region: {region}")
    print("=" * 50)
    
    # Start TCP tasks
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region))
    
    await ready_event.wait()
    await asyncio.sleep(1)
    
    task2 = asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen))
    
    print("\n✅ Bot is ONLINE!")
    print("📝 Web Panel: http://localhost:5000")
    print("💬 Send /help in game chat for commands")
    print("=" * 50)
    
    # Run both tasks
    await asyncio.gather(task1, task2)
    
async def StarTinG():
    while True:
        try: await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except asyncio.TimeoutError: print("Token ExpiRed ! , ResTartinG")
        except Exception as e: print(f"ErroR TcP - {e} => ResTarTinG ...")

def start_flask_server():
    """Start Flask web server"""
    if FLASK_AVAILABLE and app:
        port = int(os.environ.get('PORT', 5000))
        print(f"🌐 Starting Flask on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    else:
        print("ℹ️ Flask not available, web panel disabled")

async def main():
    """Main async function"""
    print("\n" + "="*50)
    print("🔥 ASHISH EMOTE BOT - READY!")
    print("="*50)
    print(f"✅ Flask Available: {FLASK_AVAILABLE}")
    print(f"✅ EMOTES Count: {len(EMOTES)}")
    print(f"✅ Commands File: {os.path.exists(COMMANDS_FILE)}")
    print("="*50)
    
    # Create commands file
    if not os.path.exists(COMMANDS_FILE):
        open(COMMANDS_FILE, "w").close()
        print("📁 Created commands.txt file")
    
    # Start Flask in separate thread if available
    if FLASK_AVAILABLE and app:
        import threading
        flask_thread = threading.Thread(target=start_flask_server, daemon=True)
        flask_thread.start()
        print("🌐 Web Panel: http://localhost:5000")
        print("   (If running locally)")
        print("   (For Render: https://your-app.onrender.com)")
    else:
        print("ℹ️ Running in terminal mode only")
    
    # Start the TCP bot
    print("🤖 Starting TCP Bot...")
    await StarTinG()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user!")
    except Exception as e:
        print(f"❌ Error: {e}")