import re
import requests
from utils.translator import translate


def replace_vars(object, variables: dict):
    """
    Replace business variables in strings

    Supports replacing environment variables in the format `$var`, where `var` must consist of lowercase letters, numbers, or underscores.
    If the environment variable does not exist, no replacement will be performed
    :param value: String, dictionary, or list
    :param variables: Dictionary of variables
    :return: Replaced string, dictionary, or list
    """
    if isinstance(object, str):
        # Match ${VAR} or $VAR format
        pattern = r'\$\{([^}]+)\}|\$([a-z0-9_]+)'

        def replace(match):
            # Get matched environment variable name
            variables_name = match.group(1) or match.group(2)
            # Return environment variable value, return empty string if not exists
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
