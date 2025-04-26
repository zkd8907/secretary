import os
import json
import http.client
from urllib.parse import urlparse

def send_qqgroup_msg(message: str, robot_ip: str, group_id: str):
    if os.getenv('DEBUG') == '1':
        print("[Debug Mode]", message)
        return

    parsed = urlparse(robot_ip if "://" in robot_ip else f"http://{robot_ip}")
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    use_https = parsed.scheme == "https"

    conn = http.client.HTTPSConnection(host, port) if use_https else http.client.HTTPConnection(host, port)

    payload = json.dumps({
        "group_id": int(group_id),
        "message": message,
        "auto_escape": False
    })

    headers = {
        'Content-Type': 'application/json',
    }

    # 发送请求
    conn.request("POST", "/send_group_msg", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
