from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('upadate_item/',views.upadateItem,name="upadate_item"),
    path('process_order/',views.processOrder,name="process_order"),
    path('login/',views.signup,name='signup'),
    path('logout/',views.logout_user,name="logout"),
    path('register/',views.register,name="register"),

]
