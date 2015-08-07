from urlparse import urljoin

from django.conf import settings

try:
    from PIL import Image
    dir(Image) # Placate PyFlakes
except ImportError:
    import Image

# AVATARS
# Paths
AVATAR_DIR = getattr(settings, 'AVATAR_DIR', 'img/avatars/')
AVATAR_DEFAULT = getattr(settings, 'AVATAR_DEFAULT', 'default.png')
AVATAR_DEFAULT_PATH = getattr(settings, 'AVATAR_DEFAULT_PATH', \
    urljoin(AVATAR_DIR, AVATAR_DEFAULT).replace('\\', '/'))
AVATAR_DEFAULT_URL = getattr(settings, 'AVATAR_DEFAULT', \
    urljoin(settings.MEDIA_URL, AVATAR_DEFAULT_PATH).replace('\\', '/'))
# Sizes
AVATAR_SMALL_SIZE = getattr(settings, 'AVATAR_SMALL_SIZE', (16,16))
AVATAR_MEDIUM_SIZE = getattr(settings, 'AVATAR_MEDIUM_SIZE', (48,48))
AVATAR_LARGE_SIZE = getattr(settings, 'AVATAR_LARGE_SIZE', (64,64))
AVATAR_DEFAULT_SIZE = getattr(settings, 'AVATAR_DEFAULT_SIZE', AVATAR_MEDIUM_SIZE)
AVATAR_SIZES = getattr(settings, 'AVATAR_SIZES', (AVATAR_SMALL_SIZE, AVATAR_MEDIUM_SIZE, AVATAR_LARGE_SIZE))
# Gravatar
AVATAR_GRAVATAR_BACKUP = getattr(settings, 'AVATAR_GRAVATAR_BACKUP', True)
AVATAR_GRAVATAR_DEFAULT = getattr(settings, 'AVATAR_GRAVATAR_DEFAULT', None)
# Filename
AVATAR_ALLOWED_FILE_EXTS = getattr(settings, 'AVATAR_ALLOWED_FILE_EXTS', None)
# Cache
AVATAR_CACHE_TIMEOUT = getattr(settings, 'AVATAR_CACHE_TIMEOUT', 60*60)

# KARMA
# User vote weights
VOTE_WEIGHT_ROOKIE = getattr(settings, 'VOTE_WEIGHT_ROOKIE', 1)
VOTE_WEIGHT_NEW = getattr(settings, 'VOTE_WEIGHT_NEW', 2)
VOTE_WEIGHT_NORMAL = getattr(settings, 'VOTE_WEIGHT_NORMAL', 3)
VOTE_WEIGHT_ADVANCED = getattr(settings, 'VOTE_WEIGHT_ADVANCED', 4)

