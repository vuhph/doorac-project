import sys
import os
import django

mycwd = os.getcwd()
sys.path.append(mycwd)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

django.setup()

from django.conf import settings

