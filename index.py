from flask import Flask, request, jsonify
from googleapiclient.discovery import build

app = Flask(__name__)

API_KEY = 'YOUR_YOUTUBE_API_KEY'
youtube = build('youtube', 'v3', developerKey=API_KEY)

@app.route('/search-videos', methods=['POST'])
def search_videos():
    data = request.json
    language = data.get('language', 'en')
    query = data.get('query', '')

    yt_request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=1,
        order="relevance",
        relevanceLanguage=language
    )
    response = yt_request.execute()

    videos = [
        {
            'title': item['snippet']['title'],
            'videoId': item['id']['videoId'],
            'description': item['snippet']['description'],
            'thumbnail': item['snippet']['thumbnails']['high']['url'],
        }
        for item in response.get('items', [])
        if item['snippet']['title'] and item['snippet']['description']
    ]

    return jsonify(videos if videos else {"message": "No relevant videos found."})

if __name__ == '__main__':
    app.run(debug=True)
