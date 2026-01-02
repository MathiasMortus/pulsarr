# Migration Guide: plex_debrid 2.x → Ocularr

This guide helps you migrate from the original plex_debrid (with debrid services) to Ocularr.

## What Changed?

### Removed Features
- All debrid services (Real-Debrid, All-Debrid, Premiumize, Debrid-Link, Put.io, Torbox)
- All torrent scrapers (RarBG, Jackett direct, Prowlarr direct, Torrentio, Nyaa, etc.)
- Release quality management and version filtering
- Manual scraper interface

### New Features
- Direct Sonarr integration for TV shows
- Direct Radarr integration for movies
- Simplified watchlist → download workflow

## Prerequisites

Before migrating, ensure you have:

1. **Sonarr v3+** installed and configured with:
   - At least one indexer (Jackett, Prowlarr, Usenet, etc.)
   - Quality profiles set up
   - Root folder configured
   - API key available

2. **Radarr v3+** installed and configured with:
   - At least one indexer (Jackett, Prowlarr, Usenet, etc.)
   - Quality profiles set up
   - Root folder configured
   - API key available

## Migration Steps

### Step 1: Backup Your Configuration

```bash
# Backup your current settings
cp settings.json settings.backup.json
```

### Step 2: Update the Code

```bash
# Pull the latest changes
git pull origin main

# Or clone fresh
git clone https://github.com/mathiasmortus/ocularr.git
cd ocularr
```

### Step 3: Run the Application

```bash
python main.py
```

You'll be prompted to reconfigure since the settings structure has changed.

### Step 4: Configure Content Services

Your **Plex** and **Trakt** watchlist settings will need to be re-entered:

1. Select **Content Services** → **Plex users**
2. Enter your Plex username
3. Enter your Plex token (find it at https://plex.tv/devices.xml)

For Trakt (optional):
1. Select **Content Services** → **Trakt users**
2. Follow the OAuth flow

### Step 5: Configure Sonarr

1. Select **Settings** → **Arr Services**
2. Enter **Sonarr Base URL**: e.g., `http://localhost:8989` or `http://sonarr:8989`
3. Enter **Sonarr API Key**:
   - Found in Sonarr: Settings → General → Security → API Key
4. Enter **Quality Profile ID**: (default is `1`)
   - To find yours: Sonarr → Settings → Profiles → note the ID number
5. Enter **Root Folder**: e.g., `/data/media/tv` or `/tv`
   - Must match a root folder configured in Sonarr

### Step 6: Configure Radarr

1. Still in **Settings** → **Arr Services**
2. Enter **Radarr Base URL**: e.g., `http://localhost:7878` or `http://radarr:7878`
3. Enter **Radarr API Key**:
   - Found in Radarr: Settings → General → Security → API Key
4. Enter **Quality Profile ID**: (default is `1`)
   - To find yours: Radarr → Settings → Profiles → note the ID number
5. Enter **Root Folder**: e.g., `/data/media/movies` or `/movies`
   - Must match a root folder configured in Radarr

### Step 7: Configure Library Services (Optional)

To avoid re-downloading content you already have:

1. Select **Settings** → **Library Services**
2. Choose **Library collection service** → select Plex or Jellyfin
3. Enter library connection details

### Step 8: Test the Integration

1. Select **Run** from the main menu
2. Add a test movie to your Plex watchlist
3. Watch the logs - you should see:
   ```
   processing movie: Test Movie (2024)
   Radarr: Looking up movie with TMDB ID: ...
   Radarr: Successfully added movie: Test Movie
   ```
4. Check Radarr - the movie should now be there with monitoring enabled

## Understanding the New Workflow

### Old Workflow (plex_debrid 2.x):
```
Watchlist → Scrape torrents → Check debrid cache → Add to debrid → Download
```

### New Workflow (Ocularr):
```
Watchlist → Add to Sonarr/Radarr (with monitoring) → Sonarr/Radarr handles the rest
```

## Key Differences

| Feature | Old (plex_debrid) | New (Sonarr/Radarr) |
|---------|-------------------|---------------------|
| Quality selection | Version filters in plex_debrid 2.x | Quality profiles in Sonarr/Radarr |
| Source selection | Multiple scrapers configured | Indexers configured in Sonarr/Radarr |
| Cache checking | Checked debrid cache before download | Sonarr/Radarr check availability |
| Download management | Handled by debrid service | Handled by Sonarr/Radarr |
| Manual scraping | Built-in scraper UI | Use Sonarr/Radarr manual search |

## Troubleshooting

### Configuration Errors

**Error: "Sonarr: Not configured"**
- Verify Sonarr base URL is accessible from where you're running Ocularr
- Test: `curl http://your-sonarr-url/api/v3/system/status -H "X-Api-Key: YOUR_API_KEY"`

**Error: "No TVDB ID found"**
- The show's Plex metadata is incomplete
- Solution: Refresh metadata in Plex, or manually add in Sonarr

**Error: "Root folder path not configured"**
- You haven't set the root folder in settings
- Must match exactly with a root folder in Sonarr/Radarr

### Connection Issues

**Sonarr/Radarr not reachable**

If running in Docker:
- Use service names instead of localhost: `http://sonarr:8989`
- Ensure containers are on the same network

If running locally:
- Use `http://localhost:8989` or `http://127.0.0.1:8989`

### Items Not Being Added

1. **Check if already in library**:
   - Library checking might be marking it as collected
   - Disable temporarily: Settings → Library Services → remove library collection service

2. **Check release status**:
   - Items must be released (not future releases)
   - Check the release date in Plex

3. **Enable debug logging**:
   - Settings → UI Settings → Debug printing → true
   - Run again and check detailed logs

## FAQ

**Q: Can I still use my debrid account?**
A: This version doesn't support debrid services. Sonarr/Radarr will download via their configured download clients (qBittorrent, SABnzbd, etc.)

**Q: What about quality preferences?**
A: Configure quality profiles in Sonarr/Radarr. The app uses the profile ID you specify in settings.

**Q: Can I manually search for releases?**
A: Yes, but through Sonarr/Radarr's UI, not through this app. The scraper feature has been removed.

**Q: Will my old watchlist items be processed?**
A: Yes! When you first run, it will process your entire current watchlist and add everything to Sonarr/Radarr.

**Q: Can I use multiple quality profiles?**
A: Currently, the app uses one profile ID for all shows (in Sonarr) and one for all movies (in Radarr). You can change these in settings.

## Getting Help

If you encounter issues:

1. Enable debug logging
2. Check the logs for specific error messages
3. Verify your Sonarr/Radarr setup works independently
4. Open a GitHub issue with:
   - Error messages
   - Your configuration (sanitized - remove API keys!)
   - Steps to reproduce

## Reverting to plex_debrid 2.x

If you need to revert:

```bash
# Checkout the last plex_debrid 2.x version
git checkout <previous-commit-hash>

# Restore your backup
cp settings.backup.json settings.json

# Run
python main.py
```
