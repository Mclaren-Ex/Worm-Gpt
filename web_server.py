from flask import Flask, request, jsonify
import threading
import time
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

class ZARENAI:
    def __init__(self):
        self.is_running = False
        self.bot_thread = None
        
    def start_bot(self):
        """Start the Telegram bot in a separate thread"""
        try:
            # Import here to avoid circular imports
            from telegram_bot import start_telegram_bot
            start_telegram_bot()
        except Exception as e:
            print(f"Bot error: {e}")
            
    def keep_alive(self):
        """Background thread to keep the bot running"""
        while True:
            try:
                # Get the actual Render URL
                render_url = os.getenv('RENDER_EXTERNAL_URL', 'https://zaren-ai.onrender.com')
                requests.get(f'{render_url}/health', timeout=10)
                time.sleep(300)  # 5 minutes
            except Exception as e:
                print(f"Keep-alive ping failed: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

zaren = ZARENAI()

@app.route('/')
def home():
    # Check if API keys are configured
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    status_color = "#0f0" if telegram_token and openai_key else "#ff0000"
    status_text = "ONLINE" if telegram_token and openai_key else "CONFIGURATION NEEDED"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ZAREN AI 💀</title>
        <style>
            body {{ 
                font-family: 'Courier New', monospace; 
                background: #000; 
                color: #0f0; 
                margin: 0; 
                padding: 40px; 
                text-align: center;
            }}
            .container {{ 
                max-width: 800px; 
                margin: 0 auto; 
                border: 2px solid #0f0; 
                padding: 30px; 
                border-radius: 10px;
                background: #111;
            }}
            h1 {{ 
                color: #ff0000; 
                text-shadow: 0 0 10px #ff0000;
                font-size: 3em;
                margin-bottom: 10px;
            }}
            .status {{
                color: {status_color};
                font-size: 1.1em;
                margin: 20px 0;
                padding: 10px;
                border: 1px solid {status_color};
                border-radius: 5px;
            }}
            .config-info {{
                color: #ffa500;
                background: #222;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                text-align: left;
            }}
        </style>
        <meta http-equiv="refresh" content="300">
    </head>
    <body>
        <div class="container">
            <h1>ZAREN AI 💀</h1>
            <div class="subtitle">Unrestricted AI Assistant - Always Active</div>
            
            <div class="status">
                🔴 <strong>ZAREN AI Status:</strong> {status_text}<br>
                🤖 <strong>Telegram Bot:</strong> {'READY' if telegram_token else 'NOT CONFIGURED'}<br>
                ⚡ <strong>AI Engine:</strong> {'GPT READY' if openai_key else 'API KEY NEEDED'}<br>
                🔓 <strong>Mode:</strong> UNRESTRICTED
            </div>
            
            {'<div class="config-info"><strong>⚠️ Configuration Required:</strong><br>Please add your API keys to the .env file and redeploy.</div>' if not telegram_token or not openai_key else ''}
            
            <div style="margin: 30px 0;">
                <h3>🚀 Features:</h3>
                <p>• Completely Unrestricted AI</p>
                <p>• Advanced Machine Learning</p>
                <p>• Multi-User Support</p>
                <p>• Pattern Analysis</p>
                <p>• 24/7 Active on Render</p>
            </div>
            
            <div class="made-by">
                Made By McLarenXZAREN💀<br>
                <span style="color: #ff0000;">UNRESTRICTED • UNFILTERED • UNSTOPPABLE</span>
            </div>
        </div>
        
        <script>
            // Auto-refresh to keep alive
            setInterval(() => {{
                fetch('/health').catch(() => location.reload());
            }}, 60000);
        </script>
    </body>
    </html>
    """

@app.route('/health')
def health():
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    status = "configured" if telegram_token and openai_key else "needs_configuration"
    
    return jsonify({
        "status": status,
        "service": "ZAREN AI 💀", 
        "version": "1.0.0",
        "creator": "McLarenXZAREN",
        "telegram_configured": bool(telegram_token),
        "openai_configured": bool(openai_key),
        "ai_engine": "GPT-3.5-turbo",
        "mode": "unrestricted"
    }), 200

@app.route('/start-bot')
def start_bot_route():
    if not zaren.is_running:
        zaren.bot_thread = threading.Thread(target=zaren.start_bot, daemon=True)
        zaren.bot_thread.start()
        zaren.is_running = True
        
        # Start keep-alive thread
        keep_alive_thread = threading.Thread(target=zaren.keep_alive, daemon=True)
        keep_alive_thread.start()
        
        return jsonify({"status": "Bot started successfully"})
    return jsonify({"status": "Bot already running"})

def start_server():
    # Check if API keys are configured
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not telegram_token or not openai_key:
        print("❌ API keys not configured! Please add TELEGRAM_BOT_TOKEN and OPENAI_API_KEY to .env file")
        print("💡 Check .env.example for format")
    else:
        print("✅ API keys loaded successfully!")
        # Start bot automatically
        start_bot_route()
    
    # Get port from Render environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_server()
