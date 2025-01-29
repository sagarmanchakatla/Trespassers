# from flask import Flask, request, jsonify
# import requests

# app = Flask(__name__)

# # Replace with your actual YouTube Data API key
# YOUTUBE_API_KEY = 'AIzaSyBe6hKp5D_VNizwr1BvhDxpbbH4IuJWVZ4'
# YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'

# @app.route('/api/youtube/<channel>', methods=['GET'])
# def search_youtube(channel):
#     # channel_name = request.args.get(channel)
#     if not channel:
#         return jsonify({"error": "Channel name is required"}), 400

#     params = {
#         'key': YOUTUBE_API_KEY,
#         'q': channel,
#         'type': 'video',
#         'part': 'snippet',
#         'maxResults': 10  # You can adjust the number of results
#     }

#     response = requests.get(YOUTUBE_API_URL, params=params)
#     if response.status_code != 200:
#         return jsonify({"error": "Failed to fetch data from YouTube API"}), 500

#     data = response.json()
#     return jsonify(data)

# if __name__ == '__main__':
#     app.run(port=5001, debug=True)


# from flask import Flask, jsonify
# import os
# import json
# from datetime import datetime, timedelta
# import pytz
# import requests

# app = Flask(__name__)

# # Replace with your actual YouTube Data API key
# YOUTUBE_API_KEY = 'AIzaSyBe6hKp5D_VNizwr1BvhDxpbbH4IuJWVZ4'
# YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'

# # Cache directory for storing YouTube API responses
# CACHE_DIR = "youtube_cache"
# TIMEZONE = pytz.UTC

# class YouTubeCache:
#     def __init__(self):
#         self.cache_dir = CACHE_DIR
#         self.ensure_cache_directory()

#     def ensure_cache_directory(self):
#         """Ensure the cache directory exists."""
#         if not os.path.exists(self.cache_dir):
#             os.makedirs(self.cache_dir)

#     def get_cache_path(self, channel_name):
#         """Get the cache file path for a specific channel."""
#         return os.path.join(self.cache_dir, f"{channel_name}.json")

#     def is_cache_valid(self, channel_name):
#         """Check if the cache is valid (less than 24 hours old)."""
#         cache_path = self.get_cache_path(channel_name)
#         if not os.path.exists(cache_path):
#             return False

#         try:
#             with open(cache_path, 'r') as f:
#                 cache_data = json.load(f)
#             last_updated = datetime.fromisoformat(cache_data.get("last_updated"))
#             return datetime.now(TIMEZONE) - last_updated < timedelta(hours=24)
#         except:
#             return False

#     def save_to_cache(self, channel_name, data):
#         """Save the API response to the cache."""
#         cache_path = self.get_cache_path(channel_name)
#         cache_data = {
#             "last_updated": datetime.now(TIMEZONE).isoformat(),
#             "data": data
#         }
#         with open(cache_path, 'w') as f:
#             json.dump(cache_data, f, indent=4)

#     def get_cached_data(self, channel_name):
#         """Retrieve cached data for a specific channel."""
#         cache_path = self.get_cache_path(channel_name)
#         try:
#             with open(cache_path, 'r') as f:
#                 cache_data = json.load(f)
#             return cache_data["data"]
#         except:
#             return None

# # Initialize the cache
# youtube_cache = YouTubeCache()

# @app.route('/api/youtube/<channel>', methods=['GET'])
# def search_youtube(channel):
#     """Fetch YouTube data for a specific channel, using cache if available."""
#     if not channel:
#         return jsonify({"error": "Channel name is required"}), 400

#     # Check if valid cache exists
#     if youtube_cache.is_cache_valid(channel):
#         print(f"Using cached data for {channel}")
#         cached_data = youtube_cache.get_cached_data(channel)
#         return jsonify(cached_data)

#     # Fetch fresh data from YouTube API
#     print(f"Fetching fresh data for {channel}")
#     params = {
#         'key': YOUTUBE_API_KEY,
#         'q': channel,
#         'type': 'video',
#         'part': 'snippet',
#         'maxResults': 10  # Adjust the number of results as needed
#     }

#     response = requests.get(YOUTUBE_API_URL, params=params)
#     if response.status_code != 200:
#         return jsonify({"error": "Failed to fetch data from YouTube API"}), 500

#     data = response.json()

#     # Save the response to cache
#     youtube_cache.save_to_cache(channel, data)

#     return jsonify(data)

# if __name__ == '__main__':
#     app.run(port=5001, debug=True)



from flask import Flask, jsonify
from flask_cors import CORS 
import os
import json
from datetime import datetime, timedelta
import pytz
import requests

app = Flask(__name__)
CORS(app) 


