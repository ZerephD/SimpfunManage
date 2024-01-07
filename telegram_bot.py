import json
import requests
import telebot
import os
import server_action as op
from flask import Flask, request

api_token = os.environ.get("BotToken")

app = Flask(__name__)
bot = telebot.TeleBot(api_token, threaded=False)

def return_massage(text,command,message):
    bot.send_message(message.chat.id, f'服务器正在{text}中，请稍候……\n\n如超过10秒未响应请到Github反馈', parse_mode="Markdown")
    code = int(op.op_server(command)['code'])
    if code == 200:
        bot.send_message(message.chat.id, f'服务器{text}成功！', parse_mode="Markdown")
    elif code == 201:
        bot.send_message(message.chat.id, f'未知错误，操作失败，请到Github反馈！', parse_mode="Markdown")
    elif code == 202:
        bot.send_message(message.chat.id, f'服务器正处于{text}状态，请勿重复{text}！', parse_mode="Markdown")

@app.route('/bot', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200
@app.route('/ini', methods=['GET'])
def set():
    webhook_host=request.url.strip('ini')+'bot'
    bot.set_webhook(url=webhook_host)
    return f'初始化成功，webhook地址为{webhook_host}，请向Bot发送信息测试是否部署成功'

#欢迎
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'欢迎使用简幻欢MC服务器管理机器人\n\n当前版本`1.1.1`\t（[检查更新](https://github.com/ZerephD/SimpfunManage)）\t（[作者](https://t.me/Zereph_Dandre)）', parse_mode="Markdown")

#帮助
@bot.message_handler(commands=['start'])
def send_welcome(message):
    commands_help=f"以下是当前支持的命令：\n" \
                  f"/start\t\t欢迎语及版本信息\n" \
                  f"/info\t\t获取账号绑定的所有服务器的信息\n" \
                  f"/sstart\t\t服务器开机(默认为第一个)\n" \
                  f"/restart\t\t服务器重启(默认为第一个)\n" \
                  f"/stop\t\t服务器关机(默认为第一个)\n\n" \
                  f"项目地址： https://github.com/ZerephD/SimpfunManage\n" \
                  f"欢迎反馈，共建一个完善的服务器管理工具😘"
    bot.send_message(message.chat.id, commands_help, parse_mode="Markdown")

#开启服务器
@bot.message_handler(commands=['sstart'])
def start(message):
    op_text='开机'
    return_massage(op_text,'start',message)

#关闭服务器
@bot.message_handler(commands=['stop'])
def stop(message):
    op_text='关机'
    return_massage(op_text,'stop',message)

#重启服务器
@bot.message_handler(commands=['restart'])
def restart(message):
    op_text='重启'
    return_massage(op_text,'restart',message)

#服务器信息
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, f'正在获取服务器信息中，请稍候……\n\n如超过10秒未响应请到Github反馈', parse_mode="Markdown")
    for id in op.serverlist:
        id=id['id']
        server_info = json.loads(requests.get(f'https://api.simpfun.cn/api/ins/{id}/detail', headers=op.head).text)
        if int(server_info['code']) == 200:
            data = server_info['data']
            info_message = (f"服务器ID：`{id}\n`"
                            f"服务器名称：`{data['name']}\n`"
                            f"服务器状态：`{data['status']}\n`"
                            f"\n"
                            f"实例类别：`{data['game_info']['game_name']}\n`"
                            f"实例服务端：`{data['game_info']['kind_name']}\n`"
                            f"实例版本(游戏版本)：`{data['game_info']['version_name']}\n`"
                            f"\n"
                            f"规格：\n"
                            f"CPU：{data['cpu']}核\n"
                            f"内存：{data['disk']}GB\n"
                            f"存储：{data['ram']}GB\n"
                            f"积分消耗：{data['point']}积分/日\n"
                            f"服务器连接：`{data['allocations'][0]['ip']}:{data['allocations'][0]['port']}\n`")
            bot.send_message(message.chat.id, info_message, parse_mode="Markdown")

        else:
            bot.send_message(message.chat.id,
                             f'服务器ID: {id} 信息获取失败\n请到Github反馈',
                             parse_mode="Markdown")


if __name__=='__main__':
    app.run()