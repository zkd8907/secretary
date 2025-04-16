import requests


def send_markdown_msg(message: str, robot_id: str):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={robot_id}'
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": message
        }
    }

    requests.post(url, json=data)
