import yfinance as yf
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
import os
import requests  # for RSS fallback

MOCK_SOCIAL_DATA = {
    'RELIANCE.NS': [
        {'text': 'Reliance breaking out! Massive volume on breakout candle #RIL', 'timestamp': '2024-10-01'},
        {'text': 'Reliance Q2 results tomorrow. Expecting 15% beat', 'timestamp': '2024-10-02'},
        # ... 50+ samples
    ]
    # Add more symbols
}

def fetch_news(symbol: str, period_days: int = 7) -> List[Dict]:
    '''Fetch real news from yfinance (free, no API key)'''
    ticker = yf.Ticker(symbol)
    news = ticker.news
    
    headlines = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_days)
    
    for item in news:
        pub_ts = datetime.fromtimestamp(item['providerPublishTime'])
        if start_date <= pub_ts <= end_date:
            headlines.append({
                'title': item['title'],
                'text': item['title'],  # Use title as proxy for full text
                'timestamp': pub_ts.isoformat(),
                'source': item.get('publisher', {}).get('name', 'Yahoo')
            })
    
    return headlines

def fetch_social_mock(symbol: str, num_samples: int = 20) -> List[Dict]:
    '''Mock social media posts (tweets/reddit)'''
    if symbol in MOCK_SOCIAL_DATA:
        posts = MOCK_SOCIAL_DATA[symbol][:num_samples]
    else:
        posts = [
            {'text': f'{symbol} looking bullish today!', 'timestamp': '2024-10-03T10:00:00'},
            {'text': f'Bearish divergence on {symbol}', 'timestamp': '2024-10-03T11:00:00'},
        ] * (num_samples // 2)
    
    return posts

def fetch_news_social(symbol: str, period_days: int = 7) -> Dict[str, List[Dict]]:
    '''Fetch news + social for symbol'''
    return {
        'news': fetch_news(symbol, period_days),
        'social': fetch_social_mock(symbol),
        'symbol': symbol,
        'fetched_at': datetime.now().isoformat()
    }

def load_mock_data(symbol: str) -> Dict:
    '''Load static mock dataset'''
    mock_file = f'mock_news_social_{symbol.replace(".", "_")}.json'
    if os.path.exists(mock_file):
        with open(mock_file, 'r') as f:
            return json.load(f)
    return {'error': 'Mock file not found'}

if __name__ == '__main__':
    data = fetch_news_social('RELIANCE.NS')
    print(json.dumps(data, indent=2))
    # Save mock
    with open('mock_news_social_RELIANCE_NS.json', 'w') as f:
        json.dump(data, f, indent=2)

