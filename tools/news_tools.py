import requests
import aiohttp
import asyncio
from typing import List, Dict, Any
from config.settings import settings
from bs4 import BeautifulSoup

class NewsTools:
    @staticmethod
    def get_top_headlines(country: str = "us", category: Optional[str] = None) -> Dict[str, Any]:
        """Get top news headlines using NewsAPI"""
        try:
            base_url = "https://newsapi.org/v2/top-headlines"
            params = {
                'country': country,
                'apiKey': settings.NEWS_API_KEY,
                'pageSize': 10
            }
            
            if category:
                params['category'] = category
            
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get('articles', [])[:5]:
                articles.append({
                    'title': article['title'],
                    'description': article['description'],
                    'source': article['source']['name'],
                    'url': article['url'],
                    'published_at': article['publishedAt']
                })
            
            return {
                'total_results': data['totalResults'],
                'articles': articles
            }
        except Exception as e:
            # Fallback to web scraping if API fails
            return NewsTools._scrape_news_fallback()

    @staticmethod
    def _scrape_news_fallback() -> Dict[str, Any]:
        """Fallback news scraping from BBC"""
        try:
            url = "https://www.bbc.com/news"
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = []
            for item in soup.select('a[data-testid="internal-link"]')[:5]:
                title = item.get_text(strip=True)
                link = item.get('href', '')
                if title and link:
                    articles.append({
                        'title': title,
                        'url': f"https://www.bbc.com{link}" if link.startswith('/') else link,
                        'source': 'BBC'
                    })
            
            return {'articles': articles, 'source': 'BBC Scraped'}
        except Exception as e:
            return {'error': f"Failed to fetch news: {str(e)}"}

    @staticmethod
    async def search_news_async(query: str) -> Dict[str, Any]:
        """Search news asynchronously"""
        async with aiohttp.ClientSession() as session:
            try:
                url = "https://newsapi.org/v2/everything"
                params = {
                    'q': query,
                    'apiKey': settings.NEWS_API_KEY,
                    'pageSize': 5,
                    'sortBy': 'relevance'
                }
                
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    
                    articles = []
                    for article in data.get('articles', []):
                        articles.append({
                            'title': article['title'],
                            'description': article['description'],
                            'url': article['url'],
                            'source': article['source']['name']
                        })
                    
                    return {
                        'query': query,
                        'articles': articles
                    }
            except Exception as e:
                return {'error': str(e)}