- Spiders là các lớp (class) định nghia một website hay 1 nhóm website sẽ scraped như thế nào, bao gồm : thực hiện crawl như thế nào và cách trích xuất dữ liệu có cấu trúc từ các pages đó.  
- Chu kì scraping :
 + Đầu tiên, bạn bắt đầu tạo các Requests để crawl các URLs, và xác định hàm callback với từng Response đã tải về từ các Requests trên. Các Request thực hiện thông qua hàm 'start_requests()', hàm sẽ khởi tạo Request cho các URLs trong thuộc tính start_urls và hàm 'parse' là hàm callback cho các Requests.o
 + Trong hàm callback, bạn truyền response và trả về hoặc là từ điển (dicts), 'Item' Object hoặc gọi đệ quy (lặp lại) các đối tượng này. Các Requests cũng chứa callback, được downloaded bởi Scrapy, sau đó các response được xử lý bởi hàm callback được chỉ định.
 + Trong hàm callback, bạn truyền nội dung pages( chính xác là source code bao gồm nội dung ở dạng HTML). Để lấy nội dung sử dụng Selectors hoặc Xpath.
 + Cuối cùng, các Items được trả về sẽ được đưa tới 1 CSDL, hoặc được ghi ra 1 file sử dụng Feed exports	

- Có 3 loại spiders cho dành cho các mục đích, ứng dụng khác nhau :

1. scrapy.Spider ------------------------------------
    'class scrapy.spiders.Spider'
    Là spider đơn giản nhất, và là lớp mà mỗi spider khác phải kế thừa. Nó chỉ cung cấp mặc hàm thực thi mặc định 'start_requests()', mà gửi Request với các URLs có trong thuộc tính 'start_urls', với mỗi kết quả Response nó sẽ gọi method 'parse()'.
_______________________
'name' : Tên spider, phải là duy nhất, có thể tạo nhiều instantiating cho cùng 1 spider. Đây là thuộc tính spider quan trọng nhất và nó là required
_______________________
'allowed_domains' : 1 list các chuỗi chứa các tên miền mà spider được crawl. Các Requests cho các URLs không thuộc tên miền được chỉ định trong list (hoặc tên miền con của chúng) sẽ không được crawl nếu 'OffsiteMiddleware' enable. 
	Vd: Url bạn muốn : 'https://www.example.com/1.html', ta thêm 'example.com' tới list 'allowed_domains'.
_______________________
'start_urls' : Chứa 1 list URLs để spider bắt đầu crawl từ các URLs này khi không có URLs nào được chỉ định. Các URLs tiếp theo sẽ được tạo ra liên tục từ dữ liệu có trong start URLs. (có thể thông qua 'follow_link')
_______________________
'custom_settings' : là 1 dictionary settings sẽ được ghi đè cho config toàn bộ project khi chạy spider này.
_______________________
'crawler' : Thuộc tính này được thiết lập bởi phương thức lớp 'from_crawler()' sau khi khởi tạo lớp, và liên kết tới Object 'Crawler' mà instance spider này được bound
_______________________
'settings' : Cấu hình để chạy spider này.
_______________________
'logger' : Logger Python được tạo với tên Spider. Bạn có thể sử dụng nó để gửi messages log thông qua nó. Xem 'Logging from Spiders'
_______________________
'from_crawler(crawler, *args, **kwargs)' : Là 1 method lớp được Scrapy sử dụng để tạo spider của bạn. Bạn có lẽ sẽ không cần override trực tiếp phương thức này, bởi vì mặc định việc triển khai hoạt động như 1 proxy với method '__init__()', gọi nó với các đối số cho trước 'args', 'kwargs'.
    + Tuy nhiên, phương thức này thiết lập các thuộc tính 'crawler', 'settings' trong instance mới để chúng có thể được truy cập sau đó trong code spider.
Parameters:	
	crawler (Crawler instance) – crawler to which the spider will be bound
	args (list) – arguments passed to the __init__() method
	kwargs (dict) – keyword arguments passed to the __init__() method
_______________________
'start_requests()' : Nó dược gọi bởi Scrapy khi spider được mở để bắt đầu scraping. Scrapy chỉ gọi nó 1 lần, nên nó là an toàn để thực thi start_requests() như 1 generator (trình khởi tạo).
 + Mặc định tạo: 'Request(url, dont_filter=True)' cho mỗi URL trong start_urls.
_______________________
'parse(response)' : Là method callback mặc định được Scrapy dùng xử lý các response đã tải về cho mỗi request. (Khi các request không chỉ định callback). 
 + Phương thức này xử lý response và trả về dữ liệu đã đc scrapted và/hoặc thêm URLs để request tiếp. Nó phải trả về hoặc lặp lại Request và/hoặc dicts hoặc là các Object Item.
_______________________
'log(message[, level, component])' : Wrapper gửi 1 message log qua Logger của Spider, giữ cho khả năng tương thích ngược.
_______________________
'closed(reason)' : Được gọi khi spider đóng. Cung cấp 1 phím tắt cho signals.connect() cho tín hiệu 'spider_closed'

2. Spider arguments------------------------------------------------
    Spider có thể nhận các đối số để sửa đổi hành vi của chúng. Một số cách sử dụng phổ biến cho các đối số spider: xác định URL bắt đầu hoặc hạn chế việc crawl các section nhất định của trang web, nhưng chúng có thể được sử dụng để định cấu hình bất kỳ chức năng nào của spider.
    Các đối số spider được truyền qua lệnh 'crawl' sử dụng option '-a'
	VD : 'scrapy crawl myspider -a category=electronics'
    Spider có thể truy cập các đối số trong method '__init__()'
    Mặc định method '__init__' sẽ lấy bất kì đối số của spider và sao chép đối số như các thuộc tính của spider.
    	VD :
import scrapy
class MySpider(scrapy.Spider):
    name = 'myspider'
    def __init__(self, category=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.example.com/categories/%s' % category]
    def start_requests(self):
        yield scrapy.Request('http://www.example.com/categories/%s' % self.category)
    Luôn nhớ các đối số của spider chỉ là các chuỗi (string).  Spider sẽ không tự phân tích cú pháp. Nếu bạn đã set thuộc tính start_urls từ dòng lệnh, bạn phải tự phân tách nó thành một list bằng cách sử dụng cái gì đó như ast.literal_eval hoặc json.loads và sau đó đặt nó làm attribute. Nếu không, bạn sẽ gây ra quá trình lặp qua chuỗi start_urls (một pitfall python rất phổ biến) dẫn đến mỗi ký tự được xem như là một url riêng biệt

3. Generic Spiders------------------------------------------------
    Scrapy đi kèm với một số spider generic hữu ích, bạn có thể sử dụng để phân lớp các spiders của bạn. Mục đích của chúng là cung cấp các hàm thuận tiện cho 1 số trường hợp scrapy thông thương, như following all links trên 1 site dựa vào 1 số quy tắc, crawling từ Sitemaps, hoặc truyền 1 XML/CSV feed.
    Giả sử bạn có 1 project với lớp 'TestItem' được định nghĩa trong modul myproject.items : 
import scrapy
class TestItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
CrawlSpider :
_______________________
'class scrapy.spiders.CrawlSpider' : Là spider được dùng phổ biến nhất để crawling các website thông thường, nó cung cấp 1 kĩ thuật tiện lợi để following links bởi định nghĩa 1 tập các rules.

Crawling rules :
_______________________
'class scrapy.spiders.Rule(link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=None)'
_______________________








