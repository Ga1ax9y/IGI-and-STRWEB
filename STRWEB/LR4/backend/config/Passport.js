const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const User = require('../models/User');
const mongoose = require('mongoose');
const { ObjectId } = mongoose.Types;
const GoogleStrategy = require('passport-google-oauth20').Strategy;
require('dotenv').config();
// Configure the local strategy
passport.use(
    new LocalStrategy({ usernameField: 'email' }, async (email, password, done) => {
      try {
        const user = await User.findOne({ email });
        if (!user) {
          return done(null, false, { message: 'User not found' });
        }
        const isMatch = await user.comparePassword(password);
        if (!isMatch) {
          return done(null, false, { message: 'Incorrect password' });
        }
        return done(null, user);
      } catch (err) {
        return done(err);
      }
    })
  );

  // Google Strategy
  passport.use(
    new GoogleStrategy(
        {
            clientID: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET,
            callbackURL: 'http://localhost:5000/api/auth/google/callback',
            passReqToCallback: true,
        },
        async (req, accessToken, refreshToken, profile, done) => {
            try {
                let user = await User.findOne({ googleId: profile.id });

                if (!user) {

                    user = new User({
                        googleId: profile.id,
                        name: profile.displayName,
                        email: profile.emails[0].value,
                        password: 'default_password',
                    });


                    await user.save();
                }

                return done(null, user);
            } catch (err) {
                console.error('Error during Google authentication:', err);
                return done(err, null);
            }
        }
    )
);


passport.serializeUser((user, done) => {
  done(null, user.id);
});


passport.deserializeUser(async (id, done) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(id)) {
        return done(new Error('Invalid ID format'));
    }
    const user = await User.findById(new mongoose.Types.ObjectId(id));
    done(null, user);
  } catch (err) {
    done(err);
  }
});

module.exports = passport;
