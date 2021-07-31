from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
import razorpay
# Create your views here.

def cart_count_show(request):
    if request.user.is_authenticated:
        cart_count = cart.objects.filter(user=request.user,status=False)
        cartt = cart_count.count()
        return {'cart_count':cartt}
    else:
        cart_count = cart.objects.all()
        return {'cart_count': cart_count}

def whish_count(request):
    if request.user.is_authenticated:
        whish_countable = Wishlist.objects.filter(user=request.user)
        whish = whish_countable.count()
        return {'whish':whish}
    else:
        whish_countable = Wishlist.objects.all()
        return {'whish':whish_countable}

def home(request):
    cat = category.objects.all()
    slid = slider.objects.all()
    l1=[]
    l2=[]
    for x in cat:
        prod = product.objects.filter(category=x)
        l1.append(prod)
        for x in prod:
            if x.category not in l2:
                l2.append(x.category)
    c= zip(l2,l1)
    return render(request,'index.html',{'category':cat,'slider':slid,"c":c})

def product_all(request,name):
    cat = category.objects.all()
    categ = category.objects.get(name=name)
    prod = product.objects.filter(category = categ)
    return render(request,'product-list.html',{'prod':prod,'cat':cat})

def product_view(request,id):
    cat = category.objects.all()
    prod = product.objects.get(id=id)
    related_prod = product.objects.filter(category = prod.category)

    return render(request,'product-detail.html',{'prod':prod,'related_prod':related_prod,'cat':cat})

def login_user(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = email,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,'Invalid User')
            return redirect('/login')
    return render(request,'login.html')

def register(request):
    if request.method=="POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pswrd = request.POST.get('pswrd')
        repswrd = request.POST.get('repswrd')
        mobile = request.POST.get('mobile')
        try:
            check_user = User.objects.get(username = email)
            messages.error(request,'Email already exists try another email')
            return redirect('/login')
        except:
            if pswrd == repswrd:
                obj = User(username = email,first_name=fname,last_name=lname,password = make_password(pswrd))
                obj.save()
                obb = user_register(user=obj,mobile=mobile)
                obb.save()
                messages.success(request,'Account created successfully')
                return redirect('/login')
            else:
                messages.error(request,'Password and Re-Password not correct')
                return redirect('/login')

def logout_user(request):
    logout(request)
    return redirect('/login')

def wishlist(request):
    if request.user.is_authenticated:
        user_instance = User.objects.get(username = request.user.username)
        whishlist_featch = Wishlist.objects.filter(user = user_instance)
        return render(request,'wishlist.html',{'whishlist':whishlist_featch})
    else:
        return redirect('/login')

def wishlist_addd(request,id):
    if request.user.is_authenticated:

        prod = product.objects.get(id=id)
        user_inst = User.objects.get(username=request.user.username)
        try:
            wh = Wishlist.objects.get(user=user_inst,product = prod)
            messages.info(request,'Product Already Add')
            return redirect('/wishlist')
        except:
            print('run ye hua')
            whish = Wishlist(user=user_inst,product=prod)
            whish.save()
            messages.success(request, 'Product add successfully')
            return redirect('/wishlist')

    else:
        return redirect('/login')

def whish_remove(request,id):
    whish = Wishlist.objects.get(id=id)
    whish.delete()
    return redirect('/wishlist')

##############################################all function here cart realated#######################################################
#cart Update
# main cart.html page
def cart_page(request):
    if request.user.is_authenticated:
        user_inst = User.objects.get(username=request.user)
        cart_featch = cart.objects.filter(user = user_inst,status=False)
        sub_total = 0
        for x in cart_featch:
            sub_total = x.total_price + sub_total
        grand_total = sub_total + 1
        return render(request,'cart.html',{'cart':cart_featch,"sub_total":sub_total,"grand_total":grand_total})

def cart_remove(request,id):
    if request.user.is_authenticated:
        ct =cart.objects.get(pk=id)
        ct.delete()
        return redirect('/cart_page')
def cart_plus(request,id):
    if request.user.is_authenticated:
        carts = cart.objects.get(id=id)
        carts.quantity = carts.quantity+1
        carts.total_price = carts.quantity * carts.product.price
        carts.save()
        return redirect('/cart_page')

