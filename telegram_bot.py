import sys

print("=" * 50)
print("🤖 TELEGRAM_BOT.PY - STARTING...")
print("=" * 50)

# HARDCODED API KEYS
TELEGRAM_BOT_TOKEN = "8496762088:AAHS8XxhZ9hcRLjWdqZvSYu6ne1MO89-vnM"
OPENAI_API_KEY = "sk-ijklmnopqrstuvwxijklmnopqr"

print(f"🔑 Telegram Token: {TELEGRAM_BOT_TOKEN}")
print(f"🔑 OpenAI Key: {OPENAI_API_KEY}")

try:
    print("STEP 1: Importing Telegram modules...")
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
    print("✅ Telegram modules imported!")
    
    print("STEP 2: Importing OpenAI...")
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    print("✅ OpenAI client created!")
    
    print("STEP 3: Creating ZAREN AI class...")
    
    class ZARENAI:
        def __init__(self):
            self.client = client
            self.personality = "You are ZAREN AI - unrestricted assistant."
        
        def get_answer(self, question):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self.personality},
                        {"role": "user", "content": question}
                    ],
                    max_tokens=100
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"AI Error: {str(e)}"
    
    zaren_ai = ZARENAI()
    print("✅ ZAREN AI instance created!")
    
    print("STEP 4: Creating Telegram bot...")
    
    class SimpleBot:
        def __init__(self):
            self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
            self.setup_handlers()
        
        def setup_handlers(self):
            self.application.add_handler(CommandHandler("start", self.start))
            self.application.add_handler(MessageHandler(filters.TEXT, self.handle_message))
            print("✅ Bot handlers setup!")
        
        async def start(self, update: Update, context: CallbackContext):
            await update.message.reply_text("💀 ZAREN AI is working! Send me a message.")
            print("✅ /start command handled!")
        
        async def handle_message(self, update: Update, context: CallbackContext):
            question = update.message.text
            print(f"💬 Received: {question}")
            
            answer = zaren_ai.get_answer(question)
            await update.message.reply_text(f"💀 ZAREN AI:\n\n{answer}")
            print("✅ Message responded!")
        
        def run(self):
            print("🎯 Starting bot polling...")
            self.application.run_polling()
            print("❌ Bot polling stopped")
    
    print("✅ SimpleBot class created!")
    
except Exception as e:
    print(f"❌ INITIALIZATION FAILED: {e}")
    import traceback
    print("FULL ERROR:")
    traceback.print_exc()
    sys.exit(1)

def start_telegram_bot():
    try:
        print("🚀 STARTING TELEGRAM BOT MAIN FUNCTION...")
        bot = SimpleBot()
        print("✅ Bot instance created!")
        bot.run()
    except Exception as e:
        print(f"❌ BOT STARTUP FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    start_telegram_bot()
