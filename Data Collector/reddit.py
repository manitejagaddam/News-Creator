import requests
import json


def get_reddit_news(title : str = "Latest Open Source Models", limit : int = 5):
    url = f"https://www.reddit.com/r/{title}/hot.json?limit={limit}"
    headers = {'User-Agent': 'AI-News-Bot-v1'}
    data = requests.get(url, headers=headers).json()
    return [post['data']['title'] for post in data['data']['children']]