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
            'pn': 60,
            'correct': KEYWORD,
            'adstart': 0,
            'tab': 'all',
            'ras': 6,
            'cn': 0,
            'gn': 0,
            'kn': 50,
            'crn': 0,
            'cuben': 0,
            'src': 'srp'
        }
        for i in range(10):
            data_control = i * 60
            data['sn'] = data_control             # 该data字段控制该请求包含的图片数量(list长度)
            data['ps'] = data_control             # 该字段控制请求中图片的开始索引为多少
            data['pc'] = data_control
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
