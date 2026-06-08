"""
敏感信息处理工具
"""

def mask_api_key(api_key: str) -> str:
    """
    API Key 脱敏
    """
    if not api_key:
        return ""

    length = len(api_key)

    # 太短就全脱敏
    if length <= 12:
        return "*" * length

    # 核心：前8位 + 中间全* + 后4位，长度不变
    prefix = api_key[:8]
    suffix = api_key[-4:]
    middle = "*" * (length - 8 - 4)

    return prefix + middle + suffix