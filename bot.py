import os
import telebot
import subprocess

# Your unique Telegram Bot Token
API_TOKEN = '7737474213:AAFuPHslXBZWF0SAXb-x8WUNY8l_5uY476c'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Send me an Aniwatch anime link, and I'll process the download.")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text
    
    # Simple check to see if it's a valid-ish link
    if "aniwatch" in url or "hianime" in url:
        bot.reply_to(message, "📥 Request received! Starting the download process. Please wait...")
        
        try:
            # We run the original downloader script using subprocess
            # main.py is the entry point for the abhinai2244/AniwatchTvdl repo
            result = subprocess.run(["python", "main.py", url], capture_output=True, text=True)
            
            if result.returncode == 0:
                bot.send_message(message.chat.id, "✅ Process completed! Check the server logs for the file.")
            else:
                bot.reply_to(message, f"❌ Script Error: {result.stderr}")
                
        except Exception as e:
            bot.reply_to(message, f"⚠️ Bot Error: {str(e)}")
    else:
        bot.reply_to(message, "❌ Please send a valid anime link.")

print("Bot is running...")
bot.infinity_polling()
