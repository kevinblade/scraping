import re
import sys
import time
import logging
import pandas as pd
import random as ran
from playwright.sync_api import sync_playwright


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
        movieb_data['name'] = movie_block.query_selector('a').inner_text() # Name of the movie
    except:
        movieb_data['name'] = None
    try:
        year = movie_block.query_selector('span.lister-item-year').inner_text() # Release year
        year = re.search(r"\d{4}", year).group(0)
        movieb_data['year'] = str(year) # Release year
    except:
        movieb_data['year'] = None
    try:
        movieb_data['rating'] = float(movie_block.query_selector('div.inline-block.ratings-imdb-rating').get_attribute('data-value')) #rating
    except:
        movieb_data['rating'] = None
    try:
        movieb_data['m_score'] = float(movie_block.query_selector('span.metascore.favorable').inner_text().strip()) #meta score
    except:
        movieb_data['m_score'] = None
    try:
        movieb_data['votes'] = int(movie_block.query_selector('span[name="nv"]').get_attribute('data-value')) # votes
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
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        url = base_url + str(new_page_number)
        page.goto(url)
        while remaining_mcount > 0:
            #set_trace()
            page.wait_for_selector("div.article > div.desc")
            movie_blocks = page.query_selector_all('div.lister-item-content')
            movie_data.extend(scrape_m_page(movie_blocks))   
            current_mcount_start = int(page.query_selector("div.nav div.desc").inner_text().split("-")[0])
            current_mcount_end = int(page.query_selector("div.nav div.desc").inner_text().split("-")[1].split(" ")[0])
            remaining_mcount = target - current_mcount_end
            logger.info(f"currently scraping movies from: {str(current_mcount_start)} - {str(current_mcount_end)} remaining count: {str(remaining_mcount)}")
            # new_page_number = current_mcount_end + 1
            page.query_selector("div.desc a.lister-page-next.next-page").click()
        page.close()
        browser.close() 
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