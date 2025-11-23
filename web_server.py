from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

# HARDCODED API KEYS
TELEGRAM_BOT_TOKEN = "8496762088:AAHS8XxhZ9hcRLjWdqZvSYu6ne1MO89-vnM"
OPENAI_API_KEY = "sk-ijklmnopqrstuvwxijklmnopqr"

class ZARENAI:
    def __init__(self):
        self.is_running = False
        
    def start_bot(self):
        try:
            print("🤖 STARTING ZAREN AI BOT...")
            print(f"🔑 Telegram Token: {TELEGRAM_BOT_TOKEN[:15]}...")
            print(f"🔑 OpenAI Key: {OPENAI_API_KEY[:15]}...")
            
            # Import and start bot
            from telegram_bot import start_telegram_bot
            print("✅ Starting bot main function...")
            start_telegram_bot()
            
        except Exception as e:
            print(f"❌ BOT CRASHED: {e}")
            import traceback
            traceback.print_exc()

zaren = ZARENAI()

@app.route('/')
def home():
    return f"""
    <html>
    <head>
        <title>ZAREN AI 💀</title>
        <style>
            body {{
                background: black;
                color: lime;
                font-family: monospace;
                padding: 40px;
                text-align: center;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                border: 2px solid lime;
                padding: 30px;
                border-radius: 10px;
            }}
            .status {{
                background: #00ff00;
                color: black;
                padding: 15px;
                margin: 15px 0;
                border-radius: 8px;
                font-weight: bold;
            }}
            .button {{
                background: lime;
                color: black;
                padding: 15px 30px;
                margin: 10px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 18px;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💀 ZAREN AI</h1>
            <p>Unrestricted AI Assistant - Hardcoded Version</p>
            
            <div class="status">
                🔑 API Keys: HARDCODED ✅<br>
                🤖 Bot Status: {'RUNNING' if zaren.is_running else 'READY TO START'}
            </div>
            
            <a href="/start-bot" class="button">🚀 START BOT</a>
            <br>
            <a href="https://t.me/8496762088Bot" class="button" target="_blank">💬 TEST BOT</a>
            
            <div style="margin-top: 30px; color: #888;">
                Made By McLarenXZAREN💀
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/start-bot')
def start_bot_route():
    if not zaren.is_running:
        print("🔄 MANUAL BOT START REQUESTED")
        bot_thread = threading.Thread(target=zaren.start_bot, daemon=True)
        bot_thread.start()
        zaren.is_running = True
        
        # Keep-alive thread
        def keep_alive():
            while True:
                try:
                    requests.get('https://worm-gpt22.onrender.com/health', timeout=10)
                    time.sleep(300)
                except:
                    time.sleep(60)
        
        keep_thread = threading.Thread(target=keep_alive, daemon=True)
        keep_thread.start()
        
        return """
        <html>
        <body style="background: black; color: lime; font-family: monospace; padding: 20px; text-align: center;">
            <h1>✅ BOT STARTED!</h1>
            <p>ZAREN AI is now running...</p>
            <p>Check Render logs for status.</p>
            <a href="/" style="color: lime;">← BACK</a>
        </body>
        </html>
        """
    return """
    <html>
    <body style="background: black; color: lime; font-family: monospace; padding: 20px; text-align: center;">
        <h1>✅ BOT ALREADY RUNNING</h1>
        <a href="/" style="color: lime;">← BACK</a>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "💀 ZAREN AI - HEALTHY", 200

def start_server():
    port = int(os.environ.get("PORT", 5000))
    print("🚀 ZAREN AI SERVER STARTING...")
    print("💀 HARDCODED VERSION - NO .env FILES")
    print(f"🔑 Telegram: {TELEGRAM_BOT_TOKEN}")
    print(f"🔑 OpenAI: {OPENAI_API_KEY}")
    print("=" * 50)
    
    # Auto-start bot after 5 seconds
    def auto_start():
        time.sleep(5)
        if not zaren.is_running:
            print("🤖 AUTO-STARTING BOT...")
            start_bot_route()
    
    threading.Thread(target=auto_start, daemon=True).start()
    
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_server()
