from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse,HttpResponse
import random

# Create your views here.

#.....index page.......
def index(r):
    if 'id' in r.session:
        print('login')
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.filter(id=val).first()
        c  = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj =products.objects.all()
        l=[]
        for i in obj:
            if len(l)<3:
                l.append(i)
            else:
                pass
        k =[]
        n=[]
        for i in obj:
            k.append(i)
        k.reverse()
        for j in k:
            if len(n)< 6:
                n.append(j)
        else:
            pass
        return render(r,'index.html',{'l':l,'n':n,'cnt':cnt,'usr':usr})
    else:
        print('hello')
        obj = products.objects.all()
        l=[]
        for i in obj:
            if len(l) < 3:
                l.append(i)
            else:
                pass
        k=[]
        n=[]
        for i in obj:
            k.append(i)
        k.reverse()
        for j in k:
            if len(n) <6:
                n.append(j)
            else:
                pass    
        print(n)
        print(k)
    return render(r,'index.html')

#...... login,regisration,logout Page start.........

# Registration page 
def reg(r1):
    if r1.method=='POST':
        n=r1.POST.get('name')
        e=r1.POST.get('email')
        ph=r1.POST.get('phone')
        u=r1.POST.get('username')
        p=r1.POST.get('password')
        p2=r1.POST.get('repassword')
        if p==p2:
            if usersignup.objects.filter(username=u).exists():
                messages.info(r1,"username already exists",extra_tags='signup')
                return redirect(reg)
            elif usersignup.objects.filter(email=e).exists():
                messages.info(r1,"Email already exists",extra_tags='signup')
                return redirect(reg)
            else:
                val=usersignup.objects.create(name=n,email=e,phone=ph,username=u,password=p)
                val.save()
        else:
            messages.info(r1,"password doesn't exist",extra_tags='signup')
            return redirect(reg)    
    return render(r1,'login.html')

#login page

def log(r2):
    if r2.method=='POST':
        u=r2.POST.get('username')
        p=r2.POST.get('password')
        if u=='admin' and p=='123':
            return redirect(adminindex)
        
        elif usersignup.objects.filter(username=u).exists():
            usr = usersignup.objects.filter(username=u).first()
            if usr.password == p:
                r2.session['id']=[usr.id]
                return redirect(index)
            else:
                messages.info(r2,'incorrect password',extra_tags='login')
                return redirect(log)
        else:
            messages.info(r2,'username not found',extra_tags='login')
            return redirect(log)
    return render(r2,'login.html')
#logout page

def logout(l):
    if'id' in l.session:
        l.session.flush()
        return redirect(index)
    return render(l,'index.html')

#........registration/login/logoutpages end.........#


#...........................CART ITEMS START....................#

# Cart items

def car(r6):
    if 'id' in r6.session:
        se = r6.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        cl = {}
        for i in c:
            print(i)
            cl[i.products] = [i.quantity,i.id]
        usr = usersignup.objects.filter(id=val).first()
        return render(r6,'cart.html',{"usr":usr,"cl":cl,"cnt":cnt})
    return redirect(log)

# Add cart items

def addcart (r3,wal=0):
    if 'id' in r3.session:
        se = r3.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr =  val).all()
        if r3.method == 'POST':
            p = products.objects.filter(id = wal).first()
            usr = usersignup.objects.get(id= val)
            if c:
                f=0
                for i in c:
                    if i.products == p:
                        f=1
                        i.quantity = i.quantity + 1
                        i.save()
                    return redirect(car)
                if f==0:
                    val = mycart.objects.create(usr = usr, products = p, quantity = 1,delivered = False)
                    val.save()
                return redirect(car)
            else:
                val = mycart.objects.create(usr = usr, products = p, quantity = 1,delivered = False)
                val.save()
            return redirect(car)
    return redirect(log)

# Deleting cart items

