from typing import Annotated
import os

from tavily import TavilyClient

from core.utils.logger import logger

async def tavily_search(query: str, max_results: int = 10) -> Annotated[str, "Performs a Tavily search and returns formatted results"]:
    """
    Performs a web search using the Tavily API and returns formatted results.

    Parameters:
    - query: The search query string.
    - max_results: The number of search results to return (default is 10).

    Returns:
    - Formatted string containing search results including titles, URLs, and snippets.
    """
    try:
        api_key = os.getenv('TAVILY_API_KEY')

        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set.")

        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=max_results)

        formatted_results = f"Search Results for '{query}':\n"
        formatted_results += f"Total Results: {len(response.get('results', []))}\n\n"

        for item in response.get("results", []):
            formatted_results += f"Title: {item.get('title', 'N/A')}\n"
            formatted_results += f"URL: {item.get('url', 'N/A')}\n"
            formatted_results += f"Snippet: {item.get('content', 'N/A')}\n\n"

        logger.info(f"Tavily search results for query '{query}'")
        logger.info(formatted_results)
        return formatted_results

    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
