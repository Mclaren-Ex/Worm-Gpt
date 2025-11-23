from flask import Flask
import threading
import time
import requests
import sys

app = Flask(__name__)

# HARDCODED API KEYS
TELEGRAM_BOT_TOKEN = "8496762088:AAHS8XxhZ9hcRLjWdqZvSYu6ne1MO89-vnM"
OPENAI_API_KEY = "sk-ijklmnopqrstuvwxijklmnopqr"

print("🚀 WEB SERVER STARTING...")
print(f"Python version: {sys.version}")
print(f"Telegram token: {TELEGRAM_BOT_TOKEN}")
print(f"OpenAI key: {OPENAI_API_KEY}")

class ZARENAI:
    def __init__(self):
        self.is_running = False
        self.bot_thread = None
        
    def start_bot(self):
        try:
            print("🤖 BOT THREAD STARTED!")
            print("STEP 1: Importing telegram_bot...")
            
            # Import the bot module
            from telegram_bot import start_telegram_bot
            
            print("STEP 2: Calling start_telegram_bot()...")
            
            # Start the bot
            start_telegram_bot()
            
            print("STEP 3: Bot function completed!")
            
        except Exception as e:
            print(f"❌ BOT THREAD CRASHED: {e}")
            import traceback
            print("FULL TRACEBACK:")
            traceback.print_exc()

zaren = ZARENAI()

@app.route('/')
def home():
    return f"""
    <html>
    <head>
        <title>ZAREN AI 💀 DEBUG</title>
        <style>
            body {{
                background: black;
                color: lime;
                font-family: monospace;
                padding: 40px;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                border: 2px solid lime;
                padding: 30px;
            }}
            .status {{
                background: {'#00ff00' if zaren.is_running else '#ff0000'};
                color: black;
                padding: 15px;
                margin: 15px 0;
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
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💀 ZAREN AI - DEBUG MODE</h1>
            
            <div class="status">
                BOT STATUS: {'RUNNING' if zaren.is_running else 'STOPPED'}
            </div>
            
            <p>Check Render logs for detailed startup messages</p>
            
            <a href="/start-bot" class="button">🚀 START BOT</a>
            <a href="https://t.me/8496762088Bot" class="button" target="_blank">💬 TEST BOT</a>
            <a href="/logs" class="button">📋 VIEW LOG HELP</a>
            
            <div style="margin-top: 30px; color: #888;">
                Made By McLarenXZAREN💀
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/start-bot')
def start_bot_route():
    print("🔄 /start-bot ROUTE CALLED!")
    
    if not zaren.is_running:
        print("🤖 CREATING BOT THREAD...")
        zaren.bot_thread = threading.Thread(target=zaren.start_bot)
        zaren.bot_thread.daemon = True
        zaren.bot_thread.start()
        zaren.is_running = True
        print("✅ BOT THREAD STARTED!")
        
        return """
        <html>
        <body style="background: black; color: lime; font-family: monospace; padding: 20px; text-align: center;">
            <h1>✅ BOT START COMMAND SENT!</h1>
            <p>Check Render logs for startup messages...</p>
            <p>Look for: "BOT THREAD STARTED" and "STEP 1, 2, 3"</p>
            <a href="/" style="color: lime;">← BACK TO STATUS</a>
        </body>
        </html>
        """
    else:
        return """
        <html>
        <body style="background: black; color: lime; font-family: monospace; padding: 20px; text-align: center;">
            <h1>✅ BOT ALREADY RUNNING</h1>
            <a href="/" style="color: lime;">← BACK TO STATUS</a>
        </body>
        </html>
        """

@app.route('/logs')
def show_logs():
    return """
    <html>
    <body style="background: black; color: lime; font-family: monospace; padding: 20px;">
        <h1>📋 HOW TO CHECK LOGS</h1>
        <p>1. Go to <a href="https://render.com" style="color: lime;">render.com</a></p>
        <p>2. Click your "zaren-ai" service</p>
        <p>3. Click "Logs" tab</p>
        <p>4. Look for these messages:</p>
        <ul>
            <li>"🚀 WEB SERVER STARTING..."</li>
            <li>"🤖 BOT THREAD STARTED!"</li>
            <li>"STEP 1: Importing telegram_bot..."</li>
            <li>Any red error messages</li>
        </ul>
        <a href="/" style="color: lime;">← BACK TO STATUS</a>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "💀 ZAREN AI - HEALTHY", 200

def start_server():
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 STARTING FLASK SERVER ON PORT {port}...")
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_server()
