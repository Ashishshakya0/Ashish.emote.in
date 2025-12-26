# web_panel.py
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import os
import re
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ashish-premium-panel-2024')

# ==================== UNIQUE EMOTE DATABASE ====================
EMOTE_CATEGORIES = {
    "EVO_GUNS": [
        {"name": "🔥 EVO M4A1 MAX", "id": "909033001", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO AK47 MAX", "id": "909000063", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO SCAR MAX", "id": "909000068", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO XMB MAX", "id": "909000065", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO MP40 MAX", "id": "909000075", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO UMP MAX", "id": "909000098", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO WOODPECKER MAX", "id": "909042008", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO M10 MAX", "id": "909000081", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO FAMAS MAX", "id": "909000090", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO MP5 MAX", "id": "909033002", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO G18 MAX", "id": "909038012", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO THOMPSON MAX", "id": "909038010", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO PARAFAL MAX", "id": "909045001", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO P90 MAX", "id": "909049010", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO M60 MAX", "id": "909051003", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 LEVEL 100 EMOTE", "id": "909042007", "icon": "fa-crown", "rarity": "mythic"},
    ],
    
    "SPECIAL_POPULAR": [
        {"name": "💰 PAISA EMOTE", "id": "909000055", "icon": "fa-money-bill-wave", "rarity": "epic"},
        {"name": "💖 HEART EMOTE", "id": "909000045", "icon": "fa-heart", "rarity": "rare"},
        {"name": "🌹 ROSE EMOTE", "id": "909000010", "icon": "fa-rose", "rarity": "rare"},
        {"name": "👑 THRONE EMOTE", "id": "909000014", "icon": "fa-crown", "rarity": "epic"},
        {"name": "🏴‍☠️ PIRATE'S FLAG", "id": "909000034", "icon": "fa-flag", "rarity": "epic"},
        {"name": "💨 EAT MY DUST", "id": "909000039", "icon": "fa-wind", "rarity": "rare"},
        {"name": "😂 LOL EMOTE", "id": "909000002", "icon": "fa-laugh", "rarity": "common"},
        {"name": "🐍 COBRA EMOTE", "id": "909000072", "icon": "fa-staff-snake", "rarity": "epic"},
        {"name": "👻 GHOST EMOTE", "id": "909036001", "icon": "fa-ghost", "rarity": "epic"},
        {"name": "🎬 SHOLAY EMOTE", "id": "909050020", "icon": "fa-film", "rarity": "legendary"},
        {"name": "🎤 PRIME 8 EMOTE", "id": "909035013", "icon": "fa-microphone", "rarity": "epic"},
        {"name": "💪 PUSH UP", "id": "909000012", "icon": "fa-dumbbell", "rarity": "common"},
        {"name": "😈 DEVIL'S MOVE", "id": "909000020", "icon": "fa-horn", "rarity": "epic"},
        {"name": "🧟 FERA3WN EMOTE", "id": "909000011", "icon": "fa-ghost", "rarity": "rare"},
        {"name": "🤝 HIGH FIVE", "id": "909000025", "icon": "fa-handshake", "rarity": "common"},
        {"name": "🐍 COBRA EMOTE 2", "id": "909000071", "icon": "fa-staff-snake", "rarity": "epic"},
        {"name": "🕺 MICHAEL JACKSON", "id": "909045009", "icon": "fa-music", "rarity": "legendary"},
        {"name": "🔄 JUJUTSU EMOTE", "id": "909050002", "icon": "fa-yin-yang", "rarity": "mythic"},
        {"name": "💍 NEW EMOTE", "id": "909050009", "icon": "fa-ring", "rarity": "epic"},
        {"name": "🐉 DRAGON'S SOUL", "id": "909000081", "icon": "fa-dragon", "rarity": "legendary"},
    ],
    
    "BASIC_EMOTES": [
        {"name": "👋 HELLO!", "id": "909000001", "icon": "fa-hand-wave", "rarity": "common"},
        {"name": "😤 PROVOKE", "id": "909000003", "icon": "fa-fist-raised", "rarity": "common"},
        {"name": "👏 APPLAUSE", "id": "909000004", "icon": "fa-hands-clapping", "rarity": "common"},
        {"name": "💃 DAB", "id": "909000005", "icon": "fa-person-dancing", "rarity": "common"},
        {"name": "🐔 CHICKEN", "id": "909000006", "icon": "fa-drumstick", "rarity": "common"},
        {"name": "👋 ARM WAVE", "id": "909000007", "icon": "fa-hand-wave", "rarity": "common"},
        {"name": "💃 SHOOT DANCE", "id": "909000008", "icon": "fa-gun", "rarity": "common"},
        {"name": "🦈 BABY SHARK", "id": "909000009", "icon": "fa-fish", "rarity": "rare"},
        {"name": "🧟 MUMMY DANCE", "id": "909000011", "icon": "fa-ghost", "rarity": "rare"},
        {"name": "🕺 SHUFFLING", "id": "909000013", "icon": "fa-person-running", "rarity": "common"},
        {"name": "🐉 DRAGON FIST", "id": "909000015", "icon": "fa-dragon", "rarity": "epic"},
        {"name": "🎯 DANGEROUS GAME", "id": "909000016", "icon": "fa-bullseye", "rarity": "rare"},
        {"name": "🐆 JAGUAR DANCE", "id": "909000017", "icon": "fa-paw", "rarity": "rare"},
        {"name": "👊 THREATEN", "id": "909000018", "icon": "fa-hand-fist", "rarity": "common"},
        {"name": "🔄 SHAKE WITH ME", "id": "909000019", "icon": "fa-people-arrows", "rarity": "common"},
        {"name": "💥 FURIOUS SLAM", "id": "909000021", "icon": "fa-explosion", "rarity": "epic"},
        {"name": "🌙 MOON FLIP", "id": "909000022", "icon": "fa-moon", "rarity": "rare"},
        {"name": "🚶 WIGGLE WALK", "id": "909000023", "icon": "fa-walking", "rarity": "common"},
        {"name": "⚔️ BATTLE DANCE", "id": "909000024", "icon": "fa-swords", "rarity": "epic"},
        {"name": "🎉 SHAKE IT UP", "id": "909000026", "icon": "fa-glass-cheers", "rarity": "common"},
        {"name": "🌀 GLORIOUS SPIN", "id": "909000027", "icon": "fa-sync", "rarity": "rare"},
        {"name": "🦢 CRANE KICK", "id": "909000028", "icon": "fa-kiwi-bird", "rarity": "rare"},
        {"name": "🎉 PARTY DANCE", "id": "909000029", "icon": "fa-party-horn", "rarity": "common"},
        {"name": "💃 JIG DANCE", "id": "909000031", "icon": "fa-music", "rarity": "common"},
        {"name": "📸 SELFIE", "id": "909000032", "icon": "fa-camera", "rarity": "common"},
        {"name": "💫 SOUL SHAKING", "id": "909000033", "icon": "fa-star", "rarity": "rare"},
        {"name": "💖 HEALING DANCE", "id": "909000035", "icon": "fa-heart-pulse", "rarity": "rare"},
        {"name": "🎧 TOP DJ", "id": "909000036", "icon": "fa-headphones", "rarity": "epic"},
        {"name": "😡 DEATH GLARE", "id": "909000037", "icon": "fa-eye", "rarity": "rare"},
        {"name": "💰 POWER OF MONEY", "id": "909000038", "icon": "fa-money-bill", "rarity": "epic"},
        {"name": "💃 BREAKDANCE", "id": "909000040", "icon": "fa-person-burst", "rarity": "epic"},
        {"name": "🥋 KUNGFU", "id": "909000041", "icon": "fa-user-ninja", "rarity": "common"},
        {"name": "🍽️ BON APPETIT", "id": "909000042", "icon": "fa-utensils", "rarity": "common"},
        {"name": "🎯 AIM; FIRE!", "id": "909000043", "icon": "fa-crosshairs", "rarity": "common"},
        {"name": "🦢 THE SWAN", "id": "909000044", "icon": "fa-dove", "rarity": "rare"},
        {"name": "☕ TEA TIME", "id": "909000046", "icon": "fa-mug-hot", "rarity": "common"},
        {"name": "🥊 BRING IT ON!", "id": "909000047", "icon": "fa-boxing-glove", "rarity": "common"},
        {"name": "🤷 WHY? OH WHY?", "id": "909000048", "icon": "fa-question", "rarity": "common"},
        {"name": "👌 FANCY HANDS", "id": "909000049", "icon": "fa-hand-sparkles", "rarity": "rare"},
        {"name": "💃 SHIMMY", "id": "909000051", "icon": "fa-person-dots-from-line", "rarity": "common"},
        {"name": "🐶 DOGGIE", "id": "909000052", "icon": "fa-dog", "rarity": "common"},
        {"name": "⚔️ CHALLENGE ON!", "id": "909000053", "icon": "fa-flag-checkered", "rarity": "common"},
        {"name": "🤠 LASSO", "id": "909000054", "icon": "fa-lasso", "rarity": "rare"},
    ],
    
    "FIREBORN_SERIES": [
        {"name": "🪶 GOLDEN FEATHER", "id": "909033002", "icon": "fa-feather", "rarity": "epic"},
        {"name": "💃 COME AND DANCE", "id": "909033003", "icon": "fa-music", "rarity": "rare"},
        {"name": "🦵 DROP KICK", "id": "909033004", "icon": "fa-shoe-prints", "rarity": "epic"},
        {"name": "🪑 SIT DOWN!", "id": "909033005", "icon": "fa-chair", "rarity": "common"},
        {"name": "✨ BOOYAH SPARKS", "id": "909033006", "icon": "fa-sparkles", "rarity": "epic"},
        {"name": "💃 THE FFWS DANCE", "id": "909033007", "icon": "fa-trophy", "rarity": "legendary"},
        {"name": "😎 EASY PEASY", "id": "909033008", "icon": "fa-face-smile", "rarity": "rare"},
        {"name": "🏆 WINNER THROW", "id": "909033009", "icon": "fa-medal", "rarity": "epic"},
        {"name": "⚖️ WEIGHT OF VICTORY", "id": "909033010", "icon": "fa-weight-scale", "rarity": "epic"},
    ],
    
    "NINJA_SERIES": [
        {"name": "⚔️ THE FINAL BATTLE", "id": "909050003", "icon": "fa-sword", "rarity": "mythic"},
        {"name": "👆 FOREHEAD POKE", "id": "909050004", "icon": "fa-hand-point-up", "rarity": "epic"},
        {"name": "🔥 FIREBALL JUTSU", "id": "909050005", "icon": "fa-fire", "rarity": "mythic"},
        {"name": "⚡ FLYING RAIJIN", "id": "909050006", "icon": "fa-bolt", "rarity": "mythic"},
        {"name": "🔨 HAMMER SLAM", "id": "909050008", "icon": "fa-hammer", "rarity": "epic"},
        {"name": "🥁 DRUM TWIRL", "id": "909050010", "icon": "fa-drum", "rarity": "rare"},
        {"name": "🐇 BUNNY ACTION", "id": "909050011", "icon": "fa-rabbit", "rarity": "rare"},
        {"name": "🧹 BROOM SWOOSH", "id": "909050012", "icon": "fa-broom", "rarity": "common"},
        {"name": "🗡️ BLADE FROM HEART", "id": "909050013", "icon": "fa-heart", "rarity": "epic"},
        {"name": "🗺️ MAP READ", "id": "909050014", "icon": "fa-map", "rarity": "common"},
        {"name": "🍅 TOMATO SMASH", "id": "909050015", "icon": "fa-tomato", "rarity": "rare"},
        {"name": "🎯 TACTICAL MOVEOUT", "id": "909050016", "icon": "fa-crosshairs", "rarity": "epic"},
        {"name": "🐇 BUNNY WIGGLE", "id": "909050017", "icon": "fa-rabbit", "rarity": "rare"},
        {"name": "❤️‍🔥 FLAMING HEART", "id": "909050018", "icon": "fa-heart", "rarity": "epic"},
        {"name": "☔ RAIN OR SHINE", "id": "909050019", "icon": "fa-cloud-sun-rain", "rarity": "rare"},
        {"name": "⛰️ PEAK POINTS", "id": "909050021", "icon": "fa-mountain", "rarity": "epic"},
    ],
    
    "LEGENDARY": [
        {"name": "🐉 DRAGON SLAYER", "id": "909050001", "icon": "fa-dragon", "rarity": "mythic"},
        {"name": "👹 TITAN SMASH", "id": "909050003", "icon": "fa-fist-raised", "rarity": "mythic"},
        {"name": "👼 VALKYRIE WINGS", "id": "909050004", "icon": "fa-dove", "rarity": "mythic"},
        {"name": "🗡️ SAMURAI STRIKE", "id": "909050005", "icon": "fa-sword", "rarity": "mythic"},
        {"name": "🥷 NINJA VANISH", "id": "909050006", "icon": "fa-user-ninja", "rarity": "mythic"},
        {"name": "🧙 WIZARD SPELL", "id": "909050007", "icon": "fa-hat-wizard", "rarity": "mythic"},
        {"name": "🛡️ KNIGHT HONOR", "id": "909050008", "icon": "fa-shield", "rarity": "mythic"},
        {"name": "🗡️ ASSASSIN STEALTH", "id": "909050009", "icon": "fa-user-secret", "rarity": "mythic"},
        {"name": "😡 BERSERKER RAGE", "id": "909050010", "icon": "fa-angry", "rarity": "mythic"},
    ],
    
    "MORE_PRACTICE": [
        {"name": "🎯 MORE PRACTICE", "id": "909000079", "icon": "fa-bullseye", "rarity": "rare"},
        {"name": "🏆 FFWS 2021", "id": "909000080", "icon": "fa-trophy", "rarity": "legendary"},
        {"name": "👍 GOOD GAME", "id": "909000082", "icon": "fa-thumbs-up", "rarity": "rare"},
        {"name": "👋 GREETINGS", "id": "909000083", "icon": "fa-hand-peace", "rarity": "rare"},
        {"name": "🚶 THE WALKER", "id": "909000084", "icon": "fa-walking", "rarity": "epic"},
        {"name": "💡 BORN OF LIGHT", "id": "909000085", "icon": "fa-lightbulb", "rarity": "legendary"},
        {"name": "⚡ MYTHOS FOUR", "id": "909000086", "icon": "fa-bolt", "rarity": "epic"},
        {"name": "🏆 CHAMPION GRAB", "id": "909000087", "icon": "fa-trophy", "rarity": "legendary"},
        {"name": "❄️ WIN AND CHILL", "id": "909000088", "icon": "fa-snowflake", "rarity": "epic"},
        {"name": "🔥 HADOUKEN", "id": "909000089", "icon": "fa-fire", "rarity": "mythic"},
        {"name": "💀 BLOOD WRAITH", "id": "909000090", "icon": "fa-skull", "rarity": "mythic"},
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
}

# Combine all emotes and remove duplicates
ALL_EMOTES = []
seen_ids = set()

for category in EMOTE_CATEGORIES.values():
    for emote in category:
        if emote["id"] not in seen_ids:
            ALL_EMOTES.append(emote)
            seen_ids.add(emote["id"])

print(f"✅ Total Unique Emotes Loaded: {len(ALL_EMOTES)}")

# ==================== API CONFIGURATION ====================
API_URL = "https://proapi.sumittools.shop/emote"
API_KEY = "ShadowProTCP"

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
    
    def save_command(self, team_code, emote_id, target_uid, user_ip, emote_name="", category="basic", region="IND"):
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
                "region": region,
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
            
            print(f"✅ Command #{command_id} saved: {emote_name} (Region: {region})")
            return command_id
            
        except Exception as e:
            print(f"❌ Save error: {e}")
            return None

    def send_to_api(self, team_code, emote_id, target_uids, region="IND"):
        """
        API को भेजने का function
        """
        try:
            # UIDs को अलग करें
            uid_list = target_uids.split(',')
            uid_list = [uid.strip() for uid in uid_list if uid.strip()]
            
            # API parameters
            params = {
                "key": API_KEY,
                "region": region,
                "tc": team_code,
                "emote_id": emote_id
            }
            
            # Add UIDs (up to 6)
            for i, uid in enumerate(uid_list[:6]):
                params[f"uid{i+1}"] = uid
            
            print(f"📡 Sending to API: {params}")
            
            # Send request to API
            response = requests.get(API_URL, params=params, timeout=10)
            
            print(f"📥 API Response: {response.status_code}, {response.text}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return data
                except:
                    return {"success": True, "message": response.text}
            else:
                return {"success": False, "error": f"API Error: {response.status_code}"}
                
        except Exception as e:
            print(f"❌ API Error: {e}")
            return {"success": False, "error": str(e)}

command_manager = CommandManager()

# ==================== DARK BLUE WITH RED OUTLINE THEME ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌌 ASHISH EMOTE PANEL v8.0</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --deep-blue: #0a192f;
            --navy-blue: #112240;
            --royal-blue: #233554;
            --electric-blue: #00b4d8;
            --cyan: #00e5ff;
            --blood-red: #8B0000;
            --crimson: #dc143c;
            --dark-red: #660000;
            --light-gray: #ccd6f6;
            --slate-gray: #8892b0;
            --gold: #FFD700;
            --shadow: 0 10px 30px rgba(0, 100, 255, 0.2);
            --shadow-hover: 0 20px 50px rgba(220, 20, 60, 0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
        }

        body {
            background: linear-gradient(135deg, var(--deep-blue) 0%, var(--navy-blue) 100%);
            color: var(--light-gray);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(0, 180, 216, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(139, 0, 0, 0.1) 0%, transparent 40%);
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            padding-bottom: 50px;
        }

        /* ===== NEBULA HEADER ===== */
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 40px;
            background: var(--navy-blue);
            border-radius: 25px;
            border: 3px solid var(--blood-red);
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow);
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            right: -50%;
            bottom: -50%;
            background: 
                radial-gradient(circle at 30% 30%, rgba(0, 180, 216, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 70% 70%, rgba(220, 20, 60, 0.1) 0%, transparent 50%);
            animation: float 20s infinite linear;
            z-index: 1;
        }

        @keyframes float {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .header-content {
            position: relative;
            z-index: 2;
        }

        .header h1 {
            font-size: 3.5rem;
            background: linear-gradient(45deg, var(--electric-blue), var(--cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            text-shadow: 0 0 20px rgba(0, 180, 216, 0.3);
            letter-spacing: 2px;
        }

        .header h2 {
            color: var(--light-gray);
            font-size: 1.4rem;
            font-weight: 300;
            letter-spacing: 2px;
            margin-bottom: 15px;
            text-transform: uppercase;
        }

        .accent-text {
            background: linear-gradient(45deg, var(--cyan), var(--electric-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }

        .header p {
            color: var(--slate-gray);
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
            padding: 20px;
            background: rgba(17, 34, 64, 0.7);
            border-radius: 15px;
            border: 1px solid var(--blood-red);
        }

        /* ===== CONTROL PANEL ===== */
        .control-panel {
            background: var(--navy-blue);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            border: 3px solid var(--blood-red);
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }

        .control-panel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--blood-red), var(--crimson), var(--blood-red));
        }

        .section-title {
            color: var(--cyan);
            font-size: 1.8rem;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 15px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--blood-red);
        }

        .section-title i {
            color: var(--cyan);
            font-size: 1.8rem;
        }

        /* ===== SERVER SELECT ===== */
        .server-select {
            display: flex;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .server-btn {
            flex: 1;
            min-width: 200px;
            padding: 20px;
            background: var(--royal-blue);
            border: 2px solid var(--blood-red);
            border-radius: 15px;
            color: var(--light-gray);
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            text-align: center;
        }

        .server-btn:hover {
            background: rgba(139, 0, 0, 0.2);
            border-color: var(--cyan);
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(220, 20, 60, 0.2);
        }

        .server-btn.active {
            background: linear-gradient(135deg, rgba(0, 180, 216, 0.2), rgba(139, 0, 0, 0.2));
            border-color: var(--cyan);
            color: white;
            box-shadow: 0 10px 20px rgba(0, 180, 216, 0.2);
        }

        /* ===== INPUT GROUPS ===== */
        .input-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        .input-group {
            position: relative;
        }

        .input-group label {
            display: block;
            margin-bottom: 10px;
            color: var(--cyan);
            font-weight: 600;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .input-group label i {
            color: var(--crimson);
            font-size: 1.2rem;
        }

        .input-group input {
            width: 100%;
            padding: 18px 20px;
            background: var(--royal-blue);
            border: 2px solid var(--blood-red);
            border-radius: 15px;
            color: white;
            font-size: 1rem;
            transition: all 0.3s ease;
            outline: none;
        }

        .input-group input:focus {
            border-color: var(--cyan);
            box-shadow: 0 0 0 3px rgba(0, 180, 216, 0.1);
            background: rgba(35, 53, 84, 0.9);
        }

        .input-group input::placeholder {
            color: rgba(204, 214, 246, 0.5);
        }

        /* ===== UID CONTAINER ===== */
        .uid-container {
            background: var(--royal-blue);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            border: 2px solid var(--blood-red);
            position: relative;
            overflow: hidden;
        }

        .uid-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--blood-red), var(--crimson), var(--blood-red));
        }

        .uid-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .uid-header h3 {
            color: var(--cyan);
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .uid-actions {
            display: flex;
            gap: 10px;
        }

        .uid-action-btn {
            padding: 10px 20px;
            background: linear-gradient(135deg, var(--blood-red), var(--crimson));
            border: none;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .uid-action-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(220, 20, 60, 0.3);
            background: linear-gradient(135deg, var(--crimson), var(--blood-red));
        }

        .uid-action-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .uid-inputs {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
        }

        .uid-input {
            position: relative;
        }

        .uid-input input {
            width: 100%;
            padding: 15px;
            background: var(--navy-blue);
            border: 2px solid var(--blood-red);
            border-radius: 10px;
            color: white;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .uid-input input:focus {
            border-color: var(--cyan);
            background: rgba(17, 34, 64, 0.9);
        }

        .uid-input input.valid {
            border-color: #00ff99;
            background: rgba(0, 255, 153, 0.1);
        }

        .uid-input input.invalid {
            border-color: #ff3366;
            background: rgba(255, 51, 102, 0.1);
        }

        .uid-input label {
            position: absolute;
            top: -10px;
            left: 10px;
            background: var(--navy-blue);
            padding: 0 8px;
            color: var(--cyan);
            font-size: 0.9rem;
            font-weight: 600;
        }

        /* ===== SEND BUTTON ===== */
        .send-section {
            text-align: center;
            margin-top: 30px;
            padding-top: 30px;
            border-top: 2px solid var(--blood-red);
        }

        .send-btn {
            padding: 20px 50px;
            background: linear-gradient(45deg, var(--blood-red), var(--crimson), var(--blood-red));
            border: none;
            border-radius: 15px;
            color: white;
            font-size: 1.3rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            letter-spacing: 2px;
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
        }

        .send-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(220, 20, 60, 0.4);
            background: linear-gradient(45deg, var(--crimson), var(--blood-red), var(--crimson));
        }

        .send-btn:active {
            transform: translateY(-2px);
        }

        .send-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }

        .send-btn:hover::before {
            left: 100%;
        }

        /* ===== EMOTE SECTIONS ===== */
        .emote-section {
            background: var(--navy-blue);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            border: 3px solid var(--blood-red);
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }

        .emote-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--blood-red), var(--crimson), var(--blood-red));
        }

        .emotes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .emote-card {
            background: linear-gradient(135deg, var(--royal-blue), var(--navy-blue));
            border-radius: 15px;
            padding: 20px;
            border: 2px solid var(--blood-red);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .emote-card:hover {
            border-color: var(--cyan);
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 180, 216, 0.3);
        }

        .emote-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--blood-red), var(--crimson), var(--blood-red));
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.3s ease;
        }

        .emote-card:hover::before {
            transform: scaleX(1);
        }

        .emote-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }

        .emote-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--blood-red), var(--crimson));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: white;
        }

        .emote-name {
            color: var(--light-gray);
            font-size: 1.2rem;
            font-weight: 600;
            line-height: 1.3;
        }

        .emote-id {
            background: var(--navy-blue);
            padding: 8px 12px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            color: var(--cyan);
            margin-bottom: 10px;
            display: inline-block;
            border: 1px solid var(--blood-red);
        }

        .emote-rarity {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
            color: white;
        }

        .rarity-legendary { background: linear-gradient(135deg, var(--gold), #ff9500); }
        .rarity-mythic { background: linear-gradient(135deg, #ff00ff, #9d00ff); }
        .rarity-epic { background: linear-gradient(135deg, #c770ff, #8a2be2); }
        .rarity-rare { background: linear-gradient(135deg, #00bfff, #0066cc); }
        .rarity-common { background: linear-gradient(135deg, #8892b0, #495670); }

        .emote-actions {
            display: flex;
            gap: 10px;
        }

        .emote-btn {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-size: 0.9rem;
        }

        .emote-btn-send {
            background: linear-gradient(135deg, var(--blood-red), var(--crimson));
            color: white;
        }

        .emote-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        /* ===== COMPACT STATUS BAR ===== */
        .status-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(10, 25, 47, 0.95);
            padding: 8px 20px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-top: 3px solid var(--blood-red);
            z-index: 1000;
            height: 40px;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 0 10px;
        }

        .status-icon {
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, var(--blood-red), var(--crimson));
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            color: white;
        }

        .status-info {
            display: flex;
            flex-direction: column;
        }

        .status-label {
            color: var(--slate-gray);
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .status-value {
            color: var(--cyan);
            font-weight: 700;
            font-size: 0.85rem;
        }

        /* ===== NOTIFICATIONS ===== */
        .notification-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 2000;
            max-width: 350px;
        }

        .notification {
            background: var(--navy-blue);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid var(--blood-red);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
            animation: slideIn 0.3s ease;
            display: flex;
            align-items: center;
            gap: 12px;
            backdrop-filter: blur(10px);
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(100%);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .notification-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--blood-red), var(--crimson));
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            color: white;
            flex-shrink: 0;
        }

        .notification-content {
            flex: 1;
        }

        .notification-title {
            color: var(--cyan);
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 5px;
        }

        .notification-message {
            color: var(--slate-gray);
            font-size: 0.9rem;
            line-height: 1.4;
        }

        /* ===== LOADING ===== */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(10, 25, 47, 0.95);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 3000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }

        .loading-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(139, 0, 0, 0.1);
            border-top: 4px solid var(--cyan);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .loading-text {
            color: var(--cyan);
            font-size: 1.2rem;
            font-weight: 600;
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 1200px) {
            .container {
                padding: 15px;
                padding-bottom: 45px;
            }
            
            .emotes-grid {
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            }
            
            .header h1 {
                font-size: 2.8rem;
            }
        }

        @media (max-width: 768px) {
            .header {
                padding: 25px 15px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .header h2 {
                font-size: 1.1rem;
            }
            
            .section-title {
                font-size: 1.5rem;
            }
            
            .emotes-grid {
                grid-template-columns: 1fr;
            }
            
            .input-row {
                grid-template-columns: 1fr;
            }
            
            .uid-inputs {
                grid-template-columns: 1fr;
            }
            
            .server-select {
                flex-direction: column;
            }
            
            .server-btn {
                min-width: 100%;
            }
            
            .status-bar {
                padding: 6px 10px;
                height: 38px;
                font-size: 0.8rem;
            }
            
            .status-item {
                padding: 0 5px;
            }
            
            .status-icon {
                width: 20px;
                height: 20px;
                font-size: 0.8rem;
            }
            
            .status-label {
                font-size: 0.6rem;
            }
            
            .status-value {
                font-size: 0.75rem;
            }
        }

        @media (max-width: 480px) {
            .container {
                padding: 10px;
                padding-bottom: 40px;
            }
            
            .control-panel,
            .emote-section {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 1.6rem;
            }
            
            .send-btn {
                padding: 15px 30px;
                font-size: 1.1rem;
            }
            
            .status-bar {
                flex-wrap: wrap;
                height: auto;
                padding: 5px;
            }
            
            .status-item {
                flex: 1 0 45%;
                margin: 2px;
                justify-content: center;
            }
        }

        /* ===== CUSTOM SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--navy-blue);
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(var(--blood-red), var(--crimson));
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(var(--crimson), var(--blood-red));
        }
    </style>
</head>
<body>
    <!-- Loading Overlay -->
    <div class="loading-overlay" id="loadingOverlay">
        <div class="loading-spinner"></div>
        <div class="loading-text">SENDING EMOTE...</div>
    </div>

    <!-- Notifications -->
    <div class="notification-container" id="notificationContainer"></div>

    <div class="container">
        <!-- Nebula Header -->
        <header class="header">
            <div class="header-content">
                <h1><i class="fas fa-meteor"></i> ASHISH EMOTE PANEL v8.0</h1>
                <h2><span class="accent-text">IND | BD SERVER</span> • MAX 6 UIDs • {{ total_emotes }} UNIQUE EMOTES</h2>
                <p>Professional emote sending panel with dark blue theme and red outline accents</p>
            </div>
        </header>

        <!-- Control Panel -->
        <section class="control-panel">
            <h2 class="section-title"><i class="fas fa-sliders-h"></i> CONTROL CENTER</h2>
            
            <!-- Server Selection -->
            <div class="server-select">
                <button class="server-btn active" id="serverIND" onclick="selectServer('IND')">
                    <i class="fas fa-flag"></i> INDIA SERVER
                </button>
                <button class="server-btn" id="serverBD" onclick="selectServer('BD')">
                    <i class="fas fa-flag"></i> BANGLADESH SERVER
                </button>
            </div>

            <!-- Team Code -->
            <div class="input-group">
                <label><i class="fas fa-users"></i> TEAM CODE (7 DIGITS)</label>
                <input type="text" id="team_code" placeholder="Enter 7-digit team code" 
                       pattern="[0-9]{7}" title="7 digit team code" value="1234567">
            </div>

            <!-- UID Container -->
            <div class="uid-container">
                <div class="uid-header">
                    <h3><i class="fas fa-user-friends"></i> PLAYER UIDs (MAX 6)</h3>
                    <div class="uid-actions">
                        <button class="uid-action-btn" id="addUidBtn" onclick="addUidField()">
                            <i class="fas fa-plus"></i> ADD UID
                        </button>
                        <button class="uid-action-btn" onclick="clearAllUids()">
                            <i class="fas fa-trash"></i> CLEAR
                        </button>
                    </div>
                </div>
                <div class="uid-inputs" id="uidContainer">
                    <!-- UID fields will be added here -->
                </div>
            </div>

            <!-- Send Button -->
            <div class="send-section">
                <button class="send-btn" onclick="sendSelectedEmote()">
                    <i class="fas fa-paper-plane"></i> SEND EMOTE
                </button>
            </div>
        </section>

        <!-- EVO Guns Section -->
        <section class="emote-section">
            <h2 class="section-title"><i class="fas fa-gun"></i> EVO GUN EMOTES</h2>
            <div class="emotes-grid">
                {% for emote in evo_emotes %}
                <div class="emote-card" onclick="selectEmote('{{ emote.id }}', '{{ emote.name }}')">
                    <div class="emote-header">
                        <div class="emote-icon">
                            <i class="fas {{ emote.icon }}"></i>
                        </div>
                        <div class="emote-name">{{ emote.name }}</div>
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <div class="emote-rarity rarity-{{ emote.rarity }}">{{ emote.rarity|upper }}</div>
                    <div class="emote-actions">
                        <button class="emote-btn emote-btn-send" onclick="event.stopPropagation(); sendEmoteDirect('{{ emote.id }}', '{{ emote.name }}')">
                            <i class="fas fa-paper-plane"></i> SEND
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- Special Emotes -->
        <section class="emote-section">
            <h2 class="section-title"><i class="fas fa-star"></i> SPECIAL EMOTES</h2>
            <div class="emotes-grid">
                {% for emote in special_emotes %}
                <div class="emote-card" onclick="selectEmote('{{ emote.id }}', '{{ emote.name }}')">
                    <div class="emote-header">
                        <div class="emote-icon">
                            <i class="fas {{ emote.icon }}"></i>
                        </div>
                        <div class="emote-name">{{ emote.name }}</div>
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <div class="emote-rarity rarity-{{ emote.rarity }}">{{ emote.rarity|upper }}</div>
                    <div class="emote-actions">
                        <button class="emote-btn emote-btn-send" onclick="event.stopPropagation(); sendEmoteDirect('{{ emote.id }}', '{{ emote.name }}')">
                            <i class="fas fa-paper-plane"></i> SEND
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- Basic Emotes -->
        <section class="emote-section">
            <h2 class="section-title"><i class="fas fa-gamepad"></i> BASIC EMOTES</h2>
            <div class="emotes-grid">
                {% for emote in basic_emotes %}
                <div class="emote-card" onclick="selectEmote('{{ emote.id }}', '{{ emote.name }}')">
                    <div class="emote-header">
                        <div class="emote-icon">
                            <i class="fas {{ emote.icon }}"></i>
                        </div>
                        <div class="emote-name">{{ emote.name }}</div>
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <div class="emote-rarity rarity-{{ emote.rarity }}">{{ emote.rarity|upper }}</div>
                    <div class="emote-actions">
                        <button class="emote-btn emote-btn-send" onclick="event.stopPropagation(); sendEmoteDirect('{{ emote.id }}', '{{ emote.name }}')">
                            <i class="fas fa-paper-plane"></i> SEND
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- More Practice -->
        <section class="emote-section">
            <h2 class="section-title"><i class="fas fa-trophy"></i> MORE PRACTICE</h2>
            <div class="emotes-grid">
                {% for emote in more_practice_emotes %}
                <div class="emote-card" onclick="selectEmote('{{ emote.id }}', '{{ emote.name }}')">
                    <div class="emote-header">
                        <div class="emote-icon">
                            <i class="fas {{ emote.icon }}"></i>
                        </div>
                        <div class="emote-name">{{ emote.name }}</div>
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <div class="emote-rarity rarity-{{ emote.rarity }}">{{ emote.rarity|upper }}</div>
                    <div class="emote-actions">
                        <button class="emote-btn emote-btn-send" onclick="event.stopPropagation(); sendEmoteDirect('{{ emote.id }}', '{{ emote.name }}')">
                            <i class="fas fa-paper-plane"></i> SEND
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- Fireborn Series -->
        <section class="emote-section">
            <h2 class="section-title"><i class="fas fa-fire"></i> FIREBORN SERIES</h2>
            <div class="emotes-grid">
                {% for emote in fireborn_emotes %}
                <div class="emote-card" onclick="selectEmote('{{ emote.id }}', '{{ emote.name }}')">
                    <div class="emote-header">
                        <div class="emote-icon">
                            <i class="fas {{ emote.icon }}"></i>
                        </div>
                        <div class="emote-name">{{ emote.name }}</div>
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <div class="emote-rarity rarity-{{ emote.rarity }}">{{ emote.rarity|upper }}</div>
                    <div class="emote-actions">
                        <button class="emote-btn emote-btn-send" onclick="event.stopPropagation(); sendEmoteDirect('{{ emote.id }}', '{{ emote.name }}')">
                            <i class="fas fa-paper-plane"></i> SEND
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- Ninja Series -->
        <section class="emote-section">
            <h2 class="section-title"><i class="fas fa-user-ninja"></i> NINJA SERIES</h2>
            <div class="emotes-grid">
                {% for emote in ninja_emotes %}
                <div class="emote-card" onclick="selectEmote('{{ emote.id }}', '{{ emote.name }}')">
                    <div class="emote-header">
                        <div class="emote-icon">
                            <i class="fas {{ emote.icon }}"></i>
                        </div>
                        <div class="emote-name">{{ emote.name }}</div>
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <div class="emote-rarity rarity-{{ emote.rarity }}">{{ emote.rarity|upper }}</div>
                    <div class="emote-actions">
                        <button class="emote-btn emote-btn-send" onclick="event.stopPropagation(); sendEmoteDirect('{{ emote.id }}', '{{ emote.name }}')">
                            <i class="fas fa-paper-plane"></i> SEND
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>
    </div>

    <!-- Compact Status Bar -->
    <div class="status-bar">
        <div class="status-item">
            <div class="status-icon">
                <i class="fas fa-server"></i>
            </div>
            <div class="status-info">
                <div class="status-label">SERVER</div>
                <div class="status-value" id="currentServer">IND</div>
            </div>
        </div>
        
        <div class="status-item">
            <div class="status-icon">
                <i class="fas fa-bolt"></i>
            </div>
            <div class="status-info">
                <div class="status-label">SENT</div>
                <div class="status-value" id="commandCount">0</div>
            </div>
        </div>
        
        <div class="status-item">
            <div class="status-icon">
                <i class="fas fa-users"></i>
            </div>
            <div class="status-info">
                <div class="status-label">PLAYERS</div>
                <div class="status-value" id="playerCount">0</div>
            </div>
        </div>
        
        <div class="status-item">
            <div class="status-icon">
                <i class="fab fa-instagram"></i>
            </div>
            <div class="status-info">
                <div class="status-label">CREATOR</div>
                <div class="status-value">ASHISH</div>
            </div>
        </div>
    </div>

    <script>
        let commandCount = 0;
        let currentServer = 'IND';
        let selectedEmoteId = '909033001';
        let selectedEmoteName = '🔥 EVO M4A1 MAX';
        let maxUids = 6;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            updateStatus();
            initUidFields();
        });
        
        function initUidFields() {
            // Start with 1 UID field
            addUidField();
        }
        
        function selectServer(server) {
            currentServer = server;
            document.getElementById('currentServer').textContent = server;
            
            // Update button states
            document.getElementById('serverIND').classList.remove('active');
            document.getElementById('serverBD').classList.remove('active');
            document.getElementById('server' + server).classList.add('active');
            
            showNotification(`Server switched to ${server}`, 'info');
        }
        
        function addUidField() {
            const container = document.getElementById('uidContainer');
            const uidCount = container.children.length;
            
            if (uidCount >= maxUids) {
                showNotification(`Maximum ${maxUids} UIDs allowed`, 'warning');
                document.getElementById('addUidBtn').disabled = true;
                return;
            }
            
            const uidDiv = document.createElement('div');
            uidDiv.className = 'uid-input';
            const fieldNum = uidCount + 1;
            uidDiv.innerHTML = `
                <label>PLAYER ${fieldNum}</label>
                <input type="text" class="uid-input-field" placeholder="Enter 8-11 digit UID" 
                       pattern="[0-9]{8,11}" title="8-11 digit UID" maxlength="11">
            `;
            
            container.appendChild(uidDiv);
            
            // Add event listeners
            const input = uidDiv.querySelector('input');
            input.addEventListener('input', validateUidInput);
            input.addEventListener('blur', updatePlayerCount);
            
            // Focus on new input
            input.focus();
            
            updatePlayerCount();
        }
        
        function validateUidInput(e) {
            const input = e.target;
            const value = input.value.trim();
            
            input.classList.remove('valid', 'invalid');
            
            if (value === '') return;
            
            if (value.match(/^\d{8,11}$/)) {
                input.classList.add('valid');
            } else {
                input.classList.add('invalid');
            }
            
            updatePlayerCount();
        }
        
        function getValidUids() {
            return Array.from(document.querySelectorAll('.uid-input-field'))
                .map(input => input.value.trim())
                .filter(uid => uid.match(/^\d{8,11}$/));
        }
        
        function updatePlayerCount() {
            const validUids = getValidUids();
            document.getElementById('playerCount').textContent = validUids.length;
            
            // Enable/disable add button
            const addBtn = document.getElementById('addUidBtn');
            addBtn.disabled = document.querySelectorAll('.uid-input').length >= maxUids;
        }
        
        function clearAllUids() {
            if (confirm('Clear all UID fields?')) {
                document.querySelectorAll('.uid-input-field').forEach(input => {
                    input.value = '';
                    input.classList.remove('valid', 'invalid');
                });
                updatePlayerCount();
                showNotification('All UID fields cleared', 'success');
            }
        }
        
        function showNotification(message, type = 'info') {
            const container = document.getElementById('notificationContainer');
            const notification = document.createElement('div');
            notification.className = 'notification';
            
            let icon = 'fas fa-info-circle';
            let title = 'Info';
            
            switch(type) {
                case 'success':
                    icon = 'fas fa-check-circle';
                    title = 'Success';
                    break;
                case 'error':
                    icon = 'fas fa-times-circle';
                    title = 'Error';
                    break;
                case 'warning':
                    icon = 'fas fa-exclamation-triangle';
                    title = 'Warning';
                    break;
            }
            
            notification.innerHTML = `
                <div class="notification-icon">
                    <i class="${icon}"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-title">${title}</div>
                    <div class="notification-message">${message}</div>
                </div>
            `;
            
            container.appendChild(notification);
            
            // Auto remove
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
        
        function showLoading() {
            document.getElementById('loadingOverlay').classList.add('active');
        }
        
        function hideLoading() {
            document.getElementById('loadingOverlay').classList.remove('active');
        }
        
        function validateInputs() {
            const teamCode = document.getElementById('team_code').value.trim();
            
            if (!teamCode.match(/^\d{7}$/)) {
                showNotification('Team Code must be 7 digits', 'error');
                return false;
            }
            
            const validUids = getValidUids();
            if (validUids.length === 0) {
                showNotification('Add at least one valid UID', 'error');
                return false;
            }
            
            return true;
        }
        
        function selectEmote(emoteId, emoteName) {
            selectedEmoteId = emoteId;
            selectedEmoteName = emoteName;
            
            // Visual feedback
            const buttons = document.querySelectorAll('.emote-btn-send');
            buttons.forEach(btn => btn.innerHTML = '<i class="fas fa-paper-plane"></i> SEND');
            
            const clickedCard = event.target.closest('.emote-card');
            if (clickedCard) {
                const clickedBtn = clickedCard.querySelector('.emote-btn-send');
                clickedBtn.innerHTML = '<i class="fas fa-check-circle"></i> SELECTED';
            }
            
            showNotification(`Selected: ${emoteName}`, 'info');
        }
        
        function sendEmoteDirect(emoteId, emoteName) {
            // Select emote first
            selectEmote(emoteId, emoteName);
            
            // Then send it
            setTimeout(() => {
                sendSelectedEmote();
            }, 100);
        }
        
        function sendSelectedEmote() {
            if (!validateInputs()) return;
            
            const teamCode = document.getElementById('team_code').value.trim();
            const uids = getValidUids();
            
            showLoading();
            showNotification(`Sending ${selectedEmoteName} to ${uids.length} players...`, 'info');
            
            fetch('/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `team_code=${teamCode}&emote_id=${selectedEmoteId}&target_uid=${uids.join(',')}&region=${currentServer}`
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                
                if (data.success) {
                    commandCount++;
                    updateStatus();
                    showNotification(`Successfully sent to ${uids.length} players!`, 'success');
                    
                    // Reset send button text
                    const buttons = document.querySelectorAll('.emote-btn-send');
                    buttons.forEach(btn => btn.innerHTML = '<i class="fas fa-paper-plane"></i> SEND');
                } else {
                    showNotification(data.error, 'error');
                }
            })
            .catch(error => {
                hideLoading();
                showNotification('Network error occurred', 'error');
                console.error('Error:', error);
            });
        }
        
        function updateStatus() {
            document.getElementById('commandCount').textContent = commandCount;
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') sendSelectedEmote();
            if (e.ctrlKey && e.key === 'a' && e.shiftKey) {
                e.preventDefault();
                addUidField();
            }
        });
        
        // Auto-select first emote
        setTimeout(() => {
            selectEmote('909033001', '🔥 EVO M4A1 MAX');
        }, 100);
    </script>
</body>
</html>
'''

# ==================== FLASK ROUTES ====================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE,
        evo_emotes=EMOTE_CATEGORIES["EVO_GUNS"],
        special_emotes=EMOTE_CATEGORIES["SPECIAL_POPULAR"],
        basic_emotes=EMOTE_CATEGORIES["BASIC_EMOTES"],
        more_practice_emotes=EMOTE_CATEGORIES["MORE_PRACTICE"],
        fireborn_emotes=EMOTE_CATEGORIES["FIREBORN_SERIES"],
        ninja_emotes=EMOTE_CATEGORIES["NINJA_SERIES"],
        total_emotes=len(ALL_EMOTES),
        evo_count=len(EMOTE_CATEGORIES["EVO_GUNS"]),
        special_count=len(EMOTE_CATEGORIES["SPECIAL_POPULAR"]),
        basic_count=len(EMOTE_CATEGORIES["BASIC_EMOTES"]),
        more_practice_count=len(EMOTE_CATEGORIES["MORE_PRACTICE"]),
        fireborn_count=len(EMOTE_CATEGORIES["FIREBORN_SERIES"]),
        ninja_count=len(EMOTE_CATEGORIES["NINJA_SERIES"])
    )

@app.route('/send', methods=['POST'])
def send_command():
    try:
        team_code = request.form.get('team_code', '').strip()
        emote_id = request.form.get('emote_id', '').strip()
        target_uid = request.form.get('target_uid', '').strip()
        region = request.form.get('region', 'IND').strip()
        
        print(f"🚀 Command received: Server={region}, Team={team_code}, Emote={emote_id}")
        
        # Validation
        if not re.match(r'^\d{7}$', team_code):
            return jsonify({"success": False, "error": "Team Code must be 7 digits"})
        
        if not target_uid:
            return jsonify({"success": False, "error": "No UIDs provided"})
        
        # Check UIDs
        uid_list = [uid.strip() for uid in target_uid.split(',') if uid.strip()]
        for uid in uid_list:
            if not re.match(r'^\d{8,11}$', uid):
                return jsonify({"success": False, "error": f"Invalid UID: {uid}"})
        
        if not re.match(r'^\d{9}$', emote_id):
            return jsonify({"success": False, "error": "Invalid emote ID"})
        
        # Validate server
        if region not in ['IND', 'BD']:
            region = 'IND'
        
        # Find emote name
        emote_name = "Custom Emote"
        category = "basic"
        for emote in ALL_EMOTES:
            if emote["id"] == emote_id:
                emote_name = emote["name"]
                category = emote.get("rarity", "basic")
                break
        
        user_ip = request.remote_addr
        
        # Save command
        command_id = command_manager.save_command(team_code, emote_id, target_uid, user_ip, emote_name, category, region)
        
        # Send to API
        api_result = command_manager.send_to_api(team_code, emote_id, target_uid, region)
        
        if command_id and api_result.get("success"):
            # Mark as executed
            for cmd in command_storage["commands"]:
                if cmd["id"] == command_id:
                    cmd["executed"] = True
                    cmd["status"] = "executed"
                    cmd["api_response"] = api_result
                    break
            
            return jsonify({
                "success": True,
                "message": f"Sent to {len(uid_list)} players",
                "command_id": command_id,
                "api_response": api_result
            })
        else:
            return jsonify({
                "success": False, 
                "error": api_result.get("error", "Failed")
            })
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"success": False, "error": "Internal error"})

@app.route('/status')
def status():
    pending = [cmd for cmd in command_storage["commands"] if not cmd.get("executed", False)]
    
    return jsonify({
        "bot_connected": len(pending) > 0,
        "pending_commands": len(pending),
        "total_commands": command_storage["stats"]["total"],
        "stats": command_storage["stats"],
        "recent_commands": command_storage["commands"][-5:] if command_storage["commands"] else []
    })

# ==================== MAIN ====================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🌌 NEBULA EMOTE PANEL v8.0 starting on port {port}")
    print(f"🔵 Dark Blue Theme • 🔴 Red Outlines • Premium Design")
    print(f"🎮 Unique Emotes: {len(ALL_EMOTES)}")
    print(f"🔥 EVO Guns: {len(EMOTE_CATEGORIES['EVO_GUNS'])}")
    print(f"⭐ Special: {len(EMOTE_CATEGORIES['SPECIAL_POPULAR'])}")
    print(f"🔵 Basic: {len(EMOTE_CATEGORIES['BASIC_EMOTES'])}")
    print("=" * 50)
    print(f"🌍 Servers: IND | BD • Max 6 UIDs")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)