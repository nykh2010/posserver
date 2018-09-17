from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from dwebsocket import require_websocket, accept_websocket
from .models import PosData

import json
import random
import time
import serial

def open_serial():
    try:
        s = serial.Serial(port='COM1', timeout=10)
    except:
        print('port already open')
    else:
        print('port open success')
    return s

def index(request):
    if request.method == 'POST':
        '''处理上传的文件信息'''
        print(request)
        # 1. 提取xls文件中的字段
        # 2. 写入数据库中
        # 3. 提取数据库文件，读取模板后返回
    else:
        '''处理GET请求'''
    return render(request, 'myindex.html', locals())

@accept_websocket
def websockTest(request):
    if not request.is_websocket():
        print('not ok')
        return HttpResponse('ok')
    else:
        try:
            s = serial.Serial(port='COM1', timeout=1)
        except:
            print('port already open')
        else:
            print('port open success')
        websock = request.websocket
        position = {}
        pos = PosData.objects.all()
        # help(pos)
        for p in pos:
            position['x'] = p.x
            position['y'] = p.y
            position['value'] = p.uid
            jsonstr = json.dumps(position)
            websock.send(jsonstr.encode('utf-8'))
        # print(posData)
        while True:
            buff = s.read(2048)
            if not buff:
                continue
            print(buff)
            position['x'] = buff[1]
            position['y'] = buff[2]
            position['value'] = buff[0]
            try:
                p = PosData.objects.get(uid=position['value'])
            except:
                # 没有记录，新增一条
                p = PosData(uid=position['value'], x=position['x'], y=position['y'])
            else:
                # 有记录
                p.x = position['x']
                p.y = position['y']
            p.save()
                
            # position['y'] = random.randint(1,10)
            # print(position)
            jsonstr = json.dumps(position)
            # print(jsonstr)
            # 发送位置信息
            websock.send(jsonstr.encode('utf-8'))

