# -*-coding:utf-8 -*-


import sys

import json
import re
import requests
import io
import time
from  multiprocessing import Process


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

parks_info = [(36, 'F1'), (37, 'F2'), (52, 'F3'), (53, 'F4'), (54, 'F5'), (49, 'D1'), (50, 'D2'), (51, 'D3'), (57, 'P1'), (58, 'P2'), (59, 'P3'), (60, 'P4'), (61, 'P5'), (62, 'P6'), (66, 'K1'), (67, 'K2'), (68, 'K3'), (69, 'K4'), (70, 'K5'), (71, 'K6'), (72, 'K7'), (73, 'K8'), (74, 'K9'), (75, 'K10'), (76, 'K11'), (77, 'K12'), (78, 'K13'), (79, 
'K14'), (80, 'K15'), (81, 'K16'), (82, 'K17'), (83, 'K18')]

# parks_info = [(80, 'K15'), (81, 'K16'), (82, 'K17'), (83, 'K18')]

parks_info = [(36, 'F1'), (37, 'F2'), (52, 'F3'), (53, 'F4'), (54, 'F5'), (66, 'K1'), (67, 'K2'), (68, 'K3'), (69, 'K4'), (70, 'K5'), (71, 'K6'), (72, 'K7'), (73, 'K8'), (74, 'K9'), (75, 'K10'), (76, 'K11'), (77, 'K12'), (78, 'K13'), (79, 
'K14'), (80, 'K15'), (81, 'K16'), (82, 'K17'), (83, 'K18')]


available = {}

parks_map = {36: 'F1', 37: 'F2', 52: 'F3', 53: 'F4', 54: 'F5', 49: 'D1', 50: 'D2', 51: 'D3', 57: 'P1', 58: 'P2', 59: 'P3', 60: 'P4', 61: 'P5', 62: 'P6', 66: 'K1', 67: 'K2', 68: 'K3', 69: 'K4', 70: 'K5', 71: 'K6', 72: 'K7', 73: 'K8', 74: 'K9', 75: 'K10', 76: 'K11', 77: 'K12', 78: 'K13', 79:
'K14', 80: 'K15', 81: 'K16', 82: 'K17', 83: 'K18'}

user_id = ''

def message_box():
    title = 'XXXXXXXXXXXXXXXXXXXXXXX'
    msg = '!!!!!!!!!!!!!!!!!!!!!!!!'
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, msg, title, 1)


def run(url, data=None):
    sess = requests.session()

    headers = {
        'Host': 'tennis.coopcloud.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1295.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://tennis.coopcloud.cn/TennisCenterInterface/toWxAouth.action?code=023jD8r62AiseO05QQt62CU6r62jD8rc&state=1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
    }

    cookie = requests.cookies.RequestsCookieJar()
    cookie.set('JSESSIONID', '')
    cookie.set('openid', '')
    sess.cookies.update(cookie)

    if data:
        response = sess.post(url, headers=headers, data=data, verify=False)
    else:
        response = sess.get(url)
    # print(response.cookies.get_dict())
    response.encoding="utf-8"

    html = response.text
    print(html, flush=True)              
#     print(response, data['parkList'])

    return html


def get_free_slots(data, times=None, reserve=False):
    js = json.loads(data)
    slots = js["datas"]['venList']
    for place in slots:
            for park in place['park']:
                    parks_info.append((park['id'], park['parkname']))
                    print((park['id'], park['parkname']), end=":\t")
                    available[park['id']] = []
                    for part in park['reserve']:
                        t = int(part['time'])
                        if times and not t in times:
                            continue
                        if reserve:
                            if part['userid']:
                                continue
                        else:
                            if part['bookstatus'] != 0:
                                continue
                        available[park['id']].append(t)
                        print(t, end="\t")
                        # message_box()
                    print()


    print("Checked", flush=True)



def query(dates=[], times=None, reserve=False):
    url = 'http://tennis.coopcloud.cn/TennisCenterInterface/pmPark/getParkShowByParam.action'


    for park_type in [1,3]:
        for date in dates:
            data = {
                    "ballcode":     '1',
                    "cardtypecode":	'-1',
                    "date":	        date,
                    "parkstatus":	'0',
                    "parktypeinfo":	park_type,
                    "userid":       user_id
            }

            res = run(url, data)
            print(" ==== Checking: " + date)
            get_free_slots(res, times, reserve)

    for park in available.keys():
        if park in parks_map and len(available[park]) > 1:
            print(park, parks_map[park], available[park], sep='\t')



def pay(order_id):
    #return

    url = 'http://tennis.coopcloud.cn//TennisCenterInterface/omOrder/payByCard.action'

    data = {
        'orderNo': order_id,
        'userid': user_id
    }

    run(url, (data))

    sys.stdout.flush()

def order(park_list):
    url = 'http://tennis.coopcloud.cn/TennisCenterInterface/pmPark/addParkOrder.action'

    print('xxx')

    data = {
    'addOrderType':	'wx',
    'parkList':	json.dumps(park_list),
    'paywaycode': '0',
    'userid':   user_id,
    }


    rsp = run(url, (data))

    if '1001' in rsp:
        order_id = json.loads(rsp)["datas"]["orderNo"]
        pay(order_id)

    sys.stdout.flush()

def book(key=None, infos=None, target_date='2020-07-31'):
    if __name__ == '__main__':
        if infos:
            print(infos)
            for line in infos.split("\n"):
                parts = line.split("    ")
                if len(parts) > 2:

                    slots = json.loads(parts[2])
                    print(slots)
                    for t in slots:
                        next = str(int(t)+1)
                        print(next, next in slots)
                        if next <= "22":
                            times = [t, next]

                            print(times)

                            park_list = [{"date": target_date,"time": t ,"parkid": parts[0],"parkname": parts[1]} for t in times]

                            x=Process(target=order,args=(park_list,))
                            x.start()

            return




        for info in parks_info:

            if key and not key in info[1]:
                continue

            print(info, flush=True)
            park_list = [{"date": target_date,"time": t ,"parkid": info[0],"parkname": info[1]} for t in times]

            x=Process(target=order,args=(park_list,))
            x.start()


# query()
# order()

# while True:
#     print('booking')
#     book('K18')
#     time.sleep(1)

# # print(parks_info)

#book()

# book('K18')


target_date = '2020-08-08'
times = [20, 21]


# query([target_date], times = [19, 20, 21, 22], reserve=True)


book(
target_date=target_date,
infos='''

52      F3      [20, 21, 22]
53      F4      [21, 22]
54      F5      [21, 22]
57      P1      [21, 22]
58      P2      [21, 22]
59      P3      [21, 22]
71      K6      [20, 21, 22]
72      K7      [20, 21, 22]
75      K10     [21, 22]
76      K11     [21, 22]
77      K12     [21, 22]
79      K14     [20, 21, 22]

''')
