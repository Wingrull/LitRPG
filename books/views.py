from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Series, Review, Rating
from .serializers import SeriesSerializer, ReviewSerializer, RatingSerializer

def series_list(request):
    series = Series.objects.all().order_by('-added_at')  # Сортировка по дате добавления, новые сверху
    return render(request, 'books/series_list.html', {'series': series})

def series_detail(request, pk):
    series = get_object_or_404(Series, pk=pk)
    books = series.books.order_by('order_in_series')  # Книги по порядку
    return render(request, 'books/series_detail.html', {'series': series, 'books': books})


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all().order_by('-added_at')
    serializer_class = SeriesSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer