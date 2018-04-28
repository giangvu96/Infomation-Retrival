1. Tải example để học-------------------------------------------
 - Chúng ta sẽ scrapy từ page 'http://quotes.toscrape.com'
 - Các bạn clone code trên git về 'https://github.com/scrapy/quotesbot'
 - Tải về giải nén được thư mục 'quotesbot' cũng giống như thư mục 'tutorial' mà ta đã tạo ở bài trước. Thư mục spider bên trong sẽ có 2 file : 'toscrape-css.py' và 'toscrape-xpath.py' 

2. Phân tích và dùng thử  2 file---------------------------------
 - File 'toscrape-css.py', là ví dụ điển hình sử dụng CSS selector để tìm elements để extract trong source HTML. 
# -*- coding: utf-8 -*-
import scrapy
class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }
        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
 - Tên spider là 'toscrape-css', để chạy nó mở terminal tới thư mục quotesbot mới giải nén. Chạy : 'scrapy crawl quotes', nó sẽ trả về kết quả ngay trên terminal của bạn, VD : 
{'text': u'\u201cThe world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.\u201d', 'tags': [u'change', u'deep-thoughts', u'thinking', u'world'], 'author': u'Albert Einstein'}
2018-03-02 08:55:20 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/>
 - Ở bài trước ta đã biết để crawl 1 website có 'urls', ta có thể khai báo 'urls' của nó trong phương thức 'start_requests()' hoặc dùng cách tắt là khai báo trong attribute 'start_urls' như trên. 
 - Khi khai báo urls như vậy, mặc định nó sẽ tạo object 'scrapy.Request' cho mỗi url đã khai báo, sau đó với mỗi khi nhận được 1 phản hồi từ mỗi request, nó sẽ khỏi tạo đối tượng 'response' và gọi method callback('parse()') với đối số là request tương ứng và đối tượng 'response'
 - Như trên ở trong 'parse()', ta thấy sử dụng tất cả là 'response.css'(nghĩa là dùng selector CSS) :
    + response.css('div.quote') : trả về list đối tượng Selector với thẻ div có thuộc tính class = 'quote'.
    + quote.css("span.text::text").extract_first() : trả về text của phần tử thẻ 'span' có thuộc tính class = 'text' đầu tiên(hàm extract_first()). 
    + quote.css("small.author::text").extract_first() : trả về text của phần tử thẻ 'span' có thuộc tính class = 'author' đầu tiên(hàm extract_first()).
    + quote.css("div.tags > a.tag::text").extract() : trả về array các text của phần tử thẻ 'a' có thuộc tính class = 'tag' có phần tử cha là 'div' có thuộc tính class = 'tags'.
    + response.css("li.next > a::attr(href)").extract_first() : trả về giá trị của thuộc tính 'href' của phần tử <a> đầu tiên năm trong thẻ '<li>' với thuộc tính class = 'next'.
 - Sử dụng yield để đưa các kết quả vào 1 dictionary của python
 - Ở bài trc cũng đã nhắc tới crawl nextpage sử dụng url hoặc selector, như bạn thấy 'next_page_urls' trả về link tương đối của page kế tiếp ví dụ '/page/2/', khi đó ta sẽ dùng 'response.urljoin(next_page_url)' nó sẽ tự động nói urls của response tương ứng với link tương đối 'next_page_url'. Vd: link ban đầu : 'http://quotes.toscrape.com' và link sau khi kết nối 'http://quotes.toscrape.com/page/2/'
 - Kế tới ta sẽ gọi 'scrapy.Request(response.urljoin(next_page_url))' truyền vào link sau khi kết nối.
 - Việc đặt keyword python yield ở trước scrapy.Request để mỗi khi response tương ứng với request xử lý trích xuất dữ liệu cho ra 1 dictionary riêng cho mỗi request

Xpath.-----------------------------
# -*- coding: utf-8 -*-
import scrapy
class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }
        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
 - Cũng tương tự như css, nó chỉ thay selector tìm kiếm phần tử dùng .xpath() như trên. Để hiểu rõ về xpath() bạn có thể vào w3school, tìm xpath đọc thêm.
