from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import os
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ashish-premium-panel-2024')

# ==================== EMOTE DATABASE FROM FILE ====================
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
        {"name": "💪 PUSH UP", "id": "909000012", "icon": "fa-dumbbell", "rarity": "rare"},
        {"name": "😈 DEVIL'S MOVE", "id": "909000020", "icon": "fa-horn", "rarity": "epic"},
        {"name": "👑 EL 3ARCH EMOTE", "id": "909000014", "icon": "fa-throne", "rarity": "legendary"},
        {"name": "✋ HIGH FIVE", "id": "909000025", "icon": "fa-hand", "rarity": "rare"},
        {"name": "🔫 SHOTGUN EMOTE", "id": "909000081", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🐉 AK DRAGON EMOTE", "id": "909000063", "icon": "fa-dragon", "rarity": "legendary"},
        {"name": "🎭 COBRA EMOTE 2", "id": "909000071", "icon": "fa-snake", "rarity": "epic"},
        {"name": "👑 EL 9ARASNA EMOTE", "id": "909000034", "icon": "fa-flag", "rarity": "epic"},
        {"name": "👻 FER3AWN EMOTE", "id": "909000011", "icon": "fa-ghost", "rarity": "epic"},
        {"name": "🕺 MICHAEL JACKSON", "id": "909045009", "icon": "fa-music", "rarity": "legendary"},
        {"name": "⚡ JUJUTSU EMOTE", "id": "909050002", "icon": "fa-bolt", "rarity": "legendary"},
        {"name": "💎 NEW EMOTE", "id": "909050009", "icon": "fa-gem", "rarity": "epic"},
        {"name": "🔥 LEVEL 100 EMOTE", "id": "909042007", "icon": "fa-fire", "rarity": "mythic"},
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
        {"name": "👊 Threaten", "id": "909000018", "icon": "fa-hand-fist", "rarity": "common"},
        {"name": "🔄 Shake With Me", "id": "909000019", "icon": "fa-people-arrows", "rarity": "common"},
        {"name": "😡 Furious Slam", "id": "909000021", "icon": "fa-angry", "rarity": "epic"},
        {"name": "🌙 Moon Flip", "id": "909000022", "icon": "fa-moon", "rarity": "epic"},
        {"name": "💃 Wiggle Walk", "id": "909000023", "icon": "fa-walking", "rarity": "common"},
        {"name": "⚔️ Battle Dance", "id": "909000024", "icon": "fa-sword", "rarity": "rare"},
        {"name": "🎉 Shake It Up", "id": "909000026", "icon": "fa-glass-cheers", "rarity": "common"},
        {"name": "🌟 Glorious Spin", "id": "909000027", "icon": "fa-star", "rarity": "epic"},
        {"name": "🦅 Crane Kick", "id": "909000028", "icon": "fa-dove", "rarity": "rare"},
        {"name": "🎉 Party Dance", "id": "909000029", "icon": "fa-champagne-glasses", "rarity": "common"},
        {"name": "💃 Jig Dance", "id": "909000031", "icon": "fa-music", "rarity": "common"},
        {"name": "📸 Selfie", "id": "909000032", "icon": "fa-camera", "rarity": "common"},
        {"name": "👻 Soul Shaking", "id": "909000033", "icon": "fa-ghost", "rarity": "epic"},
        {"name": "💕 Healing Dance", "id": "909000035", "icon": "fa-heart-pulse", "rarity": "rare"},
        {"name": "🎧 Top DJ", "id": "909000036", "icon": "fa-headphones", "rarity": "epic"},
        {"name": "😠 Death Glare", "id": "909000037", "icon": "fa-eye", "rarity": "epic"},
        {"name": "💰 Power of Money", "id": "909000038", "icon": "fa-money-bill", "rarity": "epic"},
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
        {"name": "⚔️ Challenge On!", "id": "909000053", "icon": "fa-crosshairs", "rarity": "rare"},
        {"name": "🤠 Lasso", "id": "909000054", "icon": "fa-lasso", "rarity": "rare"},
        {"name": "💰 I'm Rich!", "id": "909000055", "icon": "fa-money-bill-wave", "rarity": "epic"},
        {"name": "💪 More Practice", "id": "909000079", "icon": "fa-dumbbell", "rarity": "rare"},
        {"name": "🏆 FFWS 2021", "id": "909000080", "icon": "fa-trophy", "rarity": "legendary"},
        {"name": "🐉 Draco's Soul", "id": "909000081", "icon": "fa-dragon", "rarity": "mythic"},
        {"name": "👍 Good Game", "id": "909000082", "icon": "fa-thumbs-up", "rarity": "common"},
        {"name": "👋 Greetings", "id": "909000083", "icon": "fa-hand-peace", "rarity": "common"},
        {"name": "🚶 The Walker", "id": "909000084", "icon": "fa-walking", "rarity": "epic"},
        {"name": "💡 Born of Light", "id": "909000085", "icon": "fa-lightbulb", "rarity": "legendary"},
        {"name": "⚡ Mythos Four", "id": "909000086", "icon": "fa-bolt", "rarity": "epic"},
        {"name": "🏆 Champion Grab", "id": "909000087", "icon": "fa-trophy", "rarity": "legendary"},
        {"name": "❄️ Win and Chill", "id": "909000088", "icon": "fa-snowflake", "rarity": "epic"},
        {"name": "🔥 Hadouken", "id": "909000089", "icon": "fa-fire", "rarity": "mythic"},
        {"name": "💀 Blood Wraith", "id": "909000090", "icon": "fa-skull", "rarity": "mythic"},
        {"name": "👹 Big Smash", "id": "909000091", "icon": "fa-fist-raised", "rarity": "epic"},
        {"name": "💃 Fancy Steps", "id": "909000092", "icon": "fa-shoe-prints", "rarity": "rare"},
        {"name": "🎮 All In Control", "id": "909000093", "icon": "fa-gamepad", "rarity": "epic"},
        {"name": "🔧 Debugging", "id": "909000094", "icon": "fa-screwdriver-wrench", "rarity": "rare"},
        {"name": "👋 Waggor Wave", "id": "909000095", "icon": "fa-hand-wave", "rarity": "rare"},
        {"name": "🎸 Crazy Guitar", "id": "909000096", "icon": "fa-guitar", "rarity": "epic"},
        {"name": "✨ Poof", "id": "909000097", "icon": "fa-wand-sparkles", "rarity": "rare"},
        {"name": "👑 The Chosen Victor", "id": "909000098", "icon": "fa-crown", "rarity": "legendary"},
        {"name": "⚔️ Challenger", "id": "909000099", "icon": "fa-crosshairs", "rarity": "epic"},
    ],
    
    "SEASONAL_EMOTES": [
        {"name": "💃 Mummy Dance", "id": "909000011", "icon": "fa-ghost", "rarity": "rare"},
        {"name": "👻 Ghost Float", "id": "909036001", "icon": "fa-ghost", "rarity": "epic"},
        {"name": "🦌 Reindeer Float", "id": "909037001", "icon": "fa-horse", "rarity": "epic"},
        {"name": "🎋 Bamboo Dance", "id": "909037002", "icon": "fa-tree", "rarity": "rare"},
        {"name": "🌟 Dance of Constellation", "id": "909037003", "icon": "fa-star", "rarity": "legendary"},
        {"name": "🏆 Trophy Grab", "id": "909037004", "icon": "fa-trophy", "rarity": "epic"},
        {"name": "✨ Starry Hands", "id": "909037005", "icon": "fa-hand-sparkles", "rarity": "epic"},
        {"name": "😋 Yum", "id": "909037006", "icon": "fa-face-grin", "rarity": "common"},
        {"name": "💃 Happy Dancing", "id": "909037007", "icon": "fa-face-smile", "rarity": "common"},
        {"name": "🤹 Juggle", "id": "909037008", "icon": "fa-baseball", "rarity": "rare"},
        {"name": "💡 Neon Sign", "id": "909037009", "icon": "fa-lightbulb", "rarity": "epic"},
        {"name": "🐅 Beast Tease", "id": "909037010", "icon": "fa-paw", "rarity": "epic"},
        {"name": "🐉 Drachen Tear", "id": "909037011", "icon": "fa-dragon", "rarity": "legendary"},
        {"name": "👏 Clap Dance", "id": "909037012", "icon": "fa-hands-clapping", "rarity": "common"},
        {"name": "🎭 The Influencer", "id": "909038001", "icon": "fa-user-tie", "rarity": "epic"},
        {"name": "💃 Macarena", "id": "909038002", "icon": "fa-music", "rarity": "legendary"},
        {"name": "⚡ Techno Blast", "id": "909038003", "icon": "fa-bolt", "rarity": "epic"},
        {"name": "💝 Be My Valentine", "id": "909038004", "icon": "fa-heart", "rarity": "epic"},
        {"name": "😠 Angry Walk", "id": "909038005", "icon": "fa-face-angry", "rarity": "rare"},
        {"name": "🎉 Make Some Noise", "id": "909038006", "icon": "fa-volume-high", "rarity": "rare"},
        {"name": "🐊 Croco Hooray", "id": "909038008", "icon": "fa-reptile", "rarity": "epic"},
        {"name": "🦂 Scorpio Spin", "id": "909038009", "icon": "fa-scorpion", "rarity": "epic"},
        {"name": "🔥 Cinder Summon", "id": "909038010", "icon": "fa-fire", "rarity": "legendary"},
        {"name": "💃 Shall We Dance?", "id": "909038011", "icon": "fa-hand", "rarity": "rare"},
        {"name": "🔄 Achiever Flip", "id": "909038012", "icon": "fa-trophy", "rarity": "epic"},
        {"name": "🌀 Spin Master", "id": "909038013", "icon": "fa-sync", "rarity": "epic"},
    ],
    
    "NINJA_EMOTES": [
        {"name": "⚡ Thunder Breathing First Form", "id": "909041001", "icon": "fa-bolt", "rarity": "mythic"},
        {"name": "💧 Water Breathing Sixth Form", "id": "909041002", "icon": "fa-water", "rarity": "mythic"},
        {"name": "🐺 Beast Breathing Fifth Fang", "id": "909041003", "icon": "fa-paw", "rarity": "mythic"},
        {"name": "🎨 Flying Ink Sword", "id": "909041004", "icon": "fa-pen-fancy", "rarity": "legendary"},
        {"name": "🔫 Diz My Popblaster", "id": "909041005", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🎭 Dance Puppet, Dance!", "id": "909041006", "icon": "fa-puppet", "rarity": "epic"},
        {"name": "🦵 High Knees", "id": "909041007", "icon": "fa-person-running", "rarity": "rare"},
        {"name": "💀 Bony Fumes", "id": "909041008", "icon": "fa-skull", "rarity": "epic"},
        {"name": "⚡ Feel the Electricity", "id": "909041009", "icon": "fa-bolt", "rarity": "epic"},
        {"name": "🎯 Whac-A-Cotton", "id": "909041010", "icon": "fa-gamepad", "rarity": "rare"},
        {"name": "🏆 Honorable Mention", "id": "909041011", "icon": "fa-award", "rarity": "epic"},
        {"name": "👑 BR-Ranked Grandmaster", "id": "909041012", "icon": "fa-crown", "rarity": "legendary"},
        {"name": "👑 CS-Ranked Grandmaster", "id": "909041013", "icon": "fa-crown", "rarity": "legendary"},
        {"name": "👹 Monster Clubbing", "id": "909041014", "icon": "fa-club", "rarity": "epic"},
        {"name": "💃 Basudara Dance", "id": "909041015", "icon": "fa-people-group", "rarity": "rare"},
        {"name": "💎 Arrival of the Cyclone", "id": "909045001", "icon": "fa-tornado", "rarity": "legendary"},
        {"name": "🎸 Spring Rocker", "id": "909045002", "icon": "fa-guitar", "rarity": "epic"},
        {"name": "🏇 Giddy Up!", "id": "909045003", "icon": "fa-horse", "rarity": "rare"},
        {"name": "🦆 The Goosy Dance", "id": "909045004", "icon": "fa-dove", "rarity": "rare"},
        {"name": "⚓ Captain Victor", "id": "909045005", "icon": "fa-anchor", "rarity": "epic"},
        {"name": "😎 You Know I'm Good", "id": "909045006", "icon": "fa-face-smile-wink", "rarity": "rare"},
        {"name": "💃 Step Step", "id": "909045007", "icon": "fa-shoe-prints", "rarity": "common"},
        {"name": "🎉 Super Yay", "id": "909045008", "icon": "fa-face-grin-stars", "rarity": "rare"},
        {"name": "👟 Moonwalk", "id": "909045009", "icon": "fa-shoe-prints", "rarity": "legendary"},
        {"name": "🌺 A Flower Salute", "id": "909045010", "icon": "fa-flower", "rarity": "rare"},
        {"name": "🦊 Little Foxy Run", "id": "909045011", "icon": "fa-fox", "rarity": "epic"},
        {"name": "⚖️ Mr. Waggor's Seesaw", "id": "909045012", "icon": "fa-balance-scale", "rarity": "epic"},
        {"name": "🧘 Floating Meditation", "id": "909045015", "icon": "fa-om", "rarity": "legendary"},
        {"name": "💃 Naatu Naatu", "id": "909045016", "icon": "fa-music", "rarity": "epic"},
        {"name": "👑 Champion's Walk", "id": "909045017", "icon": "fa-crown", "rarity": "legendary"},
    ],
    
    "2024_EMOTES": [
        {"name": "💨 Money Rain", "id": "909042002", "icon": "fa-money-bill-wave", "rarity": "epic"},
        {"name": "❄️ Frostfire's Calling", "id": "909042003", "icon": "fa-snowflake", "rarity": "epic"},
        {"name": "👢 Stomping Foot", "id": "909042004", "icon": "fa-shoe-prints", "rarity": "rare"},
        {"name": "👉 This Way", "id": "909042005", "icon": "fa-hand-point-right", "rarity": "common"},
        {"name": "🤵 Excellent Service", "id": "909042006", "icon": "fa-bell-concierge", "rarity": "rare"},
        {"name": "🧊 Gloo Sculpture", "id": "909042007", "icon": "fa-snowman", "rarity": "legendary"},
        {"name": "🐅 Ever Seen a Real Tiger?", "id": "909042008", "icon": "fa-paw", "rarity": "epic"},
        {"name": "🎿 Celebration Schuss", "id": "909042009", "icon": "fa-person-skiing", "rarity": "epic"},
        {"name": "⛵ Dawn Voyage", "id": "909042011", "icon": "fa-sailboat", "rarity": "legendary"},
        {"name": "🏎️ Lamborghini Ride", "id": "909042012", "icon": "fa-car", "rarity": "mythic"},
        {"name": "👋 Hello! Frostfire Style", "id": "909042013", "icon": "fa-snowflake", "rarity": "epic"},
        {"name": "👐 Hand Grooves", "id": "909042016", "icon": "fa-hands", "rarity": "rare"},
        {"name": "🚽 Free Fire Toiletman", "id": "909042017", "icon": "fa-toilet", "rarity": "epic"},
        {"name": "🎭 Kemusan", "id": "909042018", "icon": "fa-mask", "rarity": "legendary"},
        {"name": "🐸 Ribbit Rider", "id": "909043001", "icon": "fa-frog", "rarity": "epic"},
        {"name": "🧘 Inner Self Mastery", "id": "909043002", "icon": "fa-om", "rarity": "legendary"},
        {"name": "💰 Emperor's Treasure Machine", "id": "909043003", "icon": "fa-coins", "rarity": "mythic"},
        {"name": "🌀 Why So Chaos?", "id": "909043004", "icon": "fa-spinner", "rarity": "epic"},
        {"name": "🍗 Huge Feast", "id": "909043005", "icon": "fa-drumstick", "rarity": "epic"},
        {"name": "🎨 Color Burst", "id": "909043006", "icon": "fa-palette", "rarity": "legendary"},
        {"name": "🐉 Dragon Swipe", "id": "909043007", "icon": "fa-dragon", "rarity": "mythic"},
        {"name": "💃 Samba", "id": "909043008", "icon": "fa-music", "rarity": "epic"},
        {"name": "⚡ Speed Summon", "id": "909043009", "icon": "fa-bolt", "rarity": "legendary"},
        {"name": "🏆 What a Match", "id": "909043010", "icon": "fa-trophy", "rarity": "epic"},
        {"name": "👫 What a Pair", "id": "909043013", "icon": "fa-people-arrows", "rarity": "rare"},
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
        "seasonal": 0,
        "ninja": 0,
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
    <title>🚀 ASHISH | ULTIMATE EMOTE PANEL</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <!-- Particle.js -->
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    
    <style>
        :root {
            --primary: #ff0055;
            --secondary: #00d4ff;
            --accent: #ffcc00;
            --success: #00ff88;
            --warning: #ffaa00;
            --danger: #ff2a6d;
            --dark: #0a0a1a;
            --darker: #050510;
            --light: #f0f0ff;
            
            --gradient-primary: linear-gradient(135deg, #ff0055 0%, #ff2a6d 100%);
            --gradient-secondary: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
            --gradient-accent: linear-gradient(135deg, #ffcc00 0%, #ff8800 100%);
            --gradient-success: linear-gradient(135deg, #00ff88 0%, #00cc66 100%);
            --gradient-dark: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: var(--darker);
            color: var(--light);
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            z-index: -1;
        }

        .container {
            max-width: 1800px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        /* ================= HEADER ================= */
        .header {
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 30px;
            background: rgba(10, 10, 26, 0.85);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            border: 2px solid rgba(255, 0, 85, 0.3);
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 50px rgba(255, 0, 85, 0.2);
            animation: glow 3s infinite alternate;
        }

        @keyframes glow {
            0% { box-shadow: 0 20px 50px rgba(255, 0, 85, 0.2); }
            100% { box-shadow: 0 20px 50px rgba(0, 212, 255, 0.3); }
        }

        .header::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #ff0055, #00d4ff, #ffcc00);
            z-index: -1;
            border-radius: 27px;
            animation: rotate 10s linear infinite;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(45deg, #ff0055, #00d4ff, #ffcc00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            text-shadow: 0 0 50px rgba(255, 0, 85, 0.5);
            animation: textGlow 2s infinite alternate;
        }

        @keyframes textGlow {
            0% { text-shadow: 0 0 30px rgba(255, 0, 85, 0.5); }
            100% { text-shadow: 0 0 60px rgba(0, 212, 255, 0.7); }
        }

        .tagline {
            font-size: 1.4rem;
            color: var(--secondary);
            margin-bottom: 25px;
            font-weight: 300;
            letter-spacing: 2px;
        }

        .stats-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--gradient-primary);
        }

        .stat-card:hover {
            transform: translateY(-5px);
            border-color: var(--secondary);
        }

        .stat-value {
            font-size: 2.5rem;
            font-weight: 800;
            font-family: 'Orbitron', sans-serif;
            color: var(--secondary);
            margin: 10px 0;
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--light);
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        /* ================= TABS ================= */
        .tabs-container {
            background: rgba(10, 10, 26, 0.85);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 25px;
            margin-bottom: 30px;
            border: 2px solid rgba(0, 212, 255, 0.2);
        }

        .tabs {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }

        .tab-btn {
            padding: 18px 30px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid transparent;
            color: var(--light);
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            font-family: 'Orbitron', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
            overflow: hidden;
            min-width: 220px;
            justify-content: center;
        }

        .tab-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-3px);
            border-color: var(--secondary);
        }

        .tab-btn.active {
            background: var(--gradient-primary);
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(255, 0, 85, 0.4);
            border-color: var(--secondary);
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.6s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .tab-content.active {
            display: block;
        }

        /* ================= QUICK SEND ================= */
        .quick-send {
            background: rgba(10, 10, 26, 0.9);
            border-radius: 25px;
            padding: 35px;
            margin-bottom: 30px;
            border: 2px solid var(--secondary);
            box-shadow: 0 15px 35px rgba(0, 212, 255, 0.2);
            position: relative;
            overflow: hidden;
        }

        .quick-send::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(45deg, #ff0055, #00d4ff, #ffcc00);
        }

        .section-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2rem;
            margin-bottom: 30px;
            background: linear-gradient(45deg, #00d4ff, #ffcc00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .input-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }

        .input-group label {
            display: block;
            margin-bottom: 12px;
            color: var(--secondary);
            font-weight: 600;
            font-size: 1.2rem;
            font-family: 'Orbitron', sans-serif;
        }

        .input-wrapper {
            position: relative;
        }

        .input-wrapper input {
            width: 100%;
            padding: 20px 60px;
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid var(--primary);
            border-radius: 15px;
            color: white;
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }

        .input-wrapper i {
            position: absolute;
            left: 25px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--secondary);
            font-size: 1.3rem;
        }

        .input-wrapper input:focus {
            outline: none;
            border-color: var(--secondary);
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.4);
        }

        /* ================= EMOTE CATEGORIES ================= */
        .category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }

        .category-box {
            background: rgba(10, 10, 26, 0.9);
            border-radius: 20px;
            padding: 25px;
            border: 2px solid;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .category-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
        }

        .category-box:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }

        .category-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }

        .category-icon {
            font-size: 2.5rem;
            width: 70px;
            height: 70px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .category-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
        }

        .emote-list {
            max-height: 400px;
            overflow-y: auto;
            padding-right: 10px;
        }

        .emote-list::-webkit-scrollbar {
            width: 8px;
        }

        .emote-list::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }

        .emote-list::-webkit-scrollbar-thumb {
            background: var(--secondary);
            border-radius: 10px;
        }

        .emote-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .emote-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(10px);
        }

        .emote-icon {
            font-size: 1.5rem;
            width: 50px;
            height: 50px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .emote-details {
            flex: 1;
        }

        .emote-name {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 5px;
        }

        .emote-id {
            font-family: monospace;
            font-size: 0.9rem;
            color: var(--light);
            opacity: 0.7;
        }

        .emote-send-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            background: var(--gradient-primary);
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Orbitron', sans-serif;
        }

        .emote-send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255, 0, 85, 0.4);
        }

        /* ================= BUTTONS ================= */
        .action-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }

        .action-btn {
            padding: 25px;
            border: none;
            border-radius: 15px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.4s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            position: relative;
            overflow: hidden;
        }

        .action-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        }

        .send-btn {
            background: var(--gradient-primary);
            color: white;
            grid-column: 1 / -1;
            padding: 30px;
            font-size: 1.5rem;
        }

        .send-btn:hover {
            box-shadow: 0 20px 40px rgba(255, 0, 85, 0.4);
        }

        /* ================= STATUS PANEL ================= */
        .status-panel {
            background: rgba(10, 10, 26, 0.9);
            border-radius: 25px;
            padding: 30px;
            margin-top: 40px;
            border: 2px solid var(--secondary);
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .status-card {
            background: rgba(0, 0, 0, 0.3);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .status-card:hover {
            transform: translateY(-5px);
            border-color: var(--secondary);
        }

        .status-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            font-weight: 900;
            margin: 15px 0;
        }

        .status-online { color: var(--success); }
        .status-offline { color: var(--danger); }
        .status-pending { color: var(--warning); }

        .commands-history {
            max-height: 400px;
            overflow-y: auto;
            margin-top: 20px;
        }

        .command-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 5px solid var(--secondary);
            animation: slideIn 0.5s ease;
        }

        /* ================= FOOTER ================= */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(10, 10, 26, 0.95);
            backdrop-filter: blur(15px);
            padding: 15px;
            border-top: 2px solid var(--primary);
            display: flex;
            justify-content: space-around;
            align-items: center;
            z-index: 1000;
        }

        .footer-item {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1rem;
        }

        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 10px var(--success);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); }
        }

        /* ================= NOTIFICATION ================= */
        .notification {
            position: fixed;
            top: 30px;
            right: 30px;
            padding: 25px 35px;
            border-radius: 15px;
            display: none;
            font-weight: bold;
            z-index: 2000;
            animation: slideInRight 0.4s ease;
            backdrop-filter: blur(10px);
            font-family: 'Orbitron', sans-serif;
            max-width: 400px;
        }

        .notification.show {
            animation: slideInRight 0.4s ease, fadeOut 0.4s ease 3.6s;
        }

        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes fadeOut {
            to { opacity: 0; }
        }

        .notification.success {
            background: rgba(0, 255, 136, 0.9);
            color: #000;
            border: 2px solid var(--success);
        }

        .notification.error {
            background: rgba(255, 42, 109, 0.9);
            color: white;
            border: 2px solid var(--danger);
        }

        /* ================= RESPONSIVE ================= */
        @media (max-width: 1200px) {
            .category-grid { grid-template-columns: 1fr; }
        }

        @media (max-width: 768px) {
            .logo { font-size: 3rem; }
            .tabs { flex-direction: column; }
            .tab-btn { width: 100%; }
            .footer { flex-direction: column; gap: 10px; }
            .stats-bar { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <!-- Particle.js Container -->
    <div id="particles-js"></div>
    
    <!-- Notification -->
    <div class="notification" id="notification"></div>

    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <div class="logo">
                <i class="fas fa-fire"></i> ASHISH ULTIMATE PANEL
            </div>
            <div class="tagline">⚡ Premium Emote Delivery System | 400+ Emotes Available</div>
            
            <div class="stats-bar">
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
                <i class="fas fa-bolt"></i> INSTANT EMOTE ATTACK
            </h2>
            
            <div class="input-grid">
                <div class="input-group">
                    <label><i class="fas fa-users"></i> TEAM CODE</label>
                    <div class="input-wrapper">
                        <i class="fas fa-hashtag"></i>
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
                        <i class="fas fa-magic"></i>
                        <input type="text" id="emoteId" placeholder="909033001" pattern="\d{9}" required>
                    </div>
                </div>
            </div>

            <div class="action-buttons">
                <button class="action-btn send-btn" onclick="sendQuickCommand()">
                    <i class="fas fa-rocket"></i> LAUNCH EMOTE ATTACK
                </button>
            </div>
        </div>

        <!-- TABS -->
        <div class="tabs-container">
            <div class="tabs">
                <button class="tab-btn active" onclick="openTab('evo')">
                    <i class="fas fa-gun"></i> EVO GUNS
                </button>
                <button class="tab-btn" onclick="openTab('special')">
                    <i class="fas fa-star"></i> SPECIAL
                </button>
                <button class="tab-btn" onclick="openTab('popular')">
                    <i class="fas fa-fire"></i> POPULAR
                </button>
                <button class="tab-btn" onclick="openTab('dance')">
                    <i class="fas fa-music"></i> DANCE
                </button>
                <button class="tab-btn" onclick="openTab('seasonal')">
                    <i class="fas fa-calendar"></i> SEASONAL
                </button>
                <button class="tab-btn" onclick="openTab('ninja')">
                    <i class="fas fa-user-ninja"></i> NINJA
                </button>
                <button class="tab-btn" onclick="openTab('new')">
                    <i class="fas fa-gem"></i> NEW 2024
                </button>
            </div>

            <!-- EVO GUNS TAB -->
            <div id="evo" class="tab-content active">
                <div class="category-grid">
                    <div class="category-box" style="border-color: #ff0055;">
                        <div class="category-header">
                            <div class="category-icon" style="background: var(--gradient-primary);">
                                <i class="fas fa-gun"></i>
                            </div>
                            <h3 class="category-title">EVO GUN EMOTES</h3>
                        </div>
                        <div class="emote-list">
                            {% for emote in evo_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon" style="background: rgba(255, 0, 85, 0.2);">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', event)">
                                    SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- SPECIAL EMOTES TAB -->
            <div id="special" class="tab-content">
                <div class="category-grid">
                    <div class="category-box" style="border-color: #00d4ff;">
                        <div class="category-header">
                            <div class="category-icon" style="background: var(--gradient-secondary);">
                                <i class="fas fa-star"></i>
                            </div>
                            <h3 class="category-title">SPECIAL EMOTES</h3>
                        </div>
                        <div class="emote-list">
                            {% for emote in special_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon" style="background: rgba(0, 212, 255, 0.2);">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', event)">
                                    SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- POPULAR EMOTES TAB -->
            <div id="popular" class="tab-content">
                <div class="category-grid">
                    <div class="category-box" style="border-color: #ffcc00;">
                        <div class="category-header">
                            <div class="category-icon" style="background: var(--gradient-accent);">
                                <i class="fas fa-fire"></i>
                            </div>
                            <h3 class="category-title">POPULAR EMOTES</h3>
                        </div>
                        <div class="emote-list">
                            {% for emote in popular_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon" style="background: rgba(255, 204, 0, 0.2);">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', event)">
                                    SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- DANCE EMOTES TAB -->
            <div id="dance" class="tab-content">
                <div class="category-grid">
                    <div class="category-box" style="border-color: #00ff88;">
                        <div class="category-header">
                            <div class="category-icon" style="background: var(--gradient-success);">
                                <i class="fas fa-music"></i>
                            </div>
                            <h3 class="category-title">DANCE EMOTES</h3>
                        </div>
                        <div class="emote-list">
                            {% for emote in dance_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon" style="background: rgba(0, 255, 136, 0.2);">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', event)">
                                    SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- SEASONAL EMOTES TAB -->
            <div id="seasonal" class="tab-content">
                <div class="category-grid">
                    <div class="category-box" style="border-color: #9d4edd;">
                        <div class="category-header">
                            <div class="category-icon" style="background: linear-gradient(135deg, #9d4edd, #560bad);">
                                <i class="fas fa-calendar"></i>
                            </div>
                            <h3 class="category-title">SEASONAL EMOTES</h3>
                        </div>
                        <div class="emote-list">
                            {% for emote in seasonal_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon" style="background: rgba(157, 78, 221, 0.2);">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', event)">
                                    SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- NINJA EMOTES TAB -->
            <div id="ninja" class="tab-content">
                <div class="category-grid">
                    <div class="category-box" style="border-color: #ff2a6d;">
                        <div class="category-header">
                            <div class="category-icon" style="background: linear-gradient(135deg, #ff2a6d, #ff0055);">
                                <i class="fas fa-user-ninja"></i>
                            </div>
                            <h3 class="category-title">NINJA EMOTES</h3>
                        </div>
                        <div class="emote-list">
                            {% for emote in ninja_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon" style="background: rgba(255, 42, 109, 0.2);">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', event)">
                                    SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- NEW 2024 EMOTES TAB -->
            <div id="new" class="tab-content">
                <div class="category-grid">
                    <div class="category-box" style="border-color: #00d4ff;">
                        <div class="category-header">
                            <div class="category-icon" style="background: linear-gradient(135deg, #00d4ff, #0099ff);">
                                <i class="fas fa-gem"></i>
                            </div>
                            <h3 class="category-title">NEW 2024 EMOTES</h3>
                        </div>
                        <div class="emote-list">
                            {% for emote in new_2024_emotes %}
                            <div class="emote-item" onclick="useEmote('{{ emote.id }}', '{{ emote.name }}')">
                                <div class="emote-icon" style="background: rgba(0, 212, 255, 0.2);">
                                    <i class="fas {{ emote.icon }}"></i>
                                </div>
                                <div class="emote-details">
                                    <div class="emote-name">{{ emote.name }}</div>
                                    <div class="emote-id">ID: {{ emote.id }}</div>
                                </div>
                                <button class="emote-send-btn" onclick="sendEmote('{{ emote.id }}', event)">
                                    SEND
                                </button>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <div class="footer">
        <div class="footer-item">
            <div class="status-indicator"></div>
            <span>PANEL: <span style="color: #00ff88;">ONLINE</span></span>
        </div>
        <div class="footer-item">
            <i class="fas fa-robot"></i>
            <span>EMOTES: <span id="emoteCount">{{ total_emotes }}</span></span>
        </div>
        <div class="footer-item">
            <i class="fas fa-user-ninja"></i>
            <span>DEVELOPER: ASHISH</span>
        </div>
        <div class="footer-item">
            <i class="fab fa-instagram"></i>
            <span>@ashish.shakya0001</span>
        </div>
        <div class="footer-item">
            <i class="fas fa-bolt"></i>
            <span>VERSION: ULTIMATE 4.0</span>
        </div>
    </div>

    <script>
        // Initialize particles.js
        particlesJS("particles-js", {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: ["#ff0055", "#00d4ff", "#ffcc00", "#00ff88"] },
                shape: { type: "circle" },
                opacity: { value: 0.5, random: true },
                size: { value: 3, random: true },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: "#ffffff",
                    opacity: 0.1,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 2,
                    direction: "none",
                    random: true,
                    straight: false,
                    out_mode: "out",
                    bounce: false
                }
            },
            interactivity: {
                detect_on: "canvas",
                events: {
                    onhover: { enable: true, mode: "repulse" },
                    onclick: { enable: true, mode: "push" }
                }
            }
        });

        // Global variables
        let commandsSent = 0;
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('teamCode').value = '1234567';
            document.getElementById('targetUid').value = '13706108657';
            document.getElementById('emoteId').value = '909033001';
            
            updateStats();
            setInterval(updateStats, 5000);
        });
        
        // Tab system
        function openTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        // Emote functions
        function useEmote(emoteId, emoteName) {
            document.getElementById('emoteId').value = emoteId;
            showNotification(`✅ ${emoteName} selected!`, 'success');
        }
        
        function sendEmote(emoteId, event) {
            if (event) event.stopPropagation();
            
            const team = document.getElementById('teamCode').value;
            const target = document.getElementById('targetUid').value;
            
            if (!team || !target) {
                showNotification('❌ Enter Team Code and Target UID first!', 'error');
                return;
            }
            
            sendCommand(team, emoteId, target);
        }
        
        function sendQuickCommand() {
            const team = document.getElementById('teamCode').value;
            const target = document.getElementById('targetUid').value;
            const emote = document.getElementById('emoteId').value;
            
            if (!team || !target || !emote) {
                showNotification('❌ Fill all fields!', 'error');
                return;
            }
            
            sendCommand(team, emote, target);
        }
        
        // Send command
        function sendCommand(team, emote, target) {
            const startTime = Date.now();
            const btn = document.querySelector('.send-btn');
            const originalText = btn.innerHTML;
            
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> SENDING...';
            btn.disabled = true;
            
            fetch('/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `team_code=${team}&emote_id=${emote}&target_uid=${target}`
            })
            .then(response => {
                const time = Date.now() - startTime;
                document.getElementById('responseTime').textContent = `${time}ms`;
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    commandsSent++;
                    document.getElementById('commandsSent').textContent = commandsSent;
                    showNotification(`🚀 Emote sent to UID ${target}!`, 'success');
                } else {
                    showNotification(`❌ Error: ${data.error}`, 'error');
                }
            })
            .catch(() => {
                showNotification('❌ Network error!', 'error');
            })
            .finally(() => {
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.disabled = false;
                }, 1000);
            });
        }
        
        // Stats update
        function updateStats() {
            fetch('/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('commandsSent').textContent = data.total_commands;
                    document.getElementById('onlineUsers').textContent = data.bot_connected ? '2' : '1';
                });
        }
        
        // Notification system
        function showNotification(message, type) {
            const notif = document.getElementById('notification');
            notif.textContent = message;
            notif.className = `notification ${type}`;
            notif.style.display = 'block';
            notif.classList.add('show');
            
            setTimeout(() => {
                notif.classList.remove('show');
                setTimeout(() => {
                    notif.style.display = 'none';
                }, 400);
            }, 4000);
        }
        
        // Random emote highlight
        setInterval(() => {
            const items = document.querySelectorAll('.emote-item');
            if (items.length > 0) {
                const item = items[Math.floor(Math.random() * items.length)];
                item.style.boxShadow = '0 0 20px rgba(0, 212, 255, 0.5)';
                setTimeout(() => {
                    item.style.boxShadow = '';
                }, 1000);
            }
        }, 3000);
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
        seasonal_emotes=EMOTE_DATABASE["SEASONAL_EMOTES"],
        ninja_emotes=EMOTE_DATABASE["NINJA_EMOTES"],
        new_2024_emotes=EMOTE_DATABASE["2024_EMOTES"],
        total_emotes=TOTAL_EMOTES
    )

@app.route('/send', methods=['POST'])
def send_command():
    try:
        team_code = request.form.get('team_code', '').strip()
        emote_id = request.form.get('emote_id', '').strip()
        target_uid = request.form.get('target_uid', '').strip()
        
        print(f"🚀 Command: Team={team_code}, Emote={emote_id}, Target={target_uid}")
        
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
                "message": f"Command #{command_id} queued!",
                "command_id": command_id
            })
        else:
            return jsonify({"success": False, "error": "Server error"})
            
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
        "stats": command_storage["stats"]
    })

# ==================== MAIN ====================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 ASHISH ULTIMATE EMOTE PANEL starting on port {port}")
    print(f"🎮 Total Emotes: {TOTAL_EMOTES}")
    print(f"🔥 Categories: {len(EMOTE_DATABASE)}")
    print(f"📱 Access: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)