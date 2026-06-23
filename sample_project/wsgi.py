import os
import importlib

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sample_project.settings')

# Force reload url config to bypass Vercel Lambda module cache
import django
django.setup()

from django.urls import clear_url_caches
clear_url_caches()

import sample_project.urls
importlib.reload(sample_project.urls)

application = get_wsgi_application()
app = application
