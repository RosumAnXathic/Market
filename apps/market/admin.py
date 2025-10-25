from django.contrib import admin

from .models import Product, Category, ProductImage, PhotoLike


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Քանի դատարկ դաշտ ցույց տա նոր նկար ավելացնելու համար

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(PhotoLike)