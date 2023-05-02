from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from django.http import JsonResponse
from .models import *
from . utils import cookieCart,cartData,guestOrder
import json
import datetime
from django.contrib import messages
from .forms import AddProductForm
from django.views import View




# Create your views here.
def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems }
    return render(request, 'store/store.html',context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']


    context = {'items':items ,'order':order,'cartItems':cartItems}
    return render(request, 'store/cart.html',context)

def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {'items':items ,'order':order,'cartItems':cartItems}
    return render(request, 'store/checkout.html',context)


def upadateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer ,complete=False)

    orderItem ,created = OrderItem.objects.get_or_create(order=order ,product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:  
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer ,complete=False)

    else:
        customer, order = guestOrder(request, data)
     

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment compleated',safe=False)

def signup(request):
    username=request.POST.get('username')
    password=request.POST.get('password')

    if request.method == 'POST':
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('store')

        else:
            messages.error(request,'Incorrect User-name or password ')
            return redirect('signup')
    else :

        return render(request, 'store/login.html')


def logout_user(request):
    logout(request)

    return redirect('store')

def register(request):
    try :
     if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password == confirm_password:
           user=User.objects.create_user(username=username,email=email,password=password,)
           login(request, user)
           return redirect('store')
        else:
            messages.error(request,'password not same')
            return redirect('register')
     else:

         return render(request, 'store/signup.html')
    
    except:
         messages.error(request,'username aleady exist')
         return redirect('register')
    


class adminPage(View):
    def get(self,request):
        form = AddProductForm()
        return render(request, 'store/admin.html',locals())
    
    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            reg = Product(name=name, price=price, image=image ) 
            reg.save()
            
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        
        return render(request, 'store/admin.html', locals())
    
def myProducts(request):
    add = Product.objects.all()
    return render(request,'store/product.html',locals())

class updateAdress(View):
    def get(self,request,pk):
        add = Product.objects.get(pk=pk)
        form = AddProductForm(instance=add)
        return render(request,'store/updateAdress.html',locals())
    def post(self, request,pk):
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            add = Product.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.price = form.cleaned_data['price']
            add.image = form.cleaned_data['image']
            add.save()
            
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("my-products")