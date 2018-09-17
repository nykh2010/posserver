from django.db import models

class PosData(models.Model):
    name = models.CharField(max_length=30)      # 姓名
    depatment = models.CharField(max_length=30)      # 科室
    level = models.CharField(max_length=30)
    uid = models.CharField(max_length=30)       # id
    gatewayId = models.CharField(max_length=30)     # 对应网关id
    x = models.FloatField()
    y = models.FloatField()