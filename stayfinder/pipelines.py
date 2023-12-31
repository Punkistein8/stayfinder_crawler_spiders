# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import sys
from .items import MapsItem

from scrapy.exceptions import DropItem


class MapsPipeline:
    collection = 'hoteles'

    def __init__(self, mongodb_uri, mongodb_db):
        self.items_seen = set()
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri:
            sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(MapsItem(item))
        nombreHotel = data.get('nombreHotel')
        precio = data.get('precio')

        if nombreHotel in self.items_seen:
            raise DropItem("¡🙀 Se encontró un item duplicado!: %s" % item)

        if precio in self.items_seen:
            # asignar otro precio
            data['precio'] = precio + 5

        else:
            self.items_seen.add(nombreHotel)
            self.db[self.collection].insert_one(data)
            return item
