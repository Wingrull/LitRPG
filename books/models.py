from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Series(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.BinaryField(null=True, blank=True)
    cover_content_type = models.CharField(max_length=50, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='series', blank=True)

    def __str__(self):
        return self.title

    @property
    def book_count(self):
        return self.books.count()

    @property
    def average_rating(self):
        avg = self.ratings.aggregate(Avg('value'))['value__avg']
        return avg if avg else 0


class Book(models.Model):
    series = models.ForeignKey(Series, related_name='books', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order_in_series = models.PositiveIntegerField()
    publication_year = models.PositiveIntegerField()
    cover_image = models.BinaryField(null=True, blank=True)
    cover_content_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.title} (Series: {self.series.title})"


class Review(models.Model):
    series = models.ForeignKey(Series, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.series.title} by {self.user.username}"


class Rating(models.Model):
    series = models.ForeignKey(Series, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Rating {self.value} for {self.series.title}"


class UserSeriesStatus(models.Model):
    STATUS_CHOICES = (
        ('READ', 'Прочитано'),
        ('PARTIAL', 'Не дочитал'),
        ('UNREAD', 'Не прочитано'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='series_statuses')
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='user_statuses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNREAD')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'series')  # Один пользователь — один статус для серии

    def __str__(self):
        return f"{self.user.username} - {self.series.title}: {self.get_status_display()}"
