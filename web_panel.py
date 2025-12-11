# web_panel.py
from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import json
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ashish-premium-panel-2024')

# ==================== COMPLETE EMOTE DATABASE ====================
EMOTE_CATEGORIES = {
    "EVO_GUNS": [
        {"name": "🔥 EVO M4A1 MAX", "id": "909033001", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO AK47 MAX", "id": "909000063", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO SHOTGUN MAX", "id": "909035007", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO SCAR MAX", "id": "909000068", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO XMB MAX", "id": "909000065", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO MP40 MAX", "id": "909000075", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO UMP MAX", "id": "909000098", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO WOODPECKER MAX", "id": "909042008", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO M10 MAX", "id": "909000081", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO FAMAS MAX", "id": "909000090", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "🔥 EVO MP5 MAX", "id": "909033002", "icon": "fa-gun", "rarity": "epic"},
        {"name": "🔥 EVO M1887 MAX", "id": "909035007", "icon": "fa-gun", "rarity": "legendary"},
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
        {"name": "🔥 FIRE ON EMOTE", "id": "909033001", "icon": "fa-fire", "rarity": "epic"},
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
        {"name": "🎯 LEVEL 100", "id": "909042007", "icon": "fa-trophy", "rarity": "mythic"},
        {"name": "🐉 DRAGON'S SOUL", "id": "909000081", "icon": "fa-dragon", "rarity": "legendary"},
    ],
    
    "BASIC_EMOTES": [
        {"name": "👋 HELLO!", "id": "909000001", "icon": "fa-hand-wave", "rarity": "common"},
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
        {"name": "💥 FURIOUS SLAM", "id": "909000021", "icon": "fa-explosion", "rarity": "epic"},
        {"name": "🌙 MOON FLIP", "id": "909000022", "icon": "fa-moon", "rarity": "rare"},
        {"name": "🚶 WIGGLE WALK", "id": "909000023", "icon": "fa-walking", "rarity": "common"},
        {"name": "⚔️ BATTLE DANCE", "id": "909000024", "icon": "fa-swords", "rarity": "epic"},
        {"name": "🤝 HIGH FIVE", "id": "909000025", "icon": "fa-handshake", "rarity": "common"},
        {"name": "🎉 SHAKE IT UP", "id": "909000026", "icon": "fa-glass-cheers", "rarity": "common"},
        {"name": "🌀 GLORIOUS SPIN", "id": "909000027", "icon": "fa-sync", "rarity": "rare"},
        {"name": "🦢 CRANE KICK", "id": "909000028", "icon": "fa-kiwi-bird", "rarity": "rare"},
        {"name": "🎉 PARTY DANCE", "id": "909000029", "icon": "fa-party-horn", "rarity": "common"},
        {"name": "💃 JIG DANCE", "id": "909000031", "icon": "fa-music", "rarity": "common"},
        {"name": "📸 SELFIE", "id": "909000032", "icon": "fa-camera", "rarity": "common"},
        {"name": "💫 SOUL SHAKING", "id": "909000033", "icon": "fa-star", "rarity": "rare"},
        {"name": "🏴‍☠️ PIRATE'S FLAG", "id": "909000034", "icon": "fa-flag", "rarity": "epic"},
        {"name": "💖 HEALING DANCE", "id": "909000035", "icon": "fa-heart-pulse", "rarity": "rare"},
        {"name": "🎧 TOP DJ", "id": "909000036", "icon": "fa-headphones", "rarity": "epic"},
        {"name": "😡 DEATH GLARE", "id": "909000037", "icon": "fa-eye", "rarity": "rare"},
        {"name": "💰 POWER OF MONEY", "id": "909000038", "icon": "fa-money-bill", "rarity": "epic"},
        {"name": "💨 EAT MY DUST", "id": "909000039", "icon": "fa-wind", "rarity": "rare"},
        {"name": "💃 BREAKDANCE", "id": "909000040", "icon": "fa-person-burst", "rarity": "epic"},
        {"name": "🥋 KUNGFU", "id": "909000041", "icon": "fa-user-ninja", "rarity": "common"},
        {"name": "🍽️ BON APPETIT", "id": "909000042", "icon": "fa-utensils", "rarity": "common"},
        {"name": "🎯 AIM; FIRE!", "id": "909000043", "icon": "fa-crosshairs", "rarity": "common"},
        {"name": "🦢 THE SWAN", "id": "909000044", "icon": "fa-dove", "rarity": "rare"},
        {"name": "💖 I HEART YOU", "id": "909000045", "icon": "fa-heart", "rarity": "rare"},
        {"name": "☕ TEA TIME", "id": "909000046", "icon": "fa-mug-hot", "rarity": "common"},
        {"name": "🥊 BRING IT ON!", "id": "909000047", "icon": "fa-boxing-glove", "rarity": "common"},
        {"name": "🤷 WHY? OH WHY?", "id": "909000048", "icon": "fa-question", "rarity": "common"},
        {"name": "👌 FANCY HANDS", "id": "909000049", "icon": "fa-hand-sparkles", "rarity": "rare"},
        {"name": "💃 SHIMMY", "id": "909000051", "icon": "fa-person-dots-from-line", "rarity": "common"},
        {"name": "🐶 DOGGIE", "id": "909000052", "icon": "fa-dog", "rarity": "common"},
        {"name": "⚔️ CHALLENGE ON!", "id": "909000053", "icon": "fa-flag-checkered", "rarity": "common"},
        {"name": "🤠 LASSO", "id": "909000054", "icon": "fa-lasso", "rarity": "rare"},
        {"name": "💰 I'M RICH!", "id": "909000055", "icon": "fa-money-check", "rarity": "epic"},
    ],
    
    "PARTY_GAME": [
        {"name": "🎮 PARTY GAME 5", "id": "909000100", "icon": "fa-gamepad", "rarity": "common"},
        {"name": "🎮 PARTY GAME 6", "id": "909000101", "icon": "fa-gamepad", "rarity": "common"},
        {"name": "🎮 PARTY GAME 3", "id": "909000102", "icon": "fa-gamepad", "rarity": "common"},
        {"name": "🎮 PARTY GAME 4", "id": "909000103", "icon": "fa-gamepad", "rarity": "common"},
        {"name": "🎮 PARTY GAME 7", "id": "909000104", "icon": "fa-gamepad", "rarity": "common"},
        {"name": "🎮 PARTY GAME 1", "id": "909000105", "icon": "fa-gamepad", "rarity": "common"},
        {"name": "🎮 PARTY GAME 8", "id": "909000106", "icon": "fa-gamepad", "rarity": "common"},
        {"name": "🎮 PARTY GAME 2", "id": "909000107", "icon": "fa-gamepad", "rarity": "common"},
    ],
    
    "GREETING": [
        {"name": "👋 GREETING SPECIAL 1", "id": "909000108", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 2", "id": "909000109", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 3", "id": "909000110", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 4", "id": "909000111", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 5", "id": "909000112", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 6", "id": "909000113", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 7", "id": "909000114", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 8", "id": "909000115", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 9", "id": "909000116", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 10", "id": "909000117", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 11", "id": "909000118", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 12", "id": "909000119", "icon": "fa-hand", "rarity": "common"},
        {"name": "👋 GREETING SPECIAL 13", "id": "909000120", "icon": "fa-hand", "rarity": "common"},
    ],
    
    "EXTRA_SPECIAL": [
        {"name": "🏀 DRIBBLE KING", "id": "909000121", "icon": "fa-basketball", "rarity": "epic"},
        {"name": "🎸 FFWS 2021 GUITAR", "id": "909000122", "icon": "fa-guitar", "rarity": "legendary"},
        {"name": "🧠 MIND IT!", "id": "909000123", "icon": "fa-brain", "rarity": "rare"},
        {"name": "🌟 GOLDEN COMBO", "id": "909000124", "icon": "fa-star", "rarity": "epic"},
        {"name": "🤒 SICK MOVES", "id": "909000125", "icon": "fa-head-side-virus", "rarity": "rare"},
        {"name": "🎤 RAP SWAG", "id": "909000126", "icon": "fa-microphone", "rarity": "epic"},
        {"name": "💃 BATTLE IN STYLE", "id": "909000127", "icon": "fa-sword", "rarity": "epic"},
        {"name": "🏴‍☠️ RULER'S FLAG", "id": "909000128", "icon": "fa-flag", "rarity": "epic"},
        {"name": "💸 MONEY THROW", "id": "909000129", "icon": "fa-money-bill-wave", "rarity": "epic"},
        {"name": "🔫 ENDLESS BULLETS", "id": "909000130", "icon": "fa-gun", "rarity": "legendary"},
        {"name": "💃 SMOOTH SWAY", "id": "909000131", "icon": "fa-music", "rarity": "rare"},
        {"name": "🥇 NUMBER 1", "id": "909000132", "icon": "fa-trophy", "rarity": "common"},
        {"name": "🔥 FIRE SLAM", "id": "909000133", "icon": "fa-fire", "rarity": "epic"},
        {"name": "💔 HEARTBROKEN", "id": "909000134", "icon": "fa-heart-crack", "rarity": "rare"},
        {"name": "✊ ROCK PAPER SCISSORS", "id": "909000135", "icon": "fa-hand", "rarity": "common"},
        {"name": "💔 SHATTERED REALITY", "id": "909000136", "icon": "fa-shattered-glass", "rarity": "epic"},
        {"name": "😇 HALO OF MUSIC", "id": "909000137", "icon": "fa-music", "rarity": "rare"},
        {"name": "🍖 BURNT BBQ", "id": "909000138", "icon": "fa-drumstick-bite", "rarity": "rare"},
        {"name": "👣 SWITCHING STEPS", "id": "909000139", "icon": "fa-shoe-prints", "rarity": "common"},
        {"name": "⚔️ CREED SLAY", "id": "909000140", "icon": "fa-cross", "rarity": "epic"},
        {"name": "😅 LEAP OF FAIL", "id": "909000141", "icon": "fa-face-grin-tongue", "rarity": "rare"},
        {"name": "🎶 RHYTHM GIRL", "id": "909000142", "icon": "fa-music", "rarity": "epic"},
        {"name": "🚁 HELICOPTER SHOT", "id": "909000143", "icon": "fa-helicopter", "rarity": "legendary"},
        {"name": "🐅 KUNGFU TIGERS", "id": "909000144", "icon": "fa-paw", "rarity": "epic"},
        {"name": "👹 POSSESSED WARRIOR", "id": "909000145", "icon": "fa-ghost", "rarity": "legendary"},
        {"name": "👍 RAISE YOUR THUMB!", "id": "909000150", "icon": "fa-thumbs-up", "rarity": "common"},
    ],
    
    "FIREBORN_SERIES": [
        {"name": "🔥 FIREBORN", "id": "909033001", "icon": "fa-fire", "rarity": "legendary"},
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
        {"name": "🔄 REANIMATION JUTSU", "id": "909050002", "icon": "fa-yin-yang", "rarity": "mythic"},
        {"name": "⚔️ THE FINAL BATTLE", "id": "909050003", "icon": "fa-sword", "rarity": "mythic"},
        {"name": "👆 FOREHEAD POKE", "id": "909050004", "icon": "fa-hand-point-up", "rarity": "epic"},
        {"name": "🔥 FIREBALL JUTSU", "id": "909050005", "icon": "fa-fire", "rarity": "mythic"},
        {"name": "⚡ FLYING RAIJIN", "id": "909050006", "icon": "fa-bolt", "rarity": "mythic"},
        {"name": "🔨 HAMMER SLAM", "id": "909050008", "icon": "fa-hammer", "rarity": "epic"},
        {"name": "💍 THE RINGS", "id": "909050009", "icon": "fa-ring", "rarity": "epic"},
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
        {"name": "🎬 SHOLAY", "id": "909050020", "icon": "fa-film", "rarity": "legendary"},
        {"name": "⛰️ PEAK POINTS", "id": "909050021", "icon": "fa-mountain", "rarity": "epic"},
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
    ],
    
    "MORE_PRACTICE": [
        {"name": "🎯 MORE PRACTICE", "id": "909000079", "icon": "fa-bullseye", "rarity": "rare"},
        {"name": "🏆 FFWS 2021", "id": "909000080", "icon": "fa-trophy", "rarity": "legendary"},
        {"name": "🐉 DRACO'S SOUL", "id": "909000081", "icon": "fa-dragon", "rarity": "mythic"},
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

# Combine all emotes
ALL_EMOTES = []
for category in EMOTE_CATEGORIES.values():
    ALL_EMOTES.extend(category)

print(f"✅ Total Emotes Loaded: {len(ALL_EMOTES)}")

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

# ==================== HTML TEMPLATE (MAIN.PY UI) ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🔥 ASHISH EMOTE PANEL v2.0</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #ff0000;
            --secondary: #00ff00;
            --accent: #00ffff;
            --dark: #0a0a0a;
            --darker: #050505;
            --gradient: linear-gradient(135deg, #ff0000 0%, #ff00ff 50%, #00ffff 100%);
            --card-bg: rgba(20, 20, 20, 0.7);
            --glass: rgba(255, 255, 255, 0.05);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: var(--dark);
            color: #fff;
            min-height: 100vh;
            height: 100vh;
            overflow-y: auto;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 0, 0, 0.05) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(0, 255, 255, 0.05) 0%, transparent 20%);
            overflow-x: hidden;
        }

        .container {
            max-width: 1100px;
            margin: 20px auto;
            padding: 20px;
            padding-bottom: 100px !important; 
            min-height: 120vh; 
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
            border: 1px solid rgba(255, 0, 0, 0.3);
            box-shadow: 0 10px 30px rgba(255, 0, 0, 0.2),
                        inset 0 1px 0 rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: var(--gradient);
            opacity: 0.1;
            animation: rotate 20s linear infinite;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .header h1 {
            font-size: 3rem;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-shadow: 0 0 30px rgba(255, 0, 255, 0.5);
            position: relative;
            letter-spacing: 2px;
        }

        .header h2 {
            color: var(--accent);
            font-size: 1.2rem;
            opacity: 0.9;
            font-weight: 300;
            position: relative;
        }

        .section {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .section:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(255, 0, 0, 0.2);
        }

        .section h3 {
            color: var(--secondary);
            margin-bottom: 20px;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section h3 i {
            color: var(--accent);
        }

        .input-group {
            margin-bottom: 20px;
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
            padding: 15px;
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid var(--primary);
            border-radius: 10px;
            color: white;
            font-size: 16px;
            transition: all 0.3s ease;
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
            transition: all 0.3s ease;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }

        .btn:hover::before {
            left: 100%;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(255, 0, 0, 0.4);
        }

        .btn:active {
            transform: translateY(0);
        }

        /* EVO GUN SECTION */
        .evo-section {
            background: linear-gradient(135deg, rgba(255, 0, 0, 0.1), rgba(0, 0, 0, 0.8));
            border: 2px solid var(--primary);
        }

        .evo-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .evo-btn {
            background: linear-gradient(135deg, #ff0000, #ff5500);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .evo-btn::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .evo-btn:hover::after {
            opacity: 1;
        }

        .evo-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(255, 0, 0, 0.3);
        }

        .select-all-btn {
            background: linear-gradient(135deg, #00ff00, #00cc00);
            grid-column: 1 / -1;
            padding: 20px;
            font-size: 1.2rem;
            margin-top: 10px;
        }

        /* Emotes Grid */
        .emotes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .emote-card {
            background: rgba(30, 30, 30, 0.8);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .emote-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--gradient);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .emote-card:hover::before {
            opacity: 1;
        }

        .emote-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            border-color: var(--primary);
        }

        .emote-name {
            color: #ffcc00;
            font-size: 1.3rem;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .emote-id {
            color: var(--accent);
            background: rgba(0, 0, 0, 0.5);
            padding: 8px 12px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-family: monospace;
            font-size: 0.9rem;
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
            transition: all 0.3s ease;
        }

        .send-btn:hover {
            background: linear-gradient(135deg, #00ff88, #00ff00);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 255, 0, 0.3);
        }

        /* Status Bar */
        .status-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(10, 10, 10, 0.95);
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 2px solid var(--primary);
            backdrop-filter: blur(10px);
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

        /* Notification */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 20px;
            border-radius: 10px;
            display: none;
            font-weight: bold;
            z-index: 2000;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            animation: slideIn 0.3s ease;
            max-width: 400px;
        }

        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .notification.success {
            background: linear-gradient(135deg, rgba(0, 255, 0, 0.9), rgba(0, 200, 0, 0.9));
            color: #000;
        }

        .notification.error {
            background: linear-gradient(135deg, rgba(255, 0, 0, 0.9), rgba(200, 0, 0, 0.9));
            color: white;
        }

        .notification.warning {
            background: linear-gradient(135deg, rgba(255, 255, 0, 0.9), rgba(200, 200, 0, 0.9));
            color: #000;
        }

        /* Progress Bar */
        .progress-bar {
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
            overflow: hidden;
            margin-top: 10px;
        }

        .progress-fill {
            height: 100%;
            background: var(--gradient);
            width: 0%;
            transition: width 0.3s ease;
        }

        /* TCP Status */
        .tcp-status {
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.8);
            padding: 10px 15px;
            border-radius: 10px;
            border: 2px solid var(--primary);
            z-index: 1000;
            backdrop-filter: blur(5px);
        }

        .tcp-connected {
            color: #00ff00;
            font-weight: bold;
        }

        .tcp-disconnected {
            color: #ff0000;
            font-weight: bold;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 10px;
                margin: 10px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .emotes-grid {
                grid-template-columns: 1fr;
            }
            
            .evo-buttons {
                grid-template-columns: 1fr;
            }
            
            .status-bar {
                flex-direction: column;
                gap: 10px;
                padding: 10px;
                text-align: center;
            }
            
            .tcp-status {
                position: relative;
                top: 0;
                left: 0;
                margin-bottom: 20px;
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="tcp-status" id="tcpStatus">
        <i class="fas fa-plug"></i> TCP: <span class="tcp-connected" id="tcpConnStatus">CONNECTING...</span>
    </div>
    
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-fire"></i> ASHISH EMOTE PANEL v3.0</h1>
            <h2>Premium Emote Sending System | {{ total_emotes }} Emotes Available</h2>
        </div>
        
        <div class="section">
            <h3><i class="fas fa-users"></i> TEAM INFORMATION</h3>
            <div class="input-group">
                <label>TEAM CODE (7 digits)</label>
                <input type="text" id="team_code" placeholder="Enter 7-digit team code" 
                       pattern="[0-9]{7}" title="7 digit team code" value="1234567">
            </div>
            
            <h3><i class="fas fa-user"></i> TARGET PLAYER UID</h3>
            <div class="input-group">
                <label>TARGET UID (Required)</label>
                <input type="text" id="target_uid" placeholder="Enter target UID (8-11 digits)" 
                       pattern="[0-9]{8,11}" title="8-11 digits" value="13706108657">
            </div>
            
            <button type="button" class="btn" onclick="sendQuickCommand()">
                <i class="fas fa-bolt"></i> SEND EMOTE ATTACK
            </button>
        </div>
        
        <!-- EVO GUN SECTION -->
        <div class="section evo-section">
            <h3><i class="fas fa-gun"></i> 🎯 EVO GUN EMOTES ({{ evo_count }})</h3>
            <p style="color: #aaa; margin-bottom: 15px;">Select EVO gun emotes to send instantly via TCP</p>
            
            <div class="evo-buttons">
                <button type="button" class="evo-btn select-all-btn" onclick="selectAllEvo()">
                    <i class="fas fa-check-double"></i> SELECT ALL EVO GUNS
                </button>
                
                {% for emote in evo_emotes %}
                <button type="button" class="evo-btn" onclick="sendEvoEmote('{{ emote.id }}', '{{ emote.name }}')">
                    <i class="fas {{ emote.icon }}"></i> {{ emote.name }}
                </button>
                {% endfor %}
            </div>
        </div>

        <!-- SPECIAL EMOTES SECTION -->
        <div class="section" style="background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 0, 0, 0.8)); border: 2px solid #00ffff;">
            <h3><i class="fas fa-star"></i> SPECIAL & POPULAR EMOTES ({{ special_count }})</h3>
            <div class="emotes-grid">
                {% for emote in special_emotes %}
                <div class="emote-card">
                    <div class="emote-name">
                        <i class="fas {{ emote.icon }}"></i> {{ emote.name }}
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <button type="button" class="send-btn" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <i class="fas fa-paper-plane"></i> SEND EMOTE
                    </button>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- BASIC EMOTES SECTION -->
        <div class="section" style="background: linear-gradient(135deg, rgba(157, 78, 221, 0.1), rgba(0, 0, 0, 0.8)); border: 2px solid #9d4edd;">
            <h3><i class="fas fa-gamepad"></i> BASIC EMOTES ({{ basic_count }})</h3>
            <div class="emotes-grid">
                {% for emote in basic_emotes %}
                <div class="emote-card">
                    <div class="emote-name">
                        <i class="fas {{ emote.icon }}"></i> {{ emote.name }}
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <button type="button" class="send-btn" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <i class="fas fa-paper-plane"></i> SEND EMOTE
                    </button>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- MORE PRACTICE SECTION -->
        <div class="section" style="background: linear-gradient(135deg, rgba(255, 140, 0, 0.1), rgba(0, 0, 0, 0.8)); border: 2px solid #ff8c00;">
            <h3><i class="fas fa-trophy"></i> MORE PRACTICE SERIES ({{ more_practice_count }})</h3>
            <div class="emotes-grid">
                {% for emote in more_practice_emotes %}
                <div class="emote-card">
                    <div class="emote-name">
                        <i class="fas {{ emote.icon }}"></i> {{ emote.name }}
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <button type="button" class="send-btn" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <i class="fas fa-paper-plane"></i> SEND EMOTE
                    </button>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- FIREBORN SERIES -->
        <div class="section" style="background: linear-gradient(135deg, rgba(255, 69, 0, 0.1), rgba(0, 0, 0, 0.8)); border: 2px solid #ff4500;">
            <h3><i class="fas fa-fire"></i> FIREBORN SERIES ({{ fireborn_count }})</h3>
            <div class="emotes-grid">
                {% for emote in fireborn_emotes %}
                <div class="emote-card">
                    <div class="emote-name">
                        <i class="fas {{ emote.icon }}"></i> {{ emote.name }}
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <button type="button" class="send-btn" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <i class="fas fa-paper-plane"></i> SEND EMOTE
                    </button>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- NINJA SERIES -->
        <div class="section" style="background: linear-gradient(135deg, rgba(128, 0, 128, 0.1), rgba(0, 0, 0, 0.8)); border: 2px solid #800080;">
            <h3><i class="fas fa-user-ninja"></i> NINJA SERIES ({{ ninja_count }})</h3>
            <div class="emotes-grid">
                {% for emote in ninja_emotes %}
                <div class="emote-card">
                    <div class="emote-name">
                        <i class="fas {{ emote.icon }}"></i> {{ emote.name }}
                    </div>
                    <div class="emote-id">ID: {{ emote.id }}</div>
                    <button type="button" class="send-btn" onclick="sendEmote('{{ emote.id }}', '{{ emote.name }}')">
                        <i class="fas fa-paper-plane"></i> SEND EMOTE
                    </button>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <div class="status-bar">
        <div class="status-item">
            <div class="status-dot"></div>
            <span>Status: <span id="status">ONLINE</span></span>
        </div>
        <div class="status-item">
            <i class="fas fa-bolt"></i>
            <span>Commands: <span id="count">0</span></span>
        </div>
        <div class="status-item">
            <i class="fas fa-plug"></i>
            <span>TCP: <span id="tcpConn">CONNECTED</span></span>
        </div>
        <div class="status-item">
            <i class="fas fa-fire"></i>
            <span>Emotes: {{ total_emotes }}</span>
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
        let commandCount = 0;
        let progressInterval;
        let tcpConnected = true;
        
        function updateTCPStatus(connected) {
            tcpConnected = connected;
            const statusElem = document.getElementById('tcpConnStatus');
            const connElem = document.getElementById('tcpConn');
            
            if (connected) {
                statusElem.className = 'tcp-connected';
                statusElem.textContent = 'CONNECTED';
                connElem.textContent = 'CONNECTED';
                connElem.style.color = '#00ff00';
            } else {
                statusElem.className = 'tcp-disconnected';
                statusElem.textContent = 'DISCONNECTED';
                connElem.textContent = 'DISCONNECTED';
                connElem.style.color = '#ff0000';
            }
        }
        
        function showNotification(message, type = 'success') {
            const notif = document.getElementById('notification');
            notif.textContent = message;
            notif.className = `notification ${type}`;
            notif.style.display = 'block';
            
            setTimeout(() => {
                notif.style.display = 'none';
            }, 4000);
        }
        
        function updateStatus() {
            document.getElementById('count').textContent = commandCount;
        }
        
        function startProgress() {
            const progressFill = document.createElement('div');
            progressFill.className = 'progress-fill';
            progressFill.id = 'progressFill';
            document.querySelector('.progress-bar')?.remove();
            
            const progressBar = document.createElement('div');
            progressBar.className = 'progress-bar';
            progressBar.appendChild(progressFill);
            
            const evoSection = document.querySelector('.evo-section');
            if (evoSection) {
                evoSection.appendChild(progressBar);
            }
            
            let width = 0;
            clearInterval(progressInterval);
            progressInterval = setInterval(() => {
                if (width >= 100) {
                    clearInterval(progressInterval);
                    progressFill.style.width = '0%';
                } else {
                    width += 10;
                    progressFill.style.width = width + '%';
                }
            }, 100);
        }
        
        function selectAllEvo() {
            if (!tcpConnected) {
                showNotification('❌ TCP not connected! Please check bot status.', 'error');
                return;
            }
            
            const evoButtons = document.querySelectorAll('.evo-btn:not(.select-all-btn)');
            evoButtons.forEach(btn => {
                btn.style.background = 'linear-gradient(135deg, #ff0000, #ff00ff)';
                btn.innerHTML = '<i class="fas fa-check"></i> ' + btn.textContent.replace('✓ ', '');
            });
            
            showNotification('🎯 All EVO guns selected! Ready to fire via TCP!', 'success');
            startProgress();
        }
        
        function sendEvoEmote(emoteId, emoteName) {
            sendEmote(emoteId, emoteName);
        }
        
        function sendEmote(emoteId, emoteName) {
            const teamCode = document.getElementById('team_code')?.value;
            const targetUid = document.getElementById('target_uid')?.value;
            
            if (!teamCode || !targetUid) {
                showNotification('❌ Please enter Team Code and Target UID first!', 'error');
                return;
            }
            
            if (!teamCode.match(/^\d{7}$/)) {
                showNotification('❌ Team Code must be 7 digits!', 'error');
                return;
            }
            
            if (!targetUid.match(/^\d{8,11}$/)) {
                showNotification('❌ Target UID must be 8-11 digits!', 'error');
                return;
            }
            
            showNotification(`🚀 Sending ${emoteName} to UID ${targetUid}...`, 'warning');
            
            fetch('/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `team_code=${teamCode}&emote_id=${emoteId}&target_uid=${targetUid}`
            })
            .then(r => r.json())
            .then(data => {
                if(data.success) {
                    commandCount++;
                    updateStatus();
                    showNotification(`✅ ${emoteName} sent to UID ${targetUid}!`, 'success');
                } else {
                    showNotification('❌ Error: ' + data.error, 'error');
                }
            })
            .catch(() => {
                showNotification('❌ Network error', 'error');
            });
        }
        
        function sendQuickCommand() {
            const teamCode = document.getElementById('team_code')?.value;
            const targetUid = document.getElementById('target_uid')?.value;
            const emoteId = '909033001'; // Default M4A1
            
            if (!teamCode || !targetUid) {
                showNotification('❌ Please enter Team Code and Target UID first!', 'error');
                return;
            }
            
            if (!teamCode.match(/^\d{7}$/)) {
                showNotification('❌ Team Code must be 7 digits!', 'error');
                return;
            }
            
            if (!targetUid.match(/^\d{8,11}$/)) {
                showNotification('❌ Target UID must be 8-11 digits!', 'error');
                return;
            }
            
            showNotification(`🚀 Sending emote attack to UID ${targetUid}...`, 'warning');
            
            fetch('/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `team_code=${teamCode}&emote_id=${emoteId}&target_uid=${targetUid}`
            })
            .then(r => r.json())
            .then(data => {
                if(data.success) {
                    commandCount++;
                    updateStatus();
                    showNotification(`✅ Emote attack sent to UID ${targetUid}!`, 'success');
                } else {
                    showNotification('❌ Error: ' + data.error, 'error');
                }
            })
            .catch(() => {
                showNotification('❌ Network error', 'error');
            });
        }
        
        // Initialize
        updateStatus();
        updateTCPStatus(true);
        
        // Animate status dot
        setInterval(() => {
            const dot = document.querySelector('.status-dot');
            if (dot) {
                dot.style.animation = 'none';
                setTimeout(() => {
                    dot.style.animation = 'pulse 2s infinite';
                }, 10);
            }
        }, 5000);
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
        
        print(f"🚀 Command received: Team={team_code}, Emote={emote_id}, Target={target_uid}")
        
        # Validation
        if not re.match(r'^\d{7}$', team_code):
            return jsonify({"success": False, "error": "Team Code must be 7 digits"})
        
        if not re.match(r'^\d{8,11}$', target_uid):
            return jsonify({"success": False, "error": "Target UID must be 8-11 digits"})
        
        if not re.match(r'^\d{9}$', emote_id):
            return jsonify({"success": False, "error": "Invalid emote ID"})
        
        # Find emote name and category
        emote_name = "Custom Emote"
        category = "basic"
        for cat_name, emotes in EMOTE_CATEGORIES.items():
            for emote in emotes:
                if emote["id"] == emote_id:
                    emote_name = emote["name"]
                    category = emote.get("rarity", "basic")
                    break
        
        user_ip = request.remote_addr
        command_id = command_manager.save_command(team_code, emote_id, target_uid, user_ip, emote_name, category)
        
        if command_id:
            return jsonify({
                "success": True,
                "message": f"Command #{command_id} queued for execution!",
                "command_id": command_id,
                "note": "Command saved to bot queue"
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
    print(f"🚀 ASHISH EMOTE PANEL v3.0 starting on port {port}")
    print(f"🎮 Total Emotes: {len(ALL_EMOTES)}")
    print(f"🔥 EVO Guns: {len(EMOTE_CATEGORIES['EVO_GUNS'])}")
    print(f"⭐ Special & Popular: {len(EMOTE_CATEGORIES['SPECIAL_POPULAR'])}")
    print(f"🔵 Basic: {len(EMOTE_CATEGORIES['BASIC_EMOTES'])}")
    print(f"🏆 More Practice: {len(EMOTE_CATEGORIES['MORE_PRACTICE'])}")
    print(f"🔥 Fireborn Series: {len(EMOTE_CATEGORIES['FIREBORN_SERIES'])}")
    print(f"🥷 Ninja Series: {len(EMOTE_CATEGORIES['NINJA_SERIES'])}")
    print(f"👋 Greeting: {len(EMOTE_CATEGORIES['GREETING'])}")
    print(f"🎮 Party Game: {len(EMOTE_CATEGORIES['PARTY_GAME'])}")
    print(f"⭐ Extra Special: {len(EMOTE_CATEGORIES['EXTRA_SPECIAL'])}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=False)