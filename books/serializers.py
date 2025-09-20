from rest_framework import serializers
from .models import Series, Book, Review, Rating, Genre, UserSeriesStatus
import base64


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


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
    genres = GenreSerializer(many=True, read_only=True)
    book_count = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    cover_image = serializers.SerializerMethodField()
    user_status = serializers.SerializerMethodField()

    def get_cover_image(self, obj):
        if obj.cover_image:
            base64_data = base64.b64encode(obj.cover_image).decode('utf-8')
            return f"data:{obj.cover_content_type};base64,{base64_data}"
        return None

    def get_user_status(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            status = obj.user_statuses.filter(user=user).first()
            return status.status if status else 'UNREAD'
        return None

    class Meta:
        model = Series
        fields = ['id', 'title', 'author', 'description', 'is_completed', 'added_at', 'book_count', 'average_rating',
                  'books', 'cover_image', 'genres', 'user_status']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
