import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'django' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bni_project.settings')

# Get the WSGI application
application = get_wsgi_application()
