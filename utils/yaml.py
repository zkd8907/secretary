
import os
import re
import yaml


def replace_env_vars(value):
    if isinstance(value, str):
        # 匹配 ${VAR} 或 $VAR 格式
        pattern = r'\$\{([^}]+)\}|\$([A-Za-z0-9_]+)'

        def replace(match):
            # 获取匹配到的环境变量名
            env_var = match.group(1) or match.group(2)
            # 返回环境变量值,如不存在返回空字符串
            return os.getenv(env_var, '')

        return re.sub(pattern, replace, value)
    elif isinstance(value, dict):
        return {k: replace_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [replace_env_vars(item) for item in value]
    return value


def load_config_with_env(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            # 递归处理所有值中的环境变量
            return replace_env_vars(config)
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件 {file_path} 不存在")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"配置文件格式不正确: {e}")
