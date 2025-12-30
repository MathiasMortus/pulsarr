from ui.ui_print import *

active = []

def get():
    """Get active arr services"""
    activeservices = []
    for servicename in active:
        if servicename == 'Sonarr':
            from arr.services import sonarr
            activeservices.append(sonarr)
        elif servicename == 'Radarr':
            from arr.services import radarr
            activeservices.append(radarr)
    return activeservices

def setup(cls, new=False):
    """Setup arr service"""
    if not new:
        # Test connection
        if hasattr(cls, 'test_connection'):
            cls.test_connection()
