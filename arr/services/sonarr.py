from base import *
from ui.ui_print import *

name = 'Sonarr'
short = 'SONARR'
base_url = ""
api_key = ""
quality_profile_id = "1"
root_folder_path = ""
session = requests.Session()

def setup(cls, new=False):
    from arr.services import setup
    setup(cls, new)

def test_connection():
    """Test connection to Sonarr"""
    if not base_url or not api_key:
        ui_print("Sonarr: base_url or api_key not configured", debug=ui_settings.debug)
        return False

    try:
        url = f"{base_url.rstrip('/')}/api/v3/system/status"
        headers = {'X-Api-Key': api_key}
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            ui_print(f"Sonarr: Connected successfully (version {data.get('version', 'unknown')})", debug=ui_settings.debug)
            return True
        else:
            ui_print(f"Sonarr: Connection failed with status {response.status_code}", debug=ui_settings.debug)
            return False
    except Exception as e:
        ui_print(f"Sonarr: Connection error: {str(e)}", debug=ui_settings.debug)
        return False

def get_quality_profiles():
    """Get available quality profiles"""
    try:
        url = f"{base_url.rstrip('/')}/api/v3/qualityprofile"
        headers = {'X-Api-Key': api_key}
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            ui_print(f"Sonarr: Failed to get quality profiles: {response.status_code}", debug=ui_settings.debug)
            return []
    except Exception as e:
        ui_print(f"Sonarr: Error getting quality profiles: {str(e)}", debug=ui_settings.debug)
        return []

def get_root_folders():
    """Get available root folders"""
    try:
        url = f"{base_url.rstrip('/')}/api/v3/rootfolder"
        headers = {'X-Api-Key': api_key}
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            ui_print(f"Sonarr: Failed to get root folders: {response.status_code}", debug=ui_settings.debug)
            return []
    except Exception as e:
        ui_print(f"Sonarr: Error getting root folders: {str(e)}", debug=ui_settings.debug)
        return []

def search_series(tvdb_id):
    """Look up series by TVDB ID"""
    try:
        url = f"{base_url.rstrip('/')}/api/v3/series/lookup?term=tvdb:{tvdb_id}"
        headers = {'X-Api-Key': api_key}
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            results = response.json()
            if results and len(results) > 0:
                return results[0]
        return None
    except Exception as e:
        ui_print(f"Sonarr: Error searching series: {str(e)}", debug=ui_settings.debug)
        return None

def add_series(series_data, monitored=True, search_missing=False):
    """Add series to Sonarr"""
    try:
        url = f"{base_url.rstrip('/')}/api/v3/series"
        headers = {'X-Api-Key': api_key, 'Content-Type': 'application/json'}

        payload = {
            'tvdbId': series_data['tvdbId'],
            'title': series_data['title'],
            'qualityProfileId': int(quality_profile_id),
            'titleSlug': series_data['titleSlug'],
            'images': series_data.get('images', []),
            'seasons': series_data.get('seasons', []),
            'rootFolderPath': root_folder_path,
            'monitored': monitored,
            'addOptions': {
                'searchForMissingEpisodes': search_missing
            }
        }

        response = session.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code in [200, 201]:
            ui_print(f"Sonarr: Successfully added series: {series_data['title']}")
            return True
        elif response.status_code == 400:
            error_msg = response.json()
            if 'already been added' in str(error_msg).lower() or 'already exists' in str(error_msg).lower():
                ui_print(f"Sonarr: Series already exists: {series_data['title']}", debug=ui_settings.debug)
                return True  # Consider this a success
            else:
                ui_print(f"Sonarr: Failed to add series: {error_msg}")
                return False
        else:
            ui_print(f"Sonarr: Failed to add series (status {response.status_code}): {response.text}")
            return False
    except Exception as e:
        ui_print(f"Sonarr: Error adding series: {str(e)}")
        return False

def add_from_media(media_item):
    """Add series from media item to Sonarr"""
    if not base_url or not api_key:
        ui_print("Sonarr: Not configured (missing base_url or api_key)")
        return False

    if not root_folder_path:
        ui_print("Sonarr: Root folder path not configured")
        return False

    # Extract TVDB ID from media item
    tvdb_id = None
    if hasattr(media_item, 'EID'):
        for eid in media_item.EID:
            if eid.startswith('tvdb://'):
                tvdb_id = eid.replace('tvdb://', '')
                break

    if not tvdb_id:
        ui_print(f"Sonarr: No TVDB ID found for {getattr(media_item, 'title', 'unknown')}")
        return False

    ui_print(f"Sonarr: Looking up series with TVDB ID: {tvdb_id}", debug=ui_settings.debug)

    # Search for series in Sonarr
    series_data = search_series(tvdb_id)

    if not series_data:
        ui_print(f"Sonarr: Could not find series with TVDB ID: {tvdb_id}")
        return False

    # Add series to Sonarr with monitoring enabled
    return add_series(series_data, monitored=True, search_missing=False)
