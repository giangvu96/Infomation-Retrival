 - Item Loaders cung cấp cơ chế thuận tiện cho việc nạp Items. Mặc dù Items có thể được nạp bằng việc sử dụng API dictionay, nhưng Item Loaders cung cấp nhiều API thuận tiện hơn để nạp chúng từ 1 tiến trình scraping, bằng cách tự động hóa 1 số tác vụ phổ biến như xử lý (parsing) dữ liệu thô trước khi gán nó vào biến.
 - Nói cách khác, Items cung cấp container chứa dữ liệu scraped, còn Item Loaders cung cấp kĩ thuật nạp dữ liệu vào container đó.
 - Item Loaders được thiết kế với mục đích: cung cấp cơ chế đơn giản, mềm dẻo và hiệu quả, mà nó extend và overriding các rules parsing trường (field) khác nhau, hoặc bởi spider, hoặc bởi dịnh dạng (format) mã nguồn (HTML,XML) mà ko trở thành 1 cơn ác mộng khi phải maintaining.

1. Using Item Loaders to populate items-------------------------
 - Để sử dụng Item Loader, đầu tiên bạn phải khởi tạo nó. Bạn có thể khởi tạo nó giống đối tượng từ điển object dict hoặc ko (như trong trường hợp 1 Item tự động khởi tạo trong constructor Item Loader mà nó sử dụng class Item gán trong thuộc tính(attribute) ItemLoader.default_item_class .
 - Sau đó bạn bắt đầu thu thập các giá trị trong Item Loader,dùng Selectors. Bạn có thể thêm nhiều hơn một giá trị vào cùng một trường Item; Item Loader sẽ biết cách kết nói 'join' các giá trị đó (sau) bằng cách sử dụng 1 hàm (function) xử lý thích hợp.
 - Dưới dây là 1 trường hợp sử dụng điển hình Item Loader trong 1 spider, sử dụng item Product đã được khai báo trong chương Items :
_____________________________________________
from scrapy.loader import ItemLoader
from myproject.items import Product
def parse(self, response):
    l = ItemLoader(item=Product(), response=response)
    l.add_xpath('name', '//div[@class="product_name"]')
    l.add_xpath('name', '//div[@class="product_title"]')
    l.add_xpath('price', '//p[@id="price"]')
    l.add_css('stock', 'p#stock]')
    l.add_value('last_updated', 'today') # you can also use literal values
    return l.load_item()
____________________________________________
 - Nhìn vào đoạn code trên, bạn sẽ thấy trường 'name' được lấy từ 2 vị trí Xpath khác nhau, nói cách khác dữ liệu được thu thập bởi việc lấy từ 2 vị trí Xpath sử dụng method 'add_xpath()'
//div[@class="product_name"]
//div[@class="product_title"]
nghĩa là dữ liệu sẽ được gán cho trường 'name' sau. Tiếp theo, các dòng lệnh tương tự gán các trường price, stock với vị trí xpath và css sử dụng thêm phương thức 'add_css()', và trường 'last_updated' được gán trực tiếp giá trị 'today', sử dụng method 'add_value()'.
 - Cuối cùng, khi toàn bộ dữ liệu được thu thập, phương thức 'ItemLoader.load_item()' được gọi, đây là phương thức mà trả về item thực tế với dữ liệu đã được thu thập trước đó (bởi các lời gọi 'add_xpath', 'add_css', 'add_value').

2. Trình xử lý (processors) Input and Output-------------------------
 - Một Item Loader chứa 1 processors input và 1 processors output cho mỗi field trong item. Processor input xử lý dữ liệu được thu thập extracted ngay khi nhận được (qua các method 'add_xpath', 'add_css', 'add_value'). Kết quả của processor input được lấy và lưu trong Itemloader. Sau khi thu thập tất cả dữ liệu, phương thức 'ItemLoader.load_item()' được gọi để nạp và và trả về đối tượng item đã nạp. Đây cũng là câu lệnh mà gọi processor ouput với dữ liệu đã thu thập trước đó (được xử lý bằng processor input). Kết quả của processor output là giá trị cuối cùng mà gán cho item. 
 - Nhìn ví dụ với các bước : 
l = ItemLoader(Product(), some_selector)
l.add_xpath('name', xpath1) # (1)
l.add_xpath('name', xpath2) # (2)
l.add_css('name', css) # (3)
l.add_value('name', 'test') # (4)
return l.load_item() # (5)
# (1) Dữ liệu từ xpath1 được trích xuất, và truyền qua processor input của field name. Kết quả processor input được thu thập và lưu trong ItemLoader(Nhưng không được gán cho item)
# (2) Tương tự dữ liệu từ xpaht2 được trích xuất và truyền qua processor input của Field name. Kết quả processor input được thêm vào dữ liệu đã thu thập của # (1)
# (3) Trường hợp này tương tự như trên, nó dùng Css selector. Kết quả processor input được thêm vào dữ liệu đã được thu thập trong (1) và (2) (nếu có)
# (4) Trường hợp này cũng vậy, nhưng giá trị được thu thập bị gán trực tiếp, thay thế cho việc sử dụng selector Css hoặc biểu thức Xpath. Tuy nhiên giá trị vẫn đươc truyền vào processor input. Vì giá trị trong trường hợp này ko phải là iterable, nên nó sẽ được converted sang iterable của 1 phần tử  (element) đơn trước khi truyền nó vào processor input, vì proccessor input chỉ nhận iterables
# (5) Dữ liệu được thu thập ở bước (1)(2)(3)(4) được truyền vào output processor của field name. Kết quả của processor output chính là giá trị được gán cho Field name trong item.
 - Lưu ý, processors chỉ là các đối tượng (object) có thể gọi được, được gọi với dữ liệu đã parsed(đã phân tích cú pháp), và trả về dữ liệu đã parsed(đã phân tích cú pháp). Vì vậy bạn có thể sử dụng bất kì function nào giống như processor input và output. Yêu cầu duy nhất là chúng phải nhận 1 và chỉ 1 đối số, đó là iterator.
 - Scrapy cũng đi kèm với 1 số bộ xử lý thuận tiện(xem thêm 'commonly used processors ')

3. Declaring Item Loaders--------------------------------------------
 - Dược khai báo giống Item, cú pháp khai báo lớp class :
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in = MapCompose(unicode.title)
    name_out = Join()
    price_in = MapCompose(unicode.strip)
    # ...
 - Như bạn thấy, input và output được khai báo sử dụng hậu tố _in/_out. Bạn cũng có thể khai báo 1 processor in/output sử dụng thuộc tính 'default_input_processor' và 'default_output_processor' 

4. Declaring Processors Input and Output-----------------------------
 - Trong phần 3, processor in/output có thể khai báo trong khi khai báo Item Loader, và nó rất phổ biển để khai báo processor input theo cách này. Tuy nhiên, có 1 nơi mà bạn có thể chỉ định processor input và output, trong Item Field (Metadata). Vd:
import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
def filter_price(value):
    if value.isdigit():
        return value
class Product(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags),
        		output_processor=Join())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, 				filter_price),output_processor=TakeFirst())
