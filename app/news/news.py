import requests
from flask import current_app
from app.config import Config
from datetime import datetime, timedelta
import random

class NewsService:
    @staticmethod
    def get_top_articles():
        """Fetch top 2 articles from The Grio (dummy data)"""
        return [
            {
                "title": "Breaking: Major Political Development",
                "excerpt": "Significant changes in national leadership...",
                "image": "https://via.placeholder.com/800x450",
                "url": "#",
                "category": "Politics",
                "date": "2024-01-28"
            },
            {
                "title": "New Economic Policy Announced",
                "excerpt": "Government introduces sweeping economic reforms...",
                "image": "https://via.placeholder.com/800x450",
                "url": "#",
                "category": "Economy",
                "date": "2024-01-28"
            }
        ]

    @staticmethod
    def get_recent_articles(limit=10):
        """Get recent articles (dummy pagination)"""
        return [
            {
                "title": f"News Article {i}",
                "excerpt": f"Excerpt for article {i}...",
                "image": "https://via.placeholder.com/400x225",
                "url": "#",
                "category": ["Politics", "Economy", "Culture"][i % 3],
                "date": "2024-01-28"
            } for i in range(1, limit+1)
        ]

    @staticmethod
    def get_featured_articles(count=2):
        return [{
            "title": "Breaking: Major Climate Agreement Reached",
            "summary": "Global leaders finalize historic emissions reduction pact...",
            "image": "https://source.unsplash.com/random/800x600?climate",
            "url": "#",
            "date": datetime.now().strftime("%b %d, %Y")
        }, {
            "title": "Tech Giant Unveils New AI Assistant",
            "summary": "Revolutionary AI system promises to transform daily workflows...",
            "image": "https://source.unsplash.com/random/800x600?ai",
            "url": "#",
            "date": datetime.now().strftime("%b %d, %Y")
        }][:count]

    @staticmethod
    def get_recent_articles(count=4):
        days_ago = lambda d: (datetime.now() - timedelta(days=d)).strftime("%b %d, %Y")
        return [{
            "title": f"Top Story {i+1}",
            "image": f"https://source.unsplash.com/random/600x400?news-{i}",
            "date": days_ago(random.randint(0,7)),
            "url": "#"
        } for i in range(count)]
