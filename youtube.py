import requests
from typing import List, Dict

def get_trending_videos(api_key: str, region_code: str = 'VN', max_results: int = 10) -> List[Dict]:
    """
    Get trending videos for a specific region
    """
    url = "https://www.googleapis.com/youtube/v3/videos"
    
    params = {
        'part': 'snippet,contentDetails,statistics',
        'chart': 'mostPopular',
        'regionCode': region_code,
        'maxResults': max_results,
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        trending_videos = []
        for item in data.get('items', []):
            video_info = {
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channel_title': item['snippet']['channelTitle'],
                'published_at': item['snippet']['publishedAt'],
                'view_count': item['statistics'].get('viewCount', 0),
                'like_count': item['statistics'].get('likeCount', 0),
                'comment_count': item['statistics'].get('commentCount', 0),
                'thumbnail': item['snippet']['thumbnails']['high']['url']
            }
            trending_videos.append(video_info)
        
        return trending_videos
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending videos: {e}")
        return []

# Usage example
API_KEY = 'AIzaSyA4vROMhOAyd7ZYc51n8Xau4dvYbgoYFfs'

# Get trending videos for different regions
vn_trending = get_trending_videos(API_KEY, 'VN', 10)


# Print results
for video in vn_trending:
    print(f"Title: {video['title']}")
    print(f"Channel: {video['channel_title']}")
    print(f"Views: {video['view_count']}")
    print("---")