>>> from scrapy.loader import ItemLoader
>>> il = ItemLoader(item=Product())
>>> il.add_value('name', [u'Welcome to my', u'<strong>website</strong>'])
>>> il.add_value('price', [u'&euro;', u'<span>1000</span>'])
>>> il.load_item()
{'name': u'Welcome to my website', 'price': u'1000'}
_____________________________________________________
 - Thức tự ưu tiên cho cả  in/output processor : 
#1. Ưu tiên nhất : field_in và field_out (được chỉ định trong class)
#2. Field metadata :(input_processor và output_processor)
#3. Mặc định Item Loader : default_input_processor() và default_output_processor()

5. Item Loader Context-----------------------------------------------
 - Item Loader Context là 1 dict key/values tùy ý được share giữa tất cả  các processor input và output trong Item Loader. Nó có thể được truyền khi khai báo, khởi tạo hoặc sử dụng Item Loader. Chúng được sử dụng để modify hành vi của processors input/output.
 - Vd, bạn có hàm 'parse_length()' nhận 1 giá trị text và đưa ra độ dài của nó :
def parse_length(text, loader_context):
    unit = loader_context.get('unit', 'm')
    # ... length parsing code goes here ...
    return parsed_length
==> sửa đơn vị thành 'm'(mét)
 - Bằng việc nhận argument 'loader_context', hàm này nói cho Item Loader là nó có thể nhận 1 Loader context, vì vậy Item Loader truyền context active hiện tại khi gọi nó, và hàm processor(trong trường hợp này là parse_length) có thể sử dụng.
 - Dưới đây là 1 số con đường modify giá trị Item Loader context :
