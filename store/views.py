from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cartCookieView,cartData,guestOrder
# Create your views here.


def storeView(request):
    data=cartData(request)
    items=data['items']
    cartItems=data['cartItems']
    order=data['order']

    products=Product.objects.all()

    context={'products':products,'cartItems':cartItems,'shipping':False}
    return render(request,'store/store.html',context)

def cartView(request):
    
    data=cartData(request)
    items=data['items']
    cartItems=data['cartItems']
    order=data['order']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)

def checkoutView(request):
    data=cartData(request)
    items=data['items']
    cartItems=data['cartItems']
    order=data['order']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)

def update_item(request):
    data = json.loads(request.body)
    productId=data['productId']
    action = data['action']

    print('ProductId:',productId,'Action:',action)

    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)


    if action=='add':
        orderItem.quantity+=1
    elif action=='remove':
        orderItem.quantity-=1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was Added',safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
    else:
        
        customer,order=guestOrder(request,data)
        print('Check ',customer,order)

    total=float(data['form']['total'])
    print(transaction_id)
    order.transactionId=transaction_id   

   
    if total==order.get_cart_total:
        print('Saving?.................')
        order.complete=True
    order.save()

    if order.shipping ==True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            pincode=data['shipping']['pincode'],
        )

    return JsonResponse('Payment completed',safe=False)