from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, ListView, TemplateView
from catalogo.models import Product, Review
from users.models import Customer # 👈 agrega Custome
from .models import Wishlist, Product
from .forms import ReviewForm, ProductForm
from django.db.models import Q


def is_admin(user):
    return user.is_staff

# ---------- Home ----------
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/partials/product_detail_modal.html", {"product": product})

# ---------- Productos ----------
class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product= self.get_object()  # safer than self.object if object isn't set
        context["reviews"] = Review.objects.filter(product=product, approved=True)
        context["review_form"] = ReviewForm()  # 👈 form para el POST
        return context


class ProductSearchView(ListView):
    model = Product
    template_name = "product_search.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Product.objects.filter(name__icontains=query)
    


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


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"
    paginate_by = 9  # Paginación, 9 productos por página

    def get_queryset(self):
        queryset = Product.objects.all()

        # 🔎 Búsqueda
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
            )

        # 🔎 Filtros
        category = self.request.GET.get("category")
        if category:
            # aquí buscamos tanto si tiene prefijo como si está limpio
            queryset = queryset.filter(
                Q(category=category) | Q(category__endswith=f":{category}")
            )

        nutriscore = self.request.GET.get("nutriscore")
        if nutriscore:
            queryset = queryset.filter(nutriscore=nutriscore)

        # 🔎 Ordenar por precio
        sort = self.request.GET.get("sort")
        if sort == "price_asc":
            queryset = queryset.order_by("price")
        elif sort == "price_desc":
            queryset = queryset.order_by("-price")

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
        context["nutriscores"] = Product.objects.values_list("nutriscore", flat=True).distinct()

        # mantener filtros actuales, pero quitar "page"
        current_filters = self.request.GET.copy()
        if "page" in current_filters:
            current_filters.pop("page")
        context["current_filters"] = current_filters
        
        return context


@login_required
def wishlist_view(request):
    customer = request.user.customer
    items = Wishlist.objects.filter(customer=customer)
    return render(request, 'wishlist.html', {'items': items})

@login_required
def add_to_wishlist(request, product_id):
    customer = request.user.customer
    product = get_object_or_404(Product, id_product=product_id)
    Wishlist.objects.get_or_create(customer=customer, product=product)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    customer = request.user.customer
    product = get_object_or_404(Product, id_product=product_id)
    Wishlist.objects.filter(customer=customer, product=product).delete()
    return redirect('wishlist')
