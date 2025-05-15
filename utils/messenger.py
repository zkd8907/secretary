

import re
import requests
from utils.translator import translate


def replace_vars(object, variables: dict):
    """
    替换字符串中的业务变量

    支持替换格式为 `$var` 的环境变量，其中 `var` 必须由小写字母、数字或下划线组成。
    如果环境变量不存在，则不会做任何替换操作
    :param value: 字符串、字典或列表
    :param variables: 变量字典
    :return: 替换后的字符串、字典或列表
    """
    if isinstance(object, str):
        # 匹配 ${VAR} 或 $VAR 格式
        pattern = r'\$\{([^}]+)\}|\$([a-z0-9_]+)'

        def replace(match):
            # 获取匹配到的环境变量名
            variables_name = match.group(1) or match.group(2)
            # 返回环境变量值,如不存在返回空字符串
            return variables.get(variables_name, match.group(0)).replace('\n', '\\n')

        return re.sub(pattern, replace, object)
    elif isinstance(object, dict):
        return {k: replace_vars(v, variables) for k, v in object.items()}
    elif isinstance(object, list):
        return [replace_vars(item, variables) for item in object]
    return object


def send(request_params: dict, variables: dict):
    request_params = replace_vars(request_params, variables)
    if 'body' in request_params:
        request_params['body'] = translate(
            request_params['body'], variables['content'])

    print(f"send request: {request_params}")

    try:
        url = request_params.get("url")
        method = request_params.get("method", "GET").upper()
        headers = request_params.get("headers", {})
        body = request_params.get("body", None)

        response = requests.request(method, url, headers=headers, data=body)

        if response.status_code >= 200 and response.status_code < 300:
            print(f"Request succeeded with status code {response.status_code}")
            print(f"Response: {response.text}")
        else:
            print(f"Request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            print(f"Request details: {request_params}")

    except Exception as e:
        print(f"An error occurred: {e}")
