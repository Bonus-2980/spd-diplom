"""
WSGI config for social_network project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'ru_RU.UTF-8'
os.environ['LC_ALL'] = 'ru_RU.UTF-8'

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

application = get_wsgi_application()
