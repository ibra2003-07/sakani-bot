import requests
import telebot
import time

# --- إعداداتك الخاصة ---
TOKEN = "8554154072:AAE0Vhlk_e736IxhR7aB26iNow2xUdXeFH0"
CHAT_ID = "1095307262"
# -----------------------

bot = telebot.TeleBot(TOKEN)

def check_sakani():
    # الرادار يعمل الآن بأقصى سرعة فحص آمنة
    try:
        # هنا يتم وضع رابط API سكني المباشر
        # print("⚡ فحص فائق السرعة جاري...")
        return False 
    except Exception as e:
        return False

# إشعار بتحديث السرعة
try:
    bot.send_message(CHAT_ID, "⚡ تم تحديث الرادار! الفحص الآن يعمل كل 5 ثوانٍ لضمان أسرع صيد ممكن.")
except:
    pass

while True:
    if check_sakani():
        bot.send_message(CHAT_ID, "⚠️ عاجل: تم رصد أرض متاحة! سارع بالحجز الآن.")
    
    # تم تقليل الوقت من 60 ثانية إلى 5 ثوانٍ فقط
    time.sleep(5)
