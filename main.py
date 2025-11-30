import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ChatMemberStatus

# 💥 KRİTİK UYARI: Botunuzun çalışması için bu token'ı BotFather'dan aldığınız token ile DEĞİŞTİRİN!
TOKEN = "8286341635:AAGgLpVLnvaB4NcHd5JsXv9a9-mc9d14URE" 

# Zorunlu Kanal ve İletişim Bilgileri
KANAL_ID = "@Satis_grup"  # Zorunlu katılınması gereken kanalın kullanıcı adı
KANAL_LINKI = "https://t.me/Satis_grup" # Kanalın tam linki
ODUL_ILETISIM_USER = "@ZKRVE1" # Ödül ve Satın Alma için ulaşılması gereken kullanıcı

# Fiyat Bilgileri
FIYAT_WP = 100
FIYAT_TG = 250

# Referans sayımı (Bot her yeniden başladığında SIFIRLANIR)
# Format: {user_id: referans_sayisi}
referral_counts = {}

# Loglamayı başlat
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Yardımcı Fonksiyon: Kanal üyeliğini kontrol eder
async def check_channel_membership(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=KANAL_ID, user_id=user_id)
        
        # Sadece Creator, Admin, Member ve Restricted (kısıtlı ama üye) ise True döner
        if member.status in [
            ChatMemberStatus.CREATOR, 
            ChatMemberStatus.ADMINISTRATOR, 
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.RESTRICTED 
        ]:
            logger.info(f"Kullanıcı {user_id} kanala üye.")
            return True
        
        logger.info(f"Kullanıcı {user_id} kanala üye değil veya ayrılmış. Durum: {member.status.name}")
        return False
        
    except Exception as e:
        logger.error(f"⚠️ KRİTİK HATA: Kanal üyeliği kontrolü başarısız oldu: {e}")
        logger.error(f"Lütfen botun {KANAL_ID} kanalında yönetici (admin) olduğundan emin olun.")
        return False

