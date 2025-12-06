from flask import Flask, request, send_from_directory, render_template
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = "logs/grabbed.txt"

if not os.path.exists("logs"):
    os.makedirs("logs")

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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_grab(ip, ua, timestamp)
    # send_to_discord(ip, ua, timestamp)
    
    # 1x1 투명 픽셀 반환 (시발 핵심)
    return send_from_directory('static', 'grabber.png'), 200, {
        'Content-Type': 'image/png',
        'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
