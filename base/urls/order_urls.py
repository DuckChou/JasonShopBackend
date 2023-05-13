from django.urls import path
from base.views import order_views as views

urlpatterns = [
    path('addOrder', views.addOrderItems, name="addOrder"),
    path("<str:pk>",views.getOrderById, name="get_order_by_id"),
    path("<str:pk>/pay",views.updateOrderToPaid, name="update_order_to_paid"),
    path("",views.getMyOrders, name="get_my_orders"),
    path("allOrders/",views.getOrders, name="get_orders"),
    path("<str:pk>/deliver",views.updateOrderToDelivered, name="update_order_to_delivered"),
]