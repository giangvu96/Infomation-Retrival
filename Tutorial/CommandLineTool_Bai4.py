1. Command line tool ------------------------------------
    Scrapy được điều khiển qua công cụ dòng lệnh gọi là 'Scrapy tool' để phân biệt nó với các lệnh con bên trong nó khi ta gọi 'shell' mà ta gọi là 'commands' hoặc 'Scrapy commands'
    Scrapy tool cung cấp một số lệnh cho một số mục đích, mỗi lệnh có các đối số và tùy chọn (argument và option)
    Lệnh 'scrapy deploy' đã được gỡ bỏ ở bản 1.0 vì một số lý do

2. Configuration settings -------------------------------
    Scrapy tìm các thông số cấu hình trong file 'scrapy.cfg' (ini-stype) ở các vị trí:
	1. /etc/scrapy.cfg hoặc c:\scrapy\scrapy.cfg (system-wide),
	2. ~/.config/scrapy.cfg ($XDG_CONFIG_HOME) và ~/.scrapy.cf ($HOME) for global (user-wide) settings, and
	3. scrapy.cfg (bên trong thư mục project scrapy.)
    Các settings từ các file này được merged theo thứ tự ở trên: Nhưng Các giá trị do người dùng định nghĩa có mức độ ưu tiên cao hơn các giá trị mặc định toàn hệ thống và các setting cho toàn bộ project ghi đè lên tất cả các giá trị khác, khi nó được người dùng định nghĩa.
    Scrapy có khả năng tự hiểu, có thể được cấu hình qua một số biến môi trường, ở thời điểm hiện tại có:
	. SCRAPY_SETTINGS_MODULE (see Designating the settings)
	. SCRAPY_PROJECT
	. SCRAPY_PYTHON_SHELL (see Scrapy shell)

3. Default structure of Scrapy projects------------------
    Trước khi đi sâu vào 'Scrapy tool' và các lệnh con của nó, đầu tiên hiểu rõ cấu trúc thư mục của project Scrapy
    Mặc dù project có thể được modified, nhưng tất cả project có cấu trúc file giống nhau, mặc định : 
scrapy.cfg
myproject/
    __init__.py
    items.py
    middlewares.py
    pipelines.py
    settings.py
    spiders/
        __init__.py
        spider1.py
        spider2.py
        ...
    Thư mục chứa file 'scrapy.cfg' là thư mục root của project. File này chứa tên của module 'python' ta setting project. Vd:
[settings]
default = myproject.settings

4. Using the scrapy tool---------------------------------
    Bạn có thể chạy 'Scrapy tool' mà không có arguments và nó sẽ show ra một số trợ giúp hữu ích và lệnh có sẵn như: 
|Scrapy 1.5.0 - project: tutorial
|Usage:
|  scrapy <command> [options] [args]
|Available commands:
|  bench         Run quick benchmark test
|  check         Check spider contracts
|  crawl         Run a spider
|  edit          Edit spider
|  fetch         Fetch a URL using the Scrapy downloader
|  genspider     Generate new spider using pre-defined templates
|  list          List available spiders
|  parse         Parse URL (using its spider) and print the results
|  runspider     Run a self-contained spider (without creating a project)
|  settings      Get settings values
|  shell         Interactive scraping console
|  startproject  Create new project
|  version       Print Scrapy version
| view          Open URL in browser, as seen by Scrapy
|Use "scrapy <command> -h" to see more info about a command

5. Creating projects------------------------------------
    Việc đầu tiên thường làm với 'scrapy tool' là tạo your project Scrapy: 
	| scrapy startproject myproject [project_dir] |
    Nó sẽ tạo 1 project Scrapy dưới thư mục 'project_dir'. Nếu 'project_dir' không xác định, 'project_dir' sẽ mặc định là 'myproject'
    Tiếp theo bạn vào thư mục project mới tạo : 'cd project_dir'
    Và ta đã sẵn sàng dùng các lệnh scrapy để quản lý, điều khiển your project.

6. Controlling projects---------------------------------
    Vd, tạo 1 spider mới :
	| scrapy genspider mydomain mydomain.com |
    Một số lệnh Scarpy phải chạy bên trong project Scrapy (như lệnh 'crawl'), xem thêm phần 'commands reference' để biết lệnh này phải chạy bên trong hay bên ngoài project Scrapy
    Lưu ý một số lệnh có những hành vi khác nhau khi chạy bên trong projects. Ví dụ: lệnh 'fetch' sẽ dùng các hành vi được ghi đè của spider (như thuộc tính 'user_agent' để ghi đè lên 'user-agent') nếu url đang tìm nạp liên kết với một spider cụ thể

