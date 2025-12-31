import requests
import telebot
import time

# --- إعداداتك ---
TOKEN = "8554154072:AAE0Vhlk_e736IxhR7aB26iNow2xUdXeFH0"
CHAT_ID = "1095307262"
# ---------------

bot = telebot.TeleBot(TOKEN)

# قائمة لحفظ المعرفات المكتشفة عشان ما يكرر لك التنبيه لنفس الأرض
seen_projects = set()

def check_sakani():
    # الرابط الرسمي لجلب كافة مشاريع الأراضي في المملكة
    url = "https://sakani.sa/api/v1/land_projects?per_page=100" 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Origin": "https://sakani.sa",
        "Referer": "https://sakani.sa/app/map"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            projects = data.get('projects', [])
            
            for project in projects:
                project_id = project.get('id')
                # إذا كان المشروع متاحاً ولم نرسل عنه تنبيه سابقاً
                if project.get('is_available') == True and project_id not in seen_projects:
                    name = project.get('name')
                    city = project.get('city_name')
                    price = project.get('price', 'غير محدد')
                    
                    seen_projects.add(project_id)
                    return f"📍 مخطط جديد متاح!\n🏙 المدينة: {city}\n🏡 الاسم: {name}\n💰 السعر يبدأ من: {price}\n🔗 الرابط: https://sakani.sa/app/map"
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# رسالة تأكيد نهائية
bot.send_message(CHAT_ID, "✅ تم تفعيل الرادار الشامل لجميع مخططات المملكة.\n⏱ سرعة الفحص: كل 5 ثوانٍ.\n🔇 سأصمت الآن حتى تظهر أرض.")

while True:
    try:
        alert = check_sakani()
        if alert:
            bot.send_message(CHAT_ID, alert)
    except:
        pass
    
    time.sleep(5)
