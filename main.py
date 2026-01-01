import telebot
import requests
import time

TOKEN = "8554154072:AAE0Vhlk_e736IxhR7aB26iNow2xUdXeFH0"
CHAT_ID = "1095307262"
bot = telebot.TeleBot(TOKEN)

def check():
    url = "https://sakani.sa/api/v2/land_projects?per_page=100"
    try:
        res = requests.get(url, timeout=10).json()
        projects = res.get('projects', []) or res.get('data', {}).get('projects', [])
        for p in projects:
            if p.get('available_units_count', 0) > 0:
                return f"🚨 لقطنا أرض!\nالمخطط: {p['name']}\nالمدينة: {p['city_name']}"
    except: return None
    return None

bot.send_message(CHAT_ID, "🚀 الرادار اشتغل وبدأ الفحص الفعلي.. تراقب الشاشة السوداء!")

while True:
    print(f"[{time.strftime('%H:%M:%S')}] جاري البحث في سيرفرات سكني...")
    found = check()
    if found:
        bot.send_message(CHAT_ID, found)
        time.sleep(300) # ارتاح 5 دقايق بعد الصيد
    time.sleep(10) # فحص كل 10 ثواني
