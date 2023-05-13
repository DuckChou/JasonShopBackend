from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Product Model
# 当你在 Django 中定义了一个模型之后，Django 并不会立即将这个模型同步到数据库中。
# 相反，Django 会将这个模型的定义存储在数据库的迁移记录中，并在你运行 migrate 命令时，根据这些迁移记录来同步数据库


class Product(models.Model):

    # a user can have many products, but a product can only have one user
    # User：指向的模型。在这个例子中，我们指向了 User 模型，这个模型是 Django 自带的用户认证系统提供的模型。
    # on_delete=models.SET_NULL：指定在引用的对象被删除时的行为。在这个例子中，我们设置为当 User 对象被删除时将其设为 NULL。
    # null=True：指定该字段是否允许为空。在这个例子中，我们允许 user 字段为空。
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # CharField 字符串字段，用于保存较短的字符串，比如标题、姓名、邮件地址等。
    # null-true 和 blank=true 的区别：
    # null 是数据库范畴的概念，如果 null=True, 表示数据库的该字段可以为空。
    # blank 是表单验证范畴的，如果 blank=True，表示你的表单填写该字段的时候可以不填，但是对应数据库的该字段如果没有设置null=True的话，就会报数据库错误。
    name = models.CharField(max_length=200, null=True, blank=True)

    image = models.ImageField(null=True, blank=True, default='/placeholder.png')

    brand = models.CharField(max_length=200, null=True, blank=True)

    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)

    # auto_now=True sets the date to the current date and time every time the object is saved
    # auto_now_add=True sets the date to the current date and time when the object is first created
    createdAt = models.DateTimeField(auto_now_add=True)

    # editable=False prevents the field from being displayed in any ModelForm
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):

        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)

    # autofield is an integer field that automatically increments according to available IDs
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)


class Order(models.Model):
    # an user can have many orders, but a order can only have one user
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    # auto_now_add=True sets the date to the current date and time when the object is first created
    createdAt = models.DateTimeField(auto_now_add=True)

    _id = models.AutoField(primary_key=True, editable=False)


class OrderItem(models.Model):
    # an order can have many order items, but a order item can only have one order
    # on_delete=models.SET_NULL：指定在引用的对象被删除时的行为。在这个例子中，我们设置为当 Order 对象被删除时将其设为 NULL。
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    # a product can have many order items, but a order item can only have one product
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200, null=True, blank=True)

    image = models.CharField(max_length=200, null=True, blank=True)

    qty = models.IntegerField(null=True, blank=True, default=0)

    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)

    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
    

class ShippingAddress(models.Model):
    # on_delete=models.CASCADE means that when the referenced object is deleted, all objects that have a foreign key pointing to it will also be deleted. This is known as a "cascade delete".
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)

    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)
