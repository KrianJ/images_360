# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field


class ImageItem(Item):
    # define the fields for your item here like:
    collection = table = 'images'
    id = Field()            # id
    title = Field()         # 标题
    image = Field()         # 全图
    thumb_img = Field()     # 缩略图
    tags = Field()          # 图片标签
