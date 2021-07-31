from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def cart_count_show(request):
    if request.user.is_authenticated:
        cart_count = cart.objects.filter(user=request.user)
        cartt = cart_count.count()

        return {'cart_count':cartt}
    else:
        cart_count = cart.objects.all()
        return {'cart_count': cart_count}

class slider(models.Model):
    slid = models.ImageField(upload_to="Slider")
    create_date = models.DateTimeField(auto_now_add=True)


class user_register(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

class category(models.Model):
    name = models.CharField(max_length=100)
    created_date= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class product(models.Model):
    category= models.ForeignKey(category,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    price = models.FloatField()
    quantity = models.CharField(max_length=300,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    pic1 = models.ImageField(upload_to="product",null=True)
    def __str__(self):
        return self.title



class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    date_time =models.DateTimeField(auto_now_add=True,null=True)

class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)


class delivery_address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.TextField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    mobile = models.PositiveIntegerField(null=True)
    def __int__(self):
        return self.pk

class order_detail(models.Model):
    order_stat = (
        ('Deliver', 'Deliver'),
        ('Booked', 'Booked'),
        ('Cancel', 'Cancel'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ManyToManyField(cart)
    payment_mode = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=200)
    order_id = models.CharField(max_length=200)
    signature = models.CharField(max_length=200)
    order_status = models.CharField(default='Booked', choices=order_stat, max_length=100)
    delivery_status = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)
    delivery_address = models.ForeignKey(delivery_address, on_delete=models.CASCADE, null=True)
    price = models.FloatField()



class contact_detail(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


