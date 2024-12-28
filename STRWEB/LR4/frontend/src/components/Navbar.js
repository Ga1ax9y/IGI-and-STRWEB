import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Navbar.css';

const Navbar = () => {
    const [user, setUser] = useState(null);

    const handleLogout = async () => {
        try {
            await axios.post('http://localhost:5000/api/users/logout', {}, { withCredentials: true });
            setUser(null);
        } catch (error) {
            console.error('Error logging out:', error);
            alert('Failed to log out');
        }
    };


    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/users/current', { withCredentials: true });
                setUser(response.data);
            } catch (error) {
                console.error('Error fetching current user:', error);
                setUser(null);
            }
        };

        fetchUser();

        const interval = setInterval(fetchUser, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <nav className="navbar">
            <ul className="navbar-links">
                <li><a href="/">Home</a></li>
                <li><a href="/catalog">Catalog</a></li>
                <li><a href="/news">News</a></li>
                <li><a href="/reviews">Reviews</a></li>
                <li><a href="/exampleAPI">APIs</a></li>
                {user ? (
                    <>
                        <li className="navbar-greeting">Welcome, {user.name}</li>
                        <li><button className="logout-button" onClick={handleLogout}>Logout</button></li>
                    </>
                ) : (
                    <>
                        <li><a href="/login">Login</a></li>
                        <li><a href="/register" className="register-button">Register</a></li>
                    </>
                )}
            </ul>
        </nav>
    );
};

export default Navbar;
