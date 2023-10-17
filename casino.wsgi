import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('C:/Projects/casino')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'casino.settings')
application = get_wsgi_application()