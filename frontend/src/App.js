import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SeriesList from './components/SeriesList';
import SeriesDetail from './components/SeriesDetail';
import './App.css';

function App() {
    return (
        <Router>
            <div className="App">
                <h1>Библиотека серий книг</h1>
                <Routes>
                    <Route path="/" element={<SeriesList />} />
                    <Route path="/series/:id" element={<SeriesDetail />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;