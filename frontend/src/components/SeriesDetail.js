import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const SeriesDetail = () => {
    const { id } = useParams();
    const [series, setSeries] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get(`http://localhost:8000/api/series/${id}/`)
            .then(response => setSeries(response.data))
            .catch(error => {
                console.error('Ошибка загрузки серии:', error);
                setError('Не удалось загрузить серию');
            });
    }, [id]);

    if (error) return <div>{error}</div>;
    if (!series) return <div>Загрузка...</div>;

    return (
        <div>
            <h1>{series.title} by {series.author}</h1>
            {series.cover_image && (
                <img src={series.cover_image} alt={`${series.title} обложка`} style={{ maxWidth: '200px', height: 'auto' }} />
            )}
            <p>{series.description}</p>
            <p>Книг: {series.book_count} | Рейтинг: {series.average_rating || 'Нет рейтинга'} | {series.is_completed ? 'Завершена' : 'Не завершена'}</p>
            <p>Добавлена: {series.added_at}</p>

            <h2>Книги</h2>
            <ul>
                {series.books && series.books.length > 0 ? (
                    series.books.map(book => (
                        <li key={book.id}>
                            {book.cover_image && (
                                <img src={book.cover_image} alt={`${book.title} обложка`} style={{ width: '80px', height: 'auto' }} />
                            )}
                            {book.title} (№{book.order_in_series}) - {book.publication_year}
                        </li>
                    ))
                ) : (
                    <li>Книги отсутствуют</li>
                )}
            </ul>

            <h2>Отзывы</h2>
            <ul>
                {series.reviews && series.reviews.length > 0 ? (
                    series.reviews.map(review => (
                        <li key={review.id}>{review.text} ({review.user})</li>
                    ))
                ) : (
                    <li>Отзывы отсутствуют</li>
                )}
            </ul>
        </div>
    );
};

export default SeriesDetail;