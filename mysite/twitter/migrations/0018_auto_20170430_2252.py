# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-30 10:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0017_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notificate_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
