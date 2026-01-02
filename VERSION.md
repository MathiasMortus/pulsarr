# Pulsarr - Version History

## How to Update Version

When making changes, update the version in `/ui/ui_settings.py`:

```python
version = ['X.Y.Z', "Description of changes", []]
```

### Semantic Versioning Guide

- **Major (X.0.0)**: Breaking changes, major refactors
  - Example: Changing settings format, removing features

- **Minor (1.X.0)**: New features, non-breaking changes
  - Example: Adding new integrations, new configuration options

- **Patch (1.0.X)**: Bug fixes, small improvements
  - Example: Fixing errors, improving error messages

## Version History

### 1.0.0 (2026-01-02)
**Initial Pulsarr Release**

Complete fork and refactor of plex_debrid 2.x

**Added:**
- ✅ Sonarr v3 API integration for TV shows
- ✅ Radarr v3 API integration for movies
- ✅ Auto-search enabled when adding to Sonarr/Radarr
- ✅ Simple service mode for Docker deployment
- ✅ Comprehensive logging to `pulsarr.log`

**Removed:**
- ❌ All debrid services (Real-Debrid, AllDebrid, Premiumize, etc.) - ~1000 lines
- ❌ All torrent scrapers (19+ scrapers) - ~3000 lines
- ❌ Release quality/version management - ~1700 lines
- ❌ Web UI configuration interface
- ❌ Database dependencies

**Changed:**
- 🔄 Project renamed from plex_debrid to Pulsarr
- 🔄 Simplified architecture focused on watchlist → arr services
- 🔄 Log file: `plex_debrid.log` → `pulsarr.log`

**Fixed:**
- 🐛 Circular import issues with function-level imports
- 🐛 `ui_settings` not defined errors in Sonarr/Radarr modules
- 🐛 `KeyError: 'Show Menu on Startup'` crash

**Technical:**
- Net reduction: ~5700 lines removed, ~400 lines added (93% smaller)
- Dependencies: Removed Flask, kept core dependencies only
- Philosophy: "Keep it simple" - no databases, no web UIs

---

## Future Version Planning

### 1.1.0 (Planned)
**Potential additions:**
- Notification system (Discord, Telegram, Pushover)
- Health check endpoint for monitoring
- Better error retry logic
- Statistics tracking (items added, success rate)

### 1.0.1 (Next Patch)
**Potential fixes:**
- Any bug reports from initial release
- Documentation improvements
- Docker image optimizations

---

## Version Bumping Examples

**Bug fix (1.0.0 → 1.0.1):**
```python
version = ['1.0.1', "Fix TVDB ID parsing error", []]
```

**New feature (1.0.1 → 1.1.0):**
```python
version = ['1.1.0', "Add Discord notification support", []]
```

**Breaking change (1.1.0 → 2.0.0):**
```python
version = ['2.0.0', "New settings format (migration required)", []]
```

---

## Changelog Template

When you make changes, add them here:

```markdown
### X.Y.Z (YYYY-MM-DD)
**Description**

**Added:**
- Feature 1
- Feature 2

**Changed:**
- Change 1
- Change 2

**Fixed:**
- Bug fix 1
- Bug fix 2

**Removed:**
- Deprecated feature 1
```

---

## Current Version

**Latest:** `1.0.0`
**Status:** Stable
**Release Date:** 2026-01-02
**Compatibility:** Python 3.7+, Sonarr v3+, Radarr v3+
