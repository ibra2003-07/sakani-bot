import telebot
import requests
import time
import os
from threading import Thread
from flask import Flask

# --- إعداداتك ---
TOKEN = "8554154072:AAE0Vhlk_e736IxhR7aB26iNow2xUdXeFH0"
CHAT_ID = "1095307262"
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "الرادار شغال والفحص مستمر..."

def run_web():
    # تشغيل السيرفر على البورت المطلوب من رندر
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def check_sakani():
    url = "https://sakani.sa/api/v2/land_projects?per_page=100"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            projects = response.json().get('projects', [])
            for p in projects:
                if p.get('available_units_count', 0) > 0:
                    return f"🚨 صيدة! أرض في {p['city_name']} - {p['name']}"
    except Exception as e:
        print(f"⚠️ خطأ فحص: {e}")
    return None

def main_worker():
    # ننتظر قليلاً حتى يعمل سيرفر الويب
    time.sleep(5)
    bot.send_message(CHAT_ID, "🚀 الرادار بدأ الفحص الفعلي الآن.. راقب اللوق!")
    while True:
        # هذه الجملة هي التي ستجعل اللوق "يحدث" أمامك
        current_time = time.strftime('%H:%M:%S')
        print(f"[{current_time}] 🔍 جاري فحص جميع المخططات الآن...")
        
        found = check_sakani()
        if found:
            bot.send_message(CHAT_ID, found)
            print(f"[{current_time}] 🎯 تم العثور على أرض!")
            time.sleep(300)
        
        time.sleep(15) # فحص كل 15 ثانية

if __name__ == "__main__":
    # 1. تشغيل سيرفر الويب في الخلفية
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    
    # 2. تشغيل حلقة الفحص الأساسية
    main_worker()
