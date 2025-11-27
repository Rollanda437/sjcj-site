# api/wsgi.py – LE SEUL FICHIER QUE VERCEL VEUT EN 2025
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')
application = get_wsgi_application()

# Vercel cherche exactement ça :
app = application