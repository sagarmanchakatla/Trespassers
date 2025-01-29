from flask import Flask, jsonify
import os
import json
from datetime import datetime, timedelta
import pytz
from instaloader import Instaloader, Profile
import time
from pathlib import Path

app = Flask(__name__)

class InstagramAnalyzer:
    def __init__(self):
        self.L = Instaloader()
        self.cache_dir = "instagram_cache"
        self.ensure_cache_directory()
        self.timezone = pytz.UTC

    def ensure_cache_directory(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def get_cache_path(self, username):
        return os.path.join(self.cache_dir, f"{username}")

    def save_to_cache(self, username, data):
        user_cache_dir = self.get_cache_path(username)
        if not os.path.exists(user_cache_dir):
            os.makedirs(user_cache_dir)

        with open(os.path.join(user_cache_dir, "profile_info.json"), 'w', encoding='utf-8') as f:
            json.dump(data['profile_info'], f, ensure_ascii=False, indent=4)

        with open(os.path.join(user_cache_dir, "posts_data.json"), 'w', encoding='utf-8') as f:
            json.dump(data['posts_data'], f, ensure_ascii=False, indent=4)

        with open(os.path.join(user_cache_dir, "analytics.json"), 'w', encoding='utf-8') as f:
            json.dump(data['analytics'], f, ensure_ascii=False, indent=4)

        metadata = {
            "last_updated": datetime.now(self.timezone).isoformat(),
            "username": username
        }
        with open(os.path.join(user_cache_dir, "metadata.json"), 'w') as f:
            json.dump(metadata, f, indent=4)

    def is_cache_valid(self, username):
        """Check if cache is valid (less than 24 hours old)"""
        metadata_path = os.path.join(self.get_cache_path(username), "metadata.json")
        if not os.path.exists(metadata_path):
            return False

        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            last_updated = datetime.fromisoformat(metadata["last_updated"])
            return datetime.now(self.timezone) - last_updated < timedelta(hours=24)
        except:
            return False

    def get_cached_data(self, username):
        user_cache_dir = self.get_cache_path(username)
        data = {}

        try:
            with open(os.path.join(user_cache_dir, "profile_info.json"), 'r', encoding='utf-8') as f:
                data['profile_info'] = json.load(f)
            with open(os.path.join(user_cache_dir, "posts_data.json"), 'r', encoding='utf-8') as f:
                data['posts_data'] = json.load(f)
            with open(os.path.join(user_cache_dir, "analytics.json"), 'r', encoding='utf-8') as f:
                data['analytics'] = json.load(f)
            return data
        except:
            return None

    def analyze_profile(self, username):
        # First check cache
        if self.is_cache_valid(username):
            print(f"Using cached data for {username}")
            return self.get_cached_data(username)

        print(f"Fetching fresh data for {username}")
        try:
            profile = Profile.from_username(self.L.context, username)
            
            profile_info = {
                "username": profile.username,
                "followers": profile.followers,
                "following": profile.followees,
                "media_count": profile.mediacount,
                "biography": profile.biography,
                "external_url": profile.external_url,
                "full_name": profile.full_name,
                "is_private": profile.is_private,
                "is_verified": profile.is_verified
            }

            engagement_metrics = {
                "most_liked_post": None,
                "least_liked_post": None,
                "most_liked_reel": None,
                "least_liked_reel": None,
                "most_commented_post": None,
                "least_commented_post": None,
                "most_commented_reel": None,
                "least_commented_reel": None
            }

            posts_data = []
            for post in profile.get_posts():
                post_date = post.date_local.replace(tzinfo=self.timezone)
                
                post_data = {
                    "shortcode": post.shortcode,
                    "caption": post.caption[:500] if post.caption else "",
                    "likes": post.likes,
                    "comments": post.comments,
                    "is_video": post.is_video,
                    "date": post_date.isoformat(),
                    "post_link": f"https://www.instagram.com/p/{post.shortcode}/"
                }

                posts_data.append(post_data)

                if post.is_video:
                    if not engagement_metrics["most_liked_reel"] or post.likes > engagement_metrics["most_liked_reel"]["likes"]:
                        engagement_metrics["most_liked_reel"] = post_data
                    if not engagement_metrics["least_liked_reel"] or post.likes < engagement_metrics["least_liked_reel"]["likes"]:
                        engagement_metrics["least_liked_reel"] = post_data
                    if not engagement_metrics["most_commented_reel"] or post.comments > engagement_metrics["most_commented_reel"]["comments"]:
                        engagement_metrics["most_commented_reel"] = post_data
                    if not engagement_metrics["least_commented_reel"] or post.comments < engagement_metrics["least_commented_reel"]["comments"]:
                        engagement_metrics["least_commented_reel"] = post_data
                else:
                    if not engagement_metrics["most_liked_post"] or post.likes > engagement_metrics["most_liked_post"]["likes"]:
                        engagement_metrics["most_liked_post"] = post_data
                    if not engagement_metrics["least_liked_post"] or post.likes < engagement_metrics["least_liked_post"]["likes"]:
                        engagement_metrics["least_liked_post"] = post_data
                    if not engagement_metrics["most_commented_post"] or post.comments > engagement_metrics["most_commented_post"]["comments"]:
                        engagement_metrics["most_commented_post"] = post_data
                    if not engagement_metrics["least_commented_post"] or post.comments < engagement_metrics["least_commented_post"]["comments"]:
                        engagement_metrics["least_commented_post"] = post_data

                time.sleep(0.5)  # Rate limiting

            data = {
                "profile_info": profile_info,
                "posts_data": posts_data,
                "analytics": engagement_metrics
            }

            self.save_to_cache(username, data)
            return data

        except Exception as e:
            print(f"Error analyzing profile: {str(e)}")
            return None

# Initialize analyzer
analyzer = InstagramAnalyzer()

@app.route('/api/profile/<username>')
def get_profile_data(username):
    """Get profile data, either from cache or fresh from Instagram"""
    data = analyzer.analyze_profile(username)
    if data:
        return jsonify({
            "status": "success",
            "data": data
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch profile data"
        }), 400

@app.route('/api/profile/<username>/analytics')
def get_profile_analytics(username):
    """Get only analytics data"""
    data = analyzer.analyze_profile(username)
    if data and 'analytics' in data:
        return jsonify({
            "status": "success",
            "data": data['analytics']
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch analytics data"
        }), 400

@app.route('/api/profile/<username>/info')
def get_profile_info(username):
    """Get only profile information"""
    data = analyzer.analyze_profile(username)
    if data and 'profile_info' in data:
        return jsonify({
            "status": "success",
            "data": data['profile_info']
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch profile information"
        }), 400

if __name__ == '__main__':
    app.run(debug=True)