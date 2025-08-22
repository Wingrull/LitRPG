import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const SeriesList = () => {
    const [series, setSeries] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/series/')
            .then(response => setSeries(response.data))
            .catch(error => console.error('Ошибка загрузки серий:', error));
    }, []);

    return (
        <div>
            <h2>Список серий</h2>
            <ul>
                {series.map(s => (
                    <li key={s.id}>
                        <Link to={`/series/${s.id}`}>
                            {s.cover_image && (
                                <img src={s.cover_image} alt={`${s.title} обложка`} style={{ width: '100px', height: 'auto' }} />
                            )}
                            {s.title} ({s.author}) - Книг: {s.book_count}, Рейтинг: {s.average_rating || 'Нет рейтинга'}
                            {s.is_completed && ' (Завершена)'}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SeriesList;