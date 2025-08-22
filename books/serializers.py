from rest_framework import serializers
from .models import Series, Book, Review, Rating

import base64


class BookSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    def get_cover_image(self, obj):
        if obj.cover_image:
            base64_data = base64.b64encode(obj.cover_image).decode('utf-8')
            return f"data:{obj.cover_content_type};base64,{base64_data}"
        return None

    class Meta:
        model = Book
        fields = ['id', 'title', 'order_in_series', 'description', 'publication_year', 'cover_image']


class SeriesSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    book_count = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    cover_image = serializers.SerializerMethodField()

    def get_cover_image(self, obj):
        if obj.cover_image:
            base64_data = base64.b64encode(obj.cover_image).decode('utf-8')
            return f"data:{obj.cover_content_type};base64,{base64_data}"
        return None

    class Meta:
        model = Series
        fields = ['id', 'title', 'author', 'description', 'is_completed', 'added_at', 'book_count', 'average_rating',
                  'books', 'cover_image']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Имя пользователя вместо ID

    class Meta:
        model = Review
        fields = ['id', 'series', 'user', 'text', 'created_at']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Rating
        fields = ['id', 'series', 'user', 'value', 'created_at']
