from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Article:
    def __init__(self, title, content, author=None, published_date=None):
        self.title = title
        self.content = content
        self.author = author
        self.published_date = published_date

    def save(self):
        """Save the article to the database."""
        supabase.table('articles').insert({
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'published_date': self.published_date
        }).execute()

    @staticmethod
    def get_all():
        """Fetch all articles from the database."""
        response = supabase.table('articles').select('*').execute()
        return response.data