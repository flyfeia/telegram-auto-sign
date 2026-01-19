# telegram-auto-sign

## 项目背景

实现telegram的bot自动签到和群组的自动发送消息，可以部署在github action，配置好环境变量参数即可，根据cron定时执行。

## 项目思路

> 首先获取到telegram的api、session,指定设备信息模拟自动登录
>
> 根据项目配置的cron，到了指定的时间后，随机sleep 1-60分钟  # 这一步是防止 每天固定一个时间签到 被认定脚本
>
> 进入到bot界面 sleep，然后发送配置的指令，收到回复后，再次sleep，然后匹配按钮模拟点击
>
> 完成一次bot操作后和下一次再sleep
>
> bot和group 都会增加操作间隔时间

## 技术

| 框架          | 版本  |
| ------------- | ----- |
| python-dotenv | 1.2.1 |
| python-socks  |       |
| Telethon      |       |

## 本地开发

```bash
git clone project

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```



## 环境变量参数

在项目根目录创建 `.env` 文件

```bash
# 创建API后显示的参数
TG_API_ID=TGAPIID
TG_API_HASH=TGAPIHASH
# 本地获取项目后 执行 python get_session.py ，根据界面引导 ，复制session到此变量
TG_SESSION_STRING=TG SESSION
# 如本地需开启代理，则代理的port
TG_PROXY_PORT=10808
# 是否是测试模式
TEST_MODE=true
# 发送的BOT和msg
TG_CONFIG_JSON='{"bots":[{"username":"bot","command":"/start","button_text":"签到","note":"备注"}],"groups":[{"id":-1009876543210,"message":"哈咯 大家好","note":"这是某个资源群"}]}'
```

## Log示例

```tex
✅ 成功从环境变量加载配置
🚀 程序启动...
⚡ 测试模式：跳过启动等待...
☁️ 未检测到代理配置，使用直连模式 (GitHub Actions环境)
✅ 登录成功 (已伪装成 Windows Desktop)
✅ 登录成功，开始处理任务列表...

🤖 正在执行 Bot 任务: bot (note)
   📤 发送命令: /start
   📩 收到回复，寻找按钮包含: [签到]
   👀 即将匹配按钮， 模拟人类延迟 4.61s...
   ✅ 已点击按钮: [签到]
   💤 休息 28 秒...

📢 正在执行群组任务: -1009876543210 (这是某个资源群)
   ❌ 群组任务出错: Could not find the input entity for PeerChannel(channel_id=9876543210) (PeerChannel). Please read https://docs.telethon.dev/en/stable/concepts/entities.html to find out more details. (请检查群ID是否正确)
   💤 休息 23 秒...

🎉 所有任务执行完毕！
```

