import telebot
import requests
import time

# --- بياناتك ---
TOKEN = "8554154072:AAE0Vhlk_e736IxhR7aB26iNow2xUdXeFH0"
CHAT_ID = "1095307262"
bot = telebot.TeleBot(TOKEN)

def check_sakani():
    # فحص مباشر وشامل لكل المخططات
    url = "https://sakani.sa/api/v2/land_projects?per_page=100&sort_by=available_units_count"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            projects = data.get('projects', []) or data.get('data', {}).get('projects', [])
            for p in projects:
                if p.get('available_units_count', 0) > 0:
                    return f"🚨 لقطنا أرض!\nالمخطط: {p['name']}\nالمدينة: {p['city_name']}\nالعدد: {p['available_units_count']}"
    except Exception as e:
        print(f"⚠️ خطأ اتصال: {e}")
    return None

print("🔥 انطلق الرادار.. راقب السطور تحت:")
bot.send_message(CHAT_ID, "✅ الرادار شغال الحين.. لو ما صاد، العيب في سكني!")

# اللوب اللي بيخلي السيرفر شغال غصب
while True:
    try:
        current_time = time.strftime('%H:%M:%S')
        # هذا السطر لازم يظهر في شاشة الـ Logs عندك كل 10 ثواني
        print(f"[{current_time}] 🔍 جاري البحث في كل المخططات...")
        
        found = check_sakani()
        if found:
            bot.send_message(CHAT_ID, found)
            print(f"[{current_time}] 🎯 تم الصيد! أرسلت لك في تيليجرام.")
            time.sleep(300) # ارتاح 5 دقايق بعد الصيد
            
    except Exception as e:
        print(f"❌ خطأ في اللوب: {e}")
    
    time.sleep(10) # فحص كل 10 ثواني
