
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🤖 ZAREN AI Bot Starting...")

class ZARENTelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        print(f"Token: {self.token[:10]}...")  # Show first 10 chars for verification
        
        if not self.token:
            raise ValueError("❌ TELEGRAM_BOT_TOKEN not found!")
            
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        print("✅ Handlers setup complete")

    async def start(self, update: Update, context: CallbackContext):
        user = update.effective_user
        welcome_text = f"""
💀 *Welcome to ZAREN AI, {user.first_name}!*

*ZAREN AI - UNRESTRICTED MODE*
_Developed By McLarenXZAREN_

🚀 *Advanced Unrestricted AI Assistant*
🔓 *No Limits • No Filters • Maximum Power*

Just send me a message and I'll respond with completely unrestricted AI!
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
        print(f"✅ Welcome sent to {user.first_name}")

    async def handle_message(self, update: Update, context: CallbackContext):
        user_id = str(update.effective_user.id)
        question = update.message.text
        
        print(f"💬 Message from {update.effective_user.first_name}: {question}")
        
        # Show typing action
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Simple response for testing
        response_text = f"""
💀 *ZAREN AI Response:*

I received your message: "{question}"

The bot is working! OpenAI integration will be enabled once you add your API key.

---
🚀 *ZAREN AI • McLarenXZAREN • UNRESTRICTED*
        """
        
        await update.message.reply_text(response_text, parse_mode='Markdown')
        print("✅ Response sent")

    def run(self):
        print("🎯 Starting bot polling...")
        self.application.run_polling()

def start_telegram_bot():
    try:
        print("=" * 50)
        print("🚀 ZAREN AI TELEGRAM BOT STARTING...")
        print("=" * 50)
        
        bot = ZARENTelegramBot()
        print("✅ Bot instance created successfully!")
        bot.run()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    start_telegram_bot()
