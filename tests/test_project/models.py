from django.db import models
from django.contrib.postgres.fields import JSONField as PgJSONField


class SimpleModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.NullBooleanField()
    misc_postgres_json = PgJSONField(null=True)


class SimpleModelChild(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(SimpleModel, null=True, on_delete=models.CASCADE)
