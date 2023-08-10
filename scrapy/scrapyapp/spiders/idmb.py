import re
import scrapy


class IdmbSpider(scrapy.Spider):
    name = "idmb"
    # Filtered offsite request 방지를 위해 allowed_domains 설정을 제거.
    # allowed_domains = ["idmb.com", "www.idmb.com"]

    def start_requests(self):
        self.t_count = self.settings.get("T_COUNT")
        url = "https://www.imdb.com/search/title?release_date=2018-01-01,2018-12-31&sort=boxoffice_gross_us,desc&start="
        yield scrapy.Request(url=url, meta={"base_url": url, "new_page_number": 1})

    def parse(self, response):
        movie_data = { "name": [], "year": [], "rating": [], "m_score": [], "votes": [], }
        base_url = response.meta["base_url"]
        new_page_number = response.meta["new_page_number"]
        movie_blocks = response.css('div.lister-item-content')
        page_movie_data = self.scrape_m_page(movie_blocks)   
        movie_data["name"].extend(page_movie_data["name"])
        movie_data["year"].extend(page_movie_data["year"])
        movie_data["rating"].extend(page_movie_data["rating"])
        movie_data["m_score"].extend(page_movie_data["m_score"])
        movie_data["votes"].extend(page_movie_data["votes"])
        yield movie_data
        current_mcount_start = int(response.css("div.nav div.desc > span:nth-child(1)::text").get().split("-")[0].strip())
        current_mcount_end = int(response.css("div.nav div.desc > span:nth-child(1)::text").get().split("-")[1].split(" ")[0].strip())
        remaining_mcount = self.t_count - current_mcount_end
        self.logger.info(f"currently scraping movies from: {str(current_mcount_start)} - {str(current_mcount_end)} remaining count: {str(remaining_mcount)}")
        if remaining_mcount <= 0:
            return
        new_page_number = current_mcount_end + 1
        url = base_url + str(new_page_number)
        yield scrapy.Request(url=url, meta={"base_url": base_url, "new_page_number": new_page_number})
    
    # movie_blocks의 항목들을 배열로 변환.
    def scrape_m_page(self, movie_blocks):
        page_movie_data = { "name": [], "year": [], "rating": [], "m_score": [], "votes": [], }
        num_blocks = len(movie_blocks)
        for block in range(num_blocks):
            mblock = self.scrape_mblock(movie_blocks[block])
            page_movie_data["name"].append(mblock["name"])
            page_movie_data["year"].append(mblock["year"])
            page_movie_data["rating"].append(mblock["rating"])
            page_movie_data["m_score"].append(mblock["m_score"])
            page_movie_data["votes"].append(mblock["votes"])
        return page_movie_data

    # 하나의 move_block 항목에서 name, year, rating, m_score, votes 정보들을 추출.
    def scrape_mblock(self, movie_block):
        movieb_data ={}
        try:
            movieb_data['name'] = movie_block.css('a::text').get().strip() # Name of the movie
        except:
            movieb_data['name'] = None
        try:
            year = movie_block.css('span.lister-item-year::text').get().strip() # Release year
            year = re.search(r"\d{4}", year).group(0)
            movieb_data['year'] = str(year) # Release year
        except:
            movieb_data['year'] = None
        try:
            movieb_data['rating'] = float(movie_block.css('div.inline-block.ratings-imdb-rating::attr(data-value)').get().strip()) #rating
        except:
            movieb_data['rating'] = None
        try:
            movieb_data['m_score'] = float(movie_block.css('span.metascore::text').get().strip()) #meta score
        except:
            movieb_data['m_score'] = None
        try:
            movieb_data['votes'] = int(movie_block.css('span[name="nv"]::attr(data-value)').get().strip()) # votes
        except:
            movieb_data['votes'] = None
        return movieb_data