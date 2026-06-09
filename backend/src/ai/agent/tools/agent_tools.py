import datetime
import requests
from ai.rag.rag_service import RagService
from langchain_core.tools import tool



def get_rag_tool(kb_id):
    @tool(description="从RAG本地知识库中检索信息")
    def rag_tool(query: str):
        """
        RAG 检索工具
        返回格式化的 prompt（包含检索结果和回答要求），由 LLM 自行总结
        """
        try:
            # 创建服务实例（只需要 kb_id，不需要模型配置）
            rag_service = RagService(kb_id=kb_id)
            # 调用检索方法
            return rag_service.retrieve_and_format(query)
        except Exception as e:
            return f"RAG 检索失败: {str(e)}"

    return rag_tool

@tool(description="获取当前日期和时间，格式：YYYY-MM-DD HH:MM:SS")
def get_current_time():
    """获取当前系统时间"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


@tool(description="执行数学计算，支持加减乘除、幂运算等，例如：'2 + 3 * 4' 或 'pow(2, 10)'")
def calculator(expression: str):
    """
    安全计算器
    只允许数学运算，防止代码注入
    """
    try:
        # 白名单：只允许数字、运算符和数学函数
        allowed_chars = set("0123456789+-*/().,^ pow sin cos tan sqrt pi e")

        if not all(c in allowed_chars for c in expression.lower()):
            return "错误：表达式包含非法字符"

        # 替换 ^ 为 **
        expression = expression.replace("^", "**")

        # 使用 eval 但限制命名空间
        result = eval(expression, {"__builtins__": {}}, {
            "pow": pow,
            "sin": __import__('math').sin,
            "cos": __import__('math').cos,
            "tan": __import__('math').tan,
            "sqrt": __import__('math').sqrt,
            "pi": __import__('math').pi,
            "e": __import__('math').e,
        })

        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


@tool(description="搜索互联网获取最新信息，参数 query 是搜索关键词")
def web_search(query: str):
    """
    网络搜索工具（使用免费的 DuckDuckGo API）
    注意：需要安装 ddgs 包（原 duckduckgo-search）
    """
    try:
        from ddgs import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

            if not results:
                return "未找到相关搜索结果"

            context = "【网络搜索结果】:\n"
            for i, result in enumerate(results, 1):
                title = result.get('title', '无标题')
                body = result.get('body', '无摘要')
                url = result.get('href', '无链接')

                context += f"[{i}] {title}\n"
                context += f"    摘要: {body}\n"
                context += f"    链接: {url}\n\n"

            return context
    except ImportError:
        return "错误：未安装 ddgs 包，请运行 pip install ddgs"
    except Exception as e:
        error_msg = str(e).lower()

        # 判断常见错误类型
        if "rate limit" in error_msg or "too many requests" in error_msg:
            return "搜索失败：请求过于频繁，请稍后再试"
        elif "connection" in error_msg or "timeout" in error_msg:
            return "搜索失败：网络连接超时，请检查网络或代理设置"
        elif "blocked" in error_msg or "forbidden" in error_msg:
            return "搜索失败：DuckDuckGo 服务暂时不可用，可能是 IP 被限制"
        else:
            return f"搜索失败: {str(e)}"


@tool(description="查询指定城市的天气信息，参数 city 是城市名称（如：北京、上海）")
def get_weather(city: str):
    """
    天气查询工具（使用免费的 Open-Meteo API，无需 API Key）
    """
    try:
        # 城市坐标映射（简化版，实际应该用地理编码 API）
        city_coords = {
            "北京": (39.9042, 116.4074),
            "上海": (31.2304, 121.4737),
            "广州": (23.1291, 113.2644),
            "深圳": (22.5431, 114.0579),
            "杭州": (30.2741, 120.1551),
            "成都": (30.5728, 104.0668),
        }

        if city not in city_coords:
            return f"暂不支持城市: {city}，支持的城市: {', '.join(city_coords.keys())}"

        lat, lon = city_coords[city]

        # 调用 Open-Meteo API
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            weather = data['current_weather']

            temp = weather['temperature']
            windspeed = weather['windspeed']

            # 天气代码映射
            weather_codes = {
                0: "晴朗",
                1: "多云",
                2: "阴天",
                3: "阴",
                45: "雾",
                51: "小雨",
                61: "雨",
                71: "雪",
                95: "雷雨",
            }

            weather_desc = weather_codes.get(weather['weathercode'], "未知")

            return f"{city}当前天气: {weather_desc}, 温度: {temp}°C, 风速: {windspeed} km/h"
        else:
            return f"天气API错误: {response.status_code}"
    except Exception as e:
        return f"查询失败: {str(e)}"