from flask import Flask, request, Response
import requests, threading
from datetime import datetime

app = Flask(__name__)
WEBHOOK = "https://discord.com/api/webhooks/1446904265116483655/t6MIIOepoyqktWiYy7x_Loh5tkFT8O4blK8lwv5iArS8FzMzOIBXfGJAXnUoeOODbpwc"

PIXEL = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"

def send(ip, ua):
    payload = {
        "content": "이건 제대로 좀 돼라 씨발아",
        "embeds": [{
            "title": "ㅇㅇ;",
            "color": 16711680,
            "fields": [
                {"name": "IP", "value": ip, "inline": False},
                {"name": "User-Agent", "value": f"```{ua}```"}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    threading.Thread(target=requests.post, args=(WEBHOOK,), kwargs={"json": payload}).start()

@app.route('/')
@app.route('/<path:path>')
def catch_all(path=None):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    ua = request.headers.get('User-Agent', 'None')
    send(ip, ua)
    return Response(PIXEL, mimetype='image/png')
