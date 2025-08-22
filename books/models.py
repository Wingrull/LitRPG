from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg  # Для вычисления среднего рейтинга


class Series(models.Model):
    title = models.CharField(max_length=200)  # Название серии
    author = models.CharField(max_length=200)  # Автор(ы), можно сделать ManyToMany если несколько
    description = models.TextField()  # Описание серии
    is_completed = models.BooleanField(default=False)  # Завершена ли серия (приоритет для законченных)
    added_at = models.DateTimeField(auto_now_add=True)  # Дата добавления на сайт
    cover_image = models.BinaryField(null=True, blank=True)  # Бинарные данные обложки
    cover_content_type = models.CharField(max_length=50, null=True, blank=True)  # MIME-тип, например 'image/jpeg'

    def __str__(self):
        return self.title

    @property
    def book_count(self):
        """Вычисляемое поле: количество книг в серии"""
        return self.books.count()  # 'books' — related_name из модели Book

    @property
    def average_rating(self):
        """Вычисляемое поле: средний рейтинг серии"""
        avg = self.ratings.aggregate(Avg('value'))['value__avg']
        return avg if avg else 0


class Book(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='books')  # Связь с серией
    title = models.CharField(max_length=200)  # Название книги
    order_in_series = models.IntegerField(default=1)  # Порядковый номер в серии (1, 2, 3...)
    description = models.TextField()  # Описание книги
    publication_year = models.IntegerField()  # Год издания
    cover_image = models.BinaryField(null=True, blank=True)
    cover_content_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.title} (книга {self.order_in_series} в серии {self.series.title})"


class Review(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='reviews')  # Связь с серией
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв на серию {self.series.title} от {self.user.username}"


class Rating(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='ratings')  # Связь с серией
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('series', 'user')  # Один пользователь — один рейтинг на серию

    def __str__(self):
        return f"Рейтинг {self.value} для серии {self.series.title}"
