from django.db import models
import django

if django.VERSION >= (3, 2):
    from django.contrib.postgres.fields import JSONField as PgJSONField
else:
    PgJSONField = None


class SimpleModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.NullBooleanField()
    if PgJSONField:
        misc_postgres_json = PgJSONField(null=True)


class SimpleModelChild(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(SimpleModel, null=True, on_delete=models.CASCADE)
