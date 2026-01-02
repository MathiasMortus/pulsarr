# Contributing to Ocularr

Thank you for considering contributing to Ocularr! This guide will help you make changes and update the version correctly.

## Quick Start for Contributors

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Update the version** (see below)
5. **Test your changes**
6. **Commit with descriptive message**
7. **Push and create Pull Request**

## Updating Version Numbers

### Where to Update

The version is defined in `/ui/ui_settings.py`:

```python
version = ['1.0.0', "Description of changes", []]
```

### When to Update

**Every time you make changes**, update the version according to semantic versioning:

#### Patch Release (1.0.X)
**For bug fixes and small improvements**

```python
version = ['1.0.1', "Fix TVDB ID parsing error", []]
```

Examples:
- Fixing crashes or errors
- Improving error messages
- Documentation updates
- Code cleanup without functional changes

#### Minor Release (1.X.0)
**For new features (non-breaking)**

```python
version = ['1.1.0', "Add Discord notification support", []]
```

Examples:
- Adding new integrations
- Adding new configuration options
- Adding new features
- Performance improvements

#### Major Release (X.0.0)
**For breaking changes**

```python
version = ['2.0.0', "New settings format (migration required)", []]
```

Examples:
- Changing settings.json format
- Removing features
- Major refactors that break compatibility
- Python version requirement changes

### Update Process

1. **Edit `/ui/ui_settings.py`**:
   ```python
   version = ['NEW_VERSION', "Description of what changed", []]
   ```

2. **Update `/VERSION.md`**:
   Add entry to changelog:
   ```markdown
   ### X.Y.Z (YYYY-MM-DD)
   **Description**

   **Added/Changed/Fixed:**
   - List your changes
   ```

3. **Update badges in `/README.md`** (if major/minor):
   ```markdown
   [![Version](https://img.shields.io/badge/version-X.Y.Z-blue.svg)](VERSION.md)
   ```

## Development Guidelines

### Philosophy

**Keep it simple** - The core principle of Ocularr is simplicity:

- ❌ Don't add databases
- ❌ Don't add web UIs (removed intentionally)
- ❌ Don't add complex dependencies
- ✅ Do add simple, focused features
- ✅ Do improve error handling
- ✅ Do improve documentation

### Code Style

- Follow existing code patterns
- Use function-level imports to avoid circular dependencies
- Add error handling with descriptive messages
- Log important actions for debugging

Example:
```python
def my_function():
    from ui.ui_print import ui_print
    from ui import ui_settings

    try:
        # Your code here
        ui_print("Success message")
        return True
    except Exception as e:
        ui_print(f"Error: {str(e)}", debug=ui_settings.debug)
        return False
```

### Testing

Before submitting:

1. **Test basic flow**:
   ```bash
   python main.py
   # Go through setup
   # Add item to watchlist
   # Verify it's added to Sonarr/Radarr
   ```

2. **Test service mode**:
   ```bash
   python main.py -service
   # Let it run for a few cycles
   # Check logs for errors
   ```

3. **Test error handling**:
   - Try with wrong API keys
   - Try with unavailable URLs
   - Try with missing metadata

## What We're Looking For

### High Priority

1. **Bug Fixes**
   - Crashes or errors
   - API integration issues
   - Configuration problems

2. **Documentation**
   - Improving setup guides
   - Adding troubleshooting tips
   - Clarifying confusing parts

3. **Error Handling**
   - Better error messages
   - Retry logic for transient failures
   - Validation before API calls

### Medium Priority

4. **Simple Features**
   - Notification support (Discord, Telegram)
   - Health check endpoint
   - Better logging options

5. **Performance**
   - Reducing API calls
   - Optimizing check intervals
   - Memory improvements

### Not Wanted

- ❌ Web UI (intentionally removed)
- ❌ Database support (keep it stateless)
- ❌ Complex quality management (use Sonarr/Radarr)
- ❌ Built-in scrapers (use Sonarr/Radarr indexers)

## Example Contribution

### Bug Fix Example

**Problem**: App crashes when TVDB ID is missing

**Solution**:
1. Add null check in `arr/services/sonarr.py`
2. Update version: `['1.0.1', "Fix crash when TVDB ID missing", []]`
3. Add to VERSION.md changelog
4. Test with item that has no TVDB ID
5. Commit: `git commit -m "Fix: Handle missing TVDB ID gracefully"`

### Feature Example

**Feature**: Add Discord notifications

**Solution**:
1. Create `/notifications/discord.py`
2. Add Discord webhook URL to settings
3. Send notification when item added successfully
4. Update version: `['1.1.0', "Add Discord notification support", []]`
5. Update VERSION.md and README.md
6. Test with actual Discord webhook
7. Commit: `git commit -m "Feature: Add Discord notifications"`

## Pull Request Process

1. **Descriptive title**: "Fix: Handle missing TVDB ID" or "Feature: Add Discord notifications"

2. **Description should include**:
   - What problem does this solve?
   - How did you test it?
   - Does it change the version? (yes, always)
   - Breaking changes? (if major version)

3. **Checklist**:
   - [ ] Version updated in `/ui/ui_settings.py`
   - [ ] Changelog updated in `/VERSION.md`
   - [ ] README.md badge updated (if needed)
   - [ ] Tested locally
   - [ ] No breaking changes (or documented if major version)

## Questions?

- Open a GitHub issue
- Check existing issues first
- Be respectful and constructive

## License

By contributing, you agree your contributions will be licensed under the same license as Ocularr.

---

**Thank you for helping make Ocularr better!** 🎉
