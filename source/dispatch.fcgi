#!../runenv/bin/python
#Change virtualenv path accordingly.
import sys, os

currentPath = os.path.abspath(__file__)

# Add a custom Python path.
sys.path.insert(0, currentPath)

# Switch to the directory of your project. (Optional.)
os.chdir(currentPath + "/mediadores")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "mediadores.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
