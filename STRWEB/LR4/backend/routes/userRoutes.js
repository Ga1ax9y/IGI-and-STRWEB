const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const passport = require('passport');
const User = require('../models/User');

function isAuthenticated(req, res, next) {
    if (req.isAuthenticated()) {
        return next();
    }
    res.status(401).json({ message: 'Unauthorized' });
}

router.get('/',isAuthenticated, async (req, res) => {
    try {
        const users = await User.find();
        res.json(users);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

router.post('/register', async (req, res) => {
    const { name, email, password, role } = req.body;

    if (!name || !email || !password) {
        return res.status(400).json({ message: 'Name, email, and password are required' });
    }

    try {
        const newUser = new User({ name, email, password, role });

        const savedUser = await newUser.save();
        res.status(201).json({ message: 'User registered successfully', user: savedUser });
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
});

router.post('/login', (req, res, next) => {
    console.log('Login attempt with email:', req.body.password);
    passport.authenticate('local', (err, user, info) => {
        if (err) return next(err);
        if (!user) return res.status(401).json({ message: info.message });

        req.logIn(user, (err) => {
            if (err) return next(err);
            console.log('User logged in:', user);
            return res.json({ message: 'Успешный вход', user });
        });
    })(req, res, next);
});

router.post('/logout',isAuthenticated, (req, res) => {
    req.logout(err => {
        if (err) return res.status(500).json({ message: 'Error logging out' });
        console.log('User logged out:', req.user);
        res.json({ message: 'Logged out successfully' });
    });
});

router.get('/current', (req, res) => {
    if (req.isAuthenticated()) {
        res.json(req.user);
    } else {
        res.status(401).json({ message: 'Пользователь не аутентифицирован' });
    }
});

router.get('/profile', (req, res) => {
     if (!req.isAuthenticated()) {
         return res.status(401).json({ message: 'Unauthorized' });
     }
    res.json({ message: 'Welcome to your profile', user: req.user });
});

router.get('/:id', async (req, res) => {
    try {
        const user = await User.findById(req.params.id);
        if (!user) return res.status(404).json({ message: 'User not found' });
        res.json(user);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

router.put('/:id', async (req, res) => {
    if (req.user.id !== req.params.id) {
        return res.status(403).json({ message: 'Forbidden' });
    }

    try {
        const updatedUser = await User.findByIdAndUpdate(req.params.id, req.body, { new: true });
        if (!updatedUser) return res.status(404).json({ message: 'User not found' });
        res.json(updatedUser);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
});

router.delete('/:id', async (req, res) => {
    try {
        const deletedUser = await User.findByIdAndDelete(req.params.id);
        if (!deletedUser) return res.status(404).json({ message: 'User not found' });
        res.json({ message: 'User deleted successfully' });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

module.exports = router;
