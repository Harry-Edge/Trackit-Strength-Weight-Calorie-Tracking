# Generated by Django 3.1.2 on 2021-01-15 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20210114_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='targets_enabled',
            field=models.BooleanField(null=True),
        ),
    ]
