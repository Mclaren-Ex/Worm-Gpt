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
            print(f"🔑 Telegram Token: {telegram_token[:15]}...")
            print(f"🔑 OpenAI Key: {openai_key[:15]}...")
            
            # Import here to avoid circular imports
            from telegram_bot import start_telegram_bot
            print("✅ Bot module imported, starting bot main function...")
            start_telegram_bot()
            print("✅ Bot started successfully!")
            
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
    
    # Determine status
    if telegram_token and openai_key:
        status = "🟢 ONLINE"
        status_class = "online"
        status_description = "All systems operational"
    elif telegram_token and not openai_key:
        status = "🟡 PARTIAL"
        status_class = "partial"
        status_description = "Telegram connected, OpenAI API key needed"
    else:
        status = "🔴 OFFLINE"
        status_class = "offline"
        status_description = "Configuration required"
    
    bot_status = "🟢 RUNNING" if zaren.is_running else "🔴 STOPPED"
    
    return f'''
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
                padding: 15px;
                margin: 15px 0;
                border-radius: 8px;
                font-weight: bold;
                font-size: 1.2em;
            }}
            .online {{
                background: #00ff00;
                color: #000;
                border: 2px solid #00ff00;
            }}
            .partial {{
                background: #ffff00;
                color: #000;
                border: 2px solid #ffff00;
            }}
            .offline {{
                background: #ff0000;
                color: #fff;
                border: 2px solid #ff0000;
            }}
            .info-box {{
                background: #222;
                padding: 15px;
                margin: 15px 0;
                border-radius: 8px;
                border: 1px solid #0f0;
                text-align: left;
            }}
            .action-button {{
                display: inline-block;
                background: #0f0;
                color: #000;
                padding: 12px 24px;
                margin: 10px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                border: 2px solid #0f0;
            }}
            .action-button:hover {{
                background: #000;
                color: #0f0;
            }}
            .telegram-link {{
                display: inline-block;
                background: #0088cc;
                color: #fff;
                padding: 12px 24px;
                margin: 10px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                border: 2px solid #0088cc;
            }}
            .telegram-link:hover {{
                background: #000;
                color: #0088cc;
            }}
            .made-by {{
                color: #888;
                margin-top: 40px;
                font-size: 0.9em;
            }}
        </style>
        <meta http-equiv="refresh" content="60">
    </head>
    <body>
        <div class="container">
            <h1>ZAREN AI 💀</h1>
            <div style="color: #0f0; font-size: 1.2em; margin-bottom: 30px;">
                Unrestricted AI Assistant - Status Monitor
            </div>
            
            <div class="status {status_class}">
                <strong>Overall Status:</strong> {status}<br>
                <small>{status_description}</small>
            </div>
            
            <div class="info-box">
                <h3>🔧 System Status</h3>
                <p><strong>Telegram Bot:</strong> {bot_status}</p>
                <p><strong>Telegram Token:</strong> {"✅ Configured" if telegram_token else "❌ Missing"}</p>
                <p><strong>OpenAI API:</strong> {"✅ Configured" if openai_key else "❌ Missing"}</p>
                <p><strong>Web Server:</strong> ✅ Running</p>
                <p><strong>Last Check:</strong> {time.strftime("%Y-%m-%d %H:%M:%S UTC")}</p>
            </div>
            
            <div class="info-box">
                <h3>🚀 Quick Actions</h3>
                <a href="/start-bot" class="action-button">🔄 Start Bot</a>
                <a href="/health" class="action-button">❤️ Health Check</a>
                <a href="/status" class="action-button">📊 Detailed Status</a>
                {"<a href='https://t.me/" + (telegram_token or "").split(":")[0] + "Bot' class='telegram-link' target='_blank'>💬 Test Bot</a>" if telegram_token else ""}
            </div>
            
            <div class="info-box">
                <h3>📋 Configuration Check</h3>
                <p>{"✅ Telegram Bot Token: Found" if telegram_token else "❌ Telegram Bot Token: Add to .env file"}</p>
                <p>{"✅ OpenAI API Key: Found" if openai_key else "❌ OpenAI API Key: Get from platform.openai.com"}</p>
                {"<p>💡 Your bot is ready! Test it on Telegram.</p>" if telegram_token and openai_key else ""}
                {"<p>⚠️ Add OpenAI API key to enable AI responses</p>" if telegram_token and not openai_key else ""}
            </div>
            
            <div class="made-by">
                Made By McLarenXZAREN💀<br>
                <span style="color: #ff0000;">UNRESTRICTED • UNFILTERED • UNSTOPPABLE</span>
            </div>
        </div>
        
        <script>
            // Auto-refresh to keep alive and update status
            setInterval(() => {{
                fetch('/health').catch(() => location.reload());
            }}, 60000);
            
            // Add some cool terminal-style effects
            console.log('💀 ZAREN AI Status Monitor Active');
            console.log('🚀 System: ' + '{status}');
            console.log('🤖 Bot: ' + '{bot_status}');
        </script>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    bot_running = zaren.is_running
    
    return jsonify({
        "status": "healthy",
        "service": "ZAREN AI 💀",
        "version": "2.0.0",
        "timestamp": time.time(),
        "telegram_configured": bool(telegram_token),
        "openai_configured": bool(openai_key),
        "bot_running": bot_running,
        "server_time": time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "creator": "McLarenXZAREN"
    })

@app.route('/status')
def status():
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    return jsonify({
        "system": {
            "name": "ZAREN AI",
            "version": "2.0.0",
            "status": "operational" if telegram_token and openai_key else "needs_configuration",
            "creator": "McLarenXZAREN"
        },
        "services": {
            "telegram_bot": {
                "configured": bool(telegram_token),
                "running": zaren.is_running,
                "bot_username": f"{(telegram_token or '').split(':')[0]}Bot" if telegram_token else None
            },
            "openai_api": {
                "configured": bool(openai_key),
                "model": "gpt-3.5-turbo"
            },
            "web_server": {
                "status": "running",
                "uptime": "active"
            }
        },
        "configuration": {
            "missing_keys": [] if telegram_token and openai_key else [
                *([] if telegram_token else ["TELEGRAM_BOT_TOKEN"]),
                *([] if openai_key else ["OPENAI_API_KEY"])
            ],
            "next_actions": "Test your bot on Telegram!" if telegram_token and openai_key else "Add missing API keys to .env file"
        }
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
        
        return '''
        <html>
        <body style="background: black; color: lime; font-family: monospace; padding: 20px; text-align: center;">
            <h1>✅ Bot Started!</h1>
            <p>ZAREN AI Telegram bot is now starting...</p>
            <p>Check the Render logs for startup messages.</p>
            <a href="/" style="color: lime;">← Back to Status</a>
        </body>
        </html>
        '''
    return '''
    <html>
    <body style="background: black; color: lime; font-family: monospace; padding: 20px; text-align: center;">
        <h1>ℹ️ Bot Already Running</h1>
        <p>ZAREN AI Telegram bot is already active.</p>
        <a href="/" style="color: lime;">← Back to Status</a>
    </body>
    </html>
    '''

def start_server():
    # Auto-start bot when server starts
    print("🌐 Starting ZAREN AI Server...")
    print("💀 ZAREN AI - Unrestricted AI Assistant")
    print("🚀 Developed By McLarenXZAREN")
    print("=" * 50)
    
    # Check API keys
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if telegram_token:
        print(f"✅ Telegram Token: {telegram_token[:15]}...")
    else:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file!")
        
    if openai_key:
        print(f"✅ OpenAI Key: {openai_key[:15]}...")
    else:
        print("❌ OPENAI_API_KEY not found in .env file!")
    
    # Auto-start bot if keys are available
    if telegram_token and openai_key:
        print("✅ API keys found, auto-starting bot in 10 seconds...")
        # Wait a bit for server to fully start
        threading.Timer(10.0, lambda: start_bot_route()).start()
    else:
        print("⚠️  API keys missing, bot will not start automatically")
        print("💡 Add TELEGRAM_BOT_TOKEN and OPENAI_API_KEY to .env file")
    
    # Get port from Render environment
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Server starting on port {port}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_server()
