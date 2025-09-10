from django.urls import path
from . import views
urlpatterns = [
    # Productos
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("product/<int:product_id>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("search/", views.ProductSearchView.as_view(), name="search"),
    # Carrito
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    # Reseñas
    path("product/<int:product_id>/review/", views.SubmitReviewView.as_view(), name="submit_review"),
    path("review/<int:review_id>/moderate/", views.ModerateReviewView.as_view(), name="moderate_review"),

]