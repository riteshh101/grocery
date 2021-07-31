from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.

@admin.register(user_register)
class UserRegisterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in user_register._meta.fields]

@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in category._meta.fields]

@admin.register(Wishlist)
class WhislistAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Wishlist._meta.fields]

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in product._meta.fields]

@admin.register(slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in slider._meta.fields]

@admin.register(cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in cart._meta.fields]

@admin.register(delivery_address)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in delivery_address._meta.fields]


@admin.register(order_detail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id','user','address','product','aaddress','click_me']
    def click_me(self,obj):
        return format_html(f'<button><a href="http://127.0.0.1:8000/admin/app/order_detail/{obj.id}/change/" class="default">View</a></button>')
    def address(self,obj):
        return obj.delivery_address.address,obj.delivery_address.mobile,obj.delivery_address.city,obj.delivery_address.country,obj.delivery_address.email,obj.delivery_address.state
    def product(self,obj):
        return "\n".join([p.product.title for p in obj.item.all()])

    def aaddress(self,obj):
        return format_html(f'<a href="http://127.0.0.1:8000/admin/app/delivery_address/{obj.delivery_address.id}/change/">{obj.delivery_address}</a>')
@admin.register(contact_detail)
class ContactAdminPage(admin.ModelAdmin):
    list_display = [field.name for field in contact_detail._meta.fields]