# Replace with your actual YouTube Data API key
YOUTUBE_API_KEY = 'AIzaSyBe6hKp5D_VNizwr1BvhDxpbbH4IuJWVZ4'
YOUTUBE_API_BASE_URL = 'https://www.googleapis.com/youtube/v3'
CACHE_DIR = "youtube_cache"
TIMEZONE = pytz.UTC

class YouTubeCache:
    def __init__(self):
        self.cache_dir = CACHE_DIR
        self.ensure_cache_directory()

    def ensure_cache_directory(self):
        """Ensure the cache directory exists."""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def get_cache_path(self, channel_name, data_type='basic'):
        """Get the cache file path for a specific channel and data type."""
        return os.path.join(self.cache_dir, f"{channel_name}_{data_type}.json")

    def is_cache_valid(self, channel_name, data_type='basic'):
        """Check if the cache is valid (less than 24 hours old)."""
        cache_path = self.get_cache_path(channel_name, data_type)
        if not os.path.exists(cache_path):
            return False
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            last_updated = datetime.fromisoformat(cache_data.get("last_updated"))
            return datetime.now(TIMEZONE) - last_updated < timedelta(hours=24)
        except:
            return False

    def save_to_cache(self, channel_name, data, data_type='basic'):
        """Save the API response to the cache."""
        cache_path = self.get_cache_path(channel_name, data_type)
        cache_data = {
            "last_updated": datetime.now(TIMEZONE).isoformat(),
            "data": data
        }
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f, indent=4)

    def get_cached_data(self, channel_name, data_type='basic'):
        """Retrieve cached data for a specific channel and data type."""
        cache_path = self.get_cache_path(channel_name, data_type)
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            return cache_data["data"]
        except:
            return None

class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.cache = YouTubeCache()

    def get_channel_id(self, channel_name):
        """Get channel ID from channel name."""
        params = {
            'key': self.api_key,
            'q': channel_name,
            'type': 'channel',
            'part': 'snippet',
            'maxResults': 1
        }
        response = requests.get(f"{YOUTUBE_API_BASE_URL}/search", params=params)
        if response.status_code == 200:
            data = response.json()
            if data['items']:
                return data['items'][0]['snippet']['channelId']
        return None

    def get_channel_videos(self, channel_id, max_results=50):
        """Get videos from a channel with their statistics."""
        # First, get video IDs
        params = {
            'key': self.api_key,
            'channelId': channel_id,
            'type': 'video',
            'part': 'id',
            'maxResults': max_results,
            'order': 'date'
        }
        response = requests.get(f"{YOUTUBE_API_BASE_URL}/search", params=params)
        if response.status_code != 200:
            return None

        video_ids = [item['id']['videoId'] for item in response.json().get('items', [])]
        
        # Then, get video statistics
        params = {
            'key': self.api_key,
            'id': ','.join(video_ids),
            'part': 'snippet,statistics'
        }
        response = requests.get(f"{YOUTUBE_API_BASE_URL}/videos", params=params)
        if response.status_code != 200:
            return None

        return response.json().get('items', [])

    def sort_videos(self, videos, sort_by='likes', ascending=False):
        """Sort videos by specified metric."""
        try:
            return sorted(
                videos,
                key=lambda x: int(x['statistics'].get(sort_by, 0)),
                reverse=not ascending
            )
        except:
            return videos

@app.route('/api/youtube/<channel>', methods=['GET'])
def get_channel_stats(channel):
    """Get comprehensive channel statistics including most/least liked and commented videos."""
    youtube_api = YouTubeAPI(YOUTUBE_API_KEY)
    
    # Check cache first
    if youtube_api.cache.is_cache_valid(channel, 'stats'):
        return jsonify(youtube_api.cache.get_cached_data(channel, 'stats'))

    # Get channel ID
    channel_id = youtube_api.get_channel_id(channel)
    if not channel_id:
        return jsonify({"error": "Channel not found"}), 404

    # Get videos with statistics
    videos = youtube_api.get_channel_videos(channel_id)
    if not videos:
        return jsonify({"error": "Failed to fetch video data"}), 500

    # Prepare response data
    response_data = {
        "channel_name": channel,
        "channel_id": channel_id,
        "video_stats": {
            "most_liked": youtube_api.sort_videos(videos, 'likeCount')[:5],
            "least_liked": youtube_api.sort_videos(videos, 'likeCount', True)[:5],
            "most_commented": youtube_api.sort_videos(videos, 'commentCount')[:5],
            "least_commented": youtube_api.sort_videos(videos, 'commentCount', True)[:5]
        }
    }

    # Cache the results
    youtube_api.cache.save_to_cache(channel, response_data, 'stats')

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5001, debug=True)