import telebot
import requests
import time
from threading import Thread
from flask import Flask # بنستخدم هذي عشان نخدع السيرفر

# --- إعداداتك ---
TOKEN = "8554154072:AAE0Vhlk_e736IxhR7aB26iNow2xUdXeFH0"
CHAT_ID = "1095307262"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home(): return "البوت شغال ١٠٠٪"

def run_web(): app.run(host='0.0.0.0', port=8080)

def check_sakani():
    url = "https://sakani.sa/api/v2/land_projects?per_page=100"
    try:
        res = requests.get(url, timeout=10).json()
        projects = res.get('projects', []) or res.get('data', {}).get('projects', [])
        for p in projects:
            if p.get('available_units_count', 0) > 0:
                return f"🚨 لقطنا أرض!\nالمخطط: {p['name']}\nالمدينة: {p['city_name']}"
    except: return None

def main_loop():
    bot.send_message(CHAT_ID, "🚀 الرادار V6 (النسخة النشطة) انطلق. الحين السيرفر ما يقدر ينام!")
    while True:
        print(f"[{time.strftime('%H:%M:%S')}] نبض الفحص..")
        found = check_sakani()
        if found:
            bot.send_message(CHAT_ID, found)
            time.sleep(300)
        time.sleep(15)

if __name__ == "__main__":
    # تشغيل الويب والبوت مع بعض عشان السيرفر يظل صاحي
    Thread(target=run_web).start()
    main_loop()
