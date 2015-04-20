# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IVRCall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('digit_entered', models.IntegerField(null=True, blank=True)),
                ('time_delay', models.IntegerField(null=True, blank=True)),
                ('call_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
