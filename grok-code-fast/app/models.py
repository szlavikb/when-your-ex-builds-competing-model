"""
Data models for the F1 News Dashboard application.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class NewsItem:
    """Represents a news item from F1 RSS feed."""
    title: str
    link: str
    summary: str
    published: str
    source: str = ""  # News source (e.g., 'bbc.co.uk', 'espn.com')

    @classmethod
    def from_xml(cls, item, source="") -> 'NewsItem':
        """Create NewsItem from XML element."""
        title_elem = item.find('title')
        link_elem = item.find('link')
        desc_elem = item.find('description')
        pub_elem = item.find('pubDate')

        return cls(
            title=title_elem.text or '' if title_elem is not None else '',
            link=link_elem.text or '' if link_elem is not None else '',
            summary=desc_elem.text or '' if desc_elem is not None else '',
            published=pub_elem.text or '' if pub_elem is not None else '',
            source=source
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'title': self.title,
            'link': self.link,
            'summary': self.summary,
            'published': self.published
        }


@dataclass
class Driver:
    """Represents a Formula 1 driver."""
    position: str
    name: str
    nationality: str
    constructor: str
    points: str
    wins: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'position': self.position,
            'name': self.name,
            'nationality': self.nationality,
            'constructor': self.constructor,
            'points': self.points,
            'wins': self.wins
        }


@dataclass
class Constructor:
    """Represents a Formula 1 constructor/team."""
    position: str
    name: str
    nationality: str
    points: str
    wins: str

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'position': self.position,
            'name': self.name,
            'nationality': self.nationality,
            'points': self.points,
            'wins': self.wins
        }
