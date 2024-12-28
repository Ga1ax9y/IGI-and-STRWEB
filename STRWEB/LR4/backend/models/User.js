const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'Name is required'],
    },
    email: {
        type: String,
        required: [true, 'Email is required'],
        unique: true,
        match: [/.+\@.+\..+/, 'Please enter a valid email address'],
    },
    password: {
        type: String,
        required: [true, 'Password is required'],
        minlength: [6, 'Password must be at least 6 characters long'],
    },
    googleId: { type: String },
    role: {
        type: String,
        enum: ['client', 'staff'],
        default: 'client',
    },
}, { timestamps: true });


  userSchema.methods.comparePassword = function (candidatePassword) {
    console.log('Comparing passwords:', candidatePassword, this.password);

    return candidatePassword === this.password; 
};

module.exports = mongoose.model('User', userSchema);