7. Available tool commands------------------------------
    Phần này chứa 1 list các lệnh có sẵn với mô tả cụ thể và ví dụ sử dụng, nhớ răng khi không biết lệnh 'A' dùng để làm gì, bạn có thể nhận được info của nó bằng cách gõ : 'scrapy A -h' và bạn cũng có thể thấy tất cả các lệnh gõ : 'scrapy -h'
    Có hai loại lệnh, 1 là chỉ chạy bên trong project Scrapy (Project-specific commands), loại 2 là nó vừa có thể chạy bên trong và bên ngoài project Scrapy (Global commands). Loại thứ 2 có thể có hành vi hơi khác giữa khi chạy bên trong và bên ngoài project scrapy, bởi vì chúng sử dụng các settings được ghi đè ở của project scrapy.
||||Global commands:
_______________________
|'startproject' command
    [Cú pháp : |scrapy startproject <project_name> [project_dir]|
    Tạo 1 project mới tên project_name trong thư mục project_dir
    Nếu không có project_dir, thì project_dir sẽ được đặt tên giống project_name]
	Vd : |scrapy startproject myproject|
____________________
|'genspider' command
    [Cú pháp : |scrapy genspider [-t template] <name> <domain>|
    Tạo 1 spider mới nằm trong thư mục hiện tại(ngoài project Scrapy), hoặc trong folder spider nếu nó được gọi trong project Scrapy
    Đối số <name> là tên spider, <domain> để khởi tạo thuộc tính allowed_domains và thuộc tính start_urls của spider]
	Vd : |scrapy genspider -t crawl scrapyorg scrapy.org|
___________________
|'settings' command
    [Cú pháp : |scrapy settings [options]|
    Get giá trị của một setting Scrapy
    Nếu được sử dụng bên trong project nó sẽ hiển thị giá trị setting trong project, nếu không nó sẽ hiển thị giá trị Scrapy mặc định.]
	Vd : |scrapy settings --get DOWNLOAD_DELAY|
____________________
|'runspider' command
    [Cú pháp : |scrapy runspider <spider_file.py>|
    Chạy 1 spider trong 1 file Python, mà không phải tạo project.]
    	Vd : |scrapy runspider myspider.py|
________________
|'shell' command
    [Cú pháp : |scrapy shell [url]|
    Khởi tạo Scrapy shell với URL cho trước hoặc empty nếu không có URL. Nó cũng hỗ trợ đường dẫn tương đối hoặc tuyệt đối ./ or ../
    Các option được hỗ trợ : 
    --spider=SPIDER: bypass spider autodetection and force use of specific spider
    -c code: evaluate the code in the shell, print the result and exit
    --no-redirect: do not follow HTTP 3xx redirects (default is to follow them); this only affects the URL you may pass as argument on the command line; once you are inside the shell, fetch(url) will still follow HTTP redirects by default.]
    	Vd : |scrapy shell http://www.example.com/some/page.html|
	scrapy shell --no-redirect --nolog http://httpbin.org/redirect-to?url=http%3A%2F%2Fexample.com%2F -c '(response.status, response.url)'
(302, 'http://httpbin.org/redirect-to?url=http%3A%2F%2Fexample.com%2F')
________________
|'fetch' command
    [Cú pháp : |scrapy fetch <url>|
    Downloads bởi URL sử dụng trình download Scrapy và ghi contents của URL đó tới đầu ra chuẩn
    Điều thú vị về lệnh này là nó fetch page như cách mà spider làm. Ví dụ: nếu spider có thuộc tính USER_AGENT mà ghi đè User Agent, lệnh fetch sẽ sử dụng nó.
    Vì thế, lệnh này có thể được dùng để "xem" làm thế nào spider fetch một trang nhất định.
    Nếu dùng ngoài project, nó sẽ chỉ sử dụng các thiết lập mặc định của Scrapy downloader.
    Các option được hỗ trợ : 
    --spider=SPIDER: bypass spider autodetection and force use of specific spider
    --headers:print the response’s HTTP headers instead of the response’s body
    --no-redirect: do not follow HTTP 3xx redirects (default is to follow them)]
	Vd : |scrapy fetch --nolog --headers http://www.example.com/|
