import os
import json
import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import python_socks  


# --- 加载本地 .env (用于本地测试) ---
load_dotenv()

# --- 配置读取 ---
try:
    API_ID = int(os.environ['TG_API_ID'])
    API_HASH = os.environ['TG_API_HASH']
    SESSION_STRING = os.environ['TG_SESSION_STRING']

    config_str = os.environ.get('TG_CONFIG_JSON')
    if not config_str:
        raise KeyError("TG_CONFIG_JSON")
        
    CONFIG = json.loads(config_str)
    print("✅ 成功从环境变量加载配置")
except KeyError as e:
    print(f"❌ 严重错误: 缺少环境变量 {e}")
    exit(1)


# --- 全局设置 ---
TEST_MODE = os.environ.get('TEST_MODE')  # ✅ 本地测试设为 True，部署时改为 False ;True 直接跑通，false 程序自由调用

# 把自己伪装成 Windows 10 上的 Telegram 官方桌面版
# 这样服务器看到的设备就是 "Desktop" 而不是 "Python Script"
CLIENT_PARAMS = {
    'device_model': '82Y5',      # 设备类型
    'system_version': 'Windows 11', # 系统版本
    'app_version': '6.4.2',       # App 版本 (随手填个比较新的)
    'lang_code': 'zh-hans',         # 语言
    'system_lang_code': 'zh-CN'     # 系统语言
}

async def work_with_bot(client, bot_config):
    """处理机器人签到任务 (修复版)"""
    target = bot_config['username']
    cmd = bot_config.get('command', bot_config['command'])
    btn_text = bot_config.get('button_text', bot_config['button_text'])
    
    print(f"\n🤖 正在执行 Bot 任务: {target} ({bot_config.get('note', '')})")

    try:
        # 关键修改：先建立会话上下文 (conversation)，然后再在里面发送消息
        # exclusive=False 允许你在其他地方同时也操作这个bot，防止锁死
        async with client.conversation(target, timeout=30, exclusive=False) as conv:
            
            await client.send_read_acknowledge(target)

            # 随机延迟 1-3 秒再发命令
            await asyncio.sleep(random.uniform(1, 3))
            # 1. 使用 conv.send_message 而不是 client.send_message
            # 这样 Telethon 才知道这一发一收是对应的一组
            await conv.send_message(cmd)
            print(f"   📤 发送命令: {cmd}")

            # 2. 获取回复
            # 这里的 get_response 会自动等待针对上面那条消息的回复
            response = await conv.get_response()
            print(f"   📩 收到回复，寻找按钮包含: [{btn_text}]")

            think_time = random.uniform(2, 5)
            print(f"   👀 即将匹配按钮， 模拟人类延迟 {think_time:.2f}s...")
            await asyncio.sleep(think_time)
            # 3. 找按钮并点击
            if response.buttons:
                for row in response.buttons:
                    for button in row:
                        if btn_text in button.text:
                            await button.click()
                            print(f"   ✅ 已点击按钮: [{button.text}]")
                            return
                print(f"   ⚠️ 未找到目标按钮: [{btn_text}]")
            else:
                print(f"   ⚠️ 回复中没有按钮。")

    except asyncio.TimeoutError:
        print(f"   ❌ 等待 Bot 回复超时 (可能是Bot没理你，或者是网络延迟)。")
    except Exception as e:
        # 打印更详细的错误堆栈，方便排查
        import traceback
        print(f"   ❌ Bot 任务出错: {e}")
        # print(traceback.format_exc()) # 如果还需要调试，可以取消这行的注释
async def work_with_group(client, group_config):
    """处理群组签到任务"""
    target_id = group_config['id']
    msg = group_config['message']
    
    print(f"\n📢 正在执行群组任务: {target_id} ({group_config.get('note', '')})")

    try:
        await client.send_message(target_id, msg)
        print(f"   ✅ 已发送消息: {msg}")
    except Exception as e:
        print(f"   ❌ 群组任务出错: {e} (请检查群ID是否正确)")

async def main():
    print("🚀 程序启动...")


    # 1. 启动前的随机大等待 (防定时检测)
    if TEST_MODE:
        print("⚡ 测试模式：跳过启动等待...")
    else:
        wait_time = random.randint(60, 3600)
        print(f"⏳ 计划等待启动时间: {wait_time} 秒 ({wait_time/60:.2f} 分钟)")
        await asyncio.sleep(wait_time)

    proxy_args = None
    if os.environ.get('TG_PROXY_PORT'):
        proxy_port = int(os.environ['TG_PROXY_PORT'])
        print(f"🌍 检测到本地代理配置，使用端口: {proxy_port}")
        # 这里默认使用 HTTP 代理，如果需要 SOCKS5 请改为 socks.SOCKS5
        proxy_args = (python_socks.ProxyType.HTTP, '127.0.0.1', proxy_port)
    else:
        print("☁️ 未检测到代理配置，使用直连模式 (GitHub Actions环境)")

    async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH, proxy=proxy_args,**CLIENT_PARAMS) as client:
        print("✅ 登录成功 (已伪装成 Windows Desktop)")
        print("✅ 登录成功，开始处理任务列表...")

        # 2. 遍历 Bot 列表
        bots = CONFIG.get('bots', [])
        for bot in bots:
            await work_with_bot(client, bot)
            
            # 任务间随机休息 10-30 秒 (模拟真人操作间隔)
            sleep_time = random.randint(10, 30)
            print(f"   💤 休息 {sleep_time} 秒...")
            await asyncio.sleep(sleep_time)

        # 3. 遍历 群组 列表
        groups = CONFIG.get('groups', [])
        for group in groups:
            await work_with_group(client, group)
            
            # 任务间随机休息
            sleep_time = random.randint(10, 30)
            print(f"   💤 休息 {sleep_time} 秒...")
            await asyncio.sleep(sleep_time)

    print("\n🎉 所有任务执行完毕！")

if __name__ == '__main__':
    asyncio.run(main())