def deletecart(d1,de):
    if 'id' in d1.session:
        c= mycart.objects.get(id=de)
        c.delete()
        return redirect(car)

# Decreasing cart items

def minuscart(d2,de):
    if 'id' in d2.session:
        c=mycart.objects.get(id=de)
        if c.quantity>1:
            c.quantity = c.quantity - 1
            c.save()
        else:
            c.delete()
        return redirect(car)

# increasing cart items
    
def pluscart(d3,de):
    if 'id' in d3.session:
        c=mycart.objects.get(id=de)
        if c.quantity>1:
            c.quantity = c.quantity + 1
            c.save()
        else:
            c.delete()
        return redirect(car)
#.......................CART ITEMS END..............#    
    

def allp(r3):
     l = products.objects.all()
     return render(r3,'allproducts.html',{'l':l})
def con(r4):
    return render(r4,'contact.html')   
def che(r5):
    if 'id' in r5.session:
        se = r5.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        t=0
        for i in c:
            t=t+(i.products.discount*i.quantity)
        if r5.method == 'POST':
            if profile.objects.filter(user=usr) == None:
                userprofile = profile()
                userprofile.user = usr
                userprofile.fname = r5.POST.get('fname')
                userprofile.lname = r5.POST.get('lname')
                userprofile.email = r5.POST.get('email')
                userprofile.phone = r5.POST.get('phone')
                userprofile.address = r5.POST.get('address')
                userprofile.city = r5.POST.get('city')
                userprofile.state = r5.POST.get('state')
                userprofile.country = r5.POST.get('country')
                userprofile.pincode = r5.POST.get('pincode')
                userprofile.save()

            neworder = order()
            neworder.user = usr
            neworder.fname = r5.POST.get('fname')
            neworder.lname = r5.POST.get('lname')
            neworder.email = r5.POST.get('email')
            neworder.phone = r5.POST.get('phone')
            neworder.address = r5.POST.get('address')
            neworder.city = r5.POST.get('city')
            neworder.state = r5.POST.get('state')
            neworder.country = r5.POST.get('country')
            neworder.pincode = r5.POST.get('pincode')

            neworder.total_price = t

            neworder.payment_mode = r5.POST.get('payment_mode')
            neworder.payment_id = r5.POST.get('payment_id')

            trackno = 'Eshop'+str(random.randint(1111111,9999999))
            while order.objects.filter(tracking_no=trackno) is None:
                trackno = 'Eshop'+str(random.randint(1111111,9999999))
            neworder.tracking_no = trackno
            neworder.save()

            for item in c:
                orderitem.objects.create(
                    orderdet = neworder,
                    product = item.products,
                    price = item.products.discount,
                    quantity = item.quantity
                )

            mycart.objects.filter(usr=val).delete()

            messages.success(r5, 'Your order has been placed successfully')

            payMode = r5.POST.get('payment_mode')
            if payMode == "Razorpay":
                return JsonResponse({'status':'Your order has been placed successfully'})

        return redirect(index)
    


    return render(r5,'checkout.html')
