# Complete List of Changes

This document lists all changes made to transform plex_debrid into a Plex Watchlist → Sonarr/Radarr integration tool.

## Files Created

### Arr Integration Module
- [arr/__init__.py](arr/__init__.py) - Main orchestration for routing media to Sonarr/Radarr
- [arr/services/__init__.py](arr/services/__init__.py) - Service registry
- [arr/services/sonarr.py](arr/services/sonarr.py) - Sonarr v3 API integration (~200 lines)
- [arr/services/radarr.py](arr/services/radarr.py) - Radarr v3 API integration (~200 lines)

### Documentation
- [MIGRATION.md](MIGRATION.md) - Comprehensive migration guide from plex_debrid 2.x
- [CHANGES.md](CHANGES.md) - This file

## Files Modified

### Core Application Files

#### [settings/__init__.py](settings/__init__.py)
- **Line 3-5**: Removed imports for `scraper`, `releases`, `debrid`
- **Line 4**: Added import for `arr`
- **Lines 367-398**: Removed 'Scraper Settings' section (32 lines)
- **Lines 399-425**: Removed 'Debrid Services' section (27 lines)
- **Lines 367-400**: Added 'Arr Services' section with:
  - Sonarr Base URL, API Key, Quality Profile ID, Root Folder
  - Radarr Base URL, API Key, Quality Profile ID, Root Folder

#### [content/classes.py](content/classes.py)
- **Line 3-5**: Removed imports for `releases`, `debrid`, `scraper`
- **Line 3**: Added import for `arr`
- **Line 269**: Removed `downloaded_versions = []` class variable
- **Line 676-678**: Replaced `versions()` method with stub returning empty list
- **Line 823-825**: Replaced `version_missing()` method with stub returning False
- **Line 841-843**: Replaced `set_file_names()` method with pass stub
- **Line 1153-1154**: Replaced `downloading()` method with stub returning False
- **Lines 1164-1178**: Added new `arr_add()` method for Sonarr/Radarr integration
- **Lines 1180-1220**: Completely rewrote `download()` method:
  - Removed all scraping logic (~300 lines)
  - Removed all debrid download logic (~300 lines)
  - Simplified to just validate and call `arr_add()`
  - Season/episode handling removed (Sonarr/Radarr manage this)
- **Lines 1222-1359**: Removed `downloaded()` method (138 lines)
- **Lines 1260-1300**: Removed `debrid_download()` method (40 lines)
- **Lines 1302-1320**: Removed `files()` method (18 lines)
- **Lines 1322-1338**: Removed `bitrate()` method (16 lines)
- **Lines 1340-1358**: Removed `season_pack()` method (18 lines)

#### [ui/__init__.py](ui/__init__.py)
- **Lines 3-6**: Removed imports for `scraper`, `releases`, `debrid`
- **Line 4**: Added import for `arr`
- **Lines 57-177**: Removed entire `scrape()` function (120 lines)
- **Line 103**: Removed 'Scraper' option from menu

#### [content/services/plex.py](content/services/plex.py)
- **Lines 352, 553**: Updated message to remove "mounted debrid service drive" reference
- **Lines 511-513**: Simplified library refresh logic, removed `downloaded_releases` handling

## Files Deleted

### Modules
- `/debrid/` - Entire directory (~1000 lines)
  - `/debrid/__init__.py`
  - `/debrid/services/__init__.py`
  - `/debrid/services/realdebrid.py`
  - `/debrid/services/alldebrid.py`
  - `/debrid/services/premiumize.py`
  - `/debrid/services/debridlink.py`
  - `/debrid/services/putio.py`
  - `/debrid/services/torbox.py`

- `/scraper/` - Entire directory (~3000 lines)
  - All torrent scraper implementations

- `/releases/` - Entire directory (~1700 lines)
  - Quality management and version filtering

### Total Code Removed
Approximately **5,700 lines** of code removed.

## Functional Changes

### Removed Features
1. **Debrid Integration**
   - All 6 debrid service integrations removed
   - Cache checking removed
   - Torrent streaming via debrid removed
   - Uncached download handling removed

2. **Torrent Scraping**
   - All 19+ scraper sources removed
   - Manual scraper UI removed
   - Release quality filtering removed
   - Version management removed

3. **Download Management**
   - Bitrate calculation removed
   - File name matching removed
   - Season pack detection removed
   - Multi-season release handling removed
   - Episode-level download handling removed

### New Features
1. **Sonarr Integration**
   - Automatic TV show addition with monitoring
   - TVDB ID-based lookups
   - Quality profile configuration
   - Root folder configuration
   - Duplicate detection (already in Sonarr)

2. **Radarr Integration**
   - Automatic movie addition with monitoring
   - TMDB/IMDB ID-based lookups
   - Quality profile configuration
   - Root folder configuration
   - Duplicate detection (already in Radarr)

### Preserved Features
1. **Watchlist Monitoring**
   - Plex watchlist support (maintained)
   - Trakt lists support (maintained)
   - Overseerr requests support (maintained)
   - Configurable polling interval (maintained)

2. **Library Management**
   - Plex library checking (maintained)
   - Jellyfin library support (maintained)
   - Auto-remove from watchlist (maintained)
   - Ignored media tracking (maintained)

## Configuration Changes

### Removed Settings
- Debrid Services selection
- Real-Debrid API Key
- All-Debrid API Key
- Premiumize API Key
- Debrid-Link API Key
- Put.io API Key
- Torbox API Key
- Tracker-specific Debrid Services
- Sources selection
- Versions configuration
- Special character renaming
- All scraper-specific settings (RarBG, Jackett, Prowlarr, Nyaa, Torrentio, Zilean, Mediafusion, Comet, Orionoid)

### Added Settings
- Sonarr Base URL (required)
- Sonarr API Key (required)
- Sonarr Quality Profile ID
- Sonarr Root Folder (required)
- Radarr Base URL (required)
- Radarr API Key (required)
- Radarr Quality Profile ID
- Radarr Root Folder (required)

### Preserved Settings
- Content Services (Plex, Trakt, Overseerr)
- Plex users and tokens
- Trakt authentication
- Library Services configuration
- UI Settings (debug, logging, loop interval)

## New Workflow

### Old Workflow
```
Watchlist → Scrape Sources → Check Debrid Cache → Add to Debrid → Stream/Download
```

### New Workflow
```
Watchlist → Check Library → Add to Sonarr/Radarr (monitored) → Done
```

Sonarr/Radarr then handle:
- Searching their configured indexers
- Downloading via their download clients
- Managing quality upgrades
- Organizing files
- Library scanning

## Testing Performed

- ✅ Python syntax validation on all modified files
- ✅ Import cleanup verified (no orphaned imports)
- ✅ Directory structure created correctly
- ✅ All debrid/scraper/releases references removed

## Next Steps for Users

1. Update Sonarr and Radarr to v3+
2. Configure indexers in Sonarr/Radarr (Jackett, Prowlarr, etc.)
3. Set up quality profiles
4. Configure root folders
5. Run `python main.py` and configure arr settings
6. Test by adding an item to Plex watchlist

## Compatibility Notes

- Requires Sonarr v3 or later
- Requires Radarr v3 or later
- Python 3.7+ (unchanged)
- All other dependencies remain the same (see requirements.txt)