#1 Modify context active hiện tại(thuộc tính context)
loader = ItemLoader(product)
loader.context['unit'] = 'cm'
#2 Khi khởi tạo Loader 
loader = ItemLoader(product, unit='cm')
#3 Khi khai báo Item Loader, 
class ProductLoader(ItemLoader):
    length_out = MapCompose(parse_length, unit='cm')

6. ItemLoader objects------------------------------------------------
|class scrapy.loader.ItemLoader([item, selector, response, ]**kwargs)
________________________________________________________________
________________________________________________________________
________________________________________________________________
 - Trả về 1 new Item Loader để nạp Item. Nếu ko có Item cho trước, nó tự động khởi tạo sử dụng class trong 'default_item_class'.
 - Khi được khởi tạo với parameter là 1 selector hoặc 1 response, ItemLoader cung cấp cơ chế thuận tiện để trích xuất dữ liệu từ các website mà chúng sử dụng selectors.
'Parameters':	
	|item (Item object) – The item instance to populate using subsequent calls to add_xpath(), add_css(), or add_value().
	|selector (Selector object) – The selector to extract data from, when using the add_xpath() (resp. add_css()) or replace_xpath() (resp. replace_css()) method.
	|response (Response object) – The response used to construct the selector using the default_selector_class, unless the selector argument is given, in which case this argument is ignored.
 - Item, selector, response và các argument chính còn lại được gán cho Loader context (có thể truy nhập qua thuộc tính 'context')
 - Instance của Itemloader có các phương thức sau :
__________________________________________________________
'get_value(value, *processors, **kwargs)'
 - Xử lý 'value' cho trước bằng 'processors' và các argument chính
 - Vd : 
>>> from scrapy.loader.processors import TakeFirst
>>> loader.get_value(u'name: foo', TakeFirst(), unicode.upper, re='name: (.+)')
>>> Ra :'FOO`
__________________________________________________________
'add_value(field_name, value, *processors, **kwargs)'
 - Xử lý và sau đó thêm 'value' đã cho vào trường field_name.
 - Đầu tiên, value được truyền vào hàm 'get_value()' bởi processors và kwargs, sau đó truyền vào processor input của field_name, và kết quả được thêm vào dữ liệu đã thu thập trước đó cho field_name. Nếu field_name đã chứa dữ liệu đc thu thập, dữ liệu mới sẽ được thêm vào.
 - Trong trường hợp field_name = None, các giá trị cho các field có thể được đưa vào, và giá trị được xử lý phải là 1 dictinary mà các field đưa vào map tới các giá trị đó.
 - Vd :
loader.add_value(None, {'name': u'foo', 'sex': u'male'})
loader.add_value('name', u'Color TV')
loader.add_value('colours', [u'white', u'blue'])
loader.add_value('length', u'100')
loader.add_value('name', u'name: foo', TakeFirst(), re='name: (.+)')
__________________________________________________________
'replace_value(field_name, value, *processors, **kwargs)'
 - Tương tự add_value, nhưng nó thay thế giá trị cũ với giá trị mới.
