# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_auto_20160901_1137'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ImageModel',
        ),
    ]
