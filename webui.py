#!/usr/bin/env python3
"""
Web UI for plex_monitor configuration
Provides a browser-based interface for configuring settings instead of terminal menu
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from base import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'plex_monitor_secret_key'

CONFIG_FILE = './settings.json'

def load_settings():
    """Load settings from JSON file"""
    if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_settings(settings):
    """Save settings to JSON file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

@app.route('/')
def index():
    """Main configuration page"""
    settings = load_settings()
    return render_template('index.html', settings=settings)

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """API endpoint to get current settings"""
    return jsonify(load_settings())

@app.route('/api/settings', methods=['POST'])
def update_settings():
    """API endpoint to update settings"""
    try:
        settings = request.json
        save_settings(settings)
        return jsonify({'success': True, 'message': 'Settings saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Test connection to Sonarr/Radarr"""
    data = request.json
    service = data.get('service')
    base_url = data.get('base_url')
    api_key = data.get('api_key')

    if not base_url or not api_key:
        return jsonify({'success': False, 'message': 'Missing base_url or api_key'})

    try:
        import requests as req
        url = f"{base_url.rstrip('/')}/api/v3/system/status"
        headers = {'X-Api-Key': api_key}
        response = req.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'success': True,
                'message': f"Connected successfully to {service} (version {data.get('version', 'unknown')})"
            })
        else:
            return jsonify({
                'success': False,
                'message': f"Connection failed with status {response.status_code}"
            })
    except Exception as e:
        return jsonify({'success': False, 'message': f"Connection error: {str(e)}"})

@app.route('/api/get-root-folders', methods=['POST'])
def get_root_folders():
    """Get root folders from Sonarr/Radarr"""
    data = request.json
    base_url = data.get('base_url')
    api_key = data.get('api_key')

    if not base_url or not api_key:
        return jsonify({'success': False, 'message': 'Missing base_url or api_key'})

    try:
        import requests as req
        url = f"{base_url.rstrip('/')}/api/v3/rootfolder"
        headers = {'X-Api-Key': api_key}
        response = req.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            folders = response.json()
            return jsonify({
                'success': True,
                'folders': [{'path': f['path'], 'freeSpace': f.get('freeSpace', 0)} for f in folders]
            })
        else:
            return jsonify({'success': False, 'message': f"Failed to get root folders: {response.status_code}"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/get-quality-profiles', methods=['POST'])
def get_quality_profiles():
    """Get quality profiles from Sonarr/Radarr"""
    data = request.json
    base_url = data.get('base_url')
    api_key = data.get('api_key')

    if not base_url or not api_key:
        return jsonify({'success': False, 'message': 'Missing base_url or api_key'})

    try:
        import requests as req
        url = f"{base_url.rstrip('/')}/api/v3/qualityprofile"
        headers = {'X-Api-Key': api_key}
        response = req.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            profiles = response.json()
            return jsonify({
                'success': True,
                'profiles': [{'id': p['id'], 'name': p['name']} for p in profiles]
            })
        else:
            return jsonify({'success': False, 'message': f"Failed to get quality profiles: {response.status_code}"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/status')
def status():
    """Status page showing current configuration"""
    settings = load_settings()

    status_info = {
        'sonarr_configured': bool(settings.get('arr', {}).get('services', {}).get('sonarr', {}).get('base_url')),
        'radarr_configured': bool(settings.get('arr', {}).get('services', {}).get('radarr', {}).get('base_url')),
        'plex_configured': bool(settings.get('content', {}).get('services', {}).get('plex', {}).get('users')),
    }

    return render_template('status.html', settings=settings, status=status_info)

@app.route('/api/logs')
def get_logs():
    """API endpoint to get recent log entries"""
    log_file = './plex_monitor.log'

    try:
        if os.path.exists(log_file):
            # Get the last 100 lines of the log file
            with open(log_file, 'r') as f:
                lines = f.readlines()
                # Return last 100 lines
                recent_lines = lines[-100:] if len(lines) > 100 else lines
                return jsonify({
                    'success': True,
                    'logs': ''.join(recent_lines)
                })
        else:
            return jsonify({
                'success': True,
                'logs': 'No logs available yet. Start the service to see logs here.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/api/logs/stream')
def stream_logs():
    """Server-Sent Events endpoint for live log streaming"""
    def generate():
        log_file = './plex_monitor.log'

        # Send initial logs
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()
                recent_lines = lines[-50:] if len(lines) > 50 else lines
                for line in recent_lines:
                    yield f"data: {line}\n\n"

        # Keep connection open and send new logs as they appear
        last_size = os.path.getsize(log_file) if os.path.exists(log_file) else 0

        while True:
            import time
            time.sleep(1)

            if os.path.exists(log_file):
                current_size = os.path.getsize(log_file)
                if current_size > last_size:
                    with open(log_file, 'r') as f:
                        f.seek(last_size)
                        new_content = f.read()
                        for line in new_content.split('\n'):
                            if line:
                                yield f"data: {line}\n\n"
                    last_size = current_size

    return app.response_class(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    # Run the web server
    # Use 0.0.0.0 to allow external connections (Docker)
    app.run(host='0.0.0.0', port=5001, debug=False)
