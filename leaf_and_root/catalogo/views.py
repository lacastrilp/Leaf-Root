from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, ListView, TemplateView
from catalogo.models import Product, Review
from users.models import Customer # 👈 agrega Custome
from .models import Wishlist, Product
from .forms import ReviewForm, ProductForm
from django.db.models import Q, Avg, Count
from django.contrib.auth.models import User
from django.template.loader import render_to_string



def is_admin(user):
    return user.is_staff


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})

# ---------- Productos ----------
class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"

    def get(self, request, *args, **kwargs):
        """Override para guardar productos vistos en la sesión"""
        response = super().get(request, *args, **kwargs)
        
        # Guardar en productos vistos recientemente
        product_id = self.get_object().pk
        recently_viewed = request.session.get('recently_viewed', [])
        
        # Quitar si ya existe para evitar duplicados
        if product_id in recently_viewed:
            recently_viewed.remove(product_id)
        
        # Agregar al inicio de la lista
        recently_viewed.insert(0, product_id)
        
        # Mantener solo los últimos 10
        request.session['recently_viewed'] = recently_viewed[:10]
        request.session.modified = True
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product= self.get_object()  # safer than self.object if object isn't set
        reviews_qs = Review.objects.filter(product=product, approved=True)
        context["reviews"] = reviews_qs
        context["review_form"] = ReviewForm()  # 👈 form para el POST
        agg = reviews_qs.aggregate(avg=Avg("rating"), cnt=Count("id_review"))
        context["avg_rating"] = agg.get("avg")
        context["review_count"] = agg.get("cnt", 0)
        # IDs de productos en wishlist para marcar el corazón en detalle
        user = self.request.user
        if user.is_authenticated:
            customer = getattr(user, "customer", None)
            if customer:
                context["wishlist_product_ids"] = list(
                    Wishlist.objects.filter(customer=customer).values_list("product_id", flat=True)
                )
            else:
                context["wishlist_product_ids"] = []
        else:
            context["wishlist_product_ids"] = []
        return context


class ProductSearchView(ListView):
    model = Product
    template_name = "product_search.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Product.objects.filter(name__icontains=query)


class HomeView(TemplateView):
    """Vista para la página de inicio con productos recomendados y vistos recientemente"""
    template_name = "product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Productos recomendados (primeros 4 productos con stock)
        recommended = Product.objects.filter(stock__gt=0).order_by('-id_product')[:4]
        for product in recommended:
            labels = product.labels.lower() if product.labels else ""
            if "vegan" in labels:
                product.diet_label = "vegan"  # type: ignore
            elif "vegetarian" in labels:
                product.diet_label = "vegetarian"  # type: ignore
            else:
                product.diet_label = "plant-based"  # type: ignore  
        context["recommended_products"] = recommended
        
        # Productos vistos recientemente (últimos 4 de la sesión)
        recently_viewed_ids = self.request.session.get('recently_viewed', [])[:4]
        if recently_viewed_ids:
            # Preservar el orden de la sesión
            recently_viewed = []
            for pk in recently_viewed_ids:
                try:
                    product = Product.objects.get(pk=pk)
                    labels = product.labels.lower() if product.labels else ""
                    if "vegan" in labels:
                        product.diet_label = "vegan"  # type: ignore
                    elif "vegetarian" in labels:
                        product.diet_label = "vegetarian"  # type: ignore
                    else:
                        product.diet_label = "plant-based"  # type: ignore
                    recently_viewed.append(product)
                except Product.DoesNotExist:
                    pass
            context["recently_viewed"] = recently_viewed
        else:
            context["recently_viewed"] = []
        
        # Lista de IDs de wishlist del usuario autenticado
        if self.request.user.is_authenticated:
            customer = getattr(self.request.user, "customer", None)
            if customer:
                context["wishlist_product_ids"] = list(
                    Wishlist.objects.filter(customer=customer).values_list("product_id", flat=True)
                )
            else:
                context["wishlist_product_ids"] = []
        else:
            context["wishlist_product_ids"] = []
        
        return context

    