# /start komutu ve referans işleyici
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user:
        return

    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "Anonim Kullanıcı"
    
    if user_id not in referral_counts:
        referral_counts[user_id] = 0

    if context.args:
        try:
            referrer_id = int(context.args[0])
            if referrer_id != user_id:
                referral_counts[referrer_id] = referral_counts.get(referrer_id, 0) + 1
                referrer_count = referral_counts[referrer_id]
                
                await context.bot.send_message(
                    chat_id=referrer_id,
                    # Markdown biçimlendirme kullanıldı
                    text=f"🎉 **TEBRİKLER!** 🎉\n\n{user_name} seni referans göstererek katıldı!\nGüncel referans sayın: **{referrer_count}**",
                    parse_mode='Markdown'
                )
                logger.info(f"Kullanıcı {user_id}, kullanıcı {referrer_id} tarafından referans edildi. Yeni sayı: {referrer_count}")
        except ValueError:
            logger.error("Referans ID'si sayı formatında değil.")
        except Exception as e:
            logger.error(f"Referans ekleme hatası: {e}")
        
    # Ana Menü Bilgileri
    referral_link = f"https://t.me/{context.bot.username}?start={user_id}"

    welcome_text = (
        f"👑 **FAKENO | GİZLİLİK MERKEZİ** 👑\n\n"
        f"Hoş geldin, **{user_name}**!\n\n"
        f"Arkadaşlarını getir, dev ödülleri kap ya da\n"
        f"anında teslimatla anonimliğin tadını çıkar.\n\n"
        f"Mevcut Referans Sayın: **{referral_counts[user_id]}**\n\n"
        f"🚀 **SENİN REFERANS LİNKİNİ KOPYALA:**\n`{referral_link}`" # Backtick (`) ile kod bloğu oluşturuldu
    )

    # Butonları oluştur
    keyboard = [
        [InlineKeyboardButton("🎁 Ödül Tablosu ve Şartlar", callback_data='rewards')],
        [InlineKeyboardButton("💰 Satın Al / Fiyatlar", callback_data='prices')],
        [InlineKeyboardButton("👑 Ödülümü Talep Et", callback_data='claim_reward')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown') # Markdown Modu

# Butonlara tıklandığında çalışacak fonksiyon
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    current_count = referral_counts.get(user_id, 0)
    
    if query.data == 'rewards':
        # KULLANICININ İSTEKLERİNE GÖRE GÜNCELLENMİŞ ÖDÜL TABLOSU (Markdown formatında)
        text = (
            "⚠️ **KANALA KATILIM ZORUNLU** ⚠️\n\n"
            f"Mevcut Referans Sayın: **{current_count}**\n"
            "----------------------------------\n"
            "**🎁 ÖDÜL TABLOSU:**\n"
            "   **25 Referans:** 📱 1 Adet WhatsApp Fake No\n"
            "   **35 Referans:** 🚀 1 Adet Telegram Fake No\n"
            "----------------------------------\n\n"
            "🛑 **ÖNEMLİ NOT:**\n"
            f"Ödül kazanmak için referans getirdiğin **TÜM** kullanıcıların zorunlu kanalımız olan *{KANAL_ID}* adresine **KATILMASI GEREKMEKTEDİR.**\n"
            "**KANALA KATILMAYAN KULLANICILAR ÖDÜL TALEP EDEMEZ!**"
        )
        
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➡️ Zorunlu Kanalımız", url=KANAL_LINKI)], # Kanal linki butona eklendi
                [InlineKeyboardButton("👑 Ödülümü Talep Et", callback_data='claim_reward')],
                [InlineKeyboardButton("🏠 Ana Menüye Dön", callback_data='main_menu')]
            ]),
            parse_mode='Markdown' # Markdown Modu
        )
        
    elif query.data == 'prices':
        # FİYAT VE SATIN ALMA EKRANI (Markdown formatında)
        text = (
            "💰 **FAKENO | SATIN ALMA MERKEZİ** 💰\n\n"
            "Anında teslimat ve güvenilir hizmet ile\n"
            "anonimliğe hemen geçiş yapın!\n\n"
            "----------------------------------\n"
            "📱 **WHATSAPP FAKE NO**\n"
            f"💸 Fiyat: **{FIYAT_WP} TL**\n"
            "----------------------------------\n"
            "🚀 **TELEGRAM FAKE NO**\n"
            f"💸 Fiyat: **{FIYAT_TG} TL**\n"
            "----------------------------------\n\n"
            f"👑 **SATIN ALMAK İÇİN İLETİŞİM:**\n"
            f"Hemen **{ODUL_ILETISIM_USER}** adresine ulaşın!"
        )
        
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👑 Yetkiliye Ulaş", url=f"https://t.me/{ODUL_ILETISIM_USER.replace('@', '')}")],
                [InlineKeyboardButton("🏠 Ana Menüye Dön", callback_data='main_menu')]
            ]),
            parse_mode='Markdown' # Markdown Modu
        )
        
    elif query.data == 'claim_reward':
        
        reward = None
        if current_count >= 35:
            reward = "1 Adet Telegram Fake No (35 Referans Ödülü)"
        elif current_count >= 25:
            reward = "1 Adet WhatsApp Fake No (25 Referans Ödülü)"
        
        if not reward:
            await query.edit_message_text(
                text=f"❌ **YETERSİZ REFERANS** ❌\n\n"
                     f"Şu anki referans sayın **{current_count}**. İlk ödül (WP Fake No) için **25** referansa ihtiyacın var. Daha çok arkadaş davet et!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎁 Ödül Tablosu", callback_data='rewards')],
                    [InlineKeyboardButton("🏠 Ana Menüye Dön", callback_data='main_menu')]
                ]),
                parse_mode='Markdown' # Markdown Modu
            )
            return
            
        is_member = await check_channel_membership(context.bot, user_id)

        if not is_member:
            await query.edit_message_text(
                text="⚠️ **KANAL ÜYELİĞİ ZORUNLU** ⚠️\n\n"
                     f"Ödülünü talep edebilmen için öncelikle **ZORUNLU** kanalımız olan *{KANAL_ID}* adresine katılman gerekmektedir.\n\n"
                     "Lütfen kanala katıl ve tekrar dene.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("➡️ Zorunlu Kanalımız", url=KANAL_LINKI)],
                    [InlineKeyboardButton("🔄 Tekrar Dene", callback_data='claim_reward')],
                    [InlineKeyboardButton("🏠 Ana Menüye Dön", callback_data='main_menu')]
                ]),
                parse_mode='Markdown' # Markdown Modu
            )
        else:
            await query.edit_message_text(
                text=f"✅ **TALEP BAŞARILI!** 🎉\n\n"
                     f"Tebrikler! **{reward}** kazanmaya hak kazandın.\n\n"
                     f"Ödülünü almak için:\n"
                     f"👉 **HEMEN `{ODUL_ILETISIM_USER}` adresine ulaş!**\n"
                     f"Mesajına `[TALEP KODU: REF-{user_id}]` yazarak hızlı işlem yapabilirsin.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("👑 Yetkiliye Ulaş", url=f"https://t.me/{ODUL_ILETISIM_USER.replace('@', '')}")],
                    [InlineKeyboardButton("🏠 Ana Menüye Dön", callback_data='main_menu')]
                ]),
                parse_mode='Markdown' # Markdown Modu
            )
            
    elif query.data == 'main_menu':
        user_name = query.from_user.first_name or "Anonim Kullanıcı"
        referral_link = f"https://t.me/{context.bot.username}?start={user_id}"
        
        welcome_text = (
            f"👑 **MRK FAKENO | GİZLİLİK MERKEZİ** 👑\n\n"
            f"Hoş geldin, **{user_name}**!\n\n"
            f"Mevcut Referans Sayın: **{referral_counts.get(user_id, 0)}**\n\n"
            f"🚀 **SENİN REFERANS LİNKİNİ KOPYALA:**\n`{referral_link}`" # Backtick (`) ile kod bloğu oluşturuldu
        )

        keyboard = [
            [InlineKeyboardButton("🎁 Ödül Tablosu ve Şartlar", callback_data='rewards')],
            [InlineKeyboardButton("💰 Satın Al / Fiyatlar", callback_data='prices')],
            [InlineKeyboardButton("👑 Ödülümü Talep Et", callback_data='claim_reward')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown') # Markdown Modu
        except Exception as e:
            logger.error(f"Ana menüye dönerken hata: {e}. Muhtemelen mesaj zaten aynı.")


def main() -> None:
    """Botu başlatır."""
    if TOKEN == "BURAYA_BOT_TOKEN_YAPIŞTIR" or not TOKEN:
        print("❌ HATA: Lütfen token'ınızı 'TOKEN' değişkenine yapıştırın ve botu yeniden başlatın.")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("✅ MRK FAKENO Botu güncellendi, Markdown formatında çalışıyor.")
    application.run_polling(poll_interval=1.0) 

if __name__ == "__main__":
    main()
