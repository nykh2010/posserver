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
import os
import queue


cwd = os.getcwd()
with open(cwd + r'\chart\static\colorMap.list') as f:
    colorList = f.read().split(',')

def str2HexList(strObj):
    '''字符串转十六进制列表'''
    ret = []
    for i, l in enumerate(strObj):
        if i%2:
            ret[i//2] = ret[i//2]+int(l)
        else:
            r = int(l) * 16
            ret.append(r)

    print(ret)
    return ret


def indexTest(request):
    return render(request, 'index.html')

def index(request):
    if request.method == 'POST':
        '''处理上传的文件信息'''
        PosData.objects.all().delete()
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
                    tid = data['标签id'],
                    gatewayId = data['对应网关'],
                    onlineFlag = True,
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
        # 3. 提取数据库文件，读取模板后返回，向网关发送信息

    else:
        '''处理GET请求'''
    terminals = PosData.objects.all()
    colors = colorList[:len(terminals)]
    return render(request, 'myindex.html', locals())

websocks = []

def WebProtocol(buff):
    jsonDict = json.loads(buff)
    print(jsonDict)
    res = []
    if jsonDict['type'] == 0x02:
        # 定时轮询开关
        result = [0x03,0x02,jsonDict['id'],0x01,jsonDict['message']]
        res.append(result)
    elif jsonDict['type'] == 0x01:
        # 时间同步
        result = [0x03,0x01,jsonDict['id'],19]
        tm = time.localtime()
        tm_s = '{:4}.{:0>2}.{:0>2},{:0>2}:{:0>2}:{:0>2}'.format(
            tm.tm_year, tm.tm_mon, tm.tm_mday, \
            tm.tm_hour, tm.tm_min, tm.tm_sec
        )
        rb = bytes(tm_s, encoding='utf-8')
        rl = list(rb)
        result.extend(rl)
        res.append(result)
    elif jsonDict['type'] == 0x03:
        # 个人信息更新
        try:
            terminal = PosData.objects.get(uid=jsonDict['id'])
        except:
            print("no data set")
            return
        terminal.name = jsonDict['message']['name']
        terminal.depatment = jsonDict['message']['depart']
        terminal.level = jsonDict['message']['level']
        terminal.uid = jsonDict['message']['uid']
        terminal.save()
        # 个人信息组帧
        # 姓名
        result = [0x03,0x03,0x01]
        s = '{:0>4}'.format(terminal.tid)   # 字符串转换
        l = str2HexList(s)
        result.extend(l)            # 追加至返回列表中
        r = terminal.name
        rb = bytes(r, encoding='GB2312')
        length = len(rb)
        rl = list(rb)
        result.extend(rl)
        result.insert(3, length+2)
        res.append(result)
        # 科室和职级
        result = [0x03,0x04,0x01]
        s = '{:0>4}'.format(terminal.tid)   # 字符串转换
        l = str2HexList(s)
        result.extend(l)            # 追加至返回列表中
        r = '%s %s' % (terminal.depatment, terminal.level)
        rb = bytes(r, encoding='GB2312')
        length = len(rb)
        rl = list(rb)
        result.extend(rl)
        result.insert(3, length+2)
        res.append(result)
        # 工牌号
        result = [0x03,0x05,0x01]
        s = '{:0>4}'.format(terminal.tid)   # 字符串转换
        l = str2HexList(s)
        result.extend(l)            # 追加至返回列表中
        result.insert(6, 0x04)
        r = '{:0>14}'.format(terminal.uid)
        rb = bytes(r, encoding='utf-8')
        length = len(rb)
        rl = list(rb)
        result.extend(rl)
        result.insert(3, length+2)
        res.append(result)
    elif jsonDict['type'] == 0x04:
        # 向下发送数据
        terminals = PosData.objects.all()       # 获取所有数据集
        for terminal in terminals:
            # 姓名
            result = [0x03,0x03,0x01]
            s = '{:0>4}'.format(terminal.tid)   # 字符串转换
            l = str2HexList(s)
            result.extend(l)            # 追加至返回列表中
            r = terminal.name
            rb = bytes(r, encoding='GB2312')
            length = len(rb)
            rl = list(rb)
            result.extend(rl)
            result.insert(3, length+2)
            res.append(result)
            # 科室和职级
            result = [0x03,0x04,0x01]
            s = '{:0>4}'.format(terminal.tid)   # 字符串转换
            l = str2HexList(s)
            result.extend(l)            # 追加至返回列表中
            r = '%s %s' % (terminal.depatment, terminal.level)
            rb = bytes(r, encoding='GB2312')
            length = len(rb)
            rl = list(rb)
            result.extend(rl)
            result.insert(3, length+2)
            res.append(result)
            # 工牌号
            result = [0x03,0x05,0x01]
            s = '{:0>4}'.format(terminal.tid)   # 字符串转换
            l = str2HexList(s)
            result.extend(l)            # 追加至返回列表中
            result.insert(6, 0x04)
            r = '{:0>14}'.format(terminal.uid)
            rb = bytes(r, encoding='utf-8')
            length = len(rb)
            rl = list(rb)
            result.extend(rl)
            result.insert(3, length+2)
            res.append(result)
    elif jsonDict['type'] == 0x06:
        # 消息推送
        try:
            terminal = PosData.objects.get(uid=jsonDict['id'])
        except:
            print("no data set")
            return
        result = [0x03,0x06,0x01]
        s = '{:0>4}'.format(terminal.tid)   # 字符串转换
        l = str2HexList(s)
        result.extend(l)
        r = jsonDict['message']
        rb = bytes(r, encoding='GB2312')
        length = len(rb)
        rl = list(rb)
        result.extend(rl)
        result.insert(3, length+2)
        res.append(result)


    for r in res:
        check = 0       # 校验位
        for x in r:
            check = check ^ x
        r.append(check)
    return res

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
            if message is None:
                print('message is none')
                websocks.remove(websock)
                break
            result = WebProtocol(message)
            for msgdata in result:
                print(msgdata)
                ms.sendQueue.put_nowait(msgdata)
                # 等待应答
            websock.send(message)
        return

class Result:
    def __init__(self, needToWeb, id=None, msgType=None, msg=None):
        self.needToWeb = needToWeb
        self.message = {'id':id, 'type':msgType, 'message':msg}

class MySerial(serial.Serial):
    def __init__(self, port='COM1'):
        print('myserial init')
        super().__init__(port=port, timeout=1)
        self.sendQueue = queue.Queue(maxsize=50)
        self.recvQueue = queue.Queue(maxsize=50)
        t = threading.Thread(target=self.loop, name='serail_loop')
        t.start()
    
    def checkAck(self, result):
        '''检查应答'''
        return True

    def loop(self):
        while True:
            # 发送队列优先级高于接收队列
            while not self.sendQueue.empty():
                '''发送队列非空'''
                print('serial loop')
                msg = self.sendQueue.get_nowait()   # 从队列中取出一个消息
                for i in range(3):
                    self.write(msg)
                    if self.checkAck(msg):          # 收到应答，跳出
                        break
            '''处理上报数据'''
            buff = self.read(2048)
            if not buff:
                continue
            print(buff)
            result = self.rxProtocol(buff)
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

    def txProtocol(self, msg):
        '''发送协议处理'''
        pass
    
    def rxProtocol(self, buff):
        '''协议处理'''
        
        if buff[0] == 0x02 and buff[1] == 0x07:
            '''报警信息上报'''
            result = Result(True, str(buff[4:6]), buff[1], 'none')
        elif buff[0] == 0x02 and buff[1] == 0x08:
            '''定位信息上传'''
            result = Result(True, str(buff[4:6]), buff[1], str(buff[6:10]))
        elif buff[0] == 0x02 and buff[1] == 0x00:
            '''网关上线'''
            result = Result(False, str(buff[1]), 0x00)
        else:
            '''网关应答'''
            result = Result(False)
        print(result.message)
        return result


ms = MySerial()

