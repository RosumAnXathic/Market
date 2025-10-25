from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255,unique=True)
    images=models.ImageField(upload_to='category_image')

    def __str__(self):
        return f"{self.name} Id:{self.id}"
 
class Product(models.Model):
    name =models.CharField(max_length=255,unique=True)
    price  = models.DecimalField(max_digits=10, decimal_places=2)
    description =models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} Id:{self.id}"
 
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return f"Image for {self.product.name} (Product ID: {self.product.id})"

class PhotoLike(models.Model):
    """Модель лайков для фотографий товаров"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_likes')
    photo = models.ForeignKey(ProductImage, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')  # один пользователь = один лайк на фото

    def __str__(self):
        return f"{self.user.username} liked {self.photo}"


        
