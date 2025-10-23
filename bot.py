import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# BotFather'dan aldığın YENİ ve GİZLİ token'ı buraya yapıştır
TOKEN = "8189215084:AAEcUNgiqi5aJUdcxFyoHojRRfKj6r-wQFE"

# Loglamayı başlat (hataları görmek için)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Havalı karşılama mesajı
    welcome_text = (
        "🔥 **MRK FAKENO | GİZLİLİK MERKEZİ** 🔥\n\n"
        "Sanal dünyada iz bırakma! MRK FAKENO kalitesiyle\n"
        "anonimliğin tadını çıkar.\n\n"
        "Aşağıdaki hizmetlerden birini seç:\n\n"
        "💰 *Unutma! Bizde her zaman takas ve pazarlık payı vardır.*"
    )

    # Butonları oluştur
    keyboard = [
        [InlineKeyboardButton("📱 WhatsApp Fake No", callback_data='wp_fake')],
        [InlineKeyboardButton("🚀 Telegram Fake No", callback_data='tg_fake')],
        [InlineKeyboardButton("👑 İletişim & Satın Al", callback_data='contact')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Mesajı butonlarla birlikte gönder
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# Butonlara tıklandığında çalışacak fonksiyon
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Butona tıklandığını bildir

    # Hangi butona tıklandı?
    if query.data == 'wp_fake':
        text = (
            "📱 **WHATSAPP FAKE NUMARA** 📱\n\n"
            "Gizliliğini koru, WhatsApp'ta anonim kal!\n"
            "Güvenilir ve hızlı teslimat.\n\n"
            "💸 **Fiyat:** 150 TL\n\n"
            "💰 *Takas ve pazarlık payı mevcuttur.*\n\n"
            "👉 **Hemen Satın Almak İçin:** @MRKFAKENO"
        )
    elif query.data == 'tg_fake':
        text = (
            "🚀 **TELEGRAM FAKE NUMARA** 🚀\n\n"
            "Telegram'da kimliğini gizle, özgürce takıl!\n"
            "Stoklarla sınırlı, en stabil numaralar.\n\n"
            "💸 **Fiyat:** 250 TL\n\n"
            "💰 *Takas ve pazarlık payı mevcuttur.*\n\n"
            "👉 **Hemen Satın Almak İçin:** @MRKFAKENO"
        )
    elif query.data == 'contact':
        text = (
            "👑 **MRK FAKENO | İLETİŞİM** 👑\n\n"
            "Satın almak, pazarlık yapmak veya\n"
            "takas teklifinde bulunmak için doğru yerdesin.\n\n"
            "Çekinme, hemen yaz!\n\n"
            "👉 **Yetkili:** @MRKFAKENO"
        )
    else:
        text = "Bir hata oluştu. Lütfen /start ile tekrar deneyin."

    # Yeni mesajı gönder
    await query.edit_message_text(text=text, parse_mode='Markdown')

def main() -> None:
    # Botu başlat
    application = Application.builder().token(TOKEN).build()

    # Komutları ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Botu çalıştırmaya başla
    print("Bot çalışıyor...")
    application.run_polling()

if __name__ == "__main__":
    main()
