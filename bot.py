# - * - coding: utf-8 - * -
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

TOKEN = "8578227231:AAFBAi3T0V0JfbG-Hzf0FZcOea1qg-7YnEY"

CHANNELS = ["@Ar_clash_call_shop_gp", "@Ar_clash_call_shop_gp"]


# ------------------------- START ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    text = (
        "👋 ابتدا عضو کانال‌های زیر شوید:\n\n"
        "@Ar_clash_call_shop_gp\n"
        "@Ar_clash_call_shop_shop_gp\n\n"
        "بعد از عضویت، روی دکمه زیر بزنید:"
    )

    keyboard = [
        [InlineKeyboardButton("✔️ عضویت انجام شد", callback_data="check_subs")]
    ]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# ------------------------- CHECK SUB ---------------------------
async def check_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    for ch in CHANNELS:
        member = await context.bot.get_chat_member(ch, query.from_user.id)
        if member.status == "left":
            await query.edit_message_text(
                "❌ شما هنوز عضو همه کانال‌ها نشدید.\n\n"
                "لطفاً عضو شوید و دوباره امتحان کنید."
            )
            return

    # شروع فرم
    context.user_data["step"] = "banner"
    await query.edit_message_text(
        "📸 لطفاً عکس یا ویدیو بنر ارسال کنید.\n\nلغو❌"
    )


# ------------------------- MESSAGE HANDLER ---------------------------
async def msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step")

    if not step:
        return

    msg = update.message

    # ------------------ مرحله ۱ بنر ------------------
    if step == "banner":
        if not msg.photo and not msg.video:
            await msg.reply_text("❌ لطفاً عکس یا ویدیو ارسال کنید.")
            return

        context.user_data["banner"] = msg.photo[-1].file_id if msg.photo else msg.video.file_id
        context.user_data["step"] = "change_gmail"
        await msg.reply_text("1️⃣ وضعیت چنج جیمیل؟ (بله/خیر)\n\nلغو❌")
        return

    # ------------------ مرحله ۲ ------------------
    if step == "change_gmail":
        context.user_data["change_gmail"] = msg.text
        context.user_data["step"] = "rename"
        await msg.reply_text("👤 تغییر نام؟ (بله/خیر)\n\nلغو❌")
        return

    # ------------------ مرحله ۳ ------------------
    if step == "rename":
        context.user_data["rename"] = msg.text
        context.user_data["step"] = "gems"
        await msg.reply_text("💎 تعداد جم؟\n\nلغو❌")
        return

    # ------------------ مرحله ۴ ------------------
    if step == "gems":
        context.user_data["gems"] = msg.text
        context.user_data["step"] = "lvl"
        await msg.reply_text("⚡️ لول اکانت؟\n\nلغو❌")
        return

    if step == "lvl":
        context.user_data["lvl"] = msg.text
        context.user_data["step"] = "th"
        await msg.reply_text("🏕️ لول تاون هال؟\n\nلغو❌")
        return

    if step == "th":
        context.user_data["th"] = msg.text
        context.user_data["step"] = "bh"
        await msg.reply_text("🛖 لول دهکده سازنده؟\n\nلغو❌")
        return

    if step == "bh":
        context.user_data["bh"] = msg.text
        context.user_data["step"] = "king"
        await msg.reply_text("🌟 لول کینگ؟\n\nلغو❌")
        return

    if step == "king":
        context.user_data["king"] = msg.text
        context.user_data["step"] = "queen"
        await msg.reply_text("🌟 لول کویین؟\n\nلغو❌")
        return

    if step == "queen":
        context.user_data["queen"] = msg.text
        context.user_data["step"] = "warden"
        await msg.reply_text("🌟 لول واردن؟\n\nلغو❌")
        return

    if step == "warden":
        context.user_data["warden"] = msg.text
        context.user_data["step"] = "champ"
        await msg.reply_text("🌟 لول چمپیون؟\n\nلغو❌")
        return

    if step == "champ":
        context.user_data["champ"] = msg.text
        context.user_data["step"] = "minion"
        await msg.reply_text("🌟 لول مینیون پرنس؟\n\nلغو❌")
        return

    if step == "minion":
        context.user_data["minion"] = msg.text
        context.user_data["step"] = "price"
        await msg.reply_text("💵 قیمت؟\n\nلغو❌")
        return

    if step == "price":
        context.user_data["price"] = msg.text
        context.user_data["step"] = "trade"
        await msg.reply_text("🔄 مایل به طاق هستی؟ (بله/خیر)\n\nلغو❌")
        return

    if step == "trade":
        context.user_data["trade"] = msg.text
        context.user_data["step"] = "seller"
        await msg.reply_text("👤 آیدی فروشنده؟\n\nلغو❌")
        return

    if step == "seller":
        context.user_data["seller"] = msg.text
        context.user_data["step"] = None

        # تایید نهایی
        keyboard = [
            [
                InlineKeyboardButton("✍️ ویرایش بنر", callback_data="edit_banner"),
                InlineKeyboardButton("✅ تایید نهایی", callback_data="final_confirm")
            ],
            [InlineKeyboardButton("لغو❌", callback_data="cancel")]
        ]

        text = (
            "📋 اطلاعات آگهی:\n\n"
            f"وضعیت چنج جیمیل: {context.user_data['change_gmail']}\n"
            f"تغییر نام: {context.user_data['rename']}\n"
            f"جم: {context.user_data['gems']}\n"
            f"لول: {context.user_data['lvl']}\n"
            f"تاون هال: {context.user_data['th']}\n"
            f"بیلدر: {context.user_data['bh']}\n"
            f"کینگ: {context.user_data['king']}\n"
            f"کویین: {context.user_data['queen']}\n"
            f"واردن: {context.user_data['warden']}\n"
            f"چمپیون: {context.user_data['champ']}\n"
            f"مینیون پرنس: {context.user_data['minion']}\n"
            f"قیمت: {context.user_data['price']}\n"
            f"طاق: {context.user_data['trade']}\n"
            f"فروشنده: {context.user_data['seller']}\n"
        )

        await msg.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return


# ------------------------- FINAL CONFIRM ---------------------------
async def final_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "✅ آگهی شما برای ادمین ارسال شد.\n\n"
        "آگهی Clash Of Clans ارسال شد."
    )


# ------------------------- MAIN ---------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subs, pattern="check_subs"))
    app.add_handler(CallbackQueryHandler(final_confirm, pattern="final_confirm"))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO, msg_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
