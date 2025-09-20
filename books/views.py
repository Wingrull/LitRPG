from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from rest_framework import viewsets
from .models import Series, Book, Review, Rating, UserSeriesStatus
from .serializers import SeriesSerializer, BookSerializer, ReviewSerializer, RatingSerializer
from django.contrib.auth.decorators import login_required


# Представления для шаблонов
def series_list(request):
    series_list = Series.objects.all()
    show_unread_only = request.GET.get('show_unread_only', False)

    # Подготовка списка серий с их статусами
    series_with_status = []
    for series in series_list:
        status = None
        if request.user.is_authenticated:
            status_obj = series.user_statuses.filter(user=request.user).first()
            status = status_obj.get_status_display() if status_obj else "Не прочитано"
        series_with_status.append({
            'series': series,
            'status': status
        })

    # Фильтрация по "только не прочитанные"
    if show_unread_only and request.user.is_authenticated:
        series_list = series_list.exclude(
            user_statuses__user=request.user,
            user_statuses__status__in=['READ', 'PARTIAL']
        )
        series_with_status = [
            item for item in series_with_status
            if item['series'] in series_list
        ]

    return render(request, 'series_list.html', {
        'series_with_status': series_with_status,
        'show_unread_only': show_unread_only
    })


def series_detail(request, pk):
    series = get_object_or_404(Series, pk=pk)
    # Получаем статус серии для текущего пользователя
    user_status = None
    if request.user.is_authenticated:
        status_obj = series.user_statuses.filter(user=request.user).first()
        user_status = status_obj.status if status_obj else 'UNREAD'
    return render(request, 'series_detail.html', {
        'series': series,
        'user_status': user_status
    })


@login_required
def set_series_status(request, pk):
    series = get_object_or_404(Series, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['READ', 'PARTIAL', 'UNREAD']:
            UserSeriesStatus.objects.update_or_create(
                user=request.user,
                series=series,
                defaults={'status': status}
            )
            messages.success(request, f'Статус для "{series.title}" обновлён.')
        return redirect('series_detail', pk=series.id)
    return redirect('series_detail', pk=series.id)


# Представления для авторизации
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} успешно создан! Пожалуйста, войдите.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('series_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли.')
    return redirect('series_list')


# API представления
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