# BLACKNEWS/app/services/data_import.py

import re
import pandas as pd
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import your existing models and utils
from app.models.article_model import Article
from app.config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configure paths
BASE_DIR = Path(__file__).parent.parent.parent
RAW_DATA_PATH = BASE_DIR / 'app' / 'data' / 'raw' / 'savedDataFrame2.txt'
PROCESSED_DATA_PATH = BASE_DIR / 'app' / 'data' / 'processed' / 'masterlist.xlsx'

def clean_article(text):
    """Your existing cleaning logic"""
    patterns = [
        r'Read More:|READ MORE:',
        r'\(.*?(Photo|Getty Images|Credit).*?\)',
        r'Have you subscribed to theGrio's.*',
        r'Download theGrio today\!',
        r'Loading the player...',
        r'RELATED:',
        r'\(.*?Screenshot.*?\)'
    ]
    return '\n\n'.join([
        line for line in text.split('\n\n')
        if not any(re.search(p, line) for p in patterns)
    ])

def get_or_create_category(category_name):
    """Handle category creation/retrieval"""
    if pd.isna(category_name):
        return None
    
    response = supabase.table('categories')\
                      .select('id')\
                      .eq('name', category_name)\
                      .execute()
    
    if response.data:
        return response.data[0]['id']
    else:
        new_category = supabase.table('categories')\
                             .insert({'name': category_name})\
                             .execute()
        return new_category.data[0]['id']

def main():
    try:
        # Load and merge data
        articles_df = pd.read_csv(RAW_DATA_PATH, encoding='utf-8', header=None)
        articles_df = articles_df.rename(columns={0: 'url', 1: 'article'})
        master_df = pd.read_excel(PROCESSED_DATA_PATH)
        
        merged_df = pd.merge(
            articles_df,
            master_df[['URL', 'Title', 'Publish date', 'Authors', 'Section']],
            left_on='url',
            right_on='URL'
        )
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return

    # Add cleaned content column
    merged_df['clean_content'] = merged_df['article'].apply(clean_article)

    # Example: Calculate embeddings and sentiment scores
    merged_df['embedding'] = merged_df['clean_content'].apply(lambda x: calculate_embedding(x))
    merged_df['sentiment_score'] = merged_df['clean_content'].apply(lambda x: calculate_sentiment(x))

    # Get theGrio source ID (create if doesn't exist)
    thegrio_source = supabase.table('sources')\
                           .select('id')\
                           .eq('name', 'theGrio')\
                           .execute()
    
    if not thegrio_source.data:
        new_source = supabase.table('sources')\
                           .insert({'name': 'theGrio', 'url': 'https://thegrio.com/'})\
                           .execute()
        source_id = new_source.data[0]['id']
    else:
        source_id = thegrio_source.data[0]['id']

    # Process in batches
    batch_size = 100
    for i in range(0, len(merged_df), batch_size):
        batch = merged_df.iloc[i:i+batch_size]
        articles_to_insert = []
        
        for _, row in batch.iterrows():
            # Get category ID for each article
            category_id = get_or_create_category(row['Section'])
            
            # Create Article instance
            article = Article(
                title=row['Title'],
                content=row['clean_content'],
                source_id=source_id,
                category_id=category_id,
                url=row['URL'],
                author=row['Authors'],
                published_date=row['Publish date'],
                embedding=row['embedding'],
                sentiment_score=row['sentiment_score']
            )
            
            articles_to_insert.append(article.__dict__)
        
        # Insert batch
        response = supabase.table('articles').insert(articles_to_insert).execute()
        
        if response.data:
            print(f"Successfully inserted batch {i//batch_size + 1}")
        else:
            print(f"Error inserting batch {i//batch_size + 1}: {response.error}")
            break

# Example functions for calculating embeddings and sentiment
def calculate_embedding(text):
    # Implement embedding calculation logic
    return [0.0] * 768  # Placeholder

def calculate_sentiment(text):
    # Implement sentiment analysis logic
    return 0.0  # Placeholder

if __name__ == "__main__":
    main()