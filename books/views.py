from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Series, Book, Review, Rating
from .serializers import SeriesSerializer, BookSerializer, ReviewSerializer, RatingSerializer


# Представления для шаблонов
def series_list(request):
    series_list = Series.objects.all()
    return render(request, 'series_list.html', {'series_list': series_list})


def series_detail(request, pk):
    series = get_object_or_404(Series, pk=pk)
    return render(request, 'series_detail.html', {'series': series})


# API представления (остаются без изменений)
class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
