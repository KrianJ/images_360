import scrapy
from scrapy import Request
from urllib.parse import urlencode
import json
from images_360.items import ImageItem
from images_360.settings import KEYWORD


class ImagesSpider(scrapy.Spider):
    __doc__ = """360图片采用ajax加载，分析xhr文件可以得到异步加载的请求链接
    如: https://image.so.com/zjl?ch=photography&sn=60&listtype=new&temp=1
    其中sn为偏置，其余请求参数相同"""
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        """定义爬取列表"""
        # optional words of key 'ch': [beauty, wallpaper, design#/, funny, news, art, car, photography, food, home, pet]
        data = {
            'ch': KEYWORD,
            'listtype': 'new',
            'temp': 1
        }
        base_url = 'https://image.so.com/zjl?'
        page_num = 30
        # 定义爬取的页数
        for i in range(page_num):
            data['sn'] = i * 30
            query = urlencode(data)
            url = base_url + query
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get('id')
            item['title'] = image.get('title')
            item['image'] = image.get('qhimg_url')
            item['thumb_img'] = image.get('qhimg_thumb')
            item['tags'] = image.get('pic_desc').strip()
            yield item

