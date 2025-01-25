# Location: BLACKNEWS/app/services/data_import.py

import pandas as pd
import re
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import internal modules
from app.services.database import supabase  # Assuming databases.py initializes Supabase client
from app.utils.preprocessing import clean_article
from app.models.article_model import Article  # If needed for model validation

# Configure paths
BASE_DIR = Path(__file__).parent.parent.parent
RAW_DATA_PATH = BASE_DIR / 'app' / 'data' / 'raw' / 'savedDataFrame2.txt'
PROCESSED_DATA_PATH = BASE_DIR / 'app' / 'data' / 'processed' / 'masterlist.xlsx'

# Load environment variables from root
load_dotenv(BASE_DIR / '.env')

def get_thegrio_source():
    """Get or create theGrio source in database"""
    response = supabase.table('sources').select('id').eq('name', 'theGrio').execute()
    return response.data[0]['id'] if response.data else create_source()

def create_source():
    response = supabase.table('sources').insert({
        "name": "theGrio",
        "url": "https://thegrio.com/"
    }).execute()
    return response.data[0]['id']

def process_categories(df):
    """Handle category relationships"""
    categories = df['Section'].unique()
    for cat in categories:
        if pd.notna(cat):
            supabase.table('categories').upsert({'name': cat}, on_conflict='name').execute()

def main():
    try:
        # Load data
        articles_df = pd.read_csv(RAW_DATA_PATH, encoding="utf-8").rename(columns={
            '0': 'url',
            '1': 'article'
        })
        master_df = pd.read_excel(PROCESSED_DATA_PATH)
    except Exception as e:
        print(f"Data loading error: {str(e)}")
        return

    # Merge and clean data
    merged_df = pd.merge(articles_df, master_df[['URL', 'Title', 'Publish date', 'Authors', 'Section']],
                        left_on='url', right_on='URL')
    merged_df['clean_content'] = merged_df['article'].apply(clean_article)

    # Database operations
    source_id = get_thegrio_source()
    process_categories(merged_df)

    # Prepare batch insert
    batch = [{
        'title': row['Title'],
        'content': row['clean_content'],
        'author': row['Authors'],
        'published_date': row['Publish date'],
        'source_id': source_id,
        'url': row['URL'],
        'category': row['Section']
    } for _, row in merged_df.iterrows()]

    # Insert articles
    for i in range(0, len(batch), 100):
        response = supabase.table('articles').insert(batch[i:i+100]).execute()
        if not response.data:
            print(f"Failed batch {i//100}: {response.error}")
            break

if __name__ == "__main__":
    main()