import telebot
import requests
import time
from threading import Thread
from flask import Flask # أضفنا هذي المكتبة

# --- بياناتك ---
TOKEN = "8554154072:AAE0Vhlk_e736IxhR7aB26iNow2xUdXeFH0"
CHAT_ID = "1095307262"
bot = telebot.TeleBot(TOKEN)

# --- كود خداع السيرفر (Flask) ---
app = Flask('')
@app.route('/')
def home(): return "الرادار يعمل بكفاءة!"
def run_web(): app.run(host='0.0.0.0', port=8080)

def check_sakani():
    url = "https://sakani.sa/api/v2/land_projects?per_page=100&sort_by=available_units_count"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            projects = response.json().get('projects', [])
            for p in projects:
                if p.get('available_units_count', 0) > 0:
                    return f"🚨 صيدة! أرض متاحة الآن:\n🏙 المدينة: {p['city_name']}\n🏡 المخطط: {p['name']}\n🔗 احجز: https://sakani.sa/app/map"
    except: return None
    return None

def main_loop():
    bot.send_message(CHAT_ID, "🎯 رادار الصيد (V6) يعمل الآن.. مستحيل يطفي!")
    while True:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] نبض الفحص..")
            found = check_sakani()
            if found:
                bot.send_message(CHAT_ID, found)
                time.sleep(120) 
            time.sleep(15)
        except Exception as e:
            print(f"خطأ: {e}")
            time.sleep(5)

if __name__ == "__main__":
    Thread(target=run_web).start() # شغل الويب
    main_loop() # شغل الفحص
