from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'series', views.SeriesViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'ratings', views.RatingViewSet)

urlpatterns = [
    path('', views.series_list, name='series_list'),
    path('series/<int:pk>/', views.series_detail, name='series_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
]