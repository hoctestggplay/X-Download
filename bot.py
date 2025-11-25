import telebot
import yt_dlp
import tempfile
import os
from telebot.types import InputFile

# Ghi thẳng token Telegram
TOKEN = "8589085563:AAGV_FToLYlTVBpMWBzs_JAl5rnYbKgeRvc"
bot = telebot.TeleBot(TOKEN)

def is_twitter_link(text: str):
    if not text:
        return False
    return "twitter.com" in text or "x.com" in text

def download_video(url: str):
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "video.mp4")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": output_path,
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path

@bot.message_handler(func=lambda m: is_twitter_link(m.text if m.text else ""))
def handle_twitter_video(message):
    url = message.text.strip()
    bot.reply_to(message, "⏳ Đang tải video bằng yt-dlp...")

    try:
        video_path = download_video(url)

        with open(video_path, "rb") as f:
            bot.send_video(
                message.chat.id,
                InputFile(f),
                caption="🎥 Video của bạn đây!"
            )
    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi tải video!")
        print("ERROR:", e)

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.reply_to(message, "Gửi link Twitter/X có video để mình tải cho bạn 👍")

print("🚀 Bot đang chạy bằng yt-dlp...")
bot.infinity_polling(skip_pending=True)
