import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from '../../frontend/src/components/Navbar';
import Home from './pages/Home';
import Catalog from './pages/Catalog';
import ItemDetails from './pages/ItemDetails';
import News from './pages/News';
import Reviews from './pages/Reviews';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import APIExample from './pages/APIExample';

function App() {
    return (
        <Router>
            <div>
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/catalog" element={<Catalog />} />
                    <Route path="/catalog/:id" element={<ItemDetails />} />
                    <Route path="/news" element={<News />} />
                    <Route path="/reviews" element={<Reviews />} />
                    <Route path="/exampleAPI" element={<APIExample />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
