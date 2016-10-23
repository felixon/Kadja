# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_updateprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('model_pic', models.ImageField(upload_to='profile_images', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='updateprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UpdateProfile',
        ),
    ]
