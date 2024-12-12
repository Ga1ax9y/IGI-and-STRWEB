const mongoose = require('mongoose');

const reviewSchema = new mongoose.Schema({
    client: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: [true, 'Client is required'],
    },
    rating: {
        type: Number,
        required: [true, 'Rating is required'],
        min: [1, 'Rating must be at least 1'],
        max: [5, 'Rating cannot exceed 5'],
    },
    comment: {
        type: String,
        required: [true, 'Comment is required'],
    },
}, { timestamps: true });

module.exports = mongoose.model('Review', reviewSchema);
