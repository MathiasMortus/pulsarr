from ui.ui_print import *
import arr.services

def add(media_item):
    """
    Route media item to appropriate arr service (Sonarr for TV, Radarr for movies)
    Returns: True if successfully added, False otherwise
    """
    if not hasattr(media_item, 'type'):
        ui_print("arr: Media item has no type attribute")
        return False

    if media_item.type == 'movie':
        # Use Radarr for movies
        from arr.services import radarr
        if radarr.base_url and radarr.api_key:
            return radarr.add_from_media(media_item)
        else:
            ui_print("arr: Radarr not configured")
            return False

    elif media_item.type == 'show':
        # Use Sonarr for TV shows
        from arr.services import sonarr
        if sonarr.base_url and sonarr.api_key:
            return sonarr.add_from_media(media_item)
        else:
            ui_print("arr: Sonarr not configured")
            return False

    else:
        ui_print(f"arr: Unsupported media type: {media_item.type}")
        return False
