import requests
import re
import sys
from typing import Optional

def extract_channel_id(url: str) -> Optional[str]:
    if "@" in url:
        match = re.search(r'@[\w.-]+', url)
        if match:
            return match.group(0)[1:]
    elif "channel/" in url:
        match = re.search(r'channel/([\w-]+)', url)
        if match:
            return match.group(1)
    elif "user/" in url:
        match = re.search(r'user/([\w-]+)', url)
        if match:
            return match.group(1)
    return None

def get_channel_data(channel_id: str, api_key: str) -> dict:
    base_url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "snippet,contentDetails,statistics,brandingSettings",
        "id": channel_id,
        "key": api_key
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    
    if not data.get("items"):
        raise ValueError(f"No channel found with ID: {channel_id}")
    
    return data["items"][0]

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_api.py <channel_url_or_id> [api_key]")
        sys.exit(1)
    
    url_or_id = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not api_key:
        api_key = input("Enter your YouTube Data API v3 key: ").strip()
    
    channel_id = extract_channel_id(url_or_id) or url_or_id
    
    data = get_channel_data(channel_id, api_key)
    print(data)

if __name__ == "__main__":
    main()
