# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class ScrapyappPipeline:
    def process_item(self, item, spider):
        movies=pd.DataFrame(item)
        movies.to_csv('/app/movies.csv', mode="a", index=False, header=True)
        return item
