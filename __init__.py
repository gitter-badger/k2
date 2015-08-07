"""K2 site project

Closed social website for links exchange
"""

__author__ = "Artur Maciag"
__copyright__ = "Copyright 2010, Artur Maciag"
__credits__ = ["Artur Maciag"]

__license__ = "GPL"
__version__ = "0.3.0 alpha1"
__maintainer__ = "Artur Maciag"
__email__ = "maciag.artur@gmail.com"
__status__ = "Development"

VERSION = (0, 3, 0, 'alpha', 1)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = "%s %s" % (version, VERSION[3])
            if VERSION[4] != 0:
                version = '%s %s' % (version, VERSION[4])
    return version

from k2.utils.django import InstallDjangoShotrcuts, InstallDjangoAuthentication
from k2.utils.oembed import InstallOEmbed
from k2.utils.threadedcomments import InstallThreadedComments
from k2.utils.invitation import InstallInvtation

def InstallDjango():
    InstallDjangoShotrcuts()
    InstallDjangoAuthentication()

InstallDjango()
InstallOEmbed()
InstallThreadedComments()
InstallInvtation()