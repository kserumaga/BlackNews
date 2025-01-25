# app/models/article_model.py
from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY
from datetime import datetime

# Initialize Supabase client (keep your existing setup)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Article:
    def __init__(self, title, content, source_id, category_id, url,
                 author=None, published_date=None, embedding=None, sentiment_score=None):
        self.title = title
        self.content = content
        self.source_id = source_id  # Add new required field
        self.category_id = category_id  # Add new required field
        self.url = url  # Add new required field
        self.author = author
        self.published_date = published_date or datetime.now().isoformat()
        self.embedding = embedding  # New field
        self.sentiment_score = sentiment_score  # New field

    def save(self):
        """Save the article to the database with relationships"""
        response = supabase.table('articles').insert({
            'title': self.title,
            'content': self.content,
            'source_id': self.source_id,
            'category_id': self.category_id,
            'url': self.url,
            'author': self.author,
            'published_date': self.published_date,
            'embedding': self.embedding,  # New field
            'sentiment_score': self.sentiment_score  # New field
        }).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_all(with_relations=False):
        """Fetch all articles, optionally with joined data"""
        query = supabase.table('articles').select('*')
        
        if with_relations:
            query = query.select('*, sources(*), categories(*)')
            
        response = query.execute()
        return response.data

    # New method to match your workflow
    @staticmethod
    def create_from_clean_data(clean_data):
        """Factory method for creating articles from processed data"""
        return Article(
            title=clean_data['title'],
            content=clean_data['content'],
            source_id=clean_data['source_id'],
            category_id=clean_data['category_id'],
            url=clean_data['url'],
            author=clean_data.get('author'),
            published_date=clean_data.get('published_date'),
            embedding=clean_data.get('embedding'),
            sentiment_score=clean_data.get('sentiment_score')
        )