class ProductListView(ListView):
    """Vista para el catálogo completo de productos con filtros y paginación"""
    model = Product
    template_name = "catalog.html"
    context_object_name = "products"
    paginate_by = 12  # Paginación, 12 productos por página

    def get_queryset(self):
        queryset = Product.objects.all()

        # 🔎 Búsqueda
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(description__icontains=q) |
                Q(category__icontains=q)
            )

        # 🔎 Filtros
        category = self.request.GET.get("category")
        if category:
            # aquí buscamos tanto si tiene prefijo como si está limpio
            queryset = queryset.filter(
                Q(category=category) | Q(category__endswith=f":{category}") | 
                Q(category__startswith=f"{category}:") 
            )

        # 🔎 Nuevo filtro vegan / vegetarian
        diet = self.request.GET.get("diet")
        if diet == "vegan":
            # filtrar si contienen cualquier variante de vegan
            queryset = queryset.filter(labels__icontains="vegan")
        elif diet == "vegetarian":
            # primero vegetarian, pero excluir los que también son vegan
            queryset = queryset.filter(labels__icontains="vegetarian").exclude(labels__icontains="vegan")

        # 🔎 Ordenar por precio
        sort = self.request.GET.get("sort")
        if sort == "price_asc":
            queryset = queryset.order_by("price")
        elif sort == "price_desc":
            queryset = queryset.order_by("-price")
        
        # 👉 Aquí procesamos etiquetas antes de devolver queryset
        for product in queryset:
            labels = product.labels.lower() if product.labels else ""
            if "vegan" in labels:
                product.diet_label = "vegan" # type: ignore
            elif "vegetarian" in labels:
                product.diet_label = "vegetarian" # type: ignore
            else:
                product.diet_label = "plant-based" # type: ignore

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # valores únicos para los select
        raw_categories = Product.objects.values_list("category", flat=True).distinct()

        def clean_category(c):
            if c and ":" in c:
                return c.split(":", 1)[1]
            return c

        categories = [clean_category(c) for c in raw_categories if c]

        context["categories"] = categories
        

        # mantener filtros actuales, pero quitar "page"
        current_filters = self.request.GET.copy()
        if "page" in current_filters:
            current_filters.pop("page")
        context["current_filters"] = current_filters

        context["diet_selected"] = self.request.GET.get("diet", "")

            # Lista de IDs de wishlist del usuario autenticado
        if self.request.user.is_authenticated:
            customer = getattr(self.request.user, "customer", None)
            if customer:
                context["wishlist_product_ids"] = list(
                    Wishlist.objects.filter(customer=customer).values_list("product_id", flat=True)
                )
            else:
                context["wishlist_product_ids"] = []
        else:
            context["wishlist_product_ids"] = []


        
        return context


# ---------- Reseñas ----------
class SubmitReviewView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            # asegurar Customer asociado al user
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                # crea un Customer mínimo para poder guardar la reseña
                customer, _ = Customer.objects.get_or_create(
                    user=request.user,
                    defaults={
                        "name": request.user.get_full_name() or request.user.username,
                        "email": request.user.email or f"{request.user.username}@local.local",
                        "address": "",
                        "phone": "",
                    },
                )
            review = form.save(commit=False)
            review.product = product
            review.customer = customer   # 👈 usa customer, no user
            review.approved = True       # o déjalo False si quieres moderación
            review.save()
            # Si es AJAX, devolver JSON y no redirigir
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                agg = Review.objects.filter(product=product, approved=True).aggregate(
                    avg=Avg("rating"), cnt=Count("id_review")
                )
                return JsonResponse({
                    "success": True,
                    "message": "Review submitted",
                    "avg_rating": float(agg.get("avg") or 0),
                    "review_count": agg.get("cnt", 0),
                })
            # Redirección normal a detalle del producto
            return redirect("product_detail", product_id=product.pk)
        # Form inválido
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "message": "Invalid form",
                "errors": form.errors,
            }, status=400)
        return redirect("product_detail", product_id=product.pk)


class ModerateReviewView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        review.approved = True
        review.save()
        return HttpResponse("Reseña moderada")


# --- Agregar producto ---
@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("product_list")  # redirige a la lista de productos
    else:
        form = ProductForm()
    return render(request, "add_product.html", {"form": form})

# Solo admin
# --- Editar producto ---
@login_required
@user_passes_test(is_admin)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "edit_product.html", {"form": form, "product": product})

# --- Eliminar producto ---
@login_required
@user_passes_test(is_admin)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "delete_product.html", {"product": product})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})




@login_required
def wishlist_view(request):
    customer = request.user.customer
    items = Wishlist.objects.filter(customer=customer)
    return render(request, 'wishlist.html', {'items': items})

from django.http import JsonResponse

@login_required
def toggle_wishlist(request, product_id):
    customer = request.user.customer
    product = get_object_or_404(Product, id_product=product_id)

    # buscar si ya está en wishlist
    wishlist_item = Wishlist.objects.filter(customer=customer, product=product)
    if wishlist_item.exists():
        wishlist_item.delete()
        in_wishlist = False
    else:
        Wishlist.objects.create(customer=customer, product=product)
        in_wishlist = True


    # Si es una solicitud AJAX, devolver JSON para actualizar icono en lugar de redirigir
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if is_ajax:
        return JsonResponse({
            "success": True,
            "in_wishlist": in_wishlist,
            "product_id": product_id,
            "message": "Added to wishlist" if in_wishlist else "Removed from wishlist",
        })

    # Fallback normal (no AJAX)
    return redirect("wishlist")