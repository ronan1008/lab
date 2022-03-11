# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
class MyfirstPipeline:
    def process_item(self, item, spider):
        title = item['title'] if item['title'] else ''
        if '迪士尼' in title :
            item['push'] = f"{item.get('push', '')} ...."
            item['date'] = f"2022 {item['date']}"
            print(item)
            return item
        else:
            raise DropItem(f"Drop this item: {item['title']}")
