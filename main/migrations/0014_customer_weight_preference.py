# Generated by Django 3.1.2 on 2021-01-10 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20210110_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='weight_preference',
            field=models.CharField(choices=[('KG', 'KG'), ('LBS', 'LBS')], max_length=3, null=True),
        ),
    ]
