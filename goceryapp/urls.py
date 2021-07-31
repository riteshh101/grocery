"""goceryapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('prod_list<str:name>/',views.product_all,name='product_all'),
    path('product_view<int:id>/',views.product_view,name='product_view'),
    path('login/',views.login_user,name='login_user'),
    path('register/',views.register,name='register'),
    path('logout_user/',views.logout_user,name='logout'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('wishlist_add<int:id>/',views.wishlist_addd,name='whishlist_add'),
    path('whish_remove<int:id>/',views.whish_remove,name='whish_remove'),
    path('cart_page/',views.cart_page,name='cart_page'),
    path('cart_add<int:id>/',views.cart_add,name='cart_add'),
    path('cart_remove<int:id>/',views.cart_remove,name='cart_remove'),
    path('cart_plus<int:id>/',views.cart_plus,name='cart_plus'),
    path('cart_minus<int:id>/',views.cart_minus,name='cart_minus'),
    path('checkout/',views.checkoutt,name='checkout'),
    path('payment_success/',views.payment_success,name='payment_success'),
    path('success/',views.suucess,name='success'),
    path('contact/',views.contact_page,name='contact_page'),
    path('user_account/',views.user_account,name = 'user_account'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
