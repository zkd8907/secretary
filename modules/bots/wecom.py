import requests
import os


def send_markdown_msg(message: str, robot_id: str):
    if os.getenv('DEBUG') == '1' and len(os.getenv('DEBUG_ROBOT_ID', '')) > 0:
        robot_id = os.getenv('DEBUG_ROBOT_ID')

    if len(robot_id) == 0:
        print(message)
        return

    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={robot_id}'
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": message
        }
    }

    requests.post(url, json=data)