__________________________________________________________
'get_xpath(xpath, *processors, **kwargs)'
 - Tương tự như get_value, nó nhận 1 biểu thức Xpath thay cho 1 giá trị, Biểu thức Xpath này dùng để trích xuất ra 1 list các chuỗi unicode 
 - Vd:
# HTML snippet: <p class="product-name">Color TV</p>
loader.get_xpath('//p[@class="product-name"]')
# HTML snippet: <p id="price">the price is $1200</p>
loader.get_xpath('//p[@id="price"]', TakeFirst(), re='the price is (.*)')
__________________________________________________________
'add_xpath(field_name, xpath, *processors, **kwargs)'
 - Giống add_value, nó nhận 1 biểu thức Xpath thay cho 1 giá trị, Biểu thức Xpath này dùng để trích xuất ra 1 list các chuỗi unicode
 - Vd:
# HTML snippet: <p class="product-name">Color TV</p>
loader.add_xpath('name', '//p[@class="product-name"]')
# HTML snippet: <p id="price">the price is $1200</p>
loader.add_xpath('price', '//p[@id="price"]', re='the price is (.*)')
__________________________________________________________
'replace_xpath(field_name, xpath, *processors, **kwargs)'
 - Giống add_xpath(), nó thay thế dữ liệu cũ thay vì thêm dữ liệu mới vào nó.
__________________________________________________________
'get_css(css, *processors, **kwargs)'
 - Tương tự get_xpath, nó thay thế biểu thức xpath bằng Css selector, và cũng trích xuất ra 1 list các chuỗi unicode
 - Vd : 
# HTML snippet: <p class="product-name">Color TV</p>
loader.get_css('p.product-name')
# HTML snippet: <p id="price">the price is $1200</p>
loader.get_css('p#price', TakeFirst(), re='the price is (.*)')
__________________________________________________________
'add_css(field_name, css, *processors, **kwargs)'
- Giống add_value, nó nhận 1 biểu thức Xpath thay cho 1 giá trị, Biểu thức Xpath này dùng để trích xuất ra 1 list các chuỗi unicode
 - Vd:
# HTML snippet: <p class="product-name">Color TV</p>
loader.add_css('name', 'p.product-name')
# HTML snippet: <p id="price">the price is $1200</p>
loader.add_css('price', 'p#price', re='the price is (.*)')
__________________________________________________________
'replace_css(field_name, css, *processors, **kwargs)'
- Giống add_css(), nó thay thế dữ liệu cũ thay vì thêm dữ liệu mới tới nó.
__________________________________________________________
'load_item()'
 - Nạp item với dữ liệu đã thu thập được và return item thực sự. Dữ liệu được thu thập lần đầu tiên được truyền qua ouput processors để nhận được giá trị cuối cùng để gán cho mỗi field item.
__________________________________________________________
'nested_xpath(xpath)'
 - Tạo Loader lồng nhau với 1 selector xpath. Selector được cung cấp sẽ được áp dụng liến quan tới selector associated với ItemLoader này. Nested loader chia sẻ Item với cha nó là ItemLoader để các lời gọi |add_xpath(), add_value(), replace_value()| hoạt động như mong đợi.
__________________________________________________________
'nested_xpath(xpath)'
 - Tạo Loader lồng nhau với 1 css selector. Selector được cung cấp sẽ được áp dụng liến quan tới selector associated với ItemLoader này. Nested loader chia sẻ Item với cha nó là ItemLoader để các lời gọi |add_xpath(), add_value(), replace_value()| hoạt động như mong đợi
__________________________________________________________
'get_collected_values(field_name)'
 - Trả về các giá trị đã thu thập được của 1 field.
__________________________________________________________
'get_output_value(field_name)'
 - Trả về các giá trị được thu thập đã phân tích cú pháp bằng các sử dụng output processor với trườnng field_name. Phương thức này không nạp hay modify mọi thứ của item(nó ko lm gì cả)
