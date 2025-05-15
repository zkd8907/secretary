import os
import re
import yaml


def replace_env_vars(object):
    """
    Replace environment variables in strings

    Supports replacing environment variables in the format `${VAR}` or `$VAR`, where `VAR` must consist of uppercase letters, numbers, or underscores.
    If the environment variable does not exist, it will be replaced with an empty string.
    :param value: String, dictionary, or list
    :return: String, dictionary, or list with replaced values
    """
    if isinstance(object, str):
        # Match ${VAR} or $VAR format
        pattern = r'\$\{([^}]+)\}|\$([A-Z0-9_]+)'

        def replace(match):
            # Get matched environment variable name
            env_var = match.group(1) or match.group(2)
            # Return environment variable value, return empty string if not exists
            return os.getenv(env_var, '')

        return re.sub(pattern, replace, object)
    elif isinstance(object, dict):
        return {k: replace_env_vars(v) for k, v in object.items()}
    elif isinstance(object, list):
        return [replace_env_vars(item) for item in object]
    return object


def load_config_with_env(file_path):
    """
    Load configuration file and replace environment variables in it
    :param file_path: Path to configuration file
    :return: Configuration dictionary with replaced values
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            # Recursively process all environment variables in values
            return replace_env_vars(config)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file {file_path} does not exist")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Configuration file format is invalid: {e}")
