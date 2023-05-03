from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('upadate_item/',views.upadateItem,name="upadate_item"),
 
    path('login/',views.signup,name='signup'),
    #Authentication
    path('logout/',views.logout_user,name="logout"),
    path('register/',views.register,name="register"),
    # Admin
    path('add-page/',views.adminPage.as_view(),name="admin-page"),
    path('admin-page/', views.myProducts,name='my-products'),
    path('updateproduct/<int:pk>', views.updateProduct.as_view(),name='updateproduct'),
    path('delete-product/<int:pk>', views.product_delete ,name='delete-product'),
]
