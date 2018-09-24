# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt # not to use csrfmiddleware in views have this decorator

from django.contrib.auth.models import User
from .models import Log, Door, Tag, Room
from .forms import LoginForm

from . import myultils

# Create your views here.

@login_required
def dac_index(request):
    return render(request, 'doorac/index.html', {})

def dac_login(request):
    form = LoginForm(request.POST)
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "You have logged in!")
            return redirect('doorac:index')
        else:
            messages.warning(request, "Username or Password are NOT valid!")
            return redirect('doorac:login')
    return render(request, 'doorac/login.html', {'form': form})

def dac_logout(request):
    logout(request) 
    messages.info(request, "You have logged out! Please log in to continue.")
    return redirect('doorac:login')

@login_required
def access_log(request):
    logs = Log.objects.filter(detail__startswith="Access").order_by('created_date')
    return render(request, 'doorac/usr_accesslog.html', {'logs': logs, })

@login_required
def user_devlog(request):
    devlogs = Log.objects.filter(detail__startswith="Device")
    data = {'devlogs': devlogs, }
    return render(request, 'doorac/usr_devlog.html', data)

@login_required
def user_list(request):
    users = User.objects.all()
    data = {'users':users, }
    return render(request, 'doorac/usr_list.html', data)

@login_required
def room_add(request):
    if request.method == "POST":
        name = request.POST.get('roomname', '')
        detail = request.POST.get('roomdetail', '')
        if (Room.objects.filter(name=name)):
            messages.warning(request, "Room existed!!!")
        else:
            new_room = Room(name=name, detail=detail)
            new_room.save()
            messages.warning(request, "Room added.")
    return redirect('doorac:usrsetup')

@login_required
def door_add(request):
    if request.method == "POST":
        name = request.POST.get('doorname', '')
        detail = request.POST.get('doordetail', '')
        if (Room.objects.filter(name=name)):
            messages.warning(request, "Room existed!!!")
        else:
            new_room = Room(name=name, detail=detail)
            new_room.save()
            messages.warning(request, "Room added.")
    return redirect('doorac:usrsetup')

@login_required
def web_post(request):
    log = Log()
    if request.method == "POST":
        log.detail = 'Access detected'
        reqWEB = request.POST.get('WEB', '')
        if (reqWEB == 'OPEN'):
            log.log_event = 'Force'
            log.rfid_uid = 'WEB'
            open_status = myultils.door_open_request()
            if (open_status == 200):
                log.detail = 'Access granted'
            else:
                log.detail = 'Access NOTgranted'
                log.log_event = 'Deny'
            log.save()
            return HttpResponseRedirect(reverse('doorac:usrlist',))
    log.detail = 'Access abnormal ' + myultils.get_client_ip(request)
    log.log_event = 'Refuse'
    log.save()
    return HttpResponseNotFound("<h1>Page Not Found</h1>")

@csrf_exempt
def device_post(request):
    log = Log()
    if request.method == "POST":
        log.detail = 'Access detected'
        tagUID = request.POST.get('UID', '')
        reqDEV = request.POST.get('REQ', '')
        reqWEB = request.POST.get('WEB', '')
        if (tagUID in ('97e8340c','4ad6c46f')):
            log.log_event = 'Allow'
            log.rfid_uid = tagUID
        elif (reqDEV == 'OPEN'):
            log.log_event = 'Force'
            log.rfid_uid = 'BUTTON'
        else:
            log.log_event = 'Deny'
            log.rfid_uid = tagUID + reqDEV
            log.save()
            return HttpResponse("UID.ERR")
        open_status = myultils.door_open_request()
        if (open_status == 200):
            log.detail = 'Access granted'
        else:
            log.detail = 'Access NOTgranted'
            log.log_event = 'Deny'
        log.save()
        return HttpResponse("UID.OK")
    log.detail = 'Access abnormal ' + myultils.get_client_ip(request)
    log.log_event = 'Refuse'
    log.save()
    return HttpResponseNotFound("<h1>Page Not Found</h1>")

@csrf_exempt
def device_update(request):
    log = Log()
    if request.method == "POST":
        log.detail = 'Device update'
        deviceID = request.POST.get('DID', '')
        if deviceID is not None:
            log.log_event = deviceID
            log.save()
            return HttpResponse("DID.OK")
    log.detail = 'Device abnormal'
    log.log_event = myultils.get_client_ip(request)
    log.save()
    return HttpResponseNotFound("<h1>Page Not Found</h1>")
