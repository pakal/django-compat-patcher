from django.db import models


class SimpleModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


class SimpleModelChild(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(SimpleModel, null=True, on_delete=models.CASCADE)
