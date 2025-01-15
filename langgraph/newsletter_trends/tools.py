# Importar a biblioteca necessária
from pytrends.request import TrendReq
from langchain_core.tools import StructuredTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.document_loaders import WebBaseLoader
from typing import List
from tqdm import tqdm

from dotenv import load_dotenv
import os

load_dotenv()

# Inicializar um objeto TrendReq
pytrends = TrendReq(hl='pt-BR', tz=360)

def to_list(text):
    return text.split("\n")

def trends_per_country(country: str, head: int) -> str:
    """trends per country"""
    country = country.lower()
    daily_trending_searches = pytrends.trending_searches(pn=country)
    word_list = daily_trending_searches.head(head).values.T[0]
    return "\n".join(word_list)

async def atrends_per_country(country: str, head: int) -> str:
    """trends per country"""
    country = country.lower()
    daily_trending_searches = pytrends.trending_searches(pn=country)
    word_list = daily_trending_searches.head(head).values.T[0]
    return "\n".join(word_list)

def create_trends_tool():
    return StructuredTool.from_function(func=trends_per_country, coroutine=atrends_per_country)

def get_serper_results(queries: List[str],
                       k: int=5,
                       type_content: str='news',
                       hl: str='pt',
                       gl: str='br') -> List[dict]:
    
    """
    Get the multiple search results from Google Serper API
    
    Args:
    - queries: List of queries to be searched
    - k: Number of results to be returned
    - type_content: Type of content to be searched
    - hl: Language to be searched
    - gl: Country to be searched
    
    Returns:
    - List of results from the search
    
    """

    search = GoogleSerperAPIWrapper(gl=gl,
                                    hl=hl,
                                    k=k, 
                                    type=type_content) # type: Literal['news', 'search', 'places', 'images'] = 'search'
    
    results = [search.results(query) for query in queries]
    return results

def get_serper_with_scrapping(queries: List[str],
                              k: int=5,
                              type_content: str='news',
                              hl: str='pt',
                              gl: str='br') -> List[dict]:
    
    """
    Get the multiple search results from Google Serper API and scrap the content
    
    Args:
    - queries: List of queries to be searched
    - k: Number of results to be returned
    - type_content: Type of content to be searched
    - hl: Language to be searched
    - gl: Country to be searched
    
    Returns:
    - List of results from the search
    """
    
    results = get_serper_results(queries, 
                                 k, 
                                 type_content, 
                                 hl, 
                                 gl)
    
    dict_results_news = {}
    for r in tqdm(results):
        q = r['searchParameters']['q']
        news = r['news']
        
        for i in range(len(news)):
            n = news[i]
            link = n['link']
            loader = WebBaseLoader(web_paths=[link])
            docs = loader.load()
            news[i]['content'] = "\n".join([x.page_content for x in docs])
        
        dict_results_news[q] = news
        
    return dict_results_news