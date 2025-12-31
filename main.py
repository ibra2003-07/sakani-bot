import requests
import telebot
import time

# --- إعداداتك ---
TOKEN = "8554154072:AAE0Vhlk_e736IxhR7aB26iNow2xUdXeFH0"
CHAT_ID = "1095307262"
# ---------------

bot = telebot.TeleBot(TOKEN)

def check_sakani_realtime():
    # رابط API مباشر لفحص توفر الوحدات في كافة المخططات
    url = "https://sakani.sa/api/v2/land_projects?per_page=100&sort_by=available_units_count"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Accept": "application/json",
        "X-App-Version": "3.9.1"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            projects = data.get('projects', []) or data.get('data', {}).get('projects', [])
            
            for project in projects:
                # التحقق من وجود "وحدات متاحة" فعلياً
                available = project.get('available_units_count', 0)
                if available > 0:
                    name = project.get('name')
                    city = project.get('city_name')
                    return f"🚨 صيد ثمين! توفرت أرض الآن:\n🏙 المدينة: {city}\n🏡 المخطط: {name}\n📦 المتوفر: {available} أرض\n🔗 احجز فوراً: https://sakani.sa/app/map"
        return None
    except Exception as e:
        print(f"فشل الفحص: {e}")
        return None

# رسالة تشغيل قوية
bot.send_message(CHAT_ID, "🚀 الرادار الاحترافي V4 يعمل الآن.\nبإذن الله الأرض اللي ألغيتها بنصيدها أول ما تظهر في النظام.")

while True:
    try:
        alert = check_sakani_realtime()
        if alert:
            bot.send_message(CHAT_ID, alert)
            # انتظر دقيقة بعد التنبيه عشان ما يزعجك بنفس الخبر
            time.sleep(60)
    except:
        pass
    
    time.sleep(7) # فحص كل 7 ثوانٍ (أمان للسيرفر)