def placeorder(r14):
    if 'id' in r14.session:
        se = r14.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        t=0
        for i in c:
            t=t+(i.products.discount*i.quantity)
        if r14.method == 'POST':
            if profile.objects.filter(user=usr) == None:
                userprofile = profile()
                userprofile.user = usr
                userprofile.fname = r14.POST.get('fname')
                userprofile.lname = r14.POST.get('lname')
                userprofile.email = r14.POST.get('email')
                userprofile.phone = r14.POST.get('phone')
                userprofile.address = r14.POST.get('address')
                userprofile.city = r14.POST.get('city')
                userprofile.state = r14.POST.get('state')
                userprofile.country = r14.POST.get('country')
                userprofile.pincode = r14.POST.get('pincode')
                userprofile.save()

            neworder = order()
            neworder.user = usr
            neworder.fname = r14.POST.get('fname')
            neworder.lname = r14.POST.get('lname')
            neworder.email = r14.POST.get('email')
            neworder.phone = r14.POST.get('phone')
            neworder.address = r14.POST.get('address')
            neworder.city = r14.POST.get('city')
            neworder.state = r14.POST.get('state')
            neworder.country = r14.POST.get('country')
            neworder.pincode = r14.POST.get('pincode')

            neworder.total_price = t

            neworder.payment_mode = r14.POST.get('payment_mode')
            neworder.payment_id = r14.POST.get('payment_id')

            trackno = 'Estore'+str(random.randint(1111111,9999999))
            while order.objects.filter(tracking_no=trackno) is None:
                trackno = 'estore'+str(random.randint(1111111,9999999))
            neworder.tracking_no = trackno
            neworder.save()

            for item in c:
                orderitem.objects.create(
                    orderdet = neworder,
                    product = item.products,
                    price = item.products.discount,
                    quantity = item.quantity
                )

            mycart.objects.filter(usr=val).delete()

            messages.success(r14, 'Your order has been placed successfully')

            payMode = r14.POST.get('payment_mode')
            if payMode == "Razorpay":
                return JsonResponse({'status':'Your order has been placed successfully'})
            

        return redirect(index)
