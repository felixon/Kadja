# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_delete_imagemodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='post',
        ),
    ]
