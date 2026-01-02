# Renaming Summary: plex_monitor → Pulsarr

## Changed References

### Visual Branding
- **ASCII Logo**: Updated to "Pulsarr" in terminal banner
- **Project Name**: All references changed from "plex_monitor" to "Pulsarr"

### Files Changed
- `ui/ui_print.py` - New ASCII art logo + log file name
- `README.md` - Complete rebranding
- `SUMMARY.md` - All references updated
- `MIGRATION.md` - Migration guide updated

### Configuration & Logs
- **Log file**: `plex_monitor.log` → `pulsarr.log`
- **Config directory**: `/mnt/user/appdata/plex_monitor` → `/mnt/user/appdata/pulsarr`
- **Docker container name**: `plex-monitor` → `pulsarr`
- **Git repository**: `plex_monitor` → `pulsarr`

### Commands Updated
```bash
# Old
git clone https://github.com/mathiasmortus/plex_monitor.git
docker logs -f plex-monitor
tail -f plex_monitor.log

# New
git clone https://github.com/mathiasmortus/pulsarr.git
docker logs -f pulsarr
tail -f pulsarr.log
```

## What Wasn't Changed

- Python source code (no functional changes)
- `settings.json` format (fully compatible)
- API integrations (Sonarr/Radarr/Plex)
- Command-line usage (`python main.py -service`)

## Migration for Existing Users

If you're already using plex_monitor:

1. **Update your local repository**:
   ```bash
   git pull origin main
   ```

2. **Settings are preserved** - your `settings.json` will continue to work

3. **Update log file references**:
   - Old logs will remain in `plex_monitor.log`
   - New logs will be written to `pulsarr.log`

4. **Update Docker containers**:
   ```bash
   docker stop plex-monitor
   docker rm plex-monitor
   docker run -d --name pulsarr ... # use new name
   ```

## Why "Pulsarr"?

- **Puls**: Pulse/heartbeat - constantly monitoring
- **arr**: Aligns with Sonarr/Radarr naming convention
- **Pronounceable**: Easy to say and remember
- **Unique**: Searchable and distinct
