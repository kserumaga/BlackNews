import re

def clean_article(text):
    patterns = [
        r'Read More:|READ MORE:',
        r'\(.*?(Photo|Getty Images|Credit).*?\)',
        r'Have you subscribed to theGrio’s.*',
        r'Download theGrio today\!',
        r'Loading the player...',
        r'RELATED:',
        r'\(.*?Screenshot.*?\)'
    ]
    return '\n\n'.join([
        line for line in text.split('\n\n')
        if not any(re.search(p, line) for p in patterns)
    ])