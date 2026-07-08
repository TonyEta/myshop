from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase

from .models import Category, Product
from .views import ProductList


class ProductListTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='Malt', slug='malt')
        self.product = Product.objects.create(
            name='Pilsner Malt',
            description='Test product',
            price=9.99,
            category=self.category,
            image=SimpleUploadedFile(
                'test.jpg',
                b'fake-image-bytes',
                content_type='image/jpeg',
            ),
        )

    def test_filters_products_by_category_name(self):
        request = self.factory.get('/products/', {'category': 'Malt'})
        view = ProductList()
        view.setup(request=request)

        queryset = view.get_queryset()

        self.assertIn(self.product, queryset)
