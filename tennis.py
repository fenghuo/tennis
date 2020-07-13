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

def message_box():
    title = 'go'
    msg = go
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
    print(html)              
#     print(response, data['parkList'])
    return html
def get_free_slots(data):
    js = json.loads(data)
    slots = js["datas"]['venList']
    for place in slots:
            print(place)
            for park in place['park']:
                    parks_info.append((park['id'], park['parkname']))
                    for part in park['reserve']:
                        if part['bookstatus'] == 0:
                                t = int(part['time'])
                                if t <22 and t>=18:
                                        print(park['id'], park['parkname'], t, flush=True)
                                        message_box()
    print("Checked", flush=True)
def query():
    url = 'http://tennis.coopcloud.cn/TennisCenterInterface/pmPark/getParkShowByParam.action'
    for park_type in [1,3]:
        for date in ['2020-06-25', '2020-06-26']:
            data = {
                    "ballcode":     '1',
                    "cardtypecode":	'-1',
                    "date":	        date,
                    "parkstatus":	'0',
                    "parktypeinfo":	park_type,
                    "userid":       ''
            }
            res = run(url, data)
            get_free_slots(res)
            break
def order(data):
    url = 'http://tennis.coopcloud.cn/TennisCenterInterface/pmPark/addParkOrder.action'
    run(url, (data))
target_date = '2020-06-27'
times = [20, 21]
def book():
    if __name__ == '__main__':
        for info in parks_info:
            print(info)
            park_list = [{"date": target_date,"time": t ,"parkid": info[0],"parkname": info[1]} for t in times]
            park = {
                    'addOrderType':	'wx',
                    'parkList':	json.dumps(park_list),
                    'paywaycode': '2',
                    'userid':   ''
            }
            x=Process(target=order,args=(park,))
            x.start()
# query()
# order()
# while True:
#     query()
#     time.sleep(30)
# print(parks_info)
book()
