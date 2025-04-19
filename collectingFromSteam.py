import requests
import pandas as pd
import time

APP_ID = 730
REVIEW_COUNT = 1000
PER_PAGE = 100
LANG = 'all'

reviews = []
cursor = '*'
collected = 0

while collected < REVIEW_COUNT:
    url = f"https://store.steampowered.com/appreviews/{APP_ID}?json=1"
    params = {
        'num_per_page': PER_PAGE,
        'cursor': cursor,
        'filter': 'recent',
        'language': LANG,
        'purchase_type': 'all'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'reviews' not in data or not data['reviews']:
        print("No more reviews")
        break

    for review in data['reviews']:
        reviews.append({
            'recommendation': review['voted_up'],
            'review': review['review'],
            'timestamp_created': review['timestamp_created'],
            'author': review['author']['steamid']
        })
        collected += 1
        if collected >= REVIEW_COUNT:
            break

    cursor = data.get('cursor')
    if not cursor:
        break

    print(f"Collected: {collected}/{REVIEW_COUNT}")
    time.sleep(0.3)

df = pd.DataFrame(reviews)
df.to_csv('steam_reviews_1000.csv', index=False, encoding='utf-8-sig')
print(f"Saved  {len(df)} in steam_reviews_1000.csv")
