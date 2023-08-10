import re
import sys
import bs4
import time
import httpx
import logging
import pandas as pd
import random as ran
from fake_useragent import UserAgent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(funcName)s:%(lineno)d - %(message)s",
    handlers=[
        # logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 하나의 move_block 항목에서 name, year, rating, m_score, votes 정보들을 추출.
def scrape_mblock(movie_block):
    movieb_data ={}
    try:
        movieb_data['name'] = movie_block.select_one('a').get_text() # Name of the movie
    except:
        movieb_data['name'] = None
    try:
        year = movie_block.select_one('span.lister-item-year').contents[0]
        year = re.search(r"\d{4}", year).group(0)
        movieb_data['year'] = str(year) # Release year
    except:
        movieb_data['year'] = None
    try:
        movieb_data['rating'] = float(movie_block.select_one('div.inline-block.ratings-imdb-rating').get('data-value')) #rating
    except:
        movieb_data['rating'] = None
    try:
        movieb_data['m_score'] = float(movie_block.select_one('span.metascore.favorable').contents[0].strip()) #meta score
    except:
        movieb_data['m_score'] = None
    try:
        movieb_data['votes'] = int(movie_block.select_one('span[name="nv"]').get('data-value')) # votes
    except:
        movieb_data['votes'] = None
    return movieb_data

# movie_blocks의 항목들을 배열로 변환.
def scrape_m_page(movie_blocks):
    page_movie_data = []
    num_blocks = len(movie_blocks)
    for block in range(num_blocks):
        page_movie_data.append(scrape_mblock(movie_blocks[block]))
    return page_movie_data

def scrape_this(link,t_count):
    #from IPython.core.debugger import set_trace
    base_url = link
    target = t_count
    current_mcount_start = 0
    current_mcount_end = 0
    remaining_mcount = target - current_mcount_end 
    new_page_number = 1
    movie_data = []
    
    while remaining_mcount > 0:
        url = base_url + str(new_page_number)
        #set_trace()
        ua = UserAgent()
        source = httpx.get(url, headers={"User-Agent": ua.random}, follow_redirects=True).text
        soup = bs4.BeautifulSoup(source,'html.parser')
        movie_blocks = soup.select('div.lister-item-content')
        movie_data.extend(scrape_m_page(movie_blocks))   
        current_mcount_start = int(soup.select_one("div.nav div.desc").contents[1].get_text().split("-")[0])
        current_mcount_end = int(soup.select_one("div.nav div.desc").contents[1].get_text().split("-")[1].split(" ")[0])
        remaining_mcount = target - current_mcount_end
        logger.info(f"currently scraping movies from: {str(current_mcount_start)} - {str(current_mcount_end)} remaining count: {str(remaining_mcount)}")
        new_page_number = current_mcount_end + 1
        time.sleep(ran.randint(0, 10))
    return movie_data

def main():
    base_scraping_link = "https://www.imdb.com/search/title?release_date=2018-01-01,2018-12-31&sort=boxoffice_gross_us,desc&start="
    top_movies = 150 #input("How many movies do you want to scrape?")
    films = []
    movies = scrape_this(base_scraping_link,int(top_movies))
    logger.info(f"List of top {str(top_movies)} movies:")
    movies=pd.DataFrame(movies)
    movies.to_csv('/app/movies.csv', index=False)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    logger.info(f"{end - start} seconds elapsed.")