# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SimpleModelChild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(null=True, to='test_project.SimpleModel')),
            ],
        ),
    ]
