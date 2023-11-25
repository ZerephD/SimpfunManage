from flask import Flask, request
import requests
import config
import json

#个人信息
user_id=config.userID
auth=config.Authorization
head={'Content-Type':'application/x-www-form-urlencoded','Authorization':auth}

#请求URL
get_info=f'https://api.simpfun.cn/api/ins/{user_id}/detail'
change_state=f'https://api.simpfun.cn/api/ins/{user_id}/power'

app = Flask(__name__)
@app.route('/manage', methods='GET')
def main():
    action=request.args.get('action')
    server_info=requests.get(get_info,headers=head)
    uptime=int(json.loads(server_info.text)['data']["utilization"]['uptime'])
    if action == 'start':
        if uptime == 0:
            try:
                changed=requests.get((change_state+'?action=start'),headers=head)
                return changed.text
            except:
                return {'code':201}
        else:
            return {'code':202}
    elif action == 'stop':
        if uptime == 0:
            return {'code':203}
        else:
            try:
                changed = requests.get((change_state + '?action=stop'), headers=head)
                return changed.text
            except:
                return {'code':201}
    elif action == 'restart':
        if uptime == 0:
            try:
                changed = requests.get((change_state + '?action=stop'), headers=head)
                return changed.text
            except:
                return {'code': 201}
        else:
            try:
                changed = requests.get((change_state + '?action=stop'), headers=head)
                return changed.text
            except:
                return {'code':201}
    else:
        return {'code':201}

if __name__ == '__main__':
    app.run()