import os
import sys
import time
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapyapp.spiders.idmb import IdmbSpider


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


def main():
    settings = get_project_settings()
    settings.update({ "T_COUNT": 150 })
    # Create a process
    process = CrawlerProcess(settings)

    process.crawl(IdmbSpider)
    process.start()

if __name__ == '__main__':
    start = time.time()
    if os.path.exists("movies.csv"):
        os.remove("movies.csv")
    main()
    end = time.time()
    logger.info(f"{end - start} seconds elapsed.")