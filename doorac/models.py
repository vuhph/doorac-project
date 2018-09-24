# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Log(models.Model):
    detail = models.TextField(default='', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    rfid_uid = models.TextField(default='', null=True, blank=True)
    log_event = models.TextField(default='', null=True, blank=True)
    
class Room(models.Model):
    name = models.CharField(default='', max_length=30)
    detail = models.TextField(default='', null=True, blank=True)

class Door(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    name = models.CharField(default='', max_length=30)
    door_id = models.CharField(default='', max_length=30)

class Tag(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    tag_uid = models.CharField(default='', max_length=30)

class Device(models.Model):
    door = models.ForeignKey(Door, on_delete=models.CASCADE,)
    name = models.CharField(default='', max_length=30)
    dev_id = models.CharField(default='', max_length=30, unique=True)
    dev_type = models.CharField(default='', max_length=30)
    status = models.CharField(default='', max_length=30)
    approve_tag = models.TextField()
    def __str__(self):
        return self.name

class TmpData(models.Model):
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