__________________________________________________________
'get_input_processor(field_name)'
 - Trả  về input processor của trường field_name
__________________________________________________________
'get_output_processor(field_name)'
 - Trả  về output processor của trường field_name
__________________________________________________________
__________________________________________________________
Instance ItemLoader có các thuộc tính sau :
__________________________________________________________
'item'
 - Đối tượng Item được parsed bởi Item Loader
__________________________________________________________
'context'
 - Context active hiện tại của Item Loader
__________________________________________________________
'default_item_class'
 - Một class Item (hoặc factory), được sử dụng để khởi tạo các item khi không được đưa vào constructor.
__________________________________________________________
'default_input_processor'
 - input processor mặc định để dùng cho các trường không chỉ định input processor.
__________________________________________________________
'default_output_processor'
- out processor mặc định để dùng cho các trường không chỉ định out processor.
__________________________________________________________
'default_selector_class'
 - Class được dùng để construct selector của ItemLoader nếu chỉ có 1 response được cho trước trong constructor. Nếu 1 selector được cho trước trong constructor, thuộc tính này bị bỏ qua. Thuộc tính này đôi khi bị overriden trong các class con.
__________________________________________________________
'selector'
 - Đối tượn Selector dùng để trích xuất dữ liệu từ nó. Nó hoặc được cho trước trong constructor, hoặc được tạo ra từ response cho trước trong constructor mà sử dụng 'default_selector_class'.
 - Thuộc tính này có nghĩa là read-only (chỉ đọc)

7. Nested Loaders----------------------------------------------------
 - Khi parsed các giá trị liên quan từ 1 phần documnet, nó có thể hữu ích để tạo các loader lồng. Hãy tưởng tượng bạn đang trích xuất chi tiết từ 1 footer của 1 trang web giống như sau :
<footer>
<a class="social" href="https://facebook.com/whatever">Like Us</a>
<a class="social" href="https://twitter.com/whatever">Follow Us</a>
<a class="email" href="mailto:whatever@example.com">Email Us</a>
</footer>
 - Nếu ko dùng loader lồng, bạn cần chỉ rõ full xpath hoặc full css dành cho mỗi value bạn muốn trích xuất. Như :
__________________________________________________________
loader = ItemLoader(item=Item())
# load stuff not in the footer
loader.add_xpath('social', '//footer/a[@class = "social"]/@href')
loader.add_xpath('email', '//footer/a[@class = "email"]/@href')
loader.load_item()
__________________________________________________________
 - Thay vào đó, bạn có thể tạo 1 loader lồng với selector footer và add các giá trị có liên quan tới footer. Tránh lặp lại footer selector. Vd :
__________________________________________________________
loader = ItemLoader(item=Item())
# load stuff not in the footer
footer_loader = loader.nested_xpath('//footer')
footer_loader.add_xpath('social', 'a[@class = "social"]/@href')
footer_loader.add_xpath('email', 'a[@class = "email"]/@href')
# no need to call footer_loader.load_item()
loader.load_item()
__________________________________________________________
 - Bạn có thể lồng các loader 1 cách tùy ý, hoặc với xpath, hoặc với css. Hãy sử dụng các nested loader khi chúng làm cho code bạn đơn giản hơn nhưng đừng quá đà với lồng và parser của bạn có thể trở nên khó đọc.

