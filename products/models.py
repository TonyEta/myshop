from django.db import models
from django.utils.text import slugify
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            orig_slug = self.slug
            counter = 1

            while Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{orig_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            orig_slug = self.slug
            counter = 1

            while Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{orig_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)
    
    @property
    def short_recomendation(self):
        spec = self.specifications.filter(name='Recomendation_under_photo').first()

        return spec.value if spec else ''

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name}-{self.value}"