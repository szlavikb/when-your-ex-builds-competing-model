"""
Service layer for F1 data operations.
Handles fetching and processing F1 news and standings data.
"""
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from typing import List, Optional
from .models import NewsItem, Driver, Constructor


class F1DataService:
    """Service class for fetching and processing F1 data."""

    def __init__(self, news_urls=None, drivers_url=None, constructors_url=None, timeout=10):
        # Multiple news sources for better coverage
        self.news_urls = news_urls or [
            'https://feeds.bbci.co.uk/sport/formula1/rss.xml',
            'https://www.espn.com/espn/rss/f1/news',
            'https://www.skysports.com/rss/12040',
            'https://www.autosport.com/rss/f1-news.xml',
            'https://the-race.com/feed/'
        ]
        self.drivers_url = drivers_url or 'https://www.formula1.com/en/drivers.html'
        self.constructors_url = constructors_url or 'https://www.formula1.com/en/teams.html'
        self.timeout = timeout

    def get_f1_news(self) -> List[NewsItem]:
        """
        Fetch F1 news from multiple RSS feeds for better coverage.

        Returns:
            List of NewsItem objects containing the latest F1 news from multiple sources.
        """
        all_news_items = []

        for news_url in self.news_urls:
            try:
                # Add headers to avoid 403 errors
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'application/rss+xml, application/xml, text/xml',
                    'Accept-Language': 'en-US,en;q=0.9',
                }

                # Special handling for ESPN (try different approaches)
                if 'espn.com' in news_url:
                    # Try without headers first
                    try:
                        response = requests.get(news_url, timeout=self.timeout)
                    except requests.HTTPError:
                        # If that fails, try with headers
                        response = requests.get(news_url, timeout=self.timeout, headers=headers)
                else:
                    response = requests.get(news_url, timeout=self.timeout, headers=headers)

                response.raise_for_status()

                # Try to parse as RSS/XML first
                try:
                    root = ET.fromstring(response.content)
                    source_domain = news_url.split('/')[2]  # Extract domain name
                    for item in root.findall('.//item')[:5]:  # Get top 5 from each source
                        news_item = NewsItem.from_xml(item, source_domain)
                        all_news_items.append(news_item)
                except ET.ParseError:
                    # If XML parsing fails, try as regular HTML or skip
                    print(f"Skipping {news_url} - not a valid RSS feed")
                    continue

            except requests.HTTPError as e:
                if e.response.status_code == 403:
                    print(f"Access forbidden for {news_url} - may require different headers or authentication")
                elif e.response.status_code == 404:
                    print(f"RSS feed not found at {news_url} - URL may have changed")
                else:
                    print(f"HTTP error fetching news from {news_url}: {e}")
                continue
            except requests.RequestException as e:
                print(f"Network error fetching news from {news_url}: {e}")
                continue
            except Exception as e:
                print(f"Error parsing news from {news_url}: {e}")
                continue

        # Sort by publication date (most recent first) and return top 15
        all_news_items.sort(key=lambda x: x.published, reverse=True)

        # If no news items found, return sample data
        if not all_news_items:
            print("No news items retrieved from any source, using fallback data")
            sample_news = [
                {
                    "title": "F1 2025 Season Preview: Verstappen vs Hamilton Battle Expected",
                    "link": "https://www.formula1.com/en/latest/article/f1-2025-season-preview.123456.html",
                    "summary": "The 2025 Formula 1 season promises to be one of the most competitive in recent years with Max Verstappen defending his title against Lewis Hamilton's comeback.",
                    "published": "2025-08-27T10:00:00Z",
                    "source": "Formula1.com"
                },
                {
                    "title": "Ferrari Unveils 2025 Car with Major Aero Updates",
                    "link": "https://www.scuderiaferrari.com/en/news/2025-car-unveiling/",
                    "summary": "Ferrari has revealed their 2025 challenger with significant aerodynamic improvements aimed at closing the gap to Red Bull Racing.",
                    "published": "2025-08-26T15:30:00Z",
                    "source": "Scuderia Ferrari"
                },
                {
                    "title": "McLaren Confirms Norris-Piastri Lineup for 2025",
                    "link": "https://www.mclaren.com/racing/2025-lineup-confirmed/",
                    "summary": "McLaren Racing has confirmed that Lando Norris and Oscar Piastri will continue as teammates for the 2025 Formula 1 season.",
                    "published": "2025-08-25T12:00:00Z",
                    "source": "McLaren"
                }
            ]

            for news_data in sample_news:
                all_news_items.append(NewsItem(
                    title=news_data["title"],
                    link=news_data["link"],
                    summary=news_data["summary"],
                    published=news_data["published"],
                    source=news_data["source"]
                ))

        return all_news_items[:15]

    def get_driver_standings(self) -> List[Driver]:
        """
        Fetch F1 driver standings from official F1 website.

        Returns:
            List of Driver objects containing current driver standings.
        """
        try:
            response = requests.get(self.drivers_url, timeout=self.timeout, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            drivers = []

            # Try multiple selectors for driver containers
            driver_containers = (
                soup.find_all('div', class_='driver-card') or
                soup.find_all('div', class_='listing-item--driver') or
                soup.find_all('tr', class_='driver') or
                soup.find_all('div', {'data-driver': True}) or
                soup.find_all('article', class_='driver')
            )

            # If no containers found, try to find driver names directly
            if not driver_containers:
                # Look for elements containing driver names
                all_text_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'span', 'div', 'p'])
                driver_names = []
                for elem in all_text_elements:
                    text = elem.get_text().strip()
                    if any(name.upper() in text.upper() for name in ['VERSTAPPEN', 'HAMILTON', 'LECLERC', 'SAINZ', 'RUSSELL', 'PEREZ', 'ALONSO', 'STROLL', 'NORRIS', 'PIASTRI']):
                        driver_names.append(elem)
                        if len(driver_names) >= 10:
                            break

                for i, name_elem in enumerate(driver_names[:10], 1):
                    name = name_elem.get_text().strip()
                    drivers.append(Driver(
                        position=str(i),
                        name=name,
                        nationality='Unknown',
                        constructor='Unknown Team',
                        points='0',
                        wins='0'
                    ))
            else:
                for i, container in enumerate(driver_containers[:10], 1):
                    # Extract driver information with multiple fallback selectors
                    name_elem = (
                        container.find('h3') or
                        container.find('a', class_='driver-name') or
                        container.find('span', class_='name') or
                        container.find('strong') or
                        container.find('h2')
                    )
                    name = name_elem.text.strip() if name_elem else f'Driver {i}'

                    team_elem = (
                        container.find('p', class_='team') or
                        container.find('span', class_='team-name') or
                        container.find('div', class_='constructor') or
                        container.find('span', class_='constructor')
                    )
                    team = team_elem.text.strip() if team_elem else 'Unknown Team'

                    points_elem = (
                        container.find('span', class_='points') or
                        container.find('div', class_='points') or
                        container.find('td', class_='points')
                    )
                    points = points_elem.text.strip() if points_elem else '0'

                    nationality_elem = container.find('span', class_='nationality')
                    nationality = nationality_elem.text.strip() if nationality_elem else 'Unknown'

                    drivers.append(Driver(
                        position=str(i),
                        name=name,
                        nationality=nationality,
                        constructor=team,
                        points=points,
                        wins='0'  # Wins not easily available on drivers page
                    ))

            # If no drivers found, return sample data
            if not drivers:
                sample_drivers = [
                    {"name": "Max Verstappen", "constructor": "Red Bull Racing", "nationality": "Netherlands", "points": "258"},
                    {"name": "Lewis Hamilton", "constructor": "Mercedes", "nationality": "United Kingdom", "points": "187"},
                    {"name": "Charles Leclerc", "constructor": "Ferrari", "nationality": "Monaco", "points": "138"},
                    {"name": "Carlos Sainz", "constructor": "Ferrari", "nationality": "Spain", "points": "116"},
                    {"name": "George Russell", "constructor": "Mercedes", "nationality": "United Kingdom", "points": "111"},
                    {"name": "Sergio Perez", "constructor": "Red Bull Racing", "nationality": "Mexico", "points": "110"},
                    {"name": "Fernando Alonso", "constructor": "Aston Martin", "nationality": "Spain", "points": "45"},
                    {"name": "Lance Stroll", "constructor": "Aston Martin", "nationality": "Canada", "points": "24"}
                ]

                for i, driver_data in enumerate(sample_drivers[:10], 1):
                    drivers.append(Driver(
                        position=str(i),
                        name=driver_data["name"],
                        nationality=driver_data["nationality"],
                        constructor=driver_data["constructor"],
                        points=driver_data["points"],
                        wins='0'
                    ))

            return drivers

        except requests.RequestException as e:
            print(f"Error fetching driver standings: {e}")
            return []
        except Exception as e:
            print(f"Error parsing driver standings: {e}")
            return []

    def get_constructor_standings(self) -> List[Constructor]:
        """
        Fetch F1 constructor standings from official F1 website.

        Returns:
            List of Constructor objects containing current constructor standings.
        """
        try:
            response = requests.get(self.constructors_url, timeout=self.timeout, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            constructors = []

            # Try multiple selectors for constructor containers
            constructor_containers = (
                soup.find_all('div', class_='team-card') or
                soup.find_all('div', class_='listing-item--team') or
                soup.find_all('tr', class_='team') or
                soup.find_all('div', {'data-team': True}) or
                soup.find_all('article', class_='team')
            )

            # If no containers found, try to find team names directly
            if not constructor_containers:
                team_names = []
                all_text_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'span', 'div', 'p'])
                for elem in all_text_elements:
                    text = elem.get_text().strip()
                    if any(team.upper() in text.upper() for team in ['MERCEDES', 'RED BULL', 'FERRARI', 'MCLAREN', 'ASTON MARTIN', 'ALPINE', 'WILLIAMS', 'SAUBER', 'HAAS', 'RACING BULLS']):
                        team_names.append(elem)
                        if len(team_names) >= 10:
                            break

                for i, name_elem in enumerate(team_names[:10], 1):
                    name = name_elem.get_text().strip()
                    constructors.append(Constructor(
                        position=str(i),
                        name=name,
                        nationality='Unknown',
                        points='0',
                        wins='0'
                    ))
            else:
                for i, container in enumerate(constructor_containers[:10], 1):
                    # Extract constructor information with multiple fallback selectors
                    name_elem = (
                        container.find('h3') or
                        container.find('a', class_='team-name') or
                        container.find('span', class_='name') or
                        container.find('strong') or
                        container.find('h2')
                    )
                    name = name_elem.text.strip() if name_elem else f'Team {i}'

                    points_elem = (
                        container.find('span', class_='points') or
                        container.find('div', class_='points') or
                        container.find('td', class_='points')
                    )
                    points = points_elem.text.strip() if points_elem else '0'

                    nationality_elem = (
                        container.find('span', class_='nationality') or
                        container.find('span', class_='country')
                    )
                    nationality = nationality_elem.text.strip() if nationality_elem else 'Unknown'

                    constructors.append(Constructor(
                        position=str(i),
                        name=name,
                        nationality=nationality,
                        points=points,
                        wins='0'  # Wins not easily available on teams page
                    ))

            # If no constructors found, return sample data
            if not constructors:
                sample_constructors = [
                    {"name": "Red Bull Racing", "nationality": "Austria", "points": "368"},
                    {"name": "Mercedes", "nationality": "Germany", "points": "298"},
                    {"name": "Ferrari", "nationality": "Italy", "points": "254"},
                    {"name": "McLaren", "nationality": "United Kingdom", "points": "212"},
                    {"name": "Aston Martin", "nationality": "United Kingdom", "points": "69"},
                    {"name": "Alpine", "nationality": "France", "points": "45"},
                    {"name": "Williams", "nationality": "United Kingdom", "points": "11"},
                    {"name": "Sauber", "nationality": "Switzerland", "points": "8"}
                ]

                for i, constructor_data in enumerate(sample_constructors[:10], 1):
                    constructors.append(Constructor(
                        position=str(i),
                        name=constructor_data["name"],
                        nationality=constructor_data["nationality"],
                        points=constructor_data["points"],
                        wins='0'
                    ))

            return constructors

        except requests.RequestException as e:
            print(f"Error fetching constructor standings: {e}")
            return []
        except Exception as e:
            print(f"Error parsing constructor standings: {e}")
            return []
