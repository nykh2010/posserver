from django.db import models

class PosData(models.Model):
    name = models.CharField(max_length=30)      # 姓名
    depatment = models.CharField(max_length=30)      # 科室
    level = models.CharField(max_length=30)
    tid = models.CharField(max_length=30)       # 标签id
    uid = models.CharField(max_length=30, primary_key=True)       # 工号
    gatewayId = models.CharField(max_length=30)     # 对应网关id
    x = models.FloatField()
    y = models.FloatField()