def razorpaycheck(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        t=0
        for i in c:
            t=t+(i.products.discount*i.quantity)

    return JsonResponse({
        'total_price':t
    })

def orderss(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        o = order.objects.all()
        l=[]
        for i in o:
            if i.user==usr:
                l.append(i)
        return render(r,'myorders.html',{'l':l})
    return render(r,'myorders.html')
    

   


def my(r7):
    
    return render(r7,'my-account.html')  
def lis(r8):
    l=products.objects.all()
    print(l)
    return render(r8,'categories.html',{'l':l})

def wis(r9):
    return render(r9,'wishlist.html')
def base(r10):
    return render(r10,'base.html')

def MENS(r11):
    if 'id' in r11.session:
        se = r11.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        
        for i in obj:
            if i.category=='M':
                l.append(i)
        print('hello')
        print(l)
        return render(r11,'products.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='M':
                l.append(i)
        return render(r11,'products.html',{'l':l})

def womens(r12):
    if 'id' in r12.session:
        se = r12.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        
        for i in obj:
            if i.category=='W':
                l.append(i)
        print(l)
        return render(r12,'products.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='W':
                l.append(i)
        return render(r12,'products.html',{'l':l})
def sports(r12):
    if 'id' in r12.session:
        se = r12.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        
        for i in obj:
            if i.category=='S':
                l.append(i)
        print('hello')
        print(l)
        return render(r12,'products.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='S':
                l.append(i)
        return render(r12,'products.html',{'l':l})


def kids(r12):
    if 'id' in r12.session:
        se = r12.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = car.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        
        for i in obj:
            if i.category=='K':
                l.append(i)
        print(l)
        return render(r12,'products.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='K':
                l.append(i)
        return render(r12,'products.html',{'l':l})
def babies(r12):
    if 'id' in r12.session:
        se = r12.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        
        for i in obj:
            if i.category=='B':
                l.append(i)
        print('hello')
        print(l)
        return render(r12,'products.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='B':
                l.append(i)
        return render(r12,'products.html',{'l':l})
    
def product(r13,wal):
    if 'id' in r13.session:
        se = r13.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c=mycart.objects.filter(usr=val).all
        cnt=c.count()
        l=products.objects.filter(id=wal).first
        return render(r13,'products.html',{'l':l,'cnt':cnt,'usr':usr,'c':c})
    else:
        l=products.objects.filter(id=wal).first()
        return render(r13,'products.html',{'l':l})
def searchfn(s):
    if 'id' in s.session:
        se = s.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr = val).all()
        cnt = c.count()
        if s.method == 'POST':
            sr = s.POST.get('sr')
            l = products.objects.filter(name__icontains = sr)
            return render(s,'shopitems.html',{'l':l,'cnt':cnt,'usr':usr})
        return render(s,'shopitems.html',{'l':l,'cnt':cnt,'usr':usr})
    else:
        if s.method == 'POST':
            sr = s.POST.get('sr')
            l = products.objects.filter(name__icontains = sr)
            return render(s,'shopitems.html',{'l':l})
        return render(s,'shopitems.html',{'l':l})    

def logout(l3):
    if 'id' in l3.session:
        l3.session.flush()
        return redirect(index)
    return render(l3,'index.html')    

#...........ADMIN PAGE................#    
def adminindex(a1):
    return render(a1,'myadmin/index.html')    

def adminpro(a1):
    obj = products.objects.all()
    return render(a1,'myadmin/products.html',{'obj':obj})

def adminbase(a1):
    return render(a1,'myadmin/base.html')

def  addproduct(a1):
    if a1.method=='POST':
        n=a1.POST.get('name')
        dc=a1.POST.get('description')
        f=a1.POST.get('features')
        p=a1.POST.get('price')
        d=a1.POST.get('discount')
        c=a1.POST.get('category')
        img=a1.FILES.get('image')
        obj=products.objects.create(name=n,price=p,description=dc,features=f,discount=d,category=c,image=img)
        obj.save()
    return render(a1,'myadmin/add-product.html')

def editproduct(a1,wal):
    obj = products.objects.filter(id=wal).first() 
    return render(a1,'myadmin/edit-product.html',{'obj':obj})

def editproduct2(a1,wal):
    obj = products.objects.get(id=wal)
    if a1.method=='POST':
        obj.name = a1.POST.get('name')
        obj.description = a1.POST.get('description')
        obj.features = a1. POST.get('features')
        obj.price = a1.POST.get('price')
        obj.discount = a1.POST.get('discount')
        obj.category = a1.POST.get('category')
        obj.image = a1.FILES.get('image')
        obj.save()
        return redirect(adminpro)
    return render(a1,'myadmin/edit-product.html',{'obj':obj})

def users(a2):
    obj = usersignup.objects.all()
    return render(a2,'myadmin/user.html',{'obj':obj}) 

def userbooking(a2):
    o = order.objects.all()
    return render(a2,'myadmin/userbooking.html',{'o':o})


def deleteproduct(a1,wal):
    obj=products.objects.filter(id=wal).first()
    obj.delete()
    return redirect(adminpro)

def forgot(request):  
    if request.method == 'POST':
        email = request.POST.get('email')
        
        print(email)
        user = usersignup.objects.get(email=email)
        
        token = get_random_string(length=4)
        passwordReset.objects.create(user=user,token=token)

        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        send_mail('Reset your password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
        return render(request,"reset_password.html")
    return render(request,"password_reset_send.html")

def reset_password(request,token):
    password_reset = password_reset.objects.get(token=token)
    usr = usersignup.objects.get(id=password_reset.user_id)
    return render(request,"reset_password.html",{'token':token})

def reset_password2(request,token):
    password_reset = passwordReset.objects.get(token=token)
    usr = usersignup.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('repeatpassword')
        if repeat_password == new_password:
            password_reset.user.password = new_password
            password_reset.user.save()
            password_reset.delete()
            return redirect(log) 
    return render(request,"reset_password.html")
        
def single(r22,wal):
    if 'id' in r22.session:
       se = r22.session.get('id')
       val = se[0]
       usr = usersignup.objects.get(id = val)
       c = mycart.objects.filter(usr = wal).all()
       cnt = c.count()
       l = products.objects.filter(id=wal).first()
       return render(r22,'single.html',{'l':l,'cnt':cnt,'usr':usr,'c':c})
    else:
        l=products.objects.filter(id=wal).first()
        return render(r22,'single.html',{'l':l})

   
        


    








