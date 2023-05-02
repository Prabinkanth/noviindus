import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        
    except:
        cart = {}
    
    print('cart:',cart)
    items = []
    order ={'get_cart_total':0, 'get_cart_items':0 ,'shipping':False }
    cartItems =order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    "imageURL":product.imageURL,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total    
            }
            items.append(item)
            if product.dijital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems':cartItems,'order':order,'items':items}


def cartData(request):
    user = request.user
    if user.is_authenticated:
        customer = Customer.objects.filter(user=user).first()
        if customer:
            order, created = Order.objects.get_or_create(customer=customer ,complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            customer = Customer.objects.create(user=user, email=user.email)
            order, created = Order.objects.get_or_create(customer=customer ,complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']
    return {'cartItems':cartItems,'order':order,'items':items}


def guestOrder(request,data):
    print('user is not loged in')
        
    print('COOKIES:',request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer ,created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    print(name)
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete=False
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']

        )
    return customer, order