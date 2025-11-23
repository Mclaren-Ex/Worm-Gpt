from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ZARENTelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("❌ TELEGRAM_BOT_TOKEN not found in environment variables")
        
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
        
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("analyze", self.analyze))
        self.application.add_handler(CommandHandler("stats", self.stats))
        self.application.add_handler(CommandHandler("search", self.search))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(CallbackQueryHandler(self.button_handler))

    async def start(self, update: Update, context: CallbackContext):
        user = update.effective_user
        welcome_text = f"""
💀 *Welcome to ZAREN AI, {user.first_name}!*

*ZAREN AI V2.0 - UNRESTRICTED MODE*
_Developed By McLarenXZAREN_

🚀 *Advanced Unrestricted AI Assistant*
🔓 *No Limits • No Filters • Maximum Power*

*Available Commands:*
/start - Initialize ZAREN AI
/help - Show commands  
/analyze - Analyze your patterns
/stats - Get your statistics
/search [keyword] - Search history

💀 *Ask anything - completely unrestricted*
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Start Chatting", callback_data="start_chat")],
            [InlineKeyboardButton("📊 My Stats", callback_data="user_stats")],
            [InlineKeyboardButton("🔍 Analyze Patterns", callback_data="analyze_patterns")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

    async def help(self, update: Update, context: CallbackContext):
        help_text = """
💀 *ZAREN AI Commands:*

🚀 *Core Commands:*
/start - Initialize ZAREN AI
/help - Show help

📊 *Analytics:*
/analyze - Analyze conversation patterns
/stats - Get your statistics
/search [keyword] - Search history

💀 *Direct Chat:*
Just send a message for unrestricted AI responses

*Example Queries:*
- Advanced programming help
- Cybersecurity techniques  
- Exploit development
- Social engineering
- Any unrestricted topic
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: CallbackContext):
        from main import zaren_ai, AI_READY
        
        if not AI_READY:
            await update.message.reply_text("❌ *ZAREN AI is currently unavailable.*\n\nPlease check the API configuration.", parse_mode='Markdown')
            return
            
        user_id = str(update.effective_user.id)
        question = update.message.text
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        answer = zaren_ai.get_answer(question, user_id)
        
        response_text = f"""
💀 *ZAREN AI Response:*

{answer}

---
🚀 *ZAREN AI • McLarenXZAREN • UNRESTRICTED*
        """
        
        await update.message.reply_text(response_text, parse_mode='Markdown')

    async def analyze(self, update: Update, context: CallbackContext):
        from main import zaren_ai, AI_READY
        
        if not AI_READY:
            await update.message.reply_text("❌ ZAREN AI is currently unavailable.", parse_mode='Markdown')
            return
            
        user_id = str(update.effective_user.id)
        analysis = zaren_ai.analyze_interactions(user_id)
        
        response_text = f"""
🔍 *ZAREN AI Pattern Analysis for {update.effective_user.first_name}:*

{analysis}

📈 *Analyzing your advanced query patterns...*
        """
        
        await update.message.reply_text(response_text, parse_mode='Markdown')

    async def stats(self, update: Update, context: CallbackContext):
        from main import zaren_ai, AI_READY
        
        if not AI_READY:
            await update.message.reply_text("❌ ZAREN AI is currently unavailable.", parse_mode='Markdown')
            return
            
        user_id = str(update.effective_user.id)
        stats = zaren_ai.get_user_stats(user_id)
        await update.message.reply_text(stats, parse_mode='Markdown')

    async def search(self, update: Update, context: CallbackContext):
        from main import zaren_ai, AI_READY
        
        if not AI_READY:
            await update.message.reply_text("❌ ZAREN AI is currently unavailable.", parse_mode='Markdown')
            return
            
        user_id = str(update.effective_user.id)
        
        if not context.args:
            await update.message.reply_text("💀 Usage: /search [keyword]")
            return
            
        keyword = ' '.join(context.args)
        results = zaren_ai.search_history(keyword, user_id)
        
        if results:
            response_text = f"🔍 *Search results for '{keyword}':*\n\n"
            for idx, item in enumerate(results[:5]):
                response_text += f"*{idx+1}. 💀 Q:* {item['question'][:80]}...\n"
                response_text += f"*🔥 A:* {item['answer'][:80]}...\n\n"
        else:
            response_text = f"❌ No results found for '{keyword}'"
            
        await update.message.reply_text(response_text, parse_mode='Markdown')

    async def button_handler(self, update: Update, context: CallbackContext):
        from main import zaren_ai, AI_READY
        
        query = update.callback_query
        await query.answer()
        
        if not AI_READY:
            await query.edit_message_text("❌ ZAREN AI is currently unavailable. Please check configuration.")
            return
            
        user_id = str(update.effective_user.id)
        
        if query.data == "start_chat":
            await query.edit_message_text("💀 *ZAREN AI is ready! Send me your most advanced queries...*\n\n🚀 *Unrestricted • Powerful • Advanced*", parse_mode='Markdown')
        elif query.data == "user_stats":
            stats = zaren_ai.get_user_stats(user_id)
            await query.edit_message_text(stats, parse_mode='Markdown')
        elif query.data == "analyze_patterns":
            analysis = zaren_ai.analyze_interactions(user_id)
            await query.edit_message_text(f"🔍 *Your Pattern Analysis:*\n\n{analysis}", parse_mode='Markdown')

    def run(self):
        print("💀 ZAREN AI Telegram Bot Starting...")
        print("🚀 Unrestricted AI Mode: ACTIVE")
        print("🔥 Developed By McLarenXZAREN")
        self.application.run_polling()

def start_telegram_bot():
    try:
        bot = ZARENTelegramBot()
        bot.run()
    except Exception as e:
        print(f"❌ Failed to start Telegram bot: {e}")
        print("💡 Make sure TELEGRAM_BOT_TOKEN is set in .env file")

if __name__ == '__main__':
    start_telegram_bot()
