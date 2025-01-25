# BLACKNEWS/app/utils/security.py
import pandas as pd


def get_or_create_category(supabase, category_name):
    if pd.isna(category_name):
        return None
    response = supabase.table('categories').select('id').eq('name', category_name).execute()
    if response.data:
        return response.data[0]['id']
    else:
        new_category = supabase.table('categories').insert({"name": category_name}).execute()
        return new_category.data[0]['id']