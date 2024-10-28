from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(usersignup)
admin.site.register(products)
admin.site.register(mycart)
admin.site.register(order)
admin.site.register(orderitem)
admin.site.register(profile)

