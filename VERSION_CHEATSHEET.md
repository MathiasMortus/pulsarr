# Version Update Cheat Sheet

## Quick Reference

### Every time you make changes:

1. **Update `/ui/ui_settings.py`**:
   ```python
   version = ['X.Y.Z', "What you changed", []]
   ```

2. **Add to `/VERSION.md`** changelog

3. **Update README badge** (if major/minor)

---

## Version Number Guide

### What number to use?

| Change Type | Version | Example |
|------------|---------|---------|
| **Bug fix** | 1.0.X | `1.0.1` |
| **New feature** | 1.X.0 | `1.1.0` |
| **Breaking change** | X.0.0 | `2.0.0` |

---

## Examples

### Bug Fix (1.0.0 → 1.0.1)

**File**: `/ui/ui_settings.py`
```python
version = ['1.0.1', "Fix crash when TVDB ID is missing", []]
```

**File**: `/VERSION.md`
```markdown
### 1.0.1 (2026-01-03)
**Bug Fixes**

**Fixed:**
- 🐛 App no longer crashes when TVDB ID is missing
- 🐛 Better error message for missing metadata
```

---

### New Feature (1.0.1 → 1.1.0)

**File**: `/ui/ui_settings.py`
```python
version = ['1.1.0', "Add Discord notification support", []]
```

**File**: `/VERSION.md`
```markdown
### 1.1.0 (2026-01-05)
**New Features**

**Added:**
- ✅ Discord webhook notifications
- ✅ Configurable notification events
```

**File**: `/README.md`
```markdown
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](VERSION.md)
```

---

### Breaking Change (1.1.0 → 2.0.0)

**File**: `/ui/ui_settings.py`
```python
version = ['2.0.0', "New settings format (migration required)", []]
```

**File**: `/VERSION.md`
```markdown
### 2.0.0 (2026-02-01)
**BREAKING CHANGES**

**Changed:**
- 🔄 Settings file format changed from JSON to YAML
- 🔄 Requires manual migration (see MIGRATION.md)

**Migration Guide:**
Run `python migrate.py` to convert settings
```

**File**: `/README.md`
```markdown
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](VERSION.md)
```

---

## Current Version

**Version**: `1.0.0`
**Next Version**:
- Bug fix → `1.0.1`
- Feature → `1.1.0`
- Breaking → `2.0.0`

---

## Don't Forget!

✅ Update `/ui/ui_settings.py`
✅ Update `/VERSION.md`
✅ Update `/README.md` badge (if major/minor)
✅ Test your changes
✅ Git commit with version in message

Example commit:
```bash
git commit -m "v1.0.1: Fix crash when TVDB ID is missing"
```

---

## See Also

- [VERSION.md](VERSION.md) - Full version history
- [CONTRIBUTING.md](CONTRIBUTING.md) - Detailed contribution guide