def cart_minus(request,id):
    if request.user.is_authenticated:
        carts = cart.objects.get(id=id)
        if  carts.quantity != 1:
            carts.quantity = carts.quantity - 1
            carts.total_price = carts.quantity * carts.product.price
            carts.save()
            return redirect('/cart_page')
        else:
            cart_remove(request,id)
            return redirect('/cart_page')

def cart_add(request,id):
    if request.user.is_authenticated:
        prod = product.objects.get(id=id)
        user_inst = User.objects.get(username=request.user)
        try:
            ct_featch = cart.objects.filter(user=user_inst).get(product=prod)
            messages.info(request,'Product already add in cart please increase quantity')
            return redirect('/cart_page')
        except:
            quanti=1
            tot_price = quanti * prod.price
            ct_add = cart(user=user_inst,product=prod,quantity=quanti,total_price=tot_price)
            ct_add.save()
            return redirect('/cart_page')
    else:
        return redirect('/login')

def checkoutt(request):
    if request.user.is_authenticated:
        user_inst = User.objects.get(username=request.user)
        cart_featch = cart.objects.filter(user=user_inst,status=False)
        sub_total = 0
        for x in cart_featch:
            sub_total = x.total_price + sub_total
        grand_total = sub_total + 1

        if request.method=="POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            mobile = request.POST['mobile']
            address = request.POST['address']
            city = request.POST['city']
            country = request.POST['country']
            zipcode = request.POST['zipcode']
            state = request.POST['state']

            user_inst = User.objects.get(username=request.user)
            adrs = delivery_address(user=user_inst, first_name=fname, last_name=lname, email=email, address=address,
                                    country=country, state=state, city=city, zip_code=zipcode, mobile=mobile)
            adrs.save()
            print(adrs.id)
            grand = int(grand_total * 100)
            client = razorpay.Client(auth=("rzp_test_XfqDl5oZQ0Rq4L", "gkCglJwlNEDmZcOTybIGmEl2"))
            order = client.order.create({'amount': grand, 'currency': 'INR', 'payment_capture': '1'})
            return render(request,'preview.html',{'adrs':adrs.id,'order':order,'cart':cart_featch,"sub_total":sub_total,"grand_total":grand_total})
        else:

            return render(request,'checkout.html',{'cart':cart_featch,"sub_total":sub_total,"grand_total":grand_total})
    else:
        return redirect('/login')

def payment_success(request):
    if request.user.is_authenticated:

        cart_featch = cart.objects.filter(user=request.user, status=False)
        pay = 0

        for x in cart_featch:
            pay = pay + x.total_price

        if request.method=="POST":
            a=request.POST
            address = request.POST.get('adrs')
            adrs_inst = delivery_address.objects.get(id=address)
            user_inst = User.objects.get(username=request.user)
            data = {}
            print(a)
            for key, val in a.items():
                if key == 'razorpay_order_id':
                    data['razorpay_order_id'] = val
                elif key == 'razorpay_payment_id':
                    data['razorpay_payment_id'] = val
                elif key == 'razorpay_signature':
                    data['razorpay_signature'] = val
            print('ye data hai...', data)
            client = razorpay.Client(auth=("rzp_test_XfqDl5oZQ0Rq4L", "gkCglJwlNEDmZcOTybIGmEl2"))
            check = client.utility.verify_payment_signature(data)
            if check:
                pass
            else:
                oreder_create=order_detail(user=user_inst,payment_mode="RazorPay",payment_id=data['razorpay_payment_id'],
                                              order_id=data['razorpay_order_id'], signature=data['razorpay_signature'],delivery_address=adrs_inst,price=pay)
                oreder_create.save()
                cart_featch = cart.objects.filter(user= user_inst,status = False)
                for x in cart_featch:
                    oreder_create.item.add(x)
                    x.status = True
                    x.save()
                return redirect('/success')

def suucess(request):
    return render(request,'success.html')

def contact_page(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact_fill = contact_detail(name=name,email=email,subject=subject,message=message)
        contact_fill.save()
        messages.success(request,"Your Query Submitted Successfully")
    return render(request,'contact.html')

def user_account(request):
    if request.user.is_authenticated:
        order = order_detail.objects.filter(user=request.user)

        return render(request,"my-account.html",{'order':order})