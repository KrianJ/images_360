import scrapy
from scrapy import Request
from images_360.items import SearchItem
from urllib.parse import urlencode
import json
from images_360.settings import KEYWORD


class SearchImagesSpider(scrapy.Spider):
    __doc__ = """对于关键字搜索的结果，最多显示1500张图片"""
    name = 'search_images'
    allowed_domains = ['image.so.com']
    start_urls = ['https://image.so.com']

    base_url = 'https://image.so.com/j?'

    def start_requests(self):
        data = {
            'q': KEYWORD,
            'pd': 1,
            'correct': KEYWORD,
            'sid': '20356d98549ff58fd4e7c9a804edd5a2',
            'pc': 60    # 该data字段控制该请求包含的图片数量(list长度)
        }
        total = 1500
        for i in range(10):
            start_index = i * 60
            if start_index <= 1440:
                data['ps'] = i * 60             # 该字段控制请求中图片的开始索引为多少
            elif 1440 < start_index <= total:
                data['ps'] = start_index
                data['pc'] = 1500 - start_index
            query = urlencode(data)
            url = self.base_url + query
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        text = response.text
        result = json.loads(text)
        for image in result.get('list'):
            item = SearchItem()
            item['id'] = image.get('id')
            item['title'] = image.get('title')
            item['image'] = image.get('img')
            item['thumb_img'] = image.get('thumb')
            item['img_type'] = image.get('imgtype')
            yield item
