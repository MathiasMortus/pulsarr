<div align="center">
	<img src="https://i.imgur.com/Rk8khjF.png" alt="Pulsarr Logo" width="150"/>
<h1>Ocularr</h1>

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](VERSION.md)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
</div>

## What is this?

A lightweight automation tool that monitors your Plex watchlist and automatically adds:
- **TV shows** to Sonarr
- **Movies** to Radarr

This is a fork of plex_debrid that has been completely refactored to remove all debrid and scraper functionality, focusing solely on Plex watchlist → Sonarr/Radarr integration.

## How does it work?

1. Monitors your Plex watchlist (and optionally Trakt lists or Overseerr requests)
2. When you add something to your watchlist:
   - TV shows are automatically added to Sonarr with monitoring enabled
   - Movies are automatically added to Radarr with monitoring enabled
3. Sonarr/Radarr handle finding and downloading the content through their configured indexers
4. Optionally removes items from watchlist after successfully adding to Sonarr/Radarr

## Requirements

- Python 3.7+
- Plex account with watchlist access
- Sonarr v3+ (for TV shows)
- Radarr v3+ (for movies)
- Sonarr/Radarr must be configured with:
  - At least one indexer (Jackett, Prowlarr, etc.)
  - Quality profiles
  - Root folders

## Quick Start Guide

### Step 1: Install

```bash
git clone https://github.com/mathiasmortus/ocularr.git
cd ocularr
pip install -r requirements.txt
```

### Step 2: First-Time Configuration

Run the interactive setup:

```bash
python main.py
```

You'll be prompted to configure:

#### Required Settings

**Plex Token** (Content Services → Plex)
- Get your token from: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
- Example: `xyzABC123-example-token`

**Sonarr Configuration** (Arr Services → Sonarr)
- **Base URL**: `http://localhost:8989` (or your Sonarr server address)
- **API Key**: Found in Sonarr → Settings → General → Security → API Key
- **Quality Profile ID**: Usually `1` (can be found in Sonarr → Settings → Profiles)
- **Root Folder**: Must match exactly a root folder configured in Sonarr
  - Example: `/data/media/tv` or `/tv`
  - Find in Sonarr → Settings → Media Management → Root Folders

**Radarr Configuration** (Arr Services → Radarr)
- **Base URL**: `http://localhost:7878` (or your Radarr server address)
- **API Key**: Found in Radarr → Settings → General → Security → API Key
- **Quality Profile ID**: Usually `1` (can be found in Radarr → Settings → Profiles)
- **Root Folder**: Must match exactly a root folder configured in Radarr
  - Example: `/data/media/movies` or `/movies`
  - Find in Radarr → Settings → Media Management → Root Folders

#### Optional Settings

**Library Collection Service** (Library Services)
- Choose `plex` or `jellyfin` to check what's already in your library
- Prevents re-adding content you already have

**Trakt Integration** (Content Services → Trakt)
- Optional: Monitor Trakt lists in addition to Plex watchlist

### Step 3: Test the Connection

After configuration, the setup will automatically test connections to Sonarr and Radarr. You should see:
```
✓ Sonarr: Connected successfully (version X.X.X)
✓ Radarr: Connected successfully (version X.X.X)
```

If you see errors, check:
- URLs are accessible from where you're running Ocularr
- API keys are correct
- No typos in configuration

### Step 4: Test with Watchlist

1. Add a movie or TV show to your Plex watchlist
2. Run Ocularr:
   ```bash
   python main.py
   ```
3. Choose option `1) Run`
4. Watch the logs - you should see:
   ```
   processing movie: Test Movie (2024)
   Radarr: Looking up movie with TMDB ID: ...
   Radarr: Successfully added movie: Test Movie
   ```
5. Check Sonarr/Radarr - the content should now be there with monitoring enabled

## Usage Modes

### Interactive Mode (Terminal Menu)

```bash
python main.py
```

Menu Options:
1. **Run**: Start monitoring watchlists (runs continuously)
2. **Settings**: Modify configuration (Sonarr, Radarr, Plex, etc.)
3. **Ignored Media**: View and manage items you've marked to ignore

