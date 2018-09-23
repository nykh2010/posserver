from django.db import models

class PosData(models.Model):
    name = models.CharField(max_length=30)      # 姓名
    depatment = models.CharField(max_length=30)      # 科室
    level = models.CharField(max_length=30)     # 职级
    tid = models.CharField(max_length=30)       # 标签id
    uid = models.CharField(max_length=30, primary_key=True)       # 工号
    gatewayId = models.CharField(max_length=30)     # 对应网关id
    onlineFlag = models.BooleanField(default=False)          # 在线标志
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)