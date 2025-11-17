
"""
WSGI config for gestion_ecole project.
Vercel exige que la variable s'appelle exactement « app »
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_ecole.settings')

app = get_wsgi_application()