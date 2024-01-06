from flask import Flask, request
import requests
import os
import json

# 个人信息
name = os.environ.get("Name")
passwd = os.environ.get("PassWord")
try:
    auth = os.environ.get('Token')
    if auth == None or auth == '':
        auth = json.loads(
            requests.post('https://api.simpfun.cn/api/auth/login', data={'username': name, 'passwd': passwd}).text)[
            'token']
except:
    auth = \
    json.loads(requests.post('https://api.simpfun.cn/api/auth/login', data={'username': name, 'passwd': passwd}).text)[
        'token']
head = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': auth}
serverlist = json.loads(requests.get('https://api.simpfun.cn/api/ins/list?', headers=head).text)['list']


def send_command(action, num=0):
    change_state = f"https://api.simpfun.cn/api/ins/{serverlist[num]['id']}/power"
    try:
        changed = requests.get((change_state + f'?action={action}'), headers=head)
        return json.loads(changed.text)
    except:
        return {'code': 201}


def op_server(action, num=0):
    # 请求URL
    get_info = f"https://api.simpfun.cn/api/ins/{serverlist[num]['id']}/detail"
    # 获取服务器数据
    server_info = requests.get(get_info, headers=head)
    uptime = int(json.loads(server_info.text)['data']["utilization"]['uptime'])
    if uptime == 0:
        server_open = False
    else:
        server_open = True
    if (server_open and action == 'stop') or ((not server_open) and action == 'start') or (
            server_open and action == 'restart'):
        return send_command(action, num)
    elif (server_open and action == 'start') or ((not server_open) and action == 'stop'):
        return {'code': 202}


app = Flask(__name__)


@app.route('/manage', methods=['GET'])
def main():
    action = request.args.get('action')
    num = requests.args.get('number')
    return op_server(action, num)


if __name__ == '__main__':
    app.run()
