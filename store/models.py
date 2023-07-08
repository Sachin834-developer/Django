from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# Customer,Product,Oredr,OrderItems,ShippingAddress

class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=200,null=True)

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    price=models.FloatField()
    digital=models.BooleanField(default=False,null=True,blank=True)
    image =models.ImageField(null=True,blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    def __str__(self) -> str:
        return self.name
    
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transactionId=models.CharField(max_length=200,null=True)

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([(item.get_total) for item in orderitems ])
        return total
    
    @property
    def get_cart_quantity(self):
        orderitems=self.orderitem_set.all()
        total=sum([(item.quantity) for item in orderitems ])
        return total

    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for orderitem in orderitems:
            if orderitem.product.digital==False:
                shipping=True
        return shipping

    def __str__(self) -> str:
        return str(self.id)
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    dateOrdered=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total

    def __str__(self) -> str:
        return self.product.name
    
class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    pincode=models.IntegerField(max_length=6)
    dateAdded=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address
    



