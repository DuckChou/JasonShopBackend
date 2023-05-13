from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product, Order, OrderItem, ShippingAddress, Review



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # serialize the Product model
        model = Product
        # fields = '__all__' # return all fields
        fields = '__all__'

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        # serialize the Shipping Address model
        model = ShippingAddress
        # fields = '__all__' # return all fields
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        # serialize the OrderItem model
        model = OrderItem
        # fields = '__all__' # return all fields
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        # fields = '__all__' # return all fields
        fields = '__all__'
    
    def get_orders(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data
    
    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data
        except:
            address = False
        return address
    
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    #Serializer 类中的 Meta 类是用于配置序列化器行为的元类。
    #通过在 Meta 类中定义一些属性，我们可以控制序列化器的一些行为，例如模型类、字段、验证等等。   
    # Meta 类，用于配置序列化器的一些行为，例如使用哪个模型类、序列化哪些字段等等 
    class Meta:
        # serialize the User model

        model = User
        # fields = '__all__' # return all fields
        fields = ['id', 'username', 'email', 'name', '_id', 'isAdmin']


    # 此外，这个序列化器还包含了三个自定义的方法 get__id()、get_isAdmin() 和 get_name()
    # 用于将 User 模型实例的字段进行自定义序列化处理
    def get__id(self, obj):
        return obj.id
    
    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name
    


class UserSerializerWithToken(UserSerializer):
    # 当我们需要返回的序列化数据不是 model 里面的全部字段时，
    # 我们需要将需要的额外字段在 Serializer 中进行定义，以便在序列化时能够包含这些额外信息。
    # 例如，我们需要在用户登录成功后返回用户的 token 信息，那么我们就需要在 UserSerializer 中定义一个 token 字段。
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', '_id', 'isAdmin', 'token']

    # 该方法定义token具体应该怎么生成
    # obj 是当前序列化的模型实例，也就是 User 模型的实例
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
