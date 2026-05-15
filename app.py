import requests
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
        
    api_url = f"https://v01.io{video_url}"
    
    try:
        response = requests.get(api_url, timeout=15)
        if response.status_code != 200:
            return jsonify({'error': 'Gagal mengambil data dari server'}), 500
            
        video_data = response.json()
        formats = []
        
        for stream in video_data.get('urls', []):
            formats.append({
                'resolution': stream.get('subName', 'Video'),
                'ext': stream.get('ext', 'mp4'),
                'download_url': stream.get('url')
            })
            
        if not formats:
            return jsonify({'error': 'Video tidak didukung'}), 404
            
        return jsonify({
            'title': video_data.get('title', 'Video Download'),
            'thumbnail': video_data.get('id', 'https://unsplash.com'),
            'links': formats
        })
        
    except Exception as e:
        return jsonify({'error': 'Server sibuk, silakan coba lagi'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
