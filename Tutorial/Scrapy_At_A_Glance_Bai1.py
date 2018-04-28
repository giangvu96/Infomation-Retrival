1) Ví dụ mở đầu về scapy :
Lưu file quotes_spider.py như sau :

import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

Chạy : scrapy runspider quotes_spider.py -o quotes.json
Khi đó sẽ tạo ra 1 file "quotes.json" cùng thư mục với file "quotes_spider.py" ==> xem file "quotes.json"
Giải thích : Khi chạy câu lệnh trên crawl tạo request tới URLs được định nghĩa trong start_urls cụ thể là web 'http://quotes.toscrape.com/tag/humor/' và gọi method mặc định parse, truyền đối số là đối tượng response(chính là source nguồn của trang web đó). Trong lời gọi parse, chúng ta lặp các phần tử quote sử dụng CSS selector(response.css('div.quote')), sản sinh lấy ra text và author bằng .extract_first của phần tử div.quote, sau đó tìm kiềm link tới page kế tiếp và nếu page kế tiếp khác 'None' sẽ tiếp tục gọi method parse tương tự truyền vào link web kế tiếp và parse hiện tại.

2) Một trong những ưu điểm chính của Scrapy là : Các request lên lịch và xử lý không đồng bộ. Nghĩa là Scrapy không cần đợi cho một request kết thúc và được xử lý, nó có thể gửi 1 request khác hoặc làm thứ gì khác trong thời gian chờ đợi. Cũng có nghĩa là các request khác có thể tiếp tục thậm chí nếu 1 vài request fail hoặc có lỗi xảy ra trong khi xử lý nó.

Trong khi điều này cho phép bạn crawl ( thu thập thông tin ) 1 nhanh ( có thể gửi nhiều request cùng thời điểm, với khả năng chịu lỗi ). Scrapy cũng cho bạn điều khiển qua 1 vài setting. Bạn có thể làm mọi thứ như setting thời gian delay giữa mỗi request, giới hạn lượng request đồng thời trên domain hoặc trên IP, và thậm chí sử dụng extension tự động để tự động tìm ra.

Note : Điều này sử dụng 'feed exports'(đọc ở bài feed exports ) để tạo file JSON, bạn có thể dễ dàng thay đổi export format(XML, CSV,...) hoặc storage backend ( giao thức, dịch vụ lưu trữ) (FTP or Amazon S3,..)

3) Các đặc tính mạnh của Scrapy :
 - Được built support cho 'selecting and extracting' dữ liệu từ sources code HTML/XML sử dụng CSS selector và biểu thức Xpath ( đọc bài "selectors")
 - Có 'interactive shell console' có thể thử và debug scraping code rất nhanh mà không phải chạy hẳn scrapy ( đọc bài "Scrapy shell")
 - Built support 'generating feed exports' nhiều formats(JSON, CSV, XML) và lưu chữ chúng trong nhiều backends(FTP, S3, local filesystem)
 - HỖ trợ encoding mạnh, và tự động phát hiện xử lý kí tự lạ, không chuẩn và phá vỡ khai báo encoding
 - Hỗ trợ khả năng mở rộng mạnh, cho phép bạn plug các hàm của riêng của bạn sử dụng signals và 1 API(middlewares, extensions, and pipelines) (đọc bài 'extending-scrapy', 'signals', 'Item pipelines')
 - Nhiều extension và middlewares được gán sẵn để xử lý :
   + Xử lý cookies và section
   + Tính năng HTTP : compression(nén), authentication(xác minh), caching
   + Giả mạo user-agent ( người dùng đại diện)
   + robots.txt
   + crwal giới hạn độ sâu 
   + and more
 - Một console Telnet kết nối trong console Python chạy bên trong tiến tình Scrapy của bạn, để tư duy và gỡ lỗi crawler của bạn
 - Ngoài ra còn có các tiện ích khác như trình thu thập dữ liệu có thể thu thập thông tin từ các 'Sitemaps' và nguồn cấp dữ liệu XML/CSV, đường truyền dẫn để tự động tải hình ảnh (hoặc bất kỳ phương tiện nào khác) liên quan đến các item scraped, a caching DNS resolver và nhiều hơn nữa!
