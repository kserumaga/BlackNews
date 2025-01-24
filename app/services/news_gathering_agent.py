import requests
from bs4 import BeautifulSoup
from app.models.article_model import Article

class NewsGatheringAgent:
    def __init__(self, sources):
        self.sources = sources

    def fetch_articles(self):
/*************  ✨ Codeium Command ⭐  *************/
    """
    Fetches articles from the configured news sources.

    Iterates over the list of news sources, sends an HTTP GET request to each source, and parses the HTML response
    using BeautifulSoup to extract articles. Finds all 'article' tags in the HTML and retrieves the title and content
    from 'h2' and 'p' tags respectively. Creates an Article object for each article and appends it to the list.

    Returns:
        List[Article]: A list of Article objects containing the title and content of each article found.
    """

/******  f766817f-696b-4e3f-b1d1-8bfaa026fa92  *******/
        articles = []
        for source in self.sources:
            response = requests.get(source)
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.find_all('article'):
                title = item.find('h2').text
                content = item.find('p').text
                articles.append(Article(title=title, content=content))
        return articles

    def save_articles(self, articles):
        for article in articles:
            article.save()