### Service Mode (Background/Docker)

For automated/production use:

```bash
python main.py -service
```

- Runs continuously without user interaction
- Perfect for Docker containers or background processes
- Checks watchlist every 30 seconds (configurable in settings)
- All activity logged to `ocularr.log`

**View logs in Docker**: Use `docker logs -f <container-name>` or Unraid's Docker console

## Configuration Details

### Finding Your Root Folders

Root folders must **exactly match** what's configured in Sonarr/Radarr:

**In Sonarr**:
1. Go to Settings → Media Management → Root Folders
2. Copy the exact path (e.g., `/data/media/tv`)
3. Paste this into Ocularr settings

**In Radarr**:
1. Go to Settings → Media Management → Root Folders
2. Copy the exact path (e.g., `/data/media/movies`)
3. Paste this into Ocularr settings

### Quality Profiles

Quality profiles control what quality releases Sonarr/Radarr will download:

1. Go to Settings → Profiles in Sonarr/Radarr
2. Note the ID of your preferred profile (hover over it or check the URL)
3. Use this ID in Ocularr settings (default is `1`)

### Checking Existing Library

Enable "Library Collection Service" to prevent re-adding content:

- Set to `plex` if using Plex as your media server
- Set to `jellyfin` if using Jellyfin
- Ocularr will check if content exists before adding to Sonarr/Radarr

## Docker / Unraid Setup

### Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3'
services:
  ocularr:
    image: your-image
    container_name: ocularr
    restart: unless-stopped
    volumes:
      - ./config:/app
    environment:
      - TZ=America/New_York
    command: python main.py -service
```

**First-time setup** (interactive configuration):
```bash
docker compose run --rm ocularr python main.py
```

**Normal operation**:
```bash
docker compose up -d
```

**View logs**:
```bash
docker compose logs -f
```

### Basic Docker Run

**First-time setup**:
```bash
docker run -it --rm \
  -v /path/to/config:/app \
  your-image python main.py
```

**Normal operation**:
```bash
docker run -d \
  --name ocularr \
  --restart unless-stopped \
  -v /path/to/config:/app \
  your-image python main.py -service
```

**View logs**:
```bash
docker logs -f ocularr
```

### Unraid Setup

#### Unraid Template

```xml
<Container version="2">
  <Name>ocularr</Name>
  <Repository>your-image</Repository>
  <Registry>https://hub.docker.com/</Registry>
  <Config Name="Config Directory" Target="/app" Default="/mnt/user/appdata/ocularr" Mode="rw" Description="Configuration directory" Type="Path" Display="always" Required="true" Mask="false">/mnt/user/appdata/ocularr</Config>
  <Config Name="Timezone" Target="TZ" Default="America/New_York" Mode="" Description="Timezone" Type="Variable" Display="always" Required="false" Mask="false">America/New_York</Config>
  <PostArgs>python main.py -service</PostArgs>
</Container>
```

#### Setup Steps for Unraid

1. **Install the container** using the template above
2. **Configure using Unraid Console**:
   - Click on the container icon
   - Select "Console"
   - Run: `python main.py`
   - Follow the interactive setup prompts
3. **Restart the container** - it will now run in service mode
4. **View logs**: Click container → "Logs" or use Console with `tail -f ocularr.log`

## Features

- ✅ Automatic watchlist monitoring (default: every 30 seconds)
- ✅ Sonarr integration for TV shows
- ✅ Radarr integration for movies
- ✅ Library checking to avoid duplicates
- ✅ Auto-search enabled (Sonarr/Radarr immediately search for content)
- ✅ Auto-remove from watchlist after adding (configurable)
- ✅ Support for Plex, Trakt, and Overseerr watchlists
- ✅ Jellyfin library support
- ✅ Comprehensive logging to file

## Troubleshooting

### "Sonarr: Not configured"
**Cause**: Missing or incorrect Sonarr configuration

**Solution**:
1. Verify Sonarr is running and accessible
2. Check the base URL is correct (include `http://` or `https://`)
3. Verify API key is correct (no extra spaces)
4. Test manually: `curl http://your-sonarr-url/api/v3/system/status -H "X-Api-Key: YOUR_API_KEY"`

