from django.test import TestCase
from django.urls import reverse
from leaf_and_root.carrito.models import Cart, ItemCart
from leaf_and_root.ordenes.models import Order
from leaf_and_root.catalogo.models import Product, Review, Wishlist
from leaf_and_root.users.models import Customer


class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name="Django for Beginners",
            price=59.99,
            category="Books",
            stock=10
        )
        self.assertEqual(product.name, "Django for Beginners")
        self.assertEqual(str(product), "Django for Beginners")


class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        customer = Customer.objects.create(
            name="Luis",
            email="luis@test.com",
            phone="123456789"
        )
        self.assertEqual(customer.name, "Luis")
        self.assertEqual(customer.email, "luis@test.com")


class CartAndItemTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Juan",
            email="juan@test.com",
            phone="987654321"
        )
        self.product = Product.objects.create(
            name="Laptop",
            price=1200.00,
            category="Electronics",
            stock=5
        )
        self.cart = Cart.objects.create(customer=self.customer)

    def test_add_item_to_cart(self):
        item = ItemCart.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.product.name, "Laptop")
        self.assertEqual(item.cart.customer.name, "Juan")


class OrderTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Ana",
            email="ana@test.com",
            phone="111222333"
        )
        self.order = Order.objects.create(customer=self.customer, status="Pending")

    def test_order_creation(self):
        self.assertEqual(self.order.customer.name, "Ana")
        self.assertEqual(self.order.status, "Pending")


# 🚨 IMPORTANTE:
# Solo dejo las pruebas de views si realmente tienes definidas
# las URLs "store:product_list" y "store:product_detail".
# Si no, Django va a lanzar NoReverseMatch.
# Te las ajusto a algo genérico, pero puedes comentarlas si aún no tienes vistas.

class ViewsTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Smartphone",
            price=299.99,
            category="Gadgets",
            stock=15
        )

    def test_product_list_view(self):
        response = self.client.get(reverse("store:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smartphone")

    def test_product_detail_view(self):
        response = self.client.get(reverse("store:product_detail", args=[self.product.id_product]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smartphone")
