from django.contrib import admin
from .models import Product, Category, ProductSpecification


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_active', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSpecificationInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}