### "No TVDB ID found" (TV Shows)
**Cause**: Plex metadata is incomplete or missing TVDB ID

**Solution**:
1. In Plex, go to the show → "Get Info" → "View XML"
2. Look for `tvdb://` - if missing, refresh metadata
3. Or manually add the show directly in Sonarr

### "No TMDB/IMDB ID found" (Movies)
**Cause**: Plex metadata is incomplete

**Solution**:
1. Refresh metadata in Plex for that movie
2. Or manually add the movie directly in Radarr

### "Root folder path not configured"
**Cause**: Root folder not set in Ocularr settings

**Solution**:
1. Go to Settings → Arr Services → Sonarr/Radarr
2. Set the root folder path
3. Must match exactly what's in Sonarr/Radarr → Settings → Root Folders

### Items not being added
**Possible causes**:
- Items not yet released (future release dates)
- Items already in library (if library checking is enabled)
- Missing metadata (no TVDB/TMDB/IMDB ID)

**Solution**:
1. Enable debug logging: Settings → UI Settings → Debug printing → `true`
2. Check logs for detailed error messages
3. Verify item has been released
4. Check if item already exists in Sonarr/Radarr

### "KeyError: 'Show Menu on Startup'"
**Cause**: Old or incomplete settings.json file

**Solution**: Already fixed in latest version. If you still see this, delete `settings.json` and reconfigure.

## Key Changes from plex_debrid

This fork has been completely refactored:

### Removed
- ❌ All debrid services (Real-Debrid, AllDebrid, Premiumize, etc.)
- ❌ All torrent scrapers (RarBG, Jackett, Prowlarr, Torrentio, etc.)
- ❌ Release quality management and version filtering
- ❌ Manual scraper interface
- ❌ Web UI configuration

### Added
- ✅ Sonarr API integration
- ✅ Radarr API integration
- ✅ Simplified workflow focused on watchlist → arr services
- ✅ Auto-search on add

### Philosophy
**Keep it simple**: No databases, no web UIs, no complex dependencies. Just a straightforward Python script that monitors watchlists and adds content to Sonarr/Radarr.

## Migrating from plex_debrid 2.x

If you're migrating from the original plex_debrid:

1. **Backup** your current `settings.json`
2. Pull the latest changes or clone fresh
3. Run `python main.py` - you'll be prompted to reconfigure
4. Your Plex and Trakt watchlist settings may be preserved
5. You'll need to configure new Sonarr and Radarr settings

See [MIGRATION.md](MIGRATION.md) for detailed migration guide.

## Advanced Configuration

### Check Interval
Default: 30 seconds

To change: Settings → UI Settings → Check Interval

### Auto-remove from Watchlist
Default: Enabled

To change: Settings → Content Services → Remove from watchlist after adding

### Multiple Plex Users
You can configure multiple Plex users to monitor their watchlists:

Settings → Content Services → Plex → Add Users

## Logs

All activity is logged to `ocularr.log` with timestamps:

```
[31/12/25 10:30:15] processing movie: Test Movie (2024)
[31/12/25 10:30:16] Radarr: Looking up movie with TMDB ID: 12345
[31/12/25 10:30:17] Radarr: Successfully added movie: Test Movie
```

View logs:
- **Local**: `tail -f ocularr.log`
- **Docker**: `docker logs -f ocularr`
- **Unraid**: Container → Logs button

## Environment Variables

Optional environment variables for Docker:

- `TZ`: Timezone (e.g., `America/New_York`)
- `CLIENT_ID`: Trakt OAuth client ID (if using Trakt)
- `CLIENT_SECRET`: Trakt OAuth client secret (if using Trakt)

## Documentation

