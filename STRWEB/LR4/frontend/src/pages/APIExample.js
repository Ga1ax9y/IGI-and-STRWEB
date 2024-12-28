import React, { useState } from 'react';
import axios from 'axios';
import './APIExample.css';

const APIExample = () => {
    const [name, setName] = useState('');
    const [age, setAge] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [joke, setJoke] = useState('');
    const [loadingJoke, setLoadingJoke] = useState(false);
    const [errorJoke, setErrorJoke] = useState('');

    const handlePredictAge = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        console.log('Name entered:', name);

        try {
            const response = await axios.get(`https://api.agify.io/?name=${name}`);
            console.log('Age API response:', response.data);

            if (response.data.age) {
                setAge(response.data.age);
            } else {
                setError('No age prediction available.');
                setAge(null);
            }
        } catch (error) {
            console.error('Error fetching age data:', error);
            setError('Failed to fetch age prediction.');
            setAge(null);
        } finally {
            setLoading(false);
        }
    };

    const fetchRandomJoke = async () => {
        setLoadingJoke(true);
        setErrorJoke('');
        try {
            const response = await axios.get('https://official-joke-api.appspot.com/random_joke');
            console.log('Joke API response:', response.data);
            setJoke(`${response.data.setup} - ${response.data.punchline}`);
        } catch (error) {
            console.error('Error fetching joke:', error);
            setErrorJoke('Failed to fetch joke.');
            setJoke('');
        } finally {
            setLoadingJoke(false);
        }
    };

    return (
        <div className="age-predictor-container">
            <h1>Age Predictor and Joke Generator</h1>
            <form onSubmit={handlePredictAge} className="age-form">
                <div>
                    <label htmlFor="name">Enter your name:</label>
                    <input
                        type="text"
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Loading...' : 'Predict Age'}
                </button>
            </form>

            {age !== null && (
                <div className="age-result">
                    <h2>Predicted Age:</h2>
                    <p>{`The predicted age for "${name}" is approximately ${age} years.`}</p>
                </div>
            )}

            {error && (
                <div className="error-message">
                    <p>{error}</p>
                </div>
            )}

            <div className="joke-section">
                <h2>Random Joke</h2>
                <button onClick={fetchRandomJoke} disabled={loadingJoke}>
                    {loadingJoke ? 'Loading...' : 'Get a Joke'}
                </button>
                {joke && (
                    <div className="joke-result">
                        <p>{joke}</p>
                    </div>
                )}
                {errorJoke && (
                    <div className="error-message">
                        <p>{errorJoke}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default APIExample;
