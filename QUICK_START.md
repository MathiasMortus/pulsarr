# Pulsarr - Quick Start

## For First-Time Users

### 1. Install
```bash
git clone https://github.com/mathiasmortus/pulsarr.git
cd pulsarr
pip install -r requirements.txt
```

### 2. Configure
```bash
python main.py
# Follow the interactive setup prompts
```

You need:
- Plex token
- Sonarr URL + API key + root folder
- Radarr URL + API key + root folder

### 3. Run
```bash
python main.py -service
```

### 4. Check Logs
```bash
tail -f pulsarr.log
```

---

## For Docker Users

### First-Time Setup
```bash
docker run -it --rm \
  -v ./config:/app \
  ghcr.io/mathiasmortus/pulsarr:latest \
  python main.py
```

### Normal Operation
```bash
docker run -d \
  --name pulsarr \
  --restart unless-stopped \
  -v ./config:/app \
  ghcr.io/mathiasmortus/pulsarr:latest \
  python main.py -service
```

### View Logs
```bash
docker logs -f pulsarr
```

---

## For Developers

### Making Changes

1. **Edit code**
2. **Update version** in `/ui/ui_settings.py`:
   ```python
   version = ['X.Y.Z', "What you changed", []]
   ```
3. **Test**: `python main.py`
4. **Commit**: `git commit -m "vX.Y.Z: Description"`

See [VERSION_CHEATSHEET.md](VERSION_CHEATSHEET.md) for version numbering guide.

---

## Common Tasks

### Update Version
Edit `/ui/ui_settings.py`:
```python
version = ['1.0.1', "Bug fixes", []]
```

### Enable Debug Logging
Settings → UI Settings → Debug printing → `true`

### Change Check Interval
Settings → UI Settings → Loop interval seconds → `60` (for 1 minute)

### View Configuration
```bash
cat settings.json
```

### Reset Configuration
```bash
rm settings.json
python main.py  # Will run setup again
```

---

## Need Help?

- 📖 Full guide: [README.md](README.md)
- 🔧 Troubleshooting: [README.md#troubleshooting](README.md#troubleshooting)
- 📝 Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- 🔢 Version guide: [VERSION_CHEATSHEET.md](VERSION_CHEATSHEET.md)
- 🐛 Report issues: [GitHub Issues](https://github.com/mathiasmortus/pulsarr/issues)

---

## Current Version

**v1.0.0** - Initial Pulsarr release

See [VERSION.md](VERSION.md) for full changelog.
