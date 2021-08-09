# * import DJango Settings
import os
import django
os.chdir('../')

print(os.getcwd())

os.environ['DJANGO_SETTINGS_MODULE'] = 'cashup_backend.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

django.setup()