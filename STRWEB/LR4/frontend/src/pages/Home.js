import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './Home.css';
import TimeDisplay from './TimeDisplay';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userTimeZone: '',
      currentDate: '',
      utcDate: '',
    };
  }

  componentDidMount() {
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const now = new Date();

    this.setState({
      userTimeZone: timeZone,
      currentDate: now.toLocaleString('ru-RU', {
        timeZone,
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      }),
      utcDate: now.toLocaleString('ru-RU', {
        timeZone: 'UTC',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      }),
    });
  }

  render() {
    const { userTimeZone, currentDate, utcDate } = this.state;

    return (
      <div className="home-container">
        <header className="home-header">
          <h1>Welcome to Our Cleaning Service</h1>
          <p>Explore our services and read the latest news and reviews.</p>
        </header>
        <section className="home-content">
          <Link to="/catalog" className="home-card">
            <h3>Our Services</h3>
            <p>Professional cleaning tailored to your needs.</p>
          </Link>
          <Link to="/reviews" className="home-card">
            <h3>Customer Reviews</h3>
            <p>See what our clients say about us!</p>
          </Link>
          <Link to="/news" className="home-card">
            <h3>Latest News</h3>
            <p>Stay updated with our latest cleaning tips and updates.</p>
          </Link>
        </section>
        <section className="home-time-info">
          <h2>Time Information</h2>
          {}
          <TimeDisplay label="Current Time in Your Time Zone" time={currentDate} />
          <TimeDisplay label="Your Time Zone" time={userTimeZone} />
          <TimeDisplay label="Current UTC Time" time={utcDate} />
        </section>
      </div>
    );
  }
}

export default Home;
