from django.contrib import admin
from django import forms
from django.utils.html import format_html
import base64
from .models import Series, Book, Review, Rating, Genre, UserSeriesStatus


# Кастомные формы для Series и Book
class SeriesAdminForm(forms.ModelForm):
    cover_file = forms.FileField(required=False, label="Загрузить обложку (файл)")

    class Meta:
        model = Series
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        cover_file = self.cleaned_data.get('cover_file')
        if cover_file:
            instance.cover_image = cover_file.read()
            instance.cover_content_type = cover_file.content_type
        else:
            if not self.cleaned_data.get('cover_image'):
                instance.cover_image = None
                instance.cover_content_type = None
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class BookAdminForm(forms.ModelForm):
    cover_file = forms.FileField(required=False, label="Загрузить обложку (файл)")

    class Meta:
        model = Book
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        cover_file = self.cleaned_data.get('cover_file')
        if cover_file:
            instance.cover_image = cover_file.read()
            instance.cover_content_type = cover_file.content_type
        else:
            if not self.cleaned_data.get('cover_image'):
                instance.cover_image = None
                instance.cover_content_type = None
        if commit:
            instance.save()
        return instance


# Inline для книг
class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    form = BookAdminForm


# Кастомный фильтр для жанров
class GenreFilter(admin.SimpleListFilter):
    title = 'Жанры'
    parameter_name = 'genre'

    def lookups(self, request, model_admin):
        return [(genre.id, genre.name) for genre in Genre.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(genres__id=self.value())
        return queryset


# Админка для Series
@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'author', 'book_count', 'average_rating', 'is_completed', 'added_at', 'cover_preview', 'get_genres')
    list_filter = ('is_completed', GenreFilter)
    search_fields = ('title', 'author')
    inlines = [BookInline]
    form = SeriesAdminForm
    readonly_fields = ('cover_preview',)

    def get_genres(self, obj):
        try:
            return ", ".join([genre.name for genre in obj.genres.all()]) if hasattr(obj, 'genres') else "Нет жанров"
        except AttributeError:
            return "Нет жанров"

    get_genres.short_description = "Жанры"

    def cover_preview(self, obj):
        if obj.cover_image:
            base64_data = base64.b64encode(obj.cover_image).decode('utf-8')
            return format_html('<img src="data:{};base64,{}" width="100" height="auto" />', obj.cover_content_type,
                               base64_data)
        return "Нет обложки"

    cover_preview.short_description = "Предпросмотр обложки"


# Админка для Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'series', 'order_in_series', 'publication_year', 'cover_preview')
    list_filter = ('series',)
    search_fields = ('title',)
    form = BookAdminForm
    readonly_fields = ('cover_preview',)

    def cover_preview(self, obj):
        if obj.cover_image:
            base64_data = base64.b64encode(obj.cover_image).decode('utf-8')
            return format_html('<img src="data:{};base64,{}" width="80" height="auto" />', obj.cover_content_type,
                               base64_data)
        return "Нет обложки"

    cover_preview.short_description = "Предпросмотр обложки"


# Админка для Genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Админка для UserSeriesStatus
@admin.register(UserSeriesStatus)
class UserSeriesStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'series', 'status', 'updated_at')
    list_filter = ('status', 'user')
    search_fields = ('user__username', 'series__title')


# Регистрация остальных моделей
admin.site.register(Review)
admin.site.register(Rating)