8. Reusing and extending Item Loaders--------------------------------
 - Khi project của bạn to ra và thu thập nhiều nhiều spider hơn, bảo trì trở thành một vấn đề cơ bản, đặc biệt khi bạn phải đối phó với nhiều luật parsing cho mỗi spider, có rất nhiều exception (ngoại lệ), nhưng cũng muốn tái sử dụng các processor phổ biến.
 - Item Loader được thiết kế để giảm bớt gánh nặng bảo trì các luật parsing, mà không mất tính linh hoạt, đồng thời cung cấp 1 cơ chế thuận tiện cho việc kế thừa và ghi đè chúng. Nguyên nhân là ItemLoader hỗ trợ kế thừa class Python truyền thống để ứng phó với sự khác biệt của các spider cụ thể.(hoặc 1 nhóm spider)
 - Giả sử , 1 số website bao gồm tên product trong 3 dấu gạch ngang (---Plasma TV---) và bạn không muốn kết thúc scraping với các dấu gạch ngang đó có trong tên sản phẩm.
 - Dưới đây là cách bạn có thể xóa các dấu gạch ngang bằng cách tái sử dụng và extending Product Item Loader (ProductLoader) mặc định:
__________________________________________________________
from scrapy.loader.processors import MapCompose
from myproject.ItemLoaders import ProductLoader
def strip_dashes(x):
    return x.strip('-')
class SiteSpecificLoader(ProductLoader):
    name_in = MapCompose(strip_dashes, ProductLoader.name_in)
__________________________________________________________
 - 1 trường hợp extend ItemLoader có thể rất hữu ích là khi bạn có nhiều định dạng(format) của mã nguồn(source), như XML, HTML. Trong phiên bản XML, bạn có thể muốn loại bỏ sự xuất hiện 'CDATA'. Vd :
__________________________________________________________
from scrapy.loader.processors import MapCompose
from myproject.ItemLoaders import ProductLoader
from myproject.utils.xml import remove_cdata
class XmlProductLoader(ProductLoader):
    name_in = MapCompose(remove_cdata, ProductLoader.name_in)
__________________________________________________________
 - Có nhiều con đường khác để extend, inherrit và override ItemLoader của bạn, và các cấu trúc thứ bậc ItemLoader khác nhau có thể phù hợp hơn với các project khác nhau. Scrapy chỉ cung cấp cơ chế, nó không áp đặt bất kỳ cách tổ chức cụ thể nào trong bộ sưu tập Loaders của bạn. Điều đó là tùy thuộc vào bạn, nhu cầu của bạn.

9. Available built-in processors-------------------------------------
 - Scrapy cung cấp 1 số processor phổ biến được miêu tả dưới đây:
__________________________________________________________
'class scrapy.loader.processors.Identity'
 - Là processor đơn giản nhất, nó không làm bất cứ thứ gì. Nó trả về gía trị bạn đầu không thay đổi. Nó ko nhận bất kì argument constructor, cũng ko chấp nhận Loader context.
 - Vd :
>>> from scrapy.loader.processors import Identity
>>> proc = Identity()
>>> proc(['one', 'two', 'three'])
['one', 'two', 'three']
__________________________________________________________
'class scrapy.loader.processors.TakeFirst'
 - Trả về giá trị ko phải là null/ ko phải empty từ các giá trị nhận được, vì vậy nó thường được sử dụng như 1 output processor cho các field có giá trị duy nhất. Nó ko nhận bất kì argument constructor, cũng ko chấp nhận Loader context.
 - Vd :
>>> from scrapy.loader.processors import TakeFirst
>>> proc = TakeFirst()
>>> proc(['', 'one', 'two', 'three'])
'one'
__________________________________________________________
'class scrapy.loader.processors.Join(separator=u' ')'
 - Trả về giá trị đã join (kết nối) với separator cho trước trong constructor, mặc định u''. Nó ko chấp nhận Loader context
 - Vd : 
>>> from scrapy.loader.processors import Join
>>> proc = Join()
>>> proc(['one', 'two', 'three'])
u'one two three'
>>> proc = Join('<br>')
>>> proc(['one', 'two', 'three'])
u'one<br>two<br>three'
__________________________________________________________
'class scrapy.loader.processors.Compose(*functions, **default_loader_context)'
 - Là 1 processor được construted từ thành phần của 1 hàm cho trước.
