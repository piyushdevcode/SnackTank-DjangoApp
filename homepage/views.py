from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login,authenticate,logout
from homepage.models import *   
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def homepage(request):
    items = FoodItems.objects.all()
    context = {
        'items': items
    }
    return render(request,'homepage.html',context)


def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)

            if not user_obj.exists():
                messages.error(request,'username or password incorrect')
                return redirect('/login/')

            if user_obj := authenticate(username=username, password=password):
                login(request, user_obj)
                return redirect ('/homepage/')

            messages.error(request,'username or password incorrect')
            return redirect('/login/')

        except Exception as e:
            messages.error(request,'Something went wrong')
            return redirect ('/register/')

    return render(request,'login.html')
    
def register_page(request):
    if request.method == 'POST':
        try:
            _users = User.objects.all()
            print(_users)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)

            if user_obj.exists():
                messages.error(request,'username not available')
                return redirect('/register/')

            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request,'user created successfully')
            return redirect('/login/')
        
        except Exception as e:
            messages.error(request,'Something went wrong')
            return redirect('/register/')

    return render(request,'register.html')

# adding a new item to the cart 
@login_required(login_url='/login/')  
def add_cart(request, item_uid):
    user = request.user
    item_obj = FoodItems.objects.get(uid=item_uid)

    # retrieving the unpaid cart
    cart, _ = Cart.objects.get_or_create(user=user,is_paid=False)
    
    cart_items = CartItems.objects.create(cart=cart,food_item=item_obj)

    return redirect('/homepage/')

# view for my cart 
@login_required(login_url='/login/')  
def cart(request):
    try:
        cart = Cart.objects.get(is_paid=False,user=request.user)
        context = {
            'carts': cart
        }
        print(f'Cart is {cart}, Items: {cart.cart_items.all}')
    except Cart.DoesNotExist:
        context = {'carts':None}

    return render(request,'cart.html',context=context)

@login_required(login_url='/login/')  
def remove_cart_items(request,item_uid):
    try:
        CartItems.objects.get(uid=item_uid).delete()
        return redirect('/cart/')

    except CartItems.DoesNotExist:
        return redirect('/cart/')

def order_confirmed(request):
    # to prevent access of order page
    try:
        cart = Cart.objects.get(user=request.user,is_paid=False)
    except Cart.DoesNotExist:
        return HttpResponse('not allowed')
        
    cart.is_paid = True
    cart.save()
    return render(request,'order-placed.html',context={
        'user': request.user,
        'orderid': cart.uid
    })

# showing the DASHBOARD for orders
@login_required(login_url='/login/')  
def get_orders(request):
    cart = Cart.objects.filter(is_paid=True,user=request.user)
    context = {
        'carts': cart
    }
    return render(request,'dashboard.html',context)

def logout_view(request):
    logout(request)
    return redirect('homepage')

# for adding to cart and redirecting to my carts

@login_required(login_url='/login/')  
def buy_now(request,item_uid):
    user = request.user
    item = FoodItems.objects.get(uid=item_uid)
    cart,_ = Cart.objects.get_or_create(user=user,is_paid=False)
    CartItems.objects.create(cart=cart,food_item=item)

    return redirect('/cart/')
