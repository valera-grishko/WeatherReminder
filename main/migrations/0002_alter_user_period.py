# Generated by Django 3.2.5 on 2021-07-09 13:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='period',
            field=models.DurationField(default=datetime.timedelta(seconds=300)),
        ),
    ]