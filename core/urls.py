"""
URL configuration for E-commerce site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from app1 import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.index,name='index'),

    path('log',views.log,name='log'),
    path('allp',views.allp,name='allp'),
    path('con',views.con,name='con'),
    path('che',views.che,name='che'),
    
    path('my',views.my,name='my'),
    path('lis',views.lis,name='lis'),
    path('wis',views.wis,name='wis'),
    path('reg',views.reg,name='reg'),
    path('base',views.base,name='base'),
    path('single',views.single,name='single'),
    path('search',views.searchfn,name='search'),
    path('logout',views.logout,name='logout'),
    path('checkout',views.che,name='checkout'),
    path('place-order', views.placeorder, name='placeorder'),
    path('proceed-to-pay', views.razorpaycheck, name='proceed-to-pay'),
    path('myorder', views.orderss, name='myorder'),
    

#...........CART ITEMS...................#
    path('car',views.car,name='car'),
    path('addcart/<wal>',views.addcart,name='addcart'),
    path('deletecart/<de>',views.deletecart,name='deletecart'),
    path('minuscart/<de>',views.minuscart,name='minuscart'),
    path('pluscart/<de>',views.pluscart,name='pluscart'),

#..........SEARCH ITEMS..................#
    

#...........CATOGARIES....................#
    path('mens',views.MENS,name='mens'),
    path('womens',views.womens,name='womens'),
    path('kids',views.kids,name='kids'),
    path('sports',views.sports,name='sports'),
    path('babies',views.babies,name='babies'),

#............ADMIN PAGE...................#
    path('adminindex',views.adminindex,name='adminindex'),
    path('adminpro',views.adminpro,name='adminpro'),
    path('adminbase',views.adminbase,name='adminbase'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('editproduct/<wal>',views.editproduct,name='editproduct'),
    path('editproduct/editproduct/<wal>',views.editproduct2,name='editproduct2'),
    path('deleteproduct/<wal>',views.deleteproduct,name='deleteproduct'),
    path('users',views.users,name='users'),
    path('userbooking',views.userbooking,name='userbooking'),


    path('forgot',views.forgot,name='forgot'),
    path('reset/<token>',views.reset_password,name='reset'),
    path('reset/reset2/<token>',views.reset_password,name='reset2')


]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
