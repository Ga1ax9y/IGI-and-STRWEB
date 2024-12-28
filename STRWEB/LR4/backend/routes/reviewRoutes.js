const express = require('express');
const router = express.Router();
const Review = require('../models/Review');

// Получить все отзывы
router.get('/', async (req, res) => {
    try {
        const reviews = await Review.find().populate('client', 'name');
        res.status(200).json(reviews);
    } catch (error) {
        console.error('Error fetching reviews:', error);
        res.status(500).json({ message: 'Failed to fetch reviews' });
    }
});

// Получить один отзыв по ID
router.get('/:id', async (req, res) => {
    try {
        const review = await Review.findById(req.params.id).populate('client', 'name');
        if (!review) {
            return res.status(404).json({ message: 'Review not found' });
        }
        res.status(200).json(review);
    } catch (error) {
        console.error('Error fetching review:', error);
        res.status(500).json({ message: 'Failed to fetch review' });
    }
});

// Добавить отзыв
router.post('/', async (req, res) => {
    try {
        const { rating, comment } = req.body;

        if (!rating || !comment) {
            return res.status(400).json({ message: 'All fields are required' });
        }

        const newReview = new Review({
            client: req.user.id,
            rating,
            comment,
        });

        await newReview.save();
        res.status(201).json(newReview);
    } catch (error) {
        console.error('Error creating review:', error);
        res.status(500).json({ message: 'Failed to submit review' });
    }
});

// Обновить отзыв
router.put('/:id', async (req, res) => {
    try {
        const review = await Review.findById(req.params.id);
        if (!review) {
            return res.status(404).json({ message: 'Review not found' });
        }

        if (review.client.toString() !== req.user.id) {
            return res.status(403).json({ message: 'You do not have permission to edit this review' });
        }

        const { rating, comment } = req.body;
        review.rating = rating || review.rating;
        review.comment = comment || review.comment;

        await review.save();
        res.status(200).json(review);
    } catch (error) {
        console.error('Error updating review:', error);
        res.status(500).json({ message: 'Failed to update review' });
    }
});

// Удалить отзыв
router.delete('/:id', async (req, res) => {
    try {
        const review = await Review.findById(req.params.id);
        if (!review) {
            return res.status(404).json({ message: 'Review not found' });
        }

        if (review.client.toString() !== req.user.id) {
            return res.status(403).json({ message: 'You do not have permission to delete this review' });
        }

        await review.deleteOne();
        res.status(200).json({ message: 'Review deleted successfully' });
    } catch (error) {
        console.error('Error deleting review:', error);
        res.status(500).json({ message: 'Failed to delete review' });
    }
});

module.exports = router;
