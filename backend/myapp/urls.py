from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/authcheck/', views.AuthCheckView.as_view(), name='authcheck'),
    
    path('api/users/', views.CreateUserView.as_view(), name='create-user'),
    
    path('api/books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('api/annotations/', views.AnnotationListCreateView.as_view(), name='annotation-list-create'),
    path('api/annotations/<int:pk>/', views.AnnotationDetailView.as_view(), name='annotation-detail'),
]