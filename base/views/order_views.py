
from datetime import datetime
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth.models import User


from base.serializer import OrderSerializer, ProductSerializer, UserSerializer, UserSerializerWithToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password

from rest_framework import status

from base.models import Product, Review, Order, OrderItem, ShippingAddress


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(order):
    user = order.user
    data = order.data

    orderItems = data['orderItems']
    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status= status.HTTP_400_BAD_REQUEST)
    else:
        # (1) Create order
        order = Order.objects.create(
            user = user,
            paymentMethod = data['paymentMethod'],
            taxPrice = data['taxPrice'],
            shippingPrice = data['shippingPrice'],
            totalPrice = data['totalPrice']
        )

        # (2) Create shipping address
        shipping = ShippingAddress.objects.create(
            order = order,
            address = data['shippingAddress']['address'],
            city = data['shippingAddress']['city'],
            postalCode = data['shippingAddress']['postalCode'],
            country = data['shippingAddress']['country']
        )

        # (3) Create order items and set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id = i['_id'])

            item = OrderItem.objects.create(
                product = product,
                order = order,
                name = product.name,
                qty = i['qty'],
                price = i['price'],
                image = product.image.url
            )

            # (4) Update stock
            product.countInStock -= item.qty # type: ignore
            product.save()

        serializer = OrderSerializer(order, many=False)


    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request,pk):

    user = request.user

    # 怎么在这里加一个Order里是否有包含该pk的orderItem的判断呢？
    

    try:
        order = Order.objects.get(_id = pk)
        if not order:
            return Response({'detail': 'Order does not exist'}, status= status.HTTP_400_BAD_REQUEST)
        # Check if user is staff or if the order belongs to the user
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not authorized to view this order'}, status= status.HTTP_400_BAD_REQUEST)
    # except Order.DoesNotExist:
    #     return Response({'detail': 'Order does not exist'}, status= status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status= status.HTTP_400_BAD_REQUEST)
    


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request,pk):
    
        order = Order.objects.get(_id = pk)
        order.isPaid = True
        order.paidAt = datetime.now()
        order.save()
    
        return Response('Order was paid')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteOrder(request,pk):
    order = Order.objects.get(_id = pk)
    order.delete()
    return Response('Order was deleted')

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request,pk):
    order = Order.objects.get(_id = pk)
    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response('Order was delivered')