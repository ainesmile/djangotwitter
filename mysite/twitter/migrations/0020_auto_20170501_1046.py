# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-30 22:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0019_auto_20170501_1035'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='nofiticate_type',
            new_name='notificate_type',
        ),
    ]
