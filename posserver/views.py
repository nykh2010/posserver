# from django.http import HttpRequest, HttpResponse
# from dwebsocket import require_websocket, accept_websocket
# from .models import PosData

# import json
# import random
# import time

# @accept_websocket
# def websockTest(request):
#     if not request.is_websocket():
#         print('not ok')
#         return HttpResponse('ok')
#     else:
#         print('ok')
#         websock = request.websocket
#         position = {}
#         print(PosData.objects.all())
#         # print(posData)
#         while True:
#             position['x'] = random.randint(1,10)
#             position['y'] = random.randint(1,10)
#             position['value'] = random.randint(1,100)
#             # position['y'] = random.randint(1,10)
#             print(position)
#             jsonstr = json.dumps(position)
#             print(jsonstr)
#             # 发送位置信息
#             websock.send(jsonstr.encode('utf-8'))
#             time.sleep(1)
#         # for message in websock:
#         #     print(type(message))
#         #     websock.send(message)
#         # for i in range(10):
#         #     data = ("%2d" % (i*10)).encode('utf-8')
#         #     print(data)
#         #     websock.send(data)
