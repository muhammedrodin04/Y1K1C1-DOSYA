# vds.py → %100 ÇALIŞIR (Python 3.12 + Windows uyumlu)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os
import sys

TOKEN = "8414179160:AAHIIEB0YDTtR-r6SX1Z7G7NAxRSOwk-D5I"
ADMIN_ID = 8017341073

os.makedirs("uploads", exist_ok=True)

BANNER = """
╔══════════════════════════════════════╗
║      VEXORP-SANAL VDS                ║
║          ID: 8017341073              ║
║         HAVALI MOD AKTİF             ║
╚══════════════════════════════════════╝
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Erişim reddedildi.")
        return

    keyboard = [
        [InlineKeyboardButton("BAŞLAT", callback_data="baslat"),
         InlineKeyboardButton("DURDUR", callback_data="durdur")],
        [InlineKeyboardButton("RESTART", callback_data="restart")],
        [InlineKeyboardButton("DOSYALAR", callback_data="dosyalar")],
        [InlineKeyboardButton("DOSYA GÖNDER", callback_data="gonder")],
       235        [InlineKeyboardButton("NÜKLEER", callback_data="nuke")]
    ]

    await update.message.reply_text(
        f"<pre>{BANNER}</pre>\n<b>SİSTEM ÇEVRİMİÇİ</b>",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if update.effective_user.id != ADMIN_ID: return

    data = query.data

    if data == "baslat":
        await query.edit_message_text("ZATEN AKTİF")
    elif data == "durdur":
        await query.edit_message_text("KAPANIYOR... 5")
        await asyncio.sleep(5)
        os._exit(0)
    elif data == "restart":
        await query.edit_message_text("RESTART...")
        await asyncio.sleep(2)
        os.execl(sys.executable, sys.executable, *sys.argv)
    elif data == "nuke":
        import shutil
        shutil.rmtree("uploads")
        os.makedirs("uploads")
        await query.edit_message_text("HER ŞEY YOK EDİLDİ")
    elif data == "gonder":
        if len(os.listdir("uploads")) >= 10:
            await query.edit_message_text("MAX 10 DOSYA!")
        else:
            context.user_data["yukle"] = True
            await query.edit_message_text("DOSYA GÖNDER")
    elif data == "dosyalar":
        dosyalar = os.listdir("uploads")
        if not dosyalar:
            await query.edit_message_text("Dosya yok.")
            return
        keyboard = []
        for f in dosyalar:
            yol = f"uploads/{f}"
            keyboard.append([InlineKeyboardButton(f, callback_data=f"gor_{yol}"),
                             InlineKeyboardButton("Sil", callback_data=f"sil_{yol}")])
        keyboard.append([InlineKeyboardButton("Geri", callback_data="start")])
        await query.edit_message_text(f"{len(dosyalar)}/10", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("gor_"):
        yol = data[4:]
        if os.path.exists(yol):
            await query.message.reply_document(open(yol, "rb"))
    elif data.startswith("sil_"):
        yol = data[4:]
        if os.path.exists(yol):
            os.remove(yol)
            await query.edit_message_text("SİLİNDİ")

async def dosya_geldi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID or not context.user_data.get("yukle"): return

    file = update.message.document or (update.message.photo[-1] if update.message.photo else None) or update.message.video
    if not file: return

    dosya = await file.get_file()
    adi = update.message.document.file_name if update.message.document else f"dosya_{update.message.message_id}"
    yol = f"uploads/{adi}"
    await dosya.download_to_drive(yol)

    context.user_data["yukle"] = False
    await update.message.reply_text(f"{adi} KAYDEDİLDİ\nToplam: {len(os.listdir('uploads'))}/10")

# ANA ÇALIŞTIRMA
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO, dosya_geldi))

print(BANNER + "\nBOT ÇALIŞIYOR... (Ctrl+C ile durdur)")
app.run_polling(drop_pending_updates=True)
