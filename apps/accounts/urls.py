from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView,UserDetailView, AdminUserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('admin-user/', AdminUserDetailView.as_view(), name='admin-user-detail'),
]