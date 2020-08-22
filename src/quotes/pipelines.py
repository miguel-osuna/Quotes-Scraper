# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import json
import logging

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("quotes.jl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class MongoDBPipeline:

    collection_name = "quotes"

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        """ 
        Initializes database connection and sessionmaker
        Creates tables
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        """ Creates a MongoDBPipeline instance from the crawler called. """
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "quotes_database"),
            mongo_collection=crawler.settings.get("MONGO_COLLECTION", "quotes"),
        )

    def open_spider(self, spider):
        """ Stablish connection creating a mongodb client when the spider is opened. """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        """ Close the connection with the database when the spider is closed. """
        self.client.close()

    def process_item(self, item, spider):
        quote_item = ItemAdapter(item).asdict()

        quote_exists = (
            self.db[self.mongo_collection]
            .find({"quote_content": quote_item["quote_content"]})
            .count()
        )

        if quote_exists > 0:
            raise DropItem("Quote already on the database!")
        else:
            logger.debug(
                "Quote added to the database: {0}".format(quote_item["quote_content"])
            )
            self.db[self.mongo_collection].insert_one(quote_item)

        return item

