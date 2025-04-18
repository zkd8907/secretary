import http.client
import json
import os


def send_wechat_msg(message: str, robot_ip: str, robot_token: str, robot_app_id: str, robot_chatroom_id: str):
    if os.getenv('DEBUG') == '1' or len(robot_token) == 0:
        print(message)
        return

    conn = http.client.HTTPConnection(robot_ip, 2531)
    payload = json.dumps({
        "appId": robot_app_id,
        "toWxid": robot_chatroom_id,
        "ats": "",
        "content": message
    })
    headers = {
        'X-GEWE-TOKEN': robot_token,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v2/api/message/postText", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
