from django.urls import path

from .views import storeView,cartView,checkoutView,update_item,processOrder

urlpatterns=[
    path('',storeView,name='store'),
    path('cart/',cartView,name='cart'),
    path('checkout/',checkoutView,name='checkout'),
    path('update_item/',update_item,name='update_item'),
    path('processOrder/',processOrder,name='processOrder'),

]