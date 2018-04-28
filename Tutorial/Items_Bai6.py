 - Mục tiêu scraping : Trích xuất ra dữ liệu có cấu trúc từ nguồn dữ liệu không cấu trúc, điển hình là các website. Spiders Scrapy có thể trả về dữ liệu có cấu trúc như các dictionary Python. Mà cac dict Python có cấu trúc nghèo nàn ( ko đa dangj), nó có thể dễ dàng tạo 1 lỗi đánh máy cho 1 tên field hoặc trả về dữ liệu không phù hợp, đặc biệt trong 1 project lớn hơn với nhiều spiders.
 - Để định nghĩa format dữ liệu đầu ra chung, Scrapy use Item class. Object Item đơn giản là 1 container sưu tập dữ liệu đã scraped. Chúng có cú pháp thuận tiện để định nghĩa các filed có sẵn của nó. 
 - Các thành phần khác của Scarpy sử dụng thông tin thêm được cung cấp bởi Items như : exporter nhìn vào các filed được định nghĩa để tìm ra các collumn để export, serialization có thể tùy chỉnh sử dụng Item fields metadata, Các instances 'trackref' giúp tìm ra memory leaks.

1. Declaring Items-----------------------------------------
 - Item được định nghĩa sử dụng cú pháp class đơn giản. Ở đây các đối tượng Field :
_________________________________
import scrapy
class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
_________________________________
 - Những ai quen với Django sẽ thấy Scrapy Items được định nghĩa tương tự như Django Models, nhưng Scrapy Items đơn giản hơn vì chúng không có các concept về các kiểu field khác nhau

2. Items Fields-----------------------------------------
 - Các đối tượng Field dược dùng để chỉ định metadata cho mỗi trường. Ví dụ, hàm serializer dành cho trường 'last_updated' minh họa cho ví dụ trên.
 - Bạn có thể chỉ định metadata bất kì cho mỗi trường. Không có giới hạn về các giá trị được chấp nhận bởi các 'Field' Object. Vì lý do này, không có danh sách tham chiếu của tất cả các keys metadata có sẵn. Mỗi key được định nghĩa trong đối tượng Field có thể được sử dụng bởi 1 thành phần khác nhau, và chỉ thành phần đó biết về nó. Bạn cũng có thể định nghĩa và sử dụng bất kì 'Field' key nào khác trong project của bạn, tùy nhu cầu của riêng bạn. Mục địch chính của 'Field' objects là để cung cấp 1 con đường khai báo tất cả các field metadata trong 1 nơi. Thông thường, những thành phần có hành vi phụ thuộc vào mỗi field sử dụng các key field nhất định để cấu hình hành vi đó. Bạn phải tham khảo tài liệu của chúng để xem các key metadata nào được từng thành phần sử dụng.
 - Cần lưu ý : Field objects được dùng để định nghĩa Item không được chỉnh định như các thuộc tính của class. Thay vào đó, bạn có thể truy cập nó qua thuộc tính Item.fields

3. Working with Items-----------------------------------------
 - Đây là 1 số ví dụ về các tác vụ phổ biến được thực hiện với các Item, sử dụng item 'Project' đã định nghĩa ở trên. Bạn sẽ nhận thấy API rất giống với dict API
_____________________________________
'Creating item' :
>>> product = Product(name='Desktop PC', price=1000)
>>> print product
Product(name='Desktop PC', price=1000)
_____________________________________
'Getting field values' :
>>> product['name']
Desktop PC
>>> product.get('name')
Desktop PC
>>> product['price']
1000
>>> product['last_updated']
Traceback (most recent call last):
    ...
KeyError: 'last_updated'
>>> product.get('last_updated', 'not set')
not set
>>> product['lala'] # getting unknown field
Traceback (most recent call last):
    ...
KeyError: 'lala'
>>> product.get('lala', 'unknown field')
'unknown field'
>>> 'name' in product  # is name field populated?
True
>>> 'last_updated' in product  # is last_updated populated?
False
>>> 'last_updated' in product.fields  # is last_updated a declared field?
True
>>> 'lala' in product.fields  # is lala a declared field?
False
______________________________________________
'Setting field values' :
>>> product['last_updated'] = 'today'
>>> product['last_updated']
today
>>> product['lala'] = 'test' # setting unknown field
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'
_______________________________________________
'Accessing all populated values' :
>>> product.keys()
['price', 'name']
>>> product.items()
[('price', 1000), ('name', 'Desktop PC')]
_______________________________________________
'Other common tasks' : 
||Copying items:
>>> product2 = Product(product)
>>> print product2
Product(name='Desktop PC', price=1000)
>>> product3 = product2.copy()
>>> print product3
Product(name='Desktop PC', price=1000)
||Creating dicts from items:
>>> dict(product) # create a dict from all populated values
{'price': 1000, 'name': 'Desktop PC'}
||Creating items from dicts:
>>> Product({'name': 'Laptop PC', 'price': 1500})
Product(price=1500, name='Laptop PC')
>>> Product({'name': 'Laptop PC', 'lala': 1500}) # warning: unknown field in dict
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'

4. Extending Items-------------------------------------------------
 - bạn có thể extend Items ( để thêm các trường hoặc thay đổi một số metadata cho 1 số trường) bằng cách khai báo 1 subclass của Item gốc.
 - Vd:
class DiscountedProduct(Product):
    discount_percent = scrapy.Field(serializer=str)
    discount_expiration_date = scrapy.Field()
 - Bạn cũng có thể extend field metadata bằng cách sử dụng field metadata trước và thêm giá trị hoặc thay đổi giá trị đã tồn tại như sau :
class SpecificProduct(Product):
    name = scrapy.Field(Product.fields['name'], serializer=my_serializer)
 - Nó thêm (hoặc thay thế) 'serializer' metadata key cho trường 'name' và giữ nguyên các giá trị metadata đã tồn tại trước của Product

5. Items objects-------------------------------------------------
class scrapy.item.Item([arg]) :
 - Trả về 1 Item mới được khởi tạo từ đối số [arg] đã cho.
 - Các Item sao chép chuẩn 'dict API', bao gồm constructor(hàm tạo) của nó. Thuộc tính bổ sung duy nhất bởi Item là : fields
	Nó là Một dictionary chứa tất cả các trường được khai báo cho Item này. Các keys là các tên trường và các giá trị là các đối tượng 'Field' được sử dụng trong khai báo Item.

6. Field objects-------------------------------------------------
class scrapy.item.Field([arg]) :
 - Class 'Field' chỉ là 1 alias dành cho class được built trong dict và không cung cấp thêm bất kì function hay attribute nào. Nói cách khác, 'Field' object là những dicts Python cơ bản. 
 - Nó là 1 class riêng biệt được sử dụng để hỗ trợ cú pháp khai báo 'Item' dựa trên các thuộc tính của class



