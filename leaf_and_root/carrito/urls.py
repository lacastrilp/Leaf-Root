from django.urls import path
from . import views
urlpatterns = [
    # Carrito
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    
    
    

]