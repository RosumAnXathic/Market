from . import models
from typing import Optional, List
from rest_framework import serializers
from .models import Product, ProductImage, Category, PhotoLike

class ProductImageSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'likes_count', 'dislikes_count']  # Add other fields you need

    def get_likes_count(self, obj) -> str:
        # Count of likes where is_like=True
        return obj.likes.filter(is_like=True).count()

    def get_dislikes_count(self, obj) -> str:
        # Count of dislikes where is_like=False
        return obj.likes.filter(is_like=False).count()


    def get_liked_users(self, obj) -> List[str]:
        return [like.user.username for like in obj.likes.filter(is_like=True)]

    def to_representation(self, instance):
        """Убираем liked_by_user, если None"""
        rep = super().to_representation(instance)
        if rep.get('liked_by_user') is None:
            rep.pop('liked_by_user')
        return rep


class ProductGetSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'description', 'images', 'upload_images']

    def to_representation(self, instance):
        """Передаём context для вложенного сериализатора images"""
        rep = super().to_representation(instance)
        rep['images'] = ProductImageSerializer(
            instance.images.all(),
            many=True,
            context=self.context
        ).data
        return rep
                

    def create(self, validated_data):
        images = validated_data.pop('upload_images', [])
        product = Product.objects.create(**validated_data)
        for img in images:
            ProductImage.objects.create(product=product, image=img)
        return product

class ProductUpdateSerializer(serializers.ModelSerializer):
    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'description', 'upload_images', 'images']

    def validate_upload_images(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("Можно загрузить максимум 5 изображений одновременно.")
        return value

    def get_images(self, obj) -> list[str]:
        return [img.image.url for img in obj.images.all()]

    def create(self, validated_data):
        images = validated_data.pop('upload_images', [])
        product = Product.objects.create(**validated_data)
        for img in images:
            ProductImage.objects.create(product=product, image=img)
        return product

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr != 'upload_images':
                setattr(instance, attr, value)
        instance.save()

        images = validated_data.get('upload_images', [])
        if images:
            if len(images) + instance.images.count() > 5:
                raise serializers.ValidationError("Общее количество изображений не может превышать 5.")
            for img in images:
                ProductImage.objects.create(product=instance, image=img)
        return instance

    def validate(self, attrs):
        if 'price' in attrs and attrs['price'] == "":
            attrs['price'] = None
        if 'category' in attrs and attrs['category'] == "":
            attrs['category'] = None
        return attrs

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'images']


class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductGetSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'images', 'products']

    def to_representation(self, instance):
        """Передаём context для вложенных сериализаторов"""
        rep = super().to_representation(instance)
        rep['products'] = ProductGetSerializer(
            instance.products.all(),
            many=True,
            context=self.context
        ).data
        return rep
    


class PhotoLikeRequestSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['like', 'dislike'])

class PhotoLikeStateSerializer(serializers.Serializer):
    state = serializers.CharField(allow_null=True)

class PhotoLikeStateLikesCountSerializer(serializers.Serializer):
    state = serializers.CharField(allow_null=True)
    likes_count = serializers.IntegerField()
    dislikes_count = serializers.IntegerField()