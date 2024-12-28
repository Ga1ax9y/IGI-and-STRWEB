import React, { useState, useEffect } from 'react';
import axios from 'axios';
import useAuth from '../hooks/useAuth';
import './News.css';
import Loader from '../extensions/Loader.js';

const News = () => {
    const { user, loading } = useAuth();
    const [news, setNews] = useState([]);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [image, setImage] = useState(null);
    const [editingNewsId, setEditingNewsId] = useState(null);

    const fetchNews = async () => {
        try {
            const response = await axios.get('http://localhost:5000/api/news');
            setNews(response.data);
        } catch (error) {
            console.error('Error fetching news:', error);
        }
    };

    useEffect(() => {
        fetchNews();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('title', title);
        formData.append('content', content);
        formData.append('author', user.name);
        if (image) {
            formData.append('image', image);
        } else {
            console.log("No image selected");
        }

        try {
            if (editingNewsId) {
                const response = await axios.put(`http://localhost:5000/api/news/${editingNewsId}`, formData, {
                    withCredentials: true,
                    headers: { 'Content-Type': 'multipart/form-data' },
                });
                alert('News updated successfully');
                console.log('Updated news response:', response.data);

                setNews(news.map((item) =>
                    item._id === editingNewsId
                        ? {
                            ...item,
                            title,
                            content,
                            image: response.data.image,
                        }
                        : item
                ));
                setEditingNewsId(null);
            } else {
                const response = await axios.post('http://localhost:5000/api/news', formData, {
                    withCredentials: true,
                    headers: { 'Content-Type': 'multipart/form-data' },
                });
                alert('News submitted successfully');
                console.log('New news response:', response.data);
                fetchNews();
            }
            setTitle('');
            setContent('');
            setImage(null);
        } catch (error) {
            console.error('Error submitting news:', error);
        }
    };


    const handleEdit = (id) => {
        const newsItem = news.find(item => item._id === id);
        if (newsItem) {
            setEditingNewsId(id);
            setTitle(newsItem.title);
            setContent(newsItem.content);
            setImage(null);
        }
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:5000/api/news/${id}`, {
                withCredentials: true,
            });
            alert('News deleted successfully');
            fetchNews();
        } catch (error) {
            console.error('Error deleting news:', error);
        }
    };

    if (loading) return <Loader />;

    return (
        <div className="news-container">
            {user && (
                <form className="news-form" onSubmit={handleSubmit}>
                    <h2>{editingNewsId ? 'Edit News' : 'Add News'}</h2>
                    <label>Title</label>
                    <input
                        type="text"
                        placeholder="Enter title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                    <label>Content</label>
                    <textarea
                        placeholder="Enter content"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        required
                    />
                    <label>Image</label>
                    <input
                        type="file"
                        accept="image/*"
                        onChange={(e) => setImage(e.target.files[0])}
                    />
                    <button type="submit">{editingNewsId ? 'Update' : 'Submit'}</button>
                </form>
            )}
            <h1 className="news-title">Latest News</h1>
            <div className="news-list">
                {news.map((item) => (
                    <div key={item._id} className="news-item">
                        <img
                            className="news-item-image"
                            src={`http://localhost:5000${item.image}`}
                            alt={item.title}
                        />
                        <div className="news-item-content">
                            <h3 className="news-item-title">{item.title}</h3>
                            <p className="news-item-description">{item.content}</p>
                            <small className="news-item-author">By: {item.author}</small>

                            {user && item.author === user.name && (
                                <div className="news-item-actions">
                                    <button onClick={() => handleEdit(item._id)}>Edit</button>
                                    <button onClick={() => handleDelete(item._id)}>Delete</button>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default News;
