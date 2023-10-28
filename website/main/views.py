from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from .utils import cartData
import json
from datetime import datetime

def HomePage(request):
    category = request.GET.get('category')
    categories = Category.objects.all()
    if 'search' in request.GET:
        search = request.GET['search']
        products = Product.objects.filter(name__icontains=search)
        if not products:
            products=None
    else:
        products = Product.objects.filter(category__name=category)
    productsall = Product.objects.all()
    context = {'products': products,'categories': categories,'productsall':productsall}
    return render (request, 'home.html', context)

def SignupPage(request):
    if request.user.is_authenticated:
        return redirect ('home')
    elif request.method=='POST':
        uname=request.POST.get('username')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
            messages.error(request,'Password and its confirmation do not match. Try again!')
            return redirect ('signup')
        elif len(pass1) < 8:
            messages.error(request,'Password should be atleast 8 characters long. Try again!')
            return redirect ('signup')
        try:
            my_user=User.objects.create_user(username=uname,password=pass1)
            my_user.save()
            user=authenticate(request,username=uname,password=pass1)
            login(request,user)
            user=request.user
            Customer.objects.create(username=User.objects.get(username=user))
            order=Order(customer_id=user.id,order_date=datetime.now(),cart_complete=0)
            order.save()
            return redirect('home')
        except:
            messages.error(request,'Username has already been taken. Try again!')
            return redirect ('signup')
    else:
        return render (request,'signup.html')

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect ('home')
    elif request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect ('home')
        else:
            messages.error(request,'Invalid username/password. Try again!')
            return redirect ('login')
    else:
        return render (request,'login.html')

def LogoutPage(request):
    if not request.user.is_authenticated:
        return redirect ('home')
    logout(request)
    return redirect ('home')

def ProfilePage(request):
    if not request.user.is_authenticated:
        return redirect ('home')
    return render (request,'profile.html')

def CartPage(request):
    if not request.user.is_authenticated:
        return redirect ('home')
    data = cartData(request)
    order_products = data['order_products']
    order =  data['order']
    total=round(float(order.get_total_price)*1.05,2)
    context = {'order_products':order_products, 'order':order,'total':total}
    return render(request, 'cart.html', context)

def AboutPage(request):
    return render (request,'about.html')

def TeamPage(request):
    return render (request,'team.html')

def SupportPage(request):
    return render (request,'support.html')

def DeletePage(request):
    if not request.user.is_authenticated:
        return redirect ('home')
    user=request.user
    ord = Order.objects.filter(customer_id=user.id)
    ord.delete()
    ord_user = Order_Product.objects.filter(order_id=user.id)
    ord_user.delete()
    user.delete()
    return redirect ('home')

def ChPassPage(request):
    if not request.user.is_authenticated:
        return redirect ('home')
    elif request.method=='POST':
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
            messages.error(request,'Password and its confirmation do not match. Try again!')
            return redirect ('chpass')
        elif len(pass1) < 8:
            messages.error(request,'Password should be atleast 8 characters long. Try again!')
            return redirect ('chpass')
        user=request.user
        user.set_password(pass1)
        user.save()
        return redirect ('home')
    else:
        return render (request,'chpass.html')
    
def ReceiptPage(request):
    if not request.user.is_authenticated:
        return redirect ('home')
    data=cartData(request)
    if not data['order_products']:
        return redirect ('cart')
    try:
        payment=request.GET.get('payment',None).title()
        location=request.GET.get('location',None).title()
    except:
        return redirect ('home')
    order_products = data['order_products']
    order =  data['order']
    total=round(float(order.get_total_price)*1.05,2)
    vat=round(total-float(order.get_total_price),2)
    datenow=datetime.now().strftime("%d/%m/%Y")
    timenow=datetime.now().strftime("%H:%M:%S")
    if payment=='Credit':
        try:
            cc=request.GET.get('cc',None)
            exp=request.GET.get('exp',None)
            cvv=request.GET.get('cvv',None)
        except:
            return redirect ('cart')
        else:
            flag=False
            if len(cc)!=16 or cc.isdigit()!=True:
                flag=True
                messages.error(request,'Invalid Credit Card Number!')
            if len(exp)!=5 or exp[2]!='/' or (exp[:2].isdigit()!=True and exp[3:].isdigit()!=True):
                flag=True
                messages.error(request,'Invalid Expiry Date!')
            elif 0>int(exp[:2]) or 12<int(exp[:2]):
                flag=True
                messages.error(request,'Invalid Expiry Date!')
            elif int(exp[3:])<int(datenow[8:]):
                flag=True
                messages.error(request,'Invalid Expiry Date!')
            elif int(exp[3:])==int(datenow[8:]):
                if int(exp[:2])<=int(datenow[3:5]):
                    flag=True
                    messages.error(request,'Invalid Expiry Date!')
            if len(cvv)!=3 or cvv.isdigit()!=True:
                flag=True
                messages.error(request,'Invalid CVV!')
        if flag==True:
            return redirect ('cart')
    receipt = f"""---------------------------------------------------
                Planet Supermarket
                     Al Quoz
---------------------------------------------------
Address: Planet Supermarket, Al-Quoz 4, Dubai, UAE
Email: support@planetsupermarket.com
Phone: +971 050 123 4567
---------------------------------------------------
{'Item':<27}{'Qty':<8}Price (AED)
"""
    for i in order_products:
        receipt+=f"{i.product.name:<27}{i.quantity}{i.product.unit[1:]:<7}{i.get_total} AED\n"
    receipt+="---------------------------------------------------"
    receipt+=f"\n{'Sub Total:':<35}{order.get_total_price} AED"
    receipt+=f"\n{'VAT Charged:':<35}{vat} AED"
    receipt+=f"\n{'Total:':<35}{total} AED"
    receipt+="\n---------------------------------------------------"
    receipt+=f"\n{'User:':<35}{request.user}"
    receipt+=f"\n{'Location:':<35}{location}"
    receipt+=f"\n{'Payment:':<35}{payment}"
    if payment=='Credit':
        receipt+=f"\n{'CC Number:':<35}{'*'*8+cc[8:]}"
    receipt+="\n---------------------------------------------------"
    receipt+=f"\n{'Date:':<35}{datenow}"
    receipt+=f"\n{'Time:':<35}{timenow}"
    receipt+="\n---------------------------------------------------"
    context = {'receipt':receipt,'order_products':order_products}
    user=request.user
    Order_Product.objects.filter(order_id=user.id).delete()
    return render (request,'receipt.html',context)

def ClearPage(request):
    if not request.user.is_authenticated:
        return redirect ('home')
    user=request.user
    Order_Product.objects.filter(order_id=user.id).delete()
    return redirect ('cart')
    
    
def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,cart_complete=False)
    order_Product,created=Order_Product.objects.get_or_create(order=order, product=product)
    if action=="add":
        order_Product.quantity +=1
    elif action =="remove":
        order_Product.quantity -=1
    order_Product.save()
    cart_total = order.get_total_quantity
    cart_totalPrice = order.get_total_price
    if order_Product.quantity<=0:
        order_Product.delete()
    return JsonResponse({'cart_total':cart_total,'cart_totalPrice':cart_totalPrice,'quantity':order_Product.quantity, 'unitprice':order_Product.product.price}, safe=False)