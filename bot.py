import telebot
import requests

# ===============================
# Ghi thẳng token Telegram
# ===============================
TOKEN = "8589085563:AAGV_FToLYlTVBpMWBzs_JAl5rnYbKgeRvc"
bot = telebot.TeleBot(TOKEN)

# ===============================
# Kiểm tra link Twitter/X
# ===============================
def is_twitter_link(text: str):
    return text and ("twitter.com" in text or "x.com" in text)

# ===============================
# Lấy video từ API bên thứ 3
# ===============================
def get_video(url: str):
    api_url = f"https://api.vxtwitter.com/?url={url}"
    resp = requests.get(api_url).json()
    if "mediaURLs" in resp and resp["mediaURLs"]:
        return resp["mediaURLs"][0]
    else:
        raise ValueError("Không tìm thấy video!")

# ===============================
# Xử lý tin nhắn Twitter/X
# ===============================
@bot.message_handler(func=lambda m: is_twitter_link(m.text if m.text else ""))
def handle_twitter_video(message):
    url = message.text.strip()
    bot.reply_to(message, "⏳ Đang tải video qua API...")

    try:
        video_url = get_video(url)
        bot.send_video(message.chat.id, video_url, caption="🎥 Video của bạn đây!")
    except Exception as e:
        bot.reply_to(message, "❌ Lỗi tải video hoặc không tìm thấy video!")
        print("ERROR:", e)

# ===============================
# Tin nhắn khác
# ===============================
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.reply_to(message, "Gửi link Twitter/X có video để mình tải cho bạn 👍")

# ===============================
# Start bot
# ===============================
print("🚀 Bot đang chạy với API bên thứ 3...")
bot.infinity_polling(skip_pending=True)
