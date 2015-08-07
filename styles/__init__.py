"""Styles module"""

import os

from k2.styles import settings

def get_style_list():
    return [f for f in os.listdir(settings.STYLES_ROOT) if os.path.isdir(os.path.join(settings.STYLES_ROOT, f))]
