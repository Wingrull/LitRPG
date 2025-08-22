from django.contrib import admin
from django import forms
from django.utils.html import format_html
import base64
from .models import Series, Book, Review, Rating, Genre


# Кастомная форма для Series
class SeriesAdminForm(forms.ModelForm):
    cover_file = forms.FileField(required=False, label="Загрузить обложку (файл)")  # Поле для загрузки файла

    class Meta:
        model = Series
        fields = '__all__'  # Включаем все поля модели

    def save(self, commit=True):
        instance = super().save(commit=False)  # Получаем объект, но не сохраняем в БД
        cover_file = self.cleaned_data.get('cover_file')  # Получаем загруженный файл
        if cover_file:
            instance.cover_image = cover_file.read()  # Читаем байты файла
            instance.cover_content_type = cover_file.content_type  # Сохраняем MIME-тип
        else:
            # Если файл не загружен, но поля очищены, обнуляем
            if not self.cleaned_data.get('cover_image'):
                instance.cover_image = None
                instance.cover_content_type = None
        if commit:
            instance.save()
        return instance

# Кастомная форма для Book
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

# Inline для книг в админке Series
class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    form = BookAdminForm  # Привязываем кастомную форму для книг в inline


# Кастомный фильтр для жанров
class GenreFilter(admin.SimpleListFilter):
    title = 'Жанры'  # Название фильтра в админке
    parameter_name = 'genre'  # Параметр в URL (например, ?genre=1)

    def lookups(self, request, model_admin):
        # Возвращает список жанров для фильтра
        return [(genre.id, genre.name) for genre in Genre.objects.all()]

    def queryset(self, request, queryset):
        # Фильтрует серии по выбранному жанру
        if self.value():
            return queryset.filter(genres__id=self.value())
        return queryset


# Админка для Series
@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'book_count', 'average_rating', 'is_completed', 'added_at', 'cover_preview', 'get_genres')
    list_filter = ('is_completed', GenreFilter)  # Используем кастомный фильтр
    search_fields = ('title', 'author')
    inlines = [BookInline]
    form = SeriesAdminForm  # Привязываем кастомную форму
    readonly_fields = ('cover_preview',)

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = "Жанры"

    def cover_preview(self, obj):
        if obj.cover_image:
            base64_data = base64.b64encode(obj.cover_image).decode('utf-8')
            data_url = f"data:{obj.cover_content_type};base64,{base64_data}"
            return format_html('<img src="{}" width="100" height="auto" />', data_url)
        return "Нет обложки"

    cover_preview.short_description = "Предпросмотр обложки"


# Админка для Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'series', 'order_in_series', 'publication_year', 'cover_preview')
    list_filter = ('series',)
    search_fields = ('title',)
    form = BookAdminForm  # Привязываем кастомную форму
    readonly_fields = ('cover_preview',)

    def cover_preview(self, obj):
        if obj.cover_image:
            base64_data = base64.b64encode(obj.cover_image).decode('utf-8')
            data_url = f"data:{obj.cover_content_type};base64,{base64_data}"
            return format_html('<img src="{}" width="80" height="auto" />', data_url)
        return "Нет обложки"

    cover_preview.short_description = "Предпросмотр обложки"


# Админка для Genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Регистрация остальных моделей
admin.site.register(Review)
admin.site.register(Rating)
