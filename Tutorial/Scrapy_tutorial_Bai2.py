Trong bài học, ta sẽ scrape web ' quotes.toscrape.com', 1 website chứa danh sách trích dẫn các tác giả nổi tiếng

1. Creating a new Scrapy project------------------------------------
 - Trước khi bắt đầu, bạn sẽ phải setup 1 folder project Scarpy. Vào termial cd tới nơi bạn muốn lưu project. Sau đó gõ 'scrapy startproject tutorial', thư mục có tên tutorial được tạo và có contents :
tutorial/
    scrapy.cfg            # deploy configuration file
    tutorial/             # project's Python module, you'll import your code from here
        __init__.py
        items.py          # project items definition file
        middlewares.py    # project middlewares file
        pipelines.py      # project pipelines file
        settings.py       # project settings file
        spiders/          # a directory where you'll later put your spiders
            __init__.py
 - Spiders là các class bạn định nghĩa và Scrapy sử dụng để scrape info từ 1 website(or 1 group website). Chúng phải phân lớp bằng scrapy.Spider và định nghĩa các request ban đầu để làm, tùy ý how to follow links in page, how to parse nội page được tải để trích xuất data.

2. Writing a spider to crawl a site and extract data-------------------
 - Lưu file 'quotes_spider.py' under thư mục 'tutorial/spiders' contents :
import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
 - Như bạn thấy, phân lớp Spider scrapy.Spider và define 1 vài attribute and methods
    + name : định danh Spider. Phải duy nhất trong 1 Project, ko thể set name giống nhau cho các Spiders khác nhau
    + start_requests(): phải trả về 1 1 tập request lặp lại(cái mà Spider sẽ crawl từ đó), các request kế tiếp sẽ được khỏi tạo sau request ban đầu
    + parse(): method gọi xử lý response được tải từ mỗi request. Đối số reponse là 1 instance(thể hiện) của 'TextResponse' chứa content page và có các method hữu ích để xử lý nó.
    Method parse() thường parse response, trích xuất data như dicts và cũng tìm kiếm các URL mới để theo dõi và tạo ra các new request từ chúng.
 - Để chạy spider của bạn : đi tới thư mục chứa project của bạn( ở đây là tutorial) run:  'scrapy crawl quotes'
 - Câu lệnh này run spider với tên 'quotes' mà chúng ta đã add, nó sẽ gửi 1 vài request tới domain 'quotes.toscrape.com'. Bạn sẽ nhận được 1 output console giống như : 
2018-03-01 15:26:34 [scrapy.core.engine] INFO: Spider opened
2018-03-01 15:26:34 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2018-03-01 15:26:34 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
2018-03-01 15:26:34 [scrapy.core.engine] DEBUG: Crawled (404) <GET http://quotes.toscrape.com/robots.txt> (referer: None)
2018-03-01 15:26:35 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
2018-03-01 15:26:35 [quotes] DEBUG: Saved file quotes-1.html
2018-03-01 15:26:35 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/2/> (referer: None)
2018-03-01 15:26:35 [quotes] DEBUG: Saved file quotes-2.html
2018-03-01 15:26:35 [scrapy.core.engine] INFO: Closing spider (finished)
 - Bây giờ kiểm tra các file trong thư mục hiện tại. Sẽ có 2 files mới đc tạo 'quotes-1.html' and 'quotes-2.html' với content tương ứng URLs
 - Giải thích : Scrapy lên lịch cho các đối tượng 'scrapy.Request' được trả về bơi method 'start_requests()' Spider. Khi nhận được 1 response cho mỗi request, nó khởi tạo đối tượng Response và gọi method 'parse()' truyền đối số chính là đối tượng 'Response'
 - Thay vì thực thi method 'start_requests()' khởi tạo đối tượng scrapy.Request từ URLs, bạn có thể define attribute start_urls với 1 list URLs. List này sẽ được sử dụng mặc định thực thi bởi 'start_requests()' tạo các request ban đầu của bạn :
