from django.contrib.postgres.fields import ArrayField
from django.db import models


class Plan(models.Model):
    id = models.IntegerField(primary_key=True)
    plan_code = models.CharField(max_length=50)
    minutes = models.IntegerField()
    internet = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    plan_type = models.CharField(max_length=8)
    operator = models.CharField(max_length=6)
    ddds = ArrayField(models.IntegerField())
