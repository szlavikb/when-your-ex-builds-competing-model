from f1_app.aggregator import FeedAggregator
from f1_app.standings import StandingsFetcher

feeds = [
    'https://www.planetf1.com/feed/',
    'https://www.autosport.com/feed/',
    'https://www.motorsport.com/rss/all/',
]

agg = FeedAggregator(feeds)
stand = StandingsFetcher()

print('Fetching feeds...')
items = agg.fetch()
print('Feeds fetched:', len(items))
if items:
    print('First item:', items[0].get('title'), items[0].get('link'))

print('\nFetching standings...')
s = stand.fetch()
print('Drivers:', len(s.get('drivers', [])))
if s.get('drivers'):
    d0 = s['drivers'][0]
    print('Top driver:', d0.get('position'), d0.get('Driver', {}).get('givenName'), d0.get('Driver', {}).get('familyName'))
