from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import OpenApiRequest, extend_schema
from . import models
from .models import PhotoLike, ProductImage
from . import serializers
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import GenericAPIView

class CategoryViews(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="List all categories with products",
        description="Returns a list of all categories along with their related products.",
        responses=serializers.CategoryProductSerializer(many=True),
    )
    def get(self, request):
        categories = models.Category.objects.all()
        serializer = serializers.CategoryProductSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a new category",
        description="Creates a new category. Requires a name and an image (multipart/form-data).",
        request={
            'multipart/form-data': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'default': 'Default Category Name',
                        },
                        'images': {
                            'type': 'string',
                            'format': 'binary',
                            'default': None,
                        }
                    },
                    'required': ['name', 'images']
                }
        },
        responses=serializers.CategorySerializer,
    )
    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryOneViews(APIView):
    @extend_schema(
        summary="Get a single category by ID with its products",
        description="Retrieve a specific category by its ID. Includes all related products.",
        responses=serializers.CategoryProductSerializer,
    )
    def get(self, request, pk):
        try:
            category = models.Category.objects.get(id=pk)
            serializer = serializers.CategoryProductSerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Delete a category by ID",
        description="Deletes the category with the specified ID, along with its related products.",
        responses={204: None}
    )
    def delete(self, request, pk=None):
        try:
            category = models.Category.objects.get(id=pk)
        except models.Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class ProductViews(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        summary="List all products with their category",
        description="Returns a list of all products along with their related category information.",
        responses=serializers.ProductGetSerializer(many=True),
    )
    def get(self, request):
        products = models.Product.objects.all()
        serializer = serializers.ProductGetSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a new product",
        description="Creates a new product. Requires a name, price, category, and up to 5 images (multipart/form-data).",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'default': 'Default Product Name'},
                    'price': {'type': 'number', 'format': 'float', 'default': 0.0},
                    'category': {'type': 'integer', 'default': 1},
                    'upload_images': {
                        'type': 'array',
                        'items': {'type': 'string', 'format': 'binary'},
                        'maxItems':  5,
                        'default': None
                    },
                    'description': {'type': 'string', 'default': 'Product description here'}
                },
                'required': ['name', 'price', 'category', 'upload_images']
            }
        },
        responses=serializers.ProductUpdateSerializer,
    )
    
    def post(self, request):
        serializer = serializers.ProductUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductOneViews(APIView):
    @extend_schema(
        summary="Get a single product by ID",
        description="Retrieve a specific product by its ID, including its images and category.",
        responses=serializers.ProductGetSerializer,
    )
    def get(self, request, pk):
        try:
            product = models.Product.objects.get(id=pk)
            serializer = serializers.ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Delete a product by ID",
        description="Deletes the product with the specified ID.",
        responses={204: None}
    )
    def delete(self, request, pk):
        try:
            product = models.Product.objects.get(id=pk)
        except models.Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
            summary="Update a product by ID",
            description="Updates the product with the specified ID.",
        request={
                'multipart/form-data': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'default': 'Default Product Name',
                        },
                        'price': {
                            'type': 'number',
                            'format': 'float',
                            'default': 0.0,
                        },
                        'category': {
                            'type': 'integer',
                            'default': 1,  
                        },
                        'description': {
                            'type': 'string',
                            'default': 'Product description here',
                        }
                    },
                    'required': ['name', 'price', 'category', 'description']
                }
            },
            responses=serializers.ProductUpdateSerializer,
        )
    def put(self, request, pk):
        try:
            product = models.Product.objects.get(id=pk)
        except models.Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ProductUpdateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhotoLikeView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.PhotoLikeRequestSerializer  # Обязательно укажи сериализатор
    
    @extend_schema(
        summary="Check if user liked/disliked photo",
        description="GET возвращает состояние лайка пользователя",
        responses=serializers.PhotoLikeStateSerializer  # Укажи сериализатор ответа для GET
    )
    def get(self, request, pk):
        like_obj = PhotoLike.objects.filter(user=request.user, photo_id=pk).first()
        if not like_obj:
            state = None
        elif like_obj.is_like:
            state = "liked"
        else:
            state = "disliked"
        return Response({'state': state}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Like or dislike product photo",
        description="POST с 'action' = like/dislike. Тогглит состояние лайка/дизлайка.",
        request=serializers.PhotoLikeRequestSerializer,  # Обязательно указать сериализатор для тела запроса
        responses=serializers.PhotoLikeStateLikesCountSerializer  # И сериализатор для ответа
    )
    def post(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data['action']

        photo = ProductImage.objects.filter(pk=pk).first()
        if not photo:
            return Response({'detail': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

        like_obj, created = PhotoLike.objects.get_or_create(user=request.user, photo=photo)

        if action == 'like':
            if not created and like_obj.is_like:
                like_obj.delete()
                state = None
            else:
                like_obj.is_like = True
                like_obj.save()
                state = 'liked'
        else:  # dislike
            if not created and not like_obj.is_like:
                like_obj.delete()
                state = None
            else:
                like_obj.is_like = False
                like_obj.save()
                state = 'disliked'

        likes_count = photo.likes.filter(is_like=True).count()
        dislikes_count = photo.likes.filter(is_like=False).count()

        return Response({
            'state': state,
            'likes_count': likes_count,
            'dislikes_count': dislikes_count
        }, status=status.HTTP_200_OK)