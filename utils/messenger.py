import re
import json
import requests
import copy
from utils.translator import translate


def replace_variables(data, variables: dict):
    """
    Replace business variables in strings

    Supports replacing environment variables in the format `$var`, where `var` must consist of lowercase letters, numbers, or underscores.
    If the environment variable does not exist, no replacement will be performed
    :param data: String, dictionary, or list
    :param variables: Dictionary of variables
    :return: Replaced string, dictionary, or list
    """
    if isinstance(data, str):
        # Match ${VAR} or $VAR format
        pattern = r'\$\{([^}]+)\}|\$([a-z0-9_]+)'

        def replace(match):
            # Get matched environment variable name
            variable_name = match.group(1) or match.group(2)
            # Return environment variable value, return empty string if not exists
            return variables.get(variable_name, match.group(0)).replace('\n', '\\n')

        return re.sub(pattern, replace, data)
    elif isinstance(data, dict):
        return {k: replace_variables(v, variables) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_variables(item, variables) for item in data]
    return data


def send_message(request_config: dict, message_variables: dict):
    """Send HTTP request with translated content and variable substitution"""
    # Create a deep copy to avoid modifying the original request config
    params = copy.deepcopy(request_config)
    
    if 'body' in params:
        # Convert object body to JSON string if needed
        if isinstance(params['body'], (dict, list)):
            params['body'] = json.dumps(params['body'])
        params['body'] = translate(params['body'], message_variables['content'])
    params = replace_variables(params, message_variables)

    print(f"send request: {params}")

    try:
        url = params.get("url")
        method = params.get("method", "GET").upper()
        headers = params.get("headers", {})
        body = params.get("body", None)

        response = requests.request(method, url, headers=headers, data=body)

        if response.status_code >= 200 and response.status_code < 300:
            print(f"Request succeeded with status code {response.status_code}")
            print(f"Response: {response.text}")
        else:
            print(f"Request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            print(f"Request details: {params}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Backward compatibility alias
send = send_message
