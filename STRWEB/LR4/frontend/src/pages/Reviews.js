import React, { useEffect, useState } from 'react';
import useAuth from '../hooks/useAuth';
import axios from 'axios';
import './Reviews.css';
import Loader from '../extensions/Loader.js';

const Reviews = () => {
    const { user, loading } = useAuth();
    const [reviews, setReviews] = useState([]);
    const [newReview, setNewReview] = useState({ rating: 0, comment: '' });
    const [editingReviewId, setEditingReviewId] = useState(null);

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/reviews');
                setReviews(response.data);
            } catch (error) {
                console.error('Error fetching reviews:', error);
            }
        };

        fetchReviews();
    }, []);

const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
        alert('You must be logged in to submit a review');
        return;
    }

    try {
        if (editingReviewId) {
            const response = await axios.put(`http://localhost:5000/api/reviews/${editingReviewId}`, {
                ...newReview,
                client: user.name,
            }, {
                withCredentials: true,
            });
            alert('Review updated successfully');
            setReviews(reviews.map((review) =>
                review._id === editingReviewId ? { ...review, ...newReview } : review
            ));
            setEditingReviewId(null);
        } else {
            const response = await axios.post('http://localhost:5000/api/reviews', {
                ...newReview,
                client: user.name,
            }, {
                withCredentials: true,
            });
            alert('Review submitted successfully');
            setReviews([...reviews, response.data]);
        }
        setNewReview({ rating: 0, comment: '' });
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('Failed to submit review');
    }
};

    const handleEdit = (review) => {
        setEditingReviewId(review._id);
        setNewReview({ rating: review.rating, comment: review.comment });
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:5000/api/reviews/${id}`, {
                withCredentials: true,
            });
            alert('Review deleted successfully');
            setReviews(reviews.filter((review) => review._id !== id));
        } catch (error) {
            console.error('Error deleting review:', error);
            alert('Failed to delete review');
        }
    };

    if (loading) return <Loader />;

    return (
        <div className="reviews-container">
            {user && (
                <form className="review-form" onSubmit={handleSubmit}>
                    <h2>{editingReviewId ? 'Edit Review' : 'Submit a Review'}</h2>
                    <label>Rating (1-5)</label>
                    <input
                        type="number"
                        min="1"
                        max="5"
                        value={newReview.rating}
                        onChange={(e) => setNewReview({ ...newReview, rating: Number(e.target.value) })}
                        required
                    />
                    <label>Comment</label>
                    <textarea
                        placeholder="Enter your comment"
                        value={newReview.comment}
                        onChange={(e) => setNewReview({ ...newReview, comment: e.target.value })}
                        required
                    />
                    <button type="submit">{editingReviewId ? 'Update' : 'Submit'}</button>
                </form>
            )}
            <h1>Customer Reviews</h1>
            <div className="reviews-list">
                {reviews.map((review) => (
                    <div key={review._id} className="review-item">
                        <p><strong>Rating:</strong> {review.rating}</p>
                        <p><strong>Comment:</strong> {review.comment}</p>
                        <p><small>By: {review.client.name}</small></p>
                        {user && user._id === review.client._id && (
                            <div>
                                <button onClick={() => handleEdit(review)}>Edit</button>
                                <button onClick={() => handleDelete(review._id)}>Delete</button>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Reviews;
