# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-28 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_image',
            field=models.ImageField(blank=True, upload_to='questions/'),
        ),
    ]