Điều này nghĩa là mỗi đầu vào input của processor được truyền đến hàm đầu tiên, và kết quả của hàm đó được truyền đến hàm thứ 2, và cứ như thế đến khi hàm cuối cùng trả về giá trị output của processor này.
 - Mặc định, dừng tiến trình trên bằng giá trị 'None'. Hành vi này có thể được thay đổi bằng cách truyền đối số với keyword stop_on_none=False.
 - Mỗi hàm có thể nhận 1 parameter loader_context. Processor này sẽ truyền Loader context active hiện tại qua parameter.
 - Các keyword arguments truyền trong constructor được sử dụng như các giá trị mặc định của Loader context được truyền cho mỗi lời gọi hàm. Tuy nhiên, các giá trị Loader context cuối cùng chuyển đến các hàm được ghi đè bằng Loader context hiện đang hoạt động có thể truy cập thông qua thuộc tính ItemLoader.context ().
 - Vd :
>>> from scrapy.loader.processors import Compose
>>> proc = Compose(lambda v: v[0], str.upper)
>>> proc(['hello', 'world'])
'HELLO'
__________________________________________________________
'class scrapy.loader.processors.MapCompose(*functions, **default_loader_context)'
 - Processor được constructed (xây dựng) từ thành phần của các hàm cho trước, giống như processor Compose. Sự khác biệt của processor này là các kết quả nội bộ được truyền qua các hàm như sau :
	+ Giá trị input của processor này được lặp lại và hàm đầu tiên được áp dụng cho mỗi phần tử(element). Kết quả của các lời gọi hàm này (một cho mỗi phần tử) được ghép vào để (constructed) xây dựng một iterable mới, sau đó sử dụng để áp dụng hàm thứ hai,vv, cho đến khi hàm cuối cùng được áp dụng cho mỗi giá trị của list các giá trị được thu thập trước đó. Các giá trị output của hàm cuối cùng được kết nối với nhau để tạo ra output của processor này.
	+ Mỗi hàm cụ thể trả về 1 giá trị hoặc 1 list các giá trị. Các hàm cũng có thể trả về 'None' trong trường hợp này, output của hàm đó sẽ bị loại bỏ để tiếp tục xử lý chuỗi.
	+ Processor này cung cấp 1 cách thuận tiện để biên soạn các hàm chỉ làm việc với giá trị đơn(thay vì là các iterable). Vì lý do này processor MapCompose thường được sử dụng làm input processor, vì dữ liệu thường được trích xuất bằng cách sử dụng phương thức extract() của selectors, nó trả về một danh sách các chuỗi unicode.
 - Vd : 
>>> def filter_world(x):
...     return None if x == 'world' else x
...
>>> from scrapy.loader.processors import MapCompose
>>> proc = MapCompose(filter_world, unicode.upper)
>>> proc([u'hello', u'world', u'this', u'is', u'scrapy'])
[u'HELLO, u'THIS', u'IS', u'SCRAPY']
__________________________________________________________
'class scrapy.loader.processors.SelectJmes(json_path)'
 - Truy vấn value sử dụng đường dẫn json, được cung cấp tới constructor và trả về output. Yêu cầu jmespath (https://github.com/jmespath/jmespath.py) để chạy. Processor này mỗi lần chỉ nhận 1 input
 - Vd :
>>> from scrapy.loader.processors import SelectJmes, Compose, MapCompose
>>> proc = SelectJmes("foo") #for direct use on lists and dictionaries
>>> proc({'foo': 'bar'})
'bar'
>>> proc({'foo': {'bar': 'baz'}})
{'bar': 'baz'}
__
 - Làm việc với Json :
>>> import json
>>> proc_single_json_str = Compose(json.loads, SelectJmes("foo"))
>>> proc_single_json_str('{"foo": "bar"}')
u'bar'
>>> proc_json_list = Compose(json.loads, MapCompose(SelectJmes('foo')))
>>> proc_json_list('[{"foo":"bar"}, {"baz":"tar"}]')
[u'bar']
