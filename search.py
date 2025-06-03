from serpapi.google_search import GoogleSearch
from bs4 import BeautifulSoup
import requests
from typing import List
import logging
from config import SERPAPI_KEY, MAX_SEARCH_RESULTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_and_extract(query: str, num_results: int = MAX_SEARCH_RESULTS) -> List[str]:
    """
    Search the web for the given query and extract text content from the results.
    
    Args:
        query: The search query
        num_results: Number of search results to process
        
    Returns:
        List of extracted text content from web pages
    """
    try:
        search = GoogleSearch({
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": num_results
        })
        results = search.get_dict().get("organic_results", [])
        
        if not results:
            logger.warning("No search results found for query: %s", query)
            return []
            
        docs = []
        for res in results:
            try:
                url = res["link"]
                logger.info("Fetching content from: %s", url)
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text()
                docs.append(text[:5000])  # truncate for safety
                
            except requests.RequestException as e:
                logger.error("Failed to fetch %s: %s", url, str(e))
                continue
            except Exception as e:
                logger.error("Error processing %s: %s", url, str(e))
                continue
                
        return docs
        
    except Exception as e:
        logger.error("Search failed: %s", str(e))
        raise
