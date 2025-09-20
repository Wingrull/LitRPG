""" Пример программного добавления серий и книг в базу данных """

from django.utils import timezone
from books.models import Series, Book, Genre
from datetime import date
import xml.etree.ElementTree as ET
import base64
from django.core.files.base import ContentFile


# Функция для парсинга одного FB2-файла и извлечения данных
def parse_fb2(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'}

    # Извлечение заголовка книги
    title = root.find('.//fb:title-info/fb:book-title', ns).text

    # Извлечение автора
    author_first = root.find('.//fb:title-info/fb:author/fb:first-name', ns)
    author_last = root.find('.//fb:title-info/fb:author/fb:last-name', ns)
    author = f"{author_first.text if author_first is not None else ''} {author_last.text if author_last is not None else ''}".strip()

    # Извлечение жанров
    genres = [g.text for g in root.findall('.//fb:title-info/fb:genre', ns)]

    # Извлечение описания (аннотации)
    annotation = root.find('.//fb:title-info/fb:annotation', ns)
    description = ET.tostring(annotation, encoding='unicode') if annotation is not None else ''

    # Извлечение обложки (binary)
    cover = root.find('.//fb:binary[@id="cover.jpg"]', ns)
    cover_content_type = cover.get('content-type') if cover is not None else None
    cover_image = base64.b64decode(cover.text) if cover is not None else None

    # Извлечение года публикации (если есть)
    year = root.find('.//fb:title-info/fb:date', ns)
    publication_year = int(year.text[:4]) if year is not None and year.text else None

    return {
        'title': title,
        'author': author,
        'genres': genres,
        'description': description,
        'cover_image': cover_image,
        'cover_content_type': cover_content_type,
        'publication_year': publication_year
    }


# Пример добавления серии и книг
def add_series_and_books():
    # Создаем жанры, если они не существуют
    genre_names = ['Ранобе', 'Фэнтези']
    genres = []
    for name in genre_names:
        genre, created = Genre.objects.get_or_create(name=name)
        genres.append(genre)

    # Создаем серию
    series, created = Series.objects.get_or_create(
        title="Убийцы Драконов",
        author="Ши-Лоу Е",
        defaults={
            'description': 'Описание серии Убийцы Драконов',
            'is_completed': True,  # Предполагаем, что серия завершена
            'added_at': timezone.now()
        }
    )
    series.genres.add(*genres)
    series.save()

    # Список файлов FB2 для книг в серии
    fb2_files = [
        "Убийцы Драконов 1. Убийцы Драконов I.fb2",
        "Убийцы Драконов 2. Убийцы Драконов II.fb2",
        "Убийцы Драконов 3. Убийцы Драконов III.fb2",
        "Убийцы Драконов 4. Убийцы Драконов IV.fb2",
        "Убийцы Драконов 5. Убийцы Драконов V.fb2",
        "Убийцы Драконов 6. Убийцы Драконов VI.fb2",
        "Убийцы Драконов 7. Убийцы Драконов VII.fb2",
        "Убийцы Драконов 8. Убийцы Драконов VIII.fb2",
    ]

    # Парсим каждый файл и добавляем книгу
    for index, fb2_file in enumerate(fb2_files, start=1):
        book_data = parse_fb2(fb2_file)  # Предполагаем, что файлы находятся в текущей директории или укажите путь

        book = Book.objects.create(
            series=series,
            title=book_data['title'],
            description=book_data['description'],
            order_in_series=index,
            publication_year=book_data['publication_year'] or 2016,  # Если год не указан, используем 2016
            cover_image=book_data['cover_image'],
            cover_content_type=book_data['cover_content_type']
        )
        book.save()

    # Устанавливаем дату добавления серии (27 марта 2016)
    series.added_at = timezone.make_aware(timezone.datetime(2016, 3, 27))
    series.save()

# Запуск функции
# add_series_and_books()
