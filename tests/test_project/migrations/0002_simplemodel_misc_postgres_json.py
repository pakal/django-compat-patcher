# Generated by Django 4.0 on 2022-06-15 10:08

from django.db import migrations
import django

class Migration(migrations.Migration):

    dependencies = [
        ('test_project', '0001_initial'),
    ]

    if django.VERSION >= (3, 2):
        import django.contrib.postgres.fields.jsonb
        operations = [
            migrations.AddField(
                model_name='simplemodel',
                name='misc_postgres_json',
                field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
            ),
        ]
    else:
        operations = []
