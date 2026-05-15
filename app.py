import subprocess
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/extract', methods=['POST'])
def extract_video():
    data = request.get_json()
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL tidak boleh kosong'}), 400

    command = [
    "yt-dlp", 
    "--no-warnings", 
    "-J", 
    "--no-playlist", 
    "--flat-playlist",
    "--no-check-certificate",
    "--socket-timeout", "7",
    "--extractor-args", "youtube:player_client=web",
    video_url
]


    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=25)
        if result.returncode != 0:
            return jsonify({'error': 'Gagal mengekstrak video'}), 500
            
        video_data = json.loads(result.stdout)
        formats = []
        for f in video_data.get('formats', []):
            if f.get('url') and f.get('vcodec') != 'none':
                formats.append({
                    'resolution': f.get('resolution', 'Unknown'),
                    'ext': f.get('ext', 'mp4'),
                    'download_url': f.get('url')
                })
                
        return jsonify({
            'title': video_data.get('title'),
            'thumbnail': video_data.get('thumbnail'),
            'links': formats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
