import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hiverlab_py_simulator.settings')
django.setup()
application = get_default_application()