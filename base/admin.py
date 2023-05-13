from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Product) # register the Product model with the admin site
admin.site.register(Review) # register the Review model with the admin site
admin.site.register(Order) # register the Order model with the admin site
admin.site.register(OrderItem) # register the OrderItem model with the admin site
admin.site.register(ShippingAddress) # register the ShippingAddress model with the admin site
