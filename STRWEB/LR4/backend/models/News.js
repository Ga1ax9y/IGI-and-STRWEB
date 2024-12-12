const mongoose = require('mongoose');

const newsSchema = new mongoose.Schema({
    title: {
        type: String,
        required: [true, 'Title is required'],
    },
    content: {
        type: String,
        required: [true, 'Content is required'],
    },
    author: {
        type: String,
        required: [true, 'Author is required'],
    },
    image: {
        type: String, 
        required: [true, 'Image URL is required'],
    },
    date: {
        type: Date,
        default: Date.now,
    },
    tags: {
        type: [String],
    },
}, { timestamps: true });

module.exports = mongoose.model('News', newsSchema);
