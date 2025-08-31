from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category, Order, OrderItem
from .forms import ProductForm

class CategoryModelTest(TestCase):
    def test_category_str(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(str(category), "Electronics")

class ProductModelTest(TestCase):
    def test_product_creation(self):
        category = Category.objects.create(name="Books")
        product = Product.objects.create(
            name="Django for Beginners",
            price=59.99,
            category=category
        )
        self.assertEqual(product.name, "Django for Beginners")
        self.assertEqual(str(product), "Django for Beginners")

class ProductFormTest(TestCase):
    def test_valid_product_form(self):
        category = Category.objects.create(name="Clothes")
        form_data = {
            "name": "T-Shirt",
            "price": 19.99,
            "category": category.id
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_product_form(self):
        form = ProductForm(data={"name": ""})
        self.assertFalse(form.is_valid())

class ViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Gadgets")
        self.product = Product.objects.create(
            name="Smartphone", price=299.99, category=self.category
        )

    def test_product_list_view(self):
        url = reverse("store:product_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smartphone")

    def test_product_detail_view(self):
        url = reverse("store:product_detail", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smartphone")
