import telebot
import instaloader
import os
import shutil

TOKEN = "8321394825:AAGzFqEG2JFjHcHX3ijcgOgWYjXkJy75Flk"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
                 "Salom! Men Instagram videolarini saqlab beruvchi botman. 🎬\n"
                 "Videoning linkini yubor 😊\n"
                 "Masalan: https://www.instagram.com/reel/ClXYZ12345/")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()

    # Link formatini tekshirish
    if "instagram.com" not in url:
        bot.send_message(message.chat.id, "❌ Iltimos, to‘g‘ri Instagram linkini yuboring!")
        return

    bot.send_message(message.chat.id, "Yuklab olinmoqda... ⏳")

    try:
        L = instaloader.Instaloader(download_videos=True, download_comments=False,
                                    save_metadata=False, post_metadata_txt_pattern="")

        # Agar shaxsiy akkaunt videolari uchun login kerak bo‘lsa:
        # L.login("username", "password")

        # Shortcode olish
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        folder_name = f"{post.owner_username}_video"
        L.download_post(post, target=folder_name)

        # Videoni topish va yuborish
        video_found = False
        for file in os.listdir(folder_name):
            if file.endswith(".mp4"):
                video_path = os.path.join(folder_name, file)
                bot.send_video(message.chat.id, open(video_path, "rb"))
                video_found = True
                break  # birinchi topilgan videoni yuborish

        # Fayllarni tozalash
        shutil.rmtree(folder_name)

        if not video_found:
            bot.send_message(message.chat.id, "❌ Video topilmadi yoki bu post videoga ega emas.")

    except Exception as e:
        print(e)  # xatolikni konsolga chiqarish
        bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi: {e}")

print("Bot ishga tushdi...")
bot.infinity_polling()
