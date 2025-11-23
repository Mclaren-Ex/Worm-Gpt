from flask import Flask, request, jsonify
import threading
import time
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

class ZARENAI:
    def __init__(self):
        self.is_running = False
        self.bot_thread = None
        
    def start_bot(self):
        """Start the Telegram bot in a separate thread"""
        try:
            print("🤖 Starting Telegram Bot...")
            
            # Check if API keys are available
            telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
            openai_key = os.getenv('OPENAI_API_KEY')
            
            if not telegram_token:
                print("❌ TELEGRAM_BOT_TOKEN not found!")
                return
                
            if not openai_key:
                print("❌ OPENAI_API_KEY not found!")
                return
                
            print("✅ API keys found, starting bot...")
            
            # Import here to avoid circular imports
            from telegram_bot import start_telegram_bot
            start_telegram_bot()
            
        except Exception as e:
            print(f"❌ Bot failed to start: {e}")
            import traceback
            traceback.print_exc()
            
    def keep_alive(self):
        """Background thread to keep the bot running"""
        while True:
            try:
                # Get the actual Render URL
                render_url = os.getenv('RENDER_EXTERNAL_URL', 'https://your-app.onrender.com')
                response = requests.get(f'{render_url}/health', timeout=10)
                print(f"✅ Keep-alive ping: {response.status_code}")
                time.sleep(300)  # 5 minutes
            except Exception as e:
                print(f"❌ Keep-alive failed: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

zaren = ZARENAI()

@app.route('/')
def home():
    # Check API key status
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    status = "🟢 ONLINE" if telegram_token and openai_key else "🔴 CONFIGURATION NEEDED"
    bot_status = "🟢 RUNNING" if zaren.is_running else "🔴 STOPPED"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ZAREN AI 💀</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #000; color: #0f0; }}
            .container {{ max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #0f0; }}
            .status {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .online {{ background: #00ff00; color: #000; }}
            .offline {{ background: #ff0000; color: #fff; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ZAREN AI 💀 Status</h1>
            
            <div class="status {'online' if telegram_token and openai_key else 'offline'}">
                <strong>Overall Status:</strong> {status}
            </div>
            
            <div class="status {'online' if zaren.is_running else 'offline'}">
                <strong>Telegram Bot:</strong> {bot_status}
            </div>
            
            <div>
                <h3>API Key Status:</h3>
                <p>Telegram Token: {'✅ Found' if telegram_token else '❌ Missing'}</p>
                <p>OpenAI Key: {'✅ Found' if openai_key else '❌ Missing'}</p>
            </div>
            
            <div>
                <h3>Actions:</h3>
                <p><a href="/start-bot" style="color: #0f0;">Start Bot</a></p>
                <p><a href="/health" style="color: #0f0;">Health Check</a></p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    bot_running = zaren.is_running
    
    return jsonify({
        "status": "healthy",
        "telegram_configured": bool(telegram_token),
        "openai_configured": bool(openai_key),
        "bot_running": bot_running,
        "service": "ZAREN AI"
    })

@app.route('/start-bot')
def start_bot_route():
    if not zaren.is_running:
        print("🚀 Starting bot via web request...")
        zaren.bot_thread = threading.Thread(target=zaren.start_bot, daemon=True)
        zaren.bot_thread.start()
        zaren.is_running = True
        
        # Start keep-alive thread
        keep_alive_thread = threading.Thread(target=zaren.keep_alive, daemon=True)
        keep_alive_thread.start()
        
        return jsonify({"status": "Bot started successfully", "bot_running": True})
    return jsonify({"status": "Bot already running", "bot_running": True})

def start_server():
    # Auto-start bot when server starts
    print("🌐 Starting ZAREN AI Server...")
    
    # Check API keys
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not telegram_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file!")
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in .env file!")
    
    if telegram_token and openai_key:
        print("✅ API keys found, auto-starting bot...")
        start_bot_route()
    else:
        print("⚠️  API keys missing, bot will not start automatically")
    
    # Get port from Render environment
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Server starting on port {port}")
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_server()
