  Sau khi 1 item được thu thập bởi 1 spider, nó được gửi tới Item Pipeline nơi xử lý item thông qua 1 số component được thực thi tuần tự.
  - Mỗi component item Pipeline là 1 class Python đảm nhiệm 1 chức năng đơn giản. Chúng nhận 1 Item và thực hiện 1 chức năng trên nó, cũng như quyết định xem nó được đi tiếp qua đường ống pipeline hay ko, hay bị bỏ đi và ko được xử lý nữa.
  - Các ứng dụng điển hình của Item Pipelines :
	+ Cleansing HTML data ( xóa dữ liệu, làm sạch dữ liệu HTML)
	+ Xác nhận dữ liệu được thu thập ( check xem các item có chứa các field nhất định hay ko )
	+ Check trùng lặp ( duplicate và drop chúng nếu trùng lặp)
	+ Lưu trữ item được thu thập trong 1 database

1. Writing your own item pipeline------------------------------------
  - Mỗi thành phần item pipeline là 1 class python mà phải thực thi các phương thức sau : 
_____________________________________________
'process_item(self, item, spider)' :
  - Phương thức này được gọi cho mỗi component item pipeline. Phương thức này hoặc trả về 1 dictionay data, hoặc trả về 1 Item, hoặc trả về a Twisted Deferred( xem thêm ở bài đó) hoặc là thông báo drop item (raise DropItem exception). Các item bị drop ko được xử lý tiếp bởi các pipeline components. 
	Parameters:	
	+ item (Item object or a dict) – the item scraped
	+ spider (Spider object) – the spider which scraped the item
_____________________________________________
'open_spider(self, spider)':
  - Phương thức này được gọi khi spider được mở (open)
	Parameters:	
	+ spider (Spider object) – the spider which was opened
_____________________________________________
'close_spider(self, spider)': 
  - Phương thức này được gọi khi spider đóng
	Parameters:	
	+ spider (Spider object) – the spider which was closed
_____________________________________________
'from_crawler(cls, crawler)':
  - Nếu có, phương thức lớp này được gọi để tạo 1 thực thể (instance) pipeline từ 1 trình Crawler. Nó phải trả về 1 thực thể(instance) mới của pipeline. Đối tượng Crawler cung cấp quyền truy cập tới tất cả thành phần trong core Scrapy như settings và signals. Nó là 1 con đường mà pipeline có thể truy cập chúng và lấy các chức năng của nó trong Scarpy
	Parameters:	
	+ crawler (Crawler object) – crawler that uses this pipeline

2. Ví dụ về các trường hợp sử dụng (Item pipeline example)
_____________________________________________
Price validation and dropping items with no prices
  - Ta hãy nhìn vào hypothetical pipeline để điều chỉnh thuộc tính price cho các items ko VAT(thuộc tính 'price_excludes_vat'), và xóa những items ko chứa price :
_____________________________________________
from scrapy.exceptions import DropItem
class PricePipeline(object):
    vat_factor = 1.15
    def process_item(self, item, spider):
        if item['price']:
            if item['price_excludes_vat']:
                item['price'] = item['price'] * self.vat_factor
            return item
        else:
            raise DropItem("Missing price in %s" % item)
_____________________________________________
Write items to a JSON file :
  - Pipeline dưới đây lưu trữ tất cả các items đã thu thập về ( từ tất cả các spider) trong 1 file items.jl, nó chứa 1 item / 1 dòng tuần tự theo định dạng JSON. 
  - Lưu ý: mục địch của JsonWritePipeline chỉ là giới thiệu cách ghi item pipelines ra file. Nếu bạn thực sự muốn lưu tất cả các item đã thu thập trong 1 file JSON, bạn nên sử dụng Feed exports (chương tiếp theo)
_____________________________________________
import json
class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')
    def close_spider(self, spider):
        self.file.close()
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
_____________________________________________
Write items to 1 CSDL(MongoDB):
  - Trong ví dụ này, chúng ta sẽ ghi các item tới CSDL MongoDB sử dụng 'pymongo'	. Địa chỉ MongoDB và tên database được chỉ định trong Scrapy settings. Collection MongoDB được dặt tên theo class Item.
  - Điểm chính của ví dụ này là cho chúng ta thấy cách sử dụng from_crawler() và cách xóa các tài nguyên đúng cách :
_____________________________________________
import pymongo
class MongoPipeline(object):
    collection_name = 'scrapy_items'
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def close_spider(self, spider):
        self.client.close()
    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
_____________________________________________
Take screenshot of item:
  - Ví dụ này là minh chứng cho return Deferred từ phương thức process_item(). Nó sử dụng 'Splash' để render screenshot của item url. Pipeline tạo request tới thực thể(instance) chạy local của Splash. Sau khi request được tải và Deferred gọi trả lại, nó lưu trữ item tới 1 file và thêm tên file tới item.
_____________________________________________
import scrapy
import hashlib
from urllib.parse import quote
class ScreenshotPipeline(object):
    """Pipeline that uses Splash to render screenshot of
    every Scrapy item."""
    SPLASH_URL = "http://localhost:8050/render.png?url={}"
    def process_item(self, item, spider):
        encoded_item_url = quote(item["url"])
        screenshot_url = self.SPLASH_URL.format(encoded_item_url)
        request = scrapy.Request(screenshot_url)
        dfd = spider.crawler.engine.download(request, spider)
        dfd.addBoth(self.return_item, item)
        return dfd
    def return_item(self, response, item):
        if response.status != 200:
            # Error happened, return item.
            return item
        # Save screenshot to file, filename will be hash of url.
        url = item["url"]
        url_hash = hashlib.md5(url.encode("utf8")).hexdigest()
        filename = "{}.png".format(url_hash)
        with open(filename, "wb") as f:
            f.write(response.body)
        # Store filename in item.
        item["screenshot_filename"] = filename
        return item
_____________________________________________
Duplicates filter :
  - Bộ lọc tìm kiếm các item bị trùng lặp và drop các item đó. Giả sử các item có 1 id duy nhất, nhưng spider lại trả về nhiều item với cùng id :
_____________________________________________
from scrapy.exceptions import DropItem
class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()
    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item
_____________________________________________

3. Activating an Item Pipeline component-----------------------------
  - Để kích hoạt (activate) 1 Item Pipeline component, bạn phải thêm class của nó tới 'ITEM_PIPELINES' setting, ví dụ : 
_____________________________________________
ITEM_PIPELINES = {
    'myproject.pipelines.PricePipeline': 300,
    'myproject.pipelines.JsonWriterPipeline': 800,
}
_____________________________________________
  - Giá trị số nguyên mà bạn gán cho các class trong setting trên xác định thứ tự chúng chayj: Các item đi qua các class giá trị thấp tới giá trị cao. Thông thường định nghĩa những con số này khoảng 0-1000 

