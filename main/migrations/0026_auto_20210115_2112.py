# Generated by Django 3.1.2 on 2021-01-15 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20210115_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='weight_data',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='calorie_data',
            field=models.IntegerField(null=True),
        ),
    ]