- 🚀 [QUICK_START.md](QUICK_START.md) - Get up and running fast
- 📖 [VERSION.md](VERSION.md) - Version history and changelog
- 🔢 [VERSION_CHEATSHEET.md](VERSION_CHEATSHEET.md) - Quick version numbering guide
- 📝 [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- 🔄 [MIGRATION.md](MIGRATION.md) - Migrate from plex_debrid
- 📊 [SUMMARY.md](SUMMARY.md) - Project overview

## Support

This is a community fork. For issues or questions:
- 🐛 [Open a GitHub issue](https://github.com/mathiasmortus/ocularr/issues)
- 📖 Check the documentation above
- 💬 Be specific about your setup and error messages

## Contributing

Contributions welcome! Please:
1. Keep it simple (follow the project philosophy)
2. Test thoroughly
3. Update documentation
4. **Update version in `/ui/ui_settings.py`** (see [CONTRIBUTING.md](CONTRIBUTING.md))

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines and version numbering.

## License

Same as original plex_debrid project.

## Thanks to these contributors!

<!-- readme: collaborators,contributors -start -->
<table>
	<tbody>
		<tr>
            <td align="center">
                <a href="https://github.com/itsToggle">
                    <img src="https://avatars.githubusercontent.com/u/71379623?v=4" width="64;" alt="itsToggle"/>
                    <br />
                    <sub><b>itsToggle</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/funkypenguin">
                    <img src="https://avatars.githubusercontent.com/u/1524686?v=4" width="64;" alt="funkypenguin"/>
                    <br />
                    <sub><b>funkypenguin</b></sub>
                </a>
            </td>
		<td align="center">
                <a href="https://github.com/mathiasmortus">
                    <img src="https://avatars.githubusercontent.com/u/77238760?v=4" width="64;" alt="mortus"/>
                    <br />
                    <sub><b>mortus</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/sirstudly">
                    <img src="https://avatars.githubusercontent.com/u/12377354?v=4" width="64;" alt="sirstudly"/>
                    <br />
                    <sub><b>sirstudly</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/themegaphoenix">
                    <img src="https://avatars.githubusercontent.com/u/9766462?v=4" width="64;" alt="themegaphoenix"/>
                    <br />
                    <sub><b>themegaphoenix</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/KaceCottam">
                    <img src="https://avatars.githubusercontent.com/u/28381193?v=4" width="64;" alt="KaceCottam"/>
                    <br />
                    <sub><b>KaceCottam</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/KamalF">
                    <img src="https://avatars.githubusercontent.com/u/8170277?v=4" width="64;" alt="KamalF"/>
                    <br />
                    <sub><b>KamalF</b></sub>
                </a>
            </td>
		</tr>
		<tr>
            <td align="center">
                <a href="https://github.com/maspuce">
                    <img src="https://avatars.githubusercontent.com/u/688714?v=4" width="64;" alt="maspuce"/>
                    <br />
                    <sub><b>maspuce</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Murmiration">
                    <img src="https://avatars.githubusercontent.com/u/26490372?v=4" width="64;" alt="Murmiration"/>
                    <br />
                    <sub><b>Murmiration</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/codevski">
                    <img src="https://avatars.githubusercontent.com/u/1435321?v=4" width="64;" alt="codevski"/>
                    <br />
                    <sub><b>codevski</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/kana2001">
                    <img src="https://avatars.githubusercontent.com/u/71416354?v=4" width="64;" alt="kana2001"/>
                    <br />
                    <sub><b>kana2001</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/master131">
                    <img src="https://avatars.githubusercontent.com/u/1592009?v=4" width="64;" alt="master131"/>
                    <br />
                    <sub><b>master131</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/mcorcoran">
                    <img src="https://avatars.githubusercontent.com/u/1950615?v=4" width="64;" alt="mcorcoran"/>
                    <br />
                    <sub><b>mcorcoran</b></sub>
                </a>
            </td>
		</tr>
		<tr>
            <td align="center">
                <a href="https://github.com/piratsch">
                    <img src="https://avatars.githubusercontent.com/u/106690882?v=4" width="64;" alt="piratsch"/>
                    <br />
                    <sub><b>piratsch</b></sub>
                </a>
            </td>
		</tr>
	<tbody>
</table>
<!-- readme: collaborators,contributors -end -->
