import os.path

from django.conf import settings

# Paths
STYLES_DIR = getattr(settings, 'STYLES_DIR', 'css/styles/')
STYLES_ROOT = getattr(settings, 'STYLES_ROOT', os.path.join(settings.MEDIA_ROOT, STYLES_DIR))
STYLES_URL = getattr(settings, 'STYLES_URL', os.path.join(settings.MEDIA_URL, STYLES_DIR))
STYLES_DEFAULT = getattr(settings, 'STYLES_DEFAULT', 'k2')

