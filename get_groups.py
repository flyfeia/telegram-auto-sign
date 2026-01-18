import os
import asyncio
import python_socks
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

api_id = int(os.environ['TG_API_ID'])
api_hash = os.environ['TG_API_HASH']
session_string = os.environ['TG_SESSION_STRING']

# --- 自动检测代理配置 (和你之前的 main.py 一样) ---
proxy_args = None
if os.environ.get('TG_PROXY_PORT'):
    proxy_port = int(os.environ['TG_PROXY_PORT'])
    proxy_args = (python_socks.ProxyType.HTTP, '127.0.0.1', proxy_port)

async def main():
    print("正在连接 Telegram 获取群组列表...")
    
    async with TelegramClient(StringSession(session_string), api_id, api_hash, proxy=proxy_args) as client:
        # 获取对话列表
        dialogs = await client.get_dialogs()
        
        print("\n" + "="*50)
        print(f"{'群组/频道名称':<30} | {'ID (复制这个)'}")
        print("="*50)
        
        for dialog in dialogs:
            # 只显示群组 (Group) 和 频道 (Channel)
            if dialog.is_group or dialog.is_channel:
                # 打印 ID 和 名称
                print(f"{dialog.title:<30} | {dialog.id}")
        
        print("="*50)
        print("请将上面的 ID (带负号) 填入 config.json")

if __name__ == '__main__':
    asyncio.run(main())