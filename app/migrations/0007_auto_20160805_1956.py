# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-06 02:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160729_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='food',
            name='servings',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Address'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Address'),
        ),
    ]