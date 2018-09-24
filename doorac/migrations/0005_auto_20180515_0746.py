# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-15 07:46
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('doorac', '0004_auto_20180515_0634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('dev_id', models.CharField(default='', max_length=30, unique=True)),
                ('dev_type', models.CharField(default='', max_length=30)),
                ('status', models.CharField(default='', max_length=30)),
                ('approve_tag', models.TextField()),
                ('door', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doorac.Door')),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('my_text', models.TextField(blank=True, default='', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.DeleteModel(
            name='Devices',
        ),
    ]
