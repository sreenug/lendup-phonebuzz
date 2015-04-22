# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djtwilio', '0002_ivrcall_call_sid'),
    ]

    operations = [
        migrations.AddField(
            model_name='ivrcall',
            name='call_state',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
