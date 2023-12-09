import json
import requests
import config
import telebot
import server_action as op
from flask import Flask, request, abort

api_token = config.BotToken
webhook_host = config.Domain

app = Flask(__name__)
bot = telebot.TeleBot(api_token, threaded=False)

def return_massage(text,command,message):
    bot.send_message(message.chat.id, f'服务器正在{text}中，请稍候……\n\n如超过10秒未响应请联系[开发者](https://t.me/Zereph_Dandre)', parse_mode="Markdown")
    code = int(op.op_server(command)['code'])
    if code == 200:
        bot.send_message(message.chat.id, f'服务器{text}成功！', parse_mode="Markdown")
    elif code == 201:
        bot.send_message(message.chat.id, f'未知错误，操作失败，请联系[开发者](https://t.me/Zereph_Dandre)！', parse_mode="Markdown")
    elif code == 202:
        bot.send_message(message.chat.id, f'服务器正处于{text}状态，请勿重复{text}！', parse_mode="Markdown")

@app.route('/bot', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "√", 200

#欢迎
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '欢迎使用简幻欢MC服务器管理机器人', parse_mode="Markdown")

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
    bot.send_message(message.chat.id, f'正在获取服务器信息中，请稍候……\n\n如超过10秒未响应请联系[开发者](https://t.me/Zereph_Dandre)', parse_mode="Markdown")
    server_info = requests.get(f'https://api.simpfun.cn/api/ins/{config.ServerID}/detail', headers=op.head)
    server_info=json.loads(server_info.text)
    if int(server_info['code'])==200:
        data=server_info['data']
        info_message=(f"服务器ID：`{config.ServerID}\n`"
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
        bot.send_message(message.chat.id, f'服务器ID: {config.ServerID} 信息获取失败\n请联系[开发者](https://t.me/Zereph_Dandre)', parse_mode="Markdown")


if __name__=='__main__':
    app.run()