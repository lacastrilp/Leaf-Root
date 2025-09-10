from django.urls import path
from . import views
urlpatterns = [
    # Carrito
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    #path('add-to-cart-class/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart_class'), Se la inventó esto

]