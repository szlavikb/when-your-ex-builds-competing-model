import requests

# Test the Flask app
try:
    print("Testing Flask app connection...")
    response = requests.get('http://127.0.0.1:5000/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Main page loaded successfully")

        # Now test the news API
        print("\nTesting news API...")
        news_response = requests.get('http://127.0.0.1:5000/api/news')
        print(f"News API Status: {news_response.status_code}")
        if news_response.status_code == 200:
            news_data = news_response.json()
            print(f"News items retrieved: {len(news_data)}")
        else:
            print(f"News API failed: {news_response.text}")
    else:
        print(f"Failed to load main page: {response.text}")
except Exception as e:
    print(f"Error: {e}")
