import firebase_admin
from firebase_admin import credentials, db
import telebot
import time
import os
from flask import Flask
from threading import Thread

# --- WEB SERVER (Taake Render bot ko band na kare) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT CONFIGURATION ---
BOT_TOKEN = '8630146720:AAGqP0PZIH1uivHsVoIROtcXoYGxWi4Apxc'
CHAT_ID = '8053020958'
DB_URL = 'https://eagle-trading-81262-default-rtdb.firebaseio.com/'

bot = telebot.TeleBot(BOT_TOKEN)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': DB_URL})

startup_complete = False

def send_tele(msg):
    try:
        bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
    except: pass

def monitor_deposits(event):
    global startup_complete
    if not startup_complete: return
    if event.data:
        data = event.data
        msg = f"💰 *NEW DEPOSIT*\n💵 Amount: {data.get('amount', 'N/A')}\n📱 Phone: {data.get('phone', 'N/A')}"
        send_tele(msg)

def monitor_withdraws(event):
    global startup_complete
    if not startup_complete: return
    if event.data:
        data = event.data
        msg = f"🏧 *NEW WITHDRAW*\n💵 Amount: {data.get('amount', 'N/A')}\n🏦 Method: {data.get('provider', 'N/A')}"
        send_tele(msg)

# Listeners
db.reference('requests').on_child_added(monitor_deposits)
db.reference('withdraw_requests').on_child_added(monitor_withdraws)

if __name__ == "__main__":
    keep_alive() # Web server chalu karein
    print("📡 Monitoring Active...")
    time.sleep(5)
    startup_complete = True
    while True:
        time.sleep(1)