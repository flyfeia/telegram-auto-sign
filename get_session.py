from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os
import python_socks  

load_dotenv()

try:
    api_id = int(os.environ['TG_API_ID'])
    api_hash = os.environ['TG_API_HASH']

    CLIENT_PARAMS = {
        'device_model': '82Y5',      # 设备类型
        'system_version': 'Windows 11', # 系统版本
        'app_version': '6.4.2',       # App 版本 (随手填个比较新的)
        'lang_code': 'zh-hans',         # 语言
        'system_lang_code': 'zh-CN'     # 系统语言
    }

except KeyError:
    print("❌ 错误：请检查 .env 文件")
    exit(1)

# --- 代理配置 (修正版) ---
# 使用 python_socks.ProxyType.HTTP
PROXY = (python_socks.ProxyType.HTTP, '127.0.0.1', 10808) 

# 如果你是 SOCKS5 (比如 v2ray 有时候只开 socks)，就用下面这行：
# PROXY = (python_socks.ProxyType.SOCKS5, '127.0.0.1', 10808)

print(f"正在尝试通过代理连接 Telegram... (API_ID: {api_id})")

try:
    with TelegramClient(StringSession(), api_id, api_hash, proxy=PROXY,**CLIENT_PARAMS) as client:
        print("\n✅ 连接成功！")
        print("请将下面这一长串字符复制到 .env 文件里的 TG_SESSION_STRING 后面：\n")
        print(client.session.save())
        print("\n⬆️ 复制上面这一行 ⬆️")
except Exception as e:
    print(f"\n❌ 连接失败: {e}")
    print("请检查：1. 代理端口是否正确 (Clash通常是7890)？ 2. 代理软件开启了吗？")