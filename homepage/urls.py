from django.urls import path
from . import views

urlpatterns = [
    path('homepage/',views.homepage,name='homepage'),
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('add-to-cart/<item_uid>',views.add_cart,name='add-cart'),
    path('cart/',views.cart,name='cart'),
    path('remove-from-cart/<item_uid>',views.remove_cart_items,name='remove-cart-item'),
    path('order-confirm',views.order_confirmed,name='order-confirmed'),
    path('dashboard/',views.get_orders,name='dashboard'),
    path('logout/',views.logout_view,name='logout'),    
    path('buynow/<item_uid>',views.buy_now,name='buy-now')
]