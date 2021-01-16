# Generated by Django 3.1.2 on 2021-01-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calories', models.IntegerField(max_length=4, null=True)),
                ('date_of_entry', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
