from django.urls import path
from . import views
urlpatterns = [
    path('category/',views.CategoryViews.as_view()),
    path('category/<int:pk>',views.CategoryOneViews.as_view()),
    path('product/',views.ProductViews.as_view()),
    path('product/<int:pk>/',views.ProductOneViews.as_view()),
    path('photos/<int:pk>/like/',views. PhotoLikeView.as_view()),
]