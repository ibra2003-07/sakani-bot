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
    return "الرادار يعمل والفحص مستمر في الخلفية..."

def run_flask():
    # تشغيل سيرفر الويب لإبقاء Render صاحي
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def check_sakani():
    # رابط شامل لفحص جميع مشاريع المملكة المتاحة
    url = "https://sakani.sa/api/v2/land_projects?per_page=100&sort_by=available_units_count"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            projects = response.json().get('projects', [])
            for p in projects:
                if p.get('available_units_count', 0) > 0:
                    return f"🚨 لقطنا أرض بمخطط: {p['name']} في {p['city_name']}\nالعدد المتاح: {p['available_units_count']}"
    except Exception as e:
        print(f"⚠️ خطأ أثناء الفحص: {e}")
    return None

def monitor():
    # ننتظر 5 ثواني ليتأكد السيرفر من العمل
    time.sleep(5)
    bot.send_message(CHAT_ID, "🚀 تم تفعيل الرادار بنجاح. اللوق سيبدأ بالتحديث الآن كل 15 ثانية.")
    
    while True:
        try:
            # هذه الجملة ستظهر في اللوق (Logs) أمامك غصب عن السيرفر
            current_time = time.strftime('%H:%M:%S')
            print(f"[{current_time}] 🔍 جاري البحث في سيرفرات سكني...")
            
            result = check_sakani()
            if result:
                bot.send_message(CHAT_ID, result)
                print(f"[{current_time}] 🎯 تم العثور على صيد!")
                time.sleep(300) # راحة بعد الصيد
            
        except Exception as e:
            print(f"❌ خطأ في اللوب الأساسي: {e}")
        
        time.sleep(15) # فحص كل 15 ثانية

if __name__ == "__main__":
    # 1. تشغيل Flask في الخلفية
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # 2. تشغيل عملية المراقبة في المسار الأساسي
    monitor()
