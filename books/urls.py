from django.urls import path
from .views import series_list, series_detail



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeriesViewSet, ReviewViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'series', SeriesViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'ratings', RatingViewSet)


urlpatterns = [
    path('', series_list, name='series_list'),
    path('series/<int:pk>/', series_detail, name='series_detail'),
    path('api/', include(router.urls)),
]