_______________
|'view' command
    [Cú pháp : |scrapy view <url>|
    Open URL trong trình duyệt. Thỉnh thoảng Spider see pages khác với người dùng, vì vậy lệnh này có thể dùng để kiểm tra cái mà spider "view thấy" và những gì bạn mong đợi.
    Các option được hỗ trợ : 
    --spider=SPIDER: bypass spider autodetection and force use of specific spider
    --no-redirect: do not follow HTTP 3xx redirects (default is to follow them)]
	Vd : |scrapy view http://www.example.com/some/page.html|
__________________
|'version' command
    [Cú pháp : |scrapy version [-v]|
    Print version Scrapy, nếu sử dụng option -v, nó cũng in thông tin Python, Twishted and Platform, hữu ích co reports bug
	Vd : |scrapy version -v|
||||Project-only commands:
________________ 
|'crawl' command
    [Cú pháp : |scrapy crawl <spider>|
    Start crawling spider với tên <spider>
	Vd : |scrapy crawl myspider|
________________
|'check' command
    [Cú pháp : |scrapy check [-l] <spider>|
    Run contract checks
	Vd : |scrapy check -l myspider|
_______________
|'list' command
    [Cú pháp : |scrapy list|
    Liệt kê ra list spider có sẵn trong project. Ouput : 1 spider / 1 dòng
	Vd : |scrapy list|
_______________
|'edit' command
    [Cú pháp : |scrapy edit <spider>|
    Edit spider sử dụng trình edit được định nghĩa trong biến môi trường EDITOR hoặc EDITOR setting (nếu không set).]
    Nó chỉ là 1 cách edit tắt, deverloper dĩ nhiên sẽ chọn any tool hoặc IDE để write và debug spiders
	Vd : |scrapy edit spider1|
________________
|'parse' command
    [Cú pháp : |scrapy parse <url> [options]|
    Fetches URL and parses respon tới spider xử lý nó, phương thức passed với option --callback, or parse nếu không cho trước.
    Supported options:
	--spider=SPIDER: bypass spider autodetection and force use of specific spider
	--a NAME=VALUE: set spider argument (may be repeated)
	--callback or -c: spider method to use as callback for parsing the response
	--meta or -m: additional request meta that will be passed to the callback request. This must be a valid json string. Example: –meta=’{“foo” : “bar”}’
	--pipelines: process items through pipelines
	--rules or -r: use CrawlSpider rules to discover the callback (i.e. spider method) to use for parsing the response
	--noitems: don’t show scraped items
	--nolinks: don’t show extracted links
	--nocolour: avoid using pygments to colorize the output
	--depth or -d: depth level for which the requests should be followed recursively (default: 1)
	--verbose or -v: display information for each depth level]
	Vd : |scrapy parse http://www.example.com/ -c parse_item|
________________
|'bench' command
    [Cú pháp : |scrapy bench|
    Run a quick benchmark test.
	Vd : |scrapy bench|

8. Custom project commands............................
    Bạn cũng có thể thêm các lệnh project của bạn bằng cách dùng COMMANDS_MODULE setting. Xem các lệnh Scrapy trong scrapy / commands cho các ví dụ về cách ra lệnh của bạn. ("https://github.com/scrapy/scrapy/tree/master/scrapy/commands")
_______________
COMMANDS_MODULE :
    Default: '' (empty string)
    Đây là module dùng để tìm Scrapy command custom. Việc này dùng để thêm các lệnh tùy chỉnh cho project Scrapy của bạn.
	Vd: COMMANDS_MODULE = 'mybot.commands'
___________________________________________
Register commands via setup.py entry points
Note : Đây là tính năng thử nghiệm, sử dụng cẩn thận
    Bạn cũng có thể thêm các lệnh Scrapy từ thư viện ngoài bằng việc thêm một section 'scrapy.commands' vào entry points của file thư viện 'setup.py'.
	Vd add 'my_commands' command :
	from setuptools import setup, find_packages
	setup(name='scrapy-mymodule',
	  entry_points={
	    'scrapy.commands': [
	      'my_command=my_scrapy_module.commands:MyCommand',
	    ],
	  },
	 )





    
    
    


