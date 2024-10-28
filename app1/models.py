from django.db import models

# Create your models here.
class usersignup(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self)-> str:
        return f'{self.name}'
    
class products(models.Model):
    categorychoices = (
        ('M','MENS '),
        ('W','WOMENs'),
        ('K','KIDS'),
        ('S','SPORTS DRESS'),
        ('B','babies'),
        ('a','all items'),
      )
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images')
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    features = models.CharField(max_length=1000)
    discount = models.IntegerField()
    category = models.CharField(max_length=100,default='l',choices=categorychoices)

    def str(self) -> str:
         return f'{self.name}'
   
class mycart(models.Model):
#     #products = models.ForeignKey(products,on_delete=models.CASCADE)
    products = models.ForeignKey(products,on_delete=models.CASCADE)
    usr = models.ForeignKey(usersignup,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    delivered = models.BooleanField(default=False)
    
    def str(self) -> str: 
        return f'{self.usr}'
    
class passwordReset(models.Model):
    user = models.ForeignKey(usersignup,on_delete=models.CASCADE)
    token = models.CharField(max_length=100,unique=True)
    created_at = models.DateField(auto_now=True)

class order(models.Model):
    user = models.ForeignKey(usersignup, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=150, null=True)
    orderstatus = (
        ('pending','pending'),
        ('Out for shipping','Out for shipping'),
        ('Completed','Completed')
    )
    status = models.CharField(max_length=150,choices=orderstatus, default='pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def _str_(self) -> str:
        return f'{self.tracking_no}'
    
class orderitem(models.Model):
    orderdet = models.ForeignKey(order,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def _str_(self) -> str:
        return f'{self.orderdet}'


class profile(models.Model):
    user = models.OneToOneField(usersignup,on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self) -> str:
        return f'{self.user.username}'    
        
