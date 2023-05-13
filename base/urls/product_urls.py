from django.urls import path
from base.views import products_views as views





urlpatterns = [

    path('', views.getProducts, name="products"),
    path('<str:pk>/', views.getProduct, name="product"),
    path('<str:pk>/delete', views.deleteProduct, name="product-delete"),
    path('create', views.createProduct, name="product-create"),
    path('<str:pk>/update', views.updateProduct, name="product-update"),
    path('upload', views.uploadImage, name='image-upload'),
    path('addProduct', views.addProduct, name='add-product')
]