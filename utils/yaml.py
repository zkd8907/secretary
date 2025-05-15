
import os
import re
import yaml


def replace_env_vars(object):
    """
    替换字符串中的环境变量

    支持替换格式为 `${VAR}` 或 `$VAR` 的环境变量，其中 `VAR` 必须由大写字母、数字或下划线组成。
    如果环境变量不存在，则会替换为空字符串。
    :param value: 字符串、字典或列表
    :return: 替换后的字符串、字典或列表
    """
    if isinstance(object, str):
        # 匹配 ${VAR} 或 $VAR 格式
        pattern = r'\$\{([^}]+)\}|\$([A-Z0-9_]+)'

        def replace(match):
            # 获取匹配到的环境变量名
            env_var = match.group(1) or match.group(2)
            # 返回环境变量值,如不存在返回空字符串
            return os.getenv(env_var, '')

        return re.sub(pattern, replace, object)
    elif isinstance(object, dict):
        return {k: replace_env_vars(v) for k, v in object.items()}
    elif isinstance(object, list):
        return [replace_env_vars(item) for item in object]
    return object


def load_config_with_env(file_path):
    """
    加载配置文件并替换其中的环境变量
    :param file_path: 配置文件路径
    :return: 替换后的配置字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            # 递归处理所有值中的环境变量
            return replace_env_vars(config)
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件 {file_path} 不存在")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"配置文件格式不正确: {e}")
