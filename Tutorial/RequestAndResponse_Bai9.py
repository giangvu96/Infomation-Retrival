  - Scrapy sử dụng đối tượng 'Request' và 'Response' để crawling các website.
  - Điển hình, Các đối tượng 'Request' được khởi tạo trong các spider và truyền qua hệ thống cho đến khi chúng chạm tới Downloader, cái mà thực thi request và trả về 1 đối 'Response'.
  - Cả 2 class 'Request' và 'Response' có các class con mà thêm các chức năng ko yêu cầu trong các class cơ sở. Dưới đây là mô tả Các 'Request subclass' và 'Response subclass' :

1. Request objects---------------------------------------------------
_____________________________________________
class scrapy.http.Request(url[, callback, method='GET', headers, body, cookies, meta, encoding='utf-8', priority=0, dont_filter=False, errback, flags])
_____________________________________________
  - 1 đối tượng Request biểu diễn 1 HTTP request, được tạo ra trong Spider và được thực thi bởi Downloader, và do đó tạo ra 1 Response.
  - Các parameter :
	+ url (string) – URL của request này
	+ callback (callable) – Hàm sẽ được gọi với response là đối số đầu tiên(cái mà dược Downloader tải về). Nếu 1 Request ko chỉ định 1 callback, phương thưc parse() của spider sẽ được sử dụng. Lưu ý, nếu exception tăng lên khi xử lý, errback sẽ được gọi thay thế cho callback.
	+ method (string) – the HTTP method of this request. Defaults to 'GET'.
	+ meta (dict) – the initial values for the Request.meta attribute. If given, the dict passed in this parameter will be shallow copied.
	+ body (str or unicode) – the request body. If a unicode is passed, then it’s encoded to str using the encoding passed (which defaults to utf-8). If body is not given, an empty string is stored. Bất kể of the type of this argument, the final value stored will be a str (never unicode or None).
	+ headers (dict) – the headers of this request. The dict values can be strings (for single valued headers) or lists (for multi-valued headers). If None is passed as value, the HTTP header will not be sent at all.
	+ cookies (dict or list) – the request cookies. These can be sent in two forms.
	a)Using a dict:
		request_with_cookies = Request(url="http://www.example.com",
                               cookies={'currency': 'USD', 'country': 'UY'})
	b)Using a list of dicts:
		request_with_cookies = Request(url="http://www.example.com",
                               cookies=[{'name': 'currency',
                                        'value': 'USD',
                                        'domain': 'example.com',
                                        'path': '/currency'}])
	The latter form allows for customizing the domain and path attributes of the cookie. This is only useful if the cookies are saved for later requests.

	When some site returns cookies (in a response) those are stored in the cookies for that domain and will be sent again in future requests. That’s the typical behaviour of any regular web browser. However, if, for some reason, you want to avoid merging with existing cookies you can instruct Scrapy to do so by setting the dont_merge_cookies key to True in the Request.meta.

	Example of request without merging cookies:

	request_with_cookies = Request(url="http://www.example.com",
                               cookies={'currency': 'USD', 'country': 'UY'},
                               meta={'dont_merge_cookies': True})
	For more info see CookiesMiddleware.

	+ encoding (string) – the encoding of this request (defaults to 'utf-8'). This encoding will be used to percent-encode the URL and to convert the body to str (if given as unicode).
	+ priority (int) – the priority of this request (defaults to 0). The priority is used by the scheduler to define the order used to process requests. Requests with a higher priority value will execute earlier. Negative values are allowed in order to indicate relatively low-priority.
	+ dont_filter (boolean) – indicates that this request should not be filtered by the scheduler. This is used when you want to perform an identical request multiple times, to ignore the duplicates filter. Use it with care, or you will get into crawling loops. Default to False.
	+ errback (callable) – a function that will be called if any exception was raised while processing the request. This includes pages that failed with 404 HTTP errors and such. It receives a Twisted Failure instance as first parameter. For more information, see Using errbacks to catch exceptions in request processing below.
	+ flags (list) – Flags sent to the request, can be used for logging or similar purposes.


2. Request.meta special keys-----------------------------------------



3. Request subclasses------------------------------------------------



4. Response objects--------------------------------------------------



5. Response subclasses-----------------------------------------------
