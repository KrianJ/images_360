import pymongo
import pymysql
from scrapy.exceptions import DropItem
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.collection
        # self.db[name].update_one({'id': item['id']}, {'$set': dict(item)}, upsert=True)
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()
        create_database = 'create database if not exists %s' % self.database
        self.cursor.execute(create_database)

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        # 创建数据表
        create_table = """
        create table if not exists %s (
        id char(50) primary key,
        title varchar(100),
        image varchar (100),
        thumb_img varchar(100),
        tags varchar (50)
        )ENGINE=innodb DEFAULT CHARSET=utf8;
        """ % item.table
        self.cursor.execute(create_table)
        # 写入数据
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into %s (%s) value (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """将item中的image(即图片url)作为请求返回"""
        yield Request(item['image'])

    def file_path(self, request, response=None, info=None):
        """返回保存的文件名"""
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        """
        :param results: item的下载结果信息<class list>，若为空则下载失败，抛DropItem异常
        """
        image_path = [x['path'] for status, x in results if status]
        if not image_path:
            raise DropItem('Image Download Failed')
        return item

