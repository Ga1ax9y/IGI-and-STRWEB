const express = require('express');
const router = express.Router();
const News = require('../models/News');
const multer = require('multer');
const path = require('path');

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname));
    },
});

const upload = multer({ storage });

// Get all news
router.get('/', async (req, res) => {
    try {
        const news = await News.find();
        res.json(news);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// Get news by ID
router.get('/:id', async (req, res) => {
    try {
        const newsItem = await News.findById(req.params.id);
        if (!newsItem) return res.status(404).json({ message: 'News not found' });
        res.json(newsItem);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// Create a news item
router.post('/', upload.single('image'), async (req, res) => {
    const { title, content, tags } = req.body;
    const image = req.file ? `/uploads/${req.file.filename}` : null;

    const author = req.user.name;

    const news = new News({
        title,
        content,
        author,
        tags,
        image,
    });

    try {
        const savedNews = await news.save();
        res.status(201).json(savedNews);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
});

router.put('/:id', upload.single('image'), async (req, res) => {
    try {
        const { title, content } = req.body;
        const updatedData = { title, content };

        if (req.file) {
            updatedData.image = `/uploads/${req.file.filename}`;
        }

        const updatedNews = await News.findByIdAndUpdate(req.params.id, updatedData, { new: true });

        if (!updatedNews) {
            return res.status(404).json({ message: 'News not found' });
        }

        res.json(updatedNews);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

// Delete a news item
router.delete('/:id', async (req, res) => {
    try {
        const newsItem = await News.findById(req.params.id);
        if (!newsItem) return res.status(404).json({ message: 'News not found' });

        if (newsItem.author !== req.user.name) {
            return res.status(403).json({ message: 'Unauthorized to delete this news' });
        }

        await News.findByIdAndDelete(req.params.id);
        res.json({ message: 'News deleted successfully' });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

module.exports = router;
