from django.urls import path
from .views import series_list, series_detail



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'series', views.SeriesViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'ratings', views.RatingViewSet)


urlpatterns = [
    path('', series_list, name='series_list'),
    path('series/<int:pk>/', series_detail, name='series_detail'),
    path('api/', include(router.urls)),
]
