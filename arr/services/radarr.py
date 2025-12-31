from base import *

name = 'Radarr'
short = 'RADARR'
base_url = ""
api_key = ""
quality_profile_id = "1"
root_folder_path = ""
session = requests.Session()

def setup(cls, new=False):
    from arr.services import setup
    setup(cls, new)

def test_connection():
    """Test connection to Radarr"""
    from ui.ui_print import ui_print
    from ui import ui_settings

    if not base_url or not api_key:
        ui_print("Radarr: base_url or api_key not configured", debug=ui_settings.debug)
        return False

    try:
        url = f"{base_url.rstrip('/')}/api/v3/system/status"
        headers = {'X-Api-Key': api_key}
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            ui_print(f"Radarr: Connected successfully (version {data.get('version', 'unknown')})", debug=ui_settings.debug)
            return True
        else:
            ui_print(f"Radarr: Connection failed with status {response.status_code}", debug=ui_settings.debug)
            return False
    except Exception as e:
        ui_print(f"Radarr: Connection error: {str(e)}", debug=ui_settings.debug)
        return False

def get_quality_profiles():
    """Get available quality profiles"""
    from ui.ui_print import ui_print
    from ui import ui_settings

    try:
        url = f"{base_url.rstrip('/')}/api/v3/qualityprofile"
        headers = {'X-Api-Key': api_key}
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            ui_print(f"Radarr: Failed to get quality profiles: {response.status_code}", debug=ui_settings.debug)
            return []
    except Exception as e:
        ui_print(f"Radarr: Error getting quality profiles: {str(e)}", debug=ui_settings.debug)
        return []

def get_root_folders():
    """Get available root folders"""
    from ui.ui_print import ui_print
    from ui import ui_settings

    try:
        url = f"{base_url.rstrip('/')}/api/v3/rootfolder"
        headers = {'X-Api-Key': api_key}
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            ui_print(f"Radarr: Failed to get root folders: {response.status_code}", debug=ui_settings.debug)
            return []
    except Exception as e:
        ui_print(f"Radarr: Error getting root folders: {str(e)}", debug=ui_settings.debug)
        return []

def search_movie(tmdb_id=None, imdb_id=None):
    """Look up movie by TMDB or IMDB ID"""
    from ui.ui_print import ui_print
    from ui import ui_settings

    try:
        # Prefer TMDB ID
        if tmdb_id:
            url = f"{base_url.rstrip('/')}/api/v3/movie/lookup/tmdb?tmdbId={tmdb_id}"
        elif imdb_id:
            url = f"{base_url.rstrip('/')}/api/v3/movie/lookup/imdb?imdbId={imdb_id}"
        else:
            return None

        headers = {'X-Api-Key': api_key}
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if result:
                return result
        return None
    except Exception as e:
        ui_print(f"Radarr: Error searching movie: {str(e)}", debug=ui_settings.debug)
        return None

def add_movie(movie_data, monitored=True, search_now=False):
    """Add movie to Radarr"""
    from ui.ui_print import ui_print
    from ui import ui_settings

    try:
        url = f"{base_url.rstrip('/')}/api/v3/movie"
        headers = {'X-Api-Key': api_key, 'Content-Type': 'application/json'}

        payload = {
            'tmdbId': movie_data['tmdbId'],
            'title': movie_data['title'],
            'qualityProfileId': int(quality_profile_id),
            'titleSlug': movie_data['titleSlug'],
            'images': movie_data.get('images', []),
            'year': movie_data.get('year', 0),
            'rootFolderPath': root_folder_path,
            'monitored': monitored,
            'addOptions': {
                'searchForMovie': search_now
            }
        }

        response = session.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code in [200, 201]:
            ui_print(f"Radarr: Successfully added movie: {movie_data['title']}")
            return True
        elif response.status_code == 400:
            error_msg = response.json()
            if 'already been added' in str(error_msg).lower() or 'already exists' in str(error_msg).lower():
                ui_print(f"Radarr: Movie already exists: {movie_data['title']}", debug=ui_settings.debug)
                return True  # Consider this a success
            else:
                ui_print(f"Radarr: Failed to add movie: {error_msg}")
                return False
        else:
            ui_print(f"Radarr: Failed to add movie (status {response.status_code}): {response.text}")
            return False
    except Exception as e:
        ui_print(f"Radarr: Error adding movie: {str(e)}")
        return False

def add_from_media(media_item):
    """Add movie from media item to Radarr"""
    from ui.ui_print import ui_print
    from ui import ui_settings

    if not base_url or not api_key:
        ui_print("Radarr: Not configured (missing base_url or api_key)")
        return False

    if not root_folder_path:
        ui_print("Radarr: Root folder path not configured")
        return False

    # Extract TMDB or IMDB ID from media item
    tmdb_id = None
    imdb_id = None

    if hasattr(media_item, 'EID'):
        for eid in media_item.EID:
            if eid.startswith('tmdb://'):
                tmdb_id = eid.replace('tmdb://', '')
            elif eid.startswith('imdb://'):
                imdb_id = eid.replace('imdb://', '')

    if not tmdb_id and not imdb_id:
        ui_print(f"Radarr: No TMDB or IMDB ID found for {getattr(media_item, 'title', 'unknown')}")
        return False

    ui_print(f"Radarr: Looking up movie with TMDB ID: {tmdb_id} / IMDB ID: {imdb_id}", debug=ui_settings.debug)

    # Search for movie in Radarr
    movie_data = search_movie(tmdb_id=tmdb_id, imdb_id=imdb_id)

    if not movie_data:
        ui_print(f"Radarr: Could not find movie with TMDB: {tmdb_id} or IMDB: {imdb_id}")
        return False

    # Add movie to Radarr with monitoring enabled and trigger automatic search
    return add_movie(movie_data, monitored=True, search_now=True)