import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
 - Method 'parse()' sẽ được gọi để xử lý mỗi request cho URLs mặc dù ta ko nói Scrapy làm vậy. ĐIều này bởi vì 'parse()' là method callback mặc định, cái mà được gọi cho các request mà không được chỉ định rõ ràng.

EXTRACTING DATA-----------------
 - Cách tốt nhất để học cách trích data là thử với 'selectors' sử dụng console : 'scrapy shell 'http://quotes.toscrape.com/page/1/'' bạn sẽ thấy :
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7f62769bbcd0>
[s]   item       {}
[s]   request    <GET http://quotes.toscrape.com/page/1/>
[s]   response   <200 http://quotes.toscrape.com/page/1/>
[s]   settings   <scrapy.settings.Settings object at 0x7f62769bbc50>
[s]   spider     <DefaultSpider 'default' at 0x7f6276394ed0>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects 
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser
 - Sử dụng shell, thử selecting elements sử dụng CSS với đối tượng response : 
>>> response.css('title')
[<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
 - Để lấy text của title :
>>> response.css('title::text').extract()
['Quotes to Scrape']
 - Lấy cả thẻ title : 
>>> response.css('title').extract()
['<title>Quotes to Scrape</title>']
 - Ở đây result khi gọi .extract() là 1 danh sách, bởi vì ta đang xử lý với 1 thể hiện của 'SelectorList'. Muốn lấy first result :
>>> response.css('title::text').extract_first()
'Quotes to Scrape'
 - Có thể thay thế : >>> response.css('title::text')[0].extract(), tuy nhiên sử dụng .extract_first() tránh lỗi IndexError và trả về None khi không tìm thấy bất kì element khớp với selection.
 - Ngoài  extract() and extract_first() bạn có thể dùng 're()' trích xuất sử dụng biểu thức thường :
>>> response.css('title::text').re(r'Quotes.*')
['Quotes to Scrape']
>>> response.css('title::text').re(r'Q\w+')
['Quotes']
>>> response.css('title::text').re(r'(\w+) to (\w+)')
['Quotes', 'Scrape']
 - Để tìm các CSS selectors phù hợp, bạn có thể mở page bằng trình duyện của bạn dùng developer tools tìm phần tử phù hợp. 
 - Selector Gadget là 1 công cụ hữu ích để tìm nhanh Css selector

Ngắn gọn về Xpath-----------------------------
 - Ngoài Css, Scrapy hỗ trợ selector sử dụng biểu thức XPath
>>> response.xpath('//title')
[<Selector xpath='//title' data='<title>Quotes to Scrape</title>'>]
>>> response.xpath('//title/text()').extract_first()
'Quotes to Scrape'
 - Biểu thức XPath rất mạnh, là nền tảng của Scrapy Selector. Trên thực tế, Css selector dược chuyển đổi sang XPath. Using XPath, bạn có thể select thứ như: select the link that chứa text “Next Page”. Điều này làm Xpath rất phù hợp với các task của Scrapy, và bạn nên học XPath ngay cả khi bạn đã biết cách dùng Css selector, nó sẽ làm Scraping đơn giản hơn.

Extracting quotes and authors----------------------------------
 - Mỗi quote trong 'http://quotes.toscrape.com' được biểu diễn bởi các phần tử HTML như :
<div class="quote">
    <span class="text">“The world as we have created it is a process of our
    thinking. It cannot be changed without changing our thinking.”</span>
    <span>
        by <small class="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
    </span>
    <div class="tags">
        Tags:
        <a class="tag" href="/tag/change/page/1/">change</a>
        <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
        <a class="tag" href="/tag/thinking/page/1/">thinking</a>
        <a class="tag" href="/tag/world/page/1/">world</a>
    </div>
</div>
 - Mở scrapy shell(console) và nghịch cho ra dữ liệu mà bạn muốn : scrapy shell 'http://quotes.toscrape.com'
 - Lấy list selectors các phần tử HTML quote : >>> response.css("div.quote"), nó sẽ in ra 1 loạt các selector loằng ngoằng.
 - Giờ hãy gán phần tử selector đầu tiên cho 1 biến 'quote' và ta có thể chạy trực tiếp trên biến này :quote = response.css("div.quote")[0]
 - Extract title, author, và tags từ biến quote :
>>> title = quote.css("span.text::text").extract_first()
>>> title
u'\u201cThe world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.\u201d'
>>> author = quote.css("small.author::text").extract_first()
>>> author
u'Albert Einstein'
 - Cho cacs tags laf 1 list strings, ta cos theer extract() để get all :
>>> tags = quote.css("div.tags a.tag::text").extract()
>>> tags
[u'change', u'deep-thoughts', u'thinking', u'world']
 - Ta có thể lặp lại các phần tử và đặt chúng lại với nhau trong 1 Python dictionary:
>>> for quote in response.css("div.quote"):
...  text = quote.css("span.text::text").extract_first() 
...  author = quote.css("small.author::text").extract_first()
...  tags = quote.css("div.tags a.tag::text").extract()
...  print(dict(text=text, author=author, tags=tags))
... 
{'text': u'\u201cThe world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.\u201d', 'tags': [u'change', u'deep-thoughts', u'thinking', u'world'], 'author': u'Albert Einstein'}

3. Exporting the scraped data using the command line-------------------
Extracting data in our spider-------------------------------
 - Quay trở lại sprider chúng ta. Tới giờ nó chưa trích bất kì data nào, chỉ save toàn bộ page file HTML tới local file. Hãy lặp logic trên cho spider chúng ta
 - 1 Scrapy spider thường tạo nhiều dictionary chứa dữ liệu trích ra từ page. Để làm vậy, sử dụng key yield của pythhon trong callback :
import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
- Sau đó chạy spider này 'scrapy crawl quotes', out put sẽ log như :
2018-03-01 16:45:07 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/2/>
{'text': u'\u201cI like nonsense, it wakes up the brain cells. Fantasy is a necessary ingredient in living.\u201d', 'tags': [u'fantasy'], 'author': u'Dr. Seuss'}
2018-03-01 16:45:07 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/2/>
{'text': u'\u201cI may not have gone where I intended to go, but I think I have ended up where I needed to be.\u201d', 'tags': [u'life', u'navigation'], 'author': u'Douglas Adams'

Storing the scraped data------------------------------
 - 1 cách đơn giản lưu dữ liệu đã scraped sử dụng 'Feed exports' với command : scrapy crawl quotes -o quotes.json
 - Nó sẽ tạo 1 file 'quotes.json' chứa tất cả các item đã scraped trong thư mục hiện tại(tutorial)
 - Với lý do historic, Scrapy hợp lại với file đã tồn tại thay vì ghi đè content của nó. Nếu bạn chạy command trên 2 lần mà ko xóa file trước lần thứ 2, bạn sẽ kết thúc với 1 file JSON hỏng
 - Bạn cũng có thể dùng format khác giống JSON là JSON Line : scrapy crawl quotes -o quotes.jl
 - JSON Line hữu ích vì nó trực quan, bạn có thể dễ dàng thêm record mới. Nó không có vấn đề giống JSON khi chạy 2 lần. Ngoài ra vì mỗi record là 1 dòng riêng biệt, bạn có thể xử lý các file process lớn mà không cần phải fit everything trong bộ nhớ, có những công cụ như JQ để giúp thực hiện điều trên command-line.
 - Trong small project(giống như trong bài học), như vậy là đủ. Tuy nhiên nếu bạn muốn thực hiện thêm nhiều thứ phức tạp hơn với scraped items, bạn có thể viết một 'Item Pipeline'(đọc bài 'item pipeline'). 1 file placeholder cho Item Pipelines đã được setup cho bạn khi project được tạo trong 'tutorial/pipelines.py'
 - Mặc dù bạn không cần thực hiện bất kỳ item pipelines nào nếu bạn chỉ muốn lưu trữ iteam được scraped.

4. Changing spider to recursively follow links-------------------------
FOLLOWING LINKS--------------------
 - Thay vì scraping từ 1 2 page ở 'http://quotes.toscrape.com', bạn muốn trích xuất từ toàn bộ các pages trong website.
 - Giờ bạn biết cách extract data từ pages, hãy xem cách follow links từ chúng
 - Thứ đầu tiên để extract link tới page bạn muốn follow. Kiểm tra trang của chúng ta, sẽ  thấy có 1 link tới next page như sau :
<ul class="pager">
    <li class="next">
        <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
    </li>
</ul>
 - Chúng ta có thể thử extracting nó trong shell :
>>> response.css('li.next a').extract_first()
u'<a href="/page/2/">Next <span aria-hidden="true">\u2192</span></a>'
 - Giờ xem spider đã chỉnh sửa tương ứng follow link tới next page, extracting data từ nó :
import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
 - Bây giờ sau khi extracting data, parse() tìm link tới trang kế tiếp, xây dựng link đầy đủ sử dụng 'urljoin()' và yields 1 request mới tới next page, truyền chính nó để xử lý data cho trang kế tiếp và tiếp tục crawling toan bộ pages.
 - Sử dụng cách này, bạn có thể tạo bộ máy cralers phức tạp follow links theo nguyên tắc bạn định nghĩa, và trích ra các loại dữ liệu phụ thuộc khác nhau cho page được visiting.
 - Trong ví dụ của chúng tôi, tạo loop, following tất cả các link cho tới khi ko tìm thấy link nào nữa

A shortcut for creating Requests-------------------
 - Như đg tắt tạo object Request bạn có thể dùng 'response.follow' :
yield response.follow(next_page, callback=self.parse)
 - Không giống Scrapy.Request, 'response.follow' hồ trợ quan hệ trực tiếp URLs, không cần gọi urljoin. Lưu ý 'response.follow' chỉ trả về 1 thể hiện của object Request; bạn vẫn phải yield Request này.
 - Bạn cũng có thể truyền 1 selector tới 'response.follow' thay cho 1 chuỗi, selector này nên trích xuất các attribute cần thiết :
for href in response.css('li.next a::attr(href)'):
    yield response.follow(href, callback=self.parse)
 - Phần tử <a> có 1 đg tắt : response.follow sử dụng thuộc tính href của chúng 1 cách tự động. Vì vậy code có thể tắt hơn nữa :
for a in response.css('li.next a'):
    yield response.follow(a, callback=self.parse)
 - Lưu ý response.follow(response.css('li.next a')) ko đúng vì response.css trả về 1 list selectors, ko phải single selector. Phải dùng 1 vòng for như trên hoặc lấy phần tử đầu tiên :response.follow(response.css('li.next a')[0])

5. Using spider arguments----------------------------------------------
 - Bạn có thể cung cấp đối số trên command line cho spider của bạn bằng cách sử dụng option '-a' khi chạy chúng :
'scrapy crawl quotes -o quotes-humor.json -a tag=humor'
 - Các đối số được truyền vào method __init__ và trở thành thuộc tính mặc định của spider của bạn.
 - Trong vd này, giá trị đg cung cấp là đối số tag sẽ trở thành biến thông qua self.tag. Bạn có thể sử dụng cách này để cho crawler của bạn chỉ trích xuất ra 1 thẻ cụ thể, build url dựa trên đối số :
  def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)
 - Như vậy khi truyền tag=humor, nó sẽ chỉ visit urls từ humor tag :'http://quotes.toscrape.com/tag/humor'


