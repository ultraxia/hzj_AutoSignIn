import requests
import data_layer
import time

header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0; MI 8 Build/PKQ1.180729.001; wv) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044306 Mobile Safari/537.36'}


def get_token(username, password):
    url = 'http://gzdk.gzisp.net/api/authenticateNew'
    form = {'username': username,
            'password': password,
            'schoolId': '72'}
    response = requests.post(url, form, headers=header).json()
    if response['res'] == 'succ':
        username = response['data']['userName']
        token = list(set({response['data']['id_token']}))[0]
        token = {'userName': username, 'token': token}
        return token


def check_sign(username, password):
    token = get_token(username, password)['token']
    url = 'http://gzdk.gzisp.net/sign/getMyCheckinSubList?authorization={}'.format(token)
    response = requests.get(url, headers=header).json()
    if response['res'] == 'success':
        data = response['data'][1][0]
        sendtime, address, location_x, location_y = data['sendTime'], data['label'], data['locationX'], data[
            'locationY']
        signdata = {'address': address, 'token': token, 'locationX': location_x, 'locationY': location_y,
                    'sendTime': sendtime}
        return signdata
    else:
        print(response['desc'])


def sign_action(username, password):
    signdata = check_sign(username, password)
    token, address, location_x, location_y = signdata['token'], signdata['address'], signdata['locationX'], signdata[
        'locationY']
    url = 'http://gzdk.gzisp.net/sign/addSignIn?ADDR={}&AXIS={}-{}&CONTENT=&IDS=&ISEVECTION=0&SCALE=18&authorization={}'
    url = url.format(address, location_y, location_x, token)
    response = requests.get(url, headers=header).json()
    if response['res'] == 'success':
        print('签到成功！')
    else:
        print('已签到')


def check_ifsign(username,password):
    sendtime = check_sign(username, password)['sendTime']
    lastdate = sendtime[:10]
    getdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if int(lastdate[-2:]) != int(getdate[-2:]):
        try:
            sign_action(username, password)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    tasks = data_layer.query('select * from sign')
    for task in tasks:
        username, password = task[1], task[2]
        time.sleep(20)
        print(task[0] + ' OK')
        check_ifsign(username, password)

