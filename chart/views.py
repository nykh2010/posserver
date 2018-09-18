from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from dwebsocket import require_websocket, accept_websocket
from .models import PosData

import json
import random
import time
import serial
import numpy as np
import threading

def open_serial():
    try:
        s = serial.Serial(port='COM1', timeout=10)
    except:
        print('port already open')
    else:
        print('port open success')
    return s

def indexTest(request):
    return render(request, 'index.html')

def index(request):
    if request.method == 'POST':
        '''处理上传的文件信息'''
        data = {}
        # 1. 提取xls文件中的字段
        for i, buff in enumerate(request.FILES['csvfile'].readlines()):
            indexList = buff[:-2].decode('GB2312').split(',')
            if i == 0:      # 第一行
                for key in indexList:
                    data[key] = None
                continue
            else:
                for value, key in zip(indexList, data.keys()):
                    data[key] = value
            print(data)     # 获得数据
            # 2. 写入数据库中
            try:
                dataSet = PosData.objects.get(uid=data['工号'])
            except:
                print('no data set')
                dataSet =PosData(
                    name = data['姓名'],
                    depatment = data['科室'],
                    level = data['职称'],
                    uid = data['工号'],
                    gatewayId = data['对应网关'],
                    x = data['x'],
                    y = data['y']
                )
            else:
                dataSet.name = data['姓名']
                dataSet.depatment = data['科室']
                dataSet.level = data['职称']
                dataSet.gatewayId = data['对应网关']
                dataSet.x = data['x']
                dataSet.y = data['y']
            dataSet.save()
        # 3. 提取数据库文件，读取模板后返回
        # terminals = PosData.objects.all()
    else:
        '''处理GET请求'''
    terminals = PosData.objects.all()
    return render(request, 'myindex.html', locals())

websocks = []

class WebProtocol:
    def __init__(self, jsonSubject):
        '''网页响应信息'''
        pass

@accept_websocket
def websockTest(request):
    global ms
    if not request.is_websocket():
        print('not ok')
        return HttpResponse('ok')
    else:
        websock = request.websocket
        websocks.append(websock)
        print(len(websocks))
        for message in websock:
            print(message)
            ms.write(message)
            websock.send(message)

class MySerial(serial.Serial):
    def __init__(self, port='COM10'):
        print('myserial init')
        super().__init__(port=port, timeout=1)
        t = threading.Thread(target=self.loop, name='serail_loop')
        t.start()

    def loop(self):
        while True:
            buff = self.read(2048)
            if not buff:
                continue
            print(buff)
            result = self.protocol(buff)
            if result.needToWeb:
                '''需要在页面上更新，转json格式'''
                message = json.dumps(result.message)
                print(message)
                for websock in websocks:
                    websock.send(message.encode('utf-8'))
                resp = [0x03, buff[1], buff[2], 0x00]
                check = 0       # 校验位
                for x in resp:
                    check = check ^ x
                resp.append(check)
                self.write(resp)
    
    def protocol(self, buff):
        '''协议处理'''
        class Result:
            def __init__(self, needToWeb, id=None, msgType=None, msg=None):
                self.needToWeb = needToWeb
                self.message = {'id':id, 'type':msgType, 'message':msg}
        
        if buff[0] == 0x02 and buff[1] == 0x07:
            '''报警信息上报'''
            result = Result(True, str(buff[4:6]), buff[1], 'none')
        elif buff[0] == 0x02 and buff[1] == 0x08:
            '''定位信息上传'''
            result = Result(True, str(buff[4:6]), buff[1], str(buff[6:10]))
        else:
            '''网关应答'''
            result = Result(False)
        print(result.message)
        return result


ms = MySerial()

        # try:
        #     s = serial.Serial(port='COM1', timeout=1)
        # except:
        #     print('port already open')
        # else:
        #     print('port open success')
        # websock = request.websocket
        # position = {}
        # pos = PosData.objects.all()
        # # help(pos)
        # for p in pos:
        #     position['x'] = p.x
        #     position['y'] = p.y
        #     position['value'] = p.uid
        #     jsonstr = json.dumps(position)
        #     websock.send(jsonstr.encode('utf-8'))
        # # print(posData)
        # while True:
        #     buff = s.read(2048)
        #     if not buff:
        #         continue
        #     print(buff)
        #     position['x'] = buff[1]
        #     position['y'] = buff[2]
        #     position['value'] = buff[0]
        #     try:
        #         p = PosData.objects.get(uid=position['value'])
        #     except:
        #         # 没有记录，新增一条
        #         p = PosData(uid=position['value'], x=position['x'], y=position['y'])
        #     else:
        #         # 有记录
        #         p.x = position['x']
        #         p.y = position['y']
        #     p.save()
                
        #     # position['y'] = random.randint(1,10)
        #     # print(position)
        #     jsonstr = json.dumps(position)
        #     # print(jsonstr)
        #     # 发送位置信息
        #     websock.send(jsonstr.encode('utf-8'))

