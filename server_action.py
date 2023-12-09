from flask import Flask, request
import requests
import config
import json

#个人信息
user_id=config.ServerID
auth=config.Authorization
head={'Content-Type':'application/x-www-form-urlencoded','Authorization':auth}

#请求URL
get_info=f'https://api.simpfun.cn/api/ins/{user_id}/detail'
change_state=f'https://api.simpfun.cn/api/ins/{user_id}/power'

#获取服务器数据
server_info=requests.get(get_info,headers=head)
uptime=int(json.loads(server_info.text)['data']["utilization"]['uptime'])

def send_command(action):
    try:
        changed = requests.get((change_state + f'?action={action}'), headers=head)
        return json.loads(changed.text)
    except:
        return {'code': 201}

def op_server(action):
    if uptime==0:
        server_open=False
    else:
        server_open=True
    if (server_open and action=='stop') or ((not server_open) and action=='start') or (server_open and action=='restart'):
        return send_command(action)
    elif (server_open and action=='start') or ((not server_open) and action=='stop'):
        return {'code': 202}
app = Flask(__name__)
@app.route('/manage', methods=['GET'])
def main():
    action=request.args.get('action')
    return  op_server(action)

if __name__ == '__main__':
    app.run()