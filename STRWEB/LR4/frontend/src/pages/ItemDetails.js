import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './ItemDetails.css';
import Loader from '../extensions/Loader.js';

const ItemDetails = () => {
  const { id } = useParams();
  const [service, setService] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const formatDate = (date, timeZone = 'UTC') => {
    return new Date(date).toLocaleString('ru-RU', {
      timeZone,
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  useEffect(() => {
    axios.get(`http://localhost:5000/api/services/${id}`)
      .then(response => {
        setService(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching service:', err);
        setError('Failed to load service details');
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return <Loader />;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!service) {
    return <div>Service not found</div>;
  }

  const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

  return (
    <div className="service-details-container">
      <h1 className="service-title">{service.title}</h1>
      <p className="service-description">{service.description}</p>
      <p className="service-price">Цена: ${service.price.toFixed(2)}</p>
      <p><strong>Дата добавления (ваша временная зона):</strong> {formatDate(service.createdAt, userTimeZone)}</p>
      <p><strong>Дата добавления (UTC):</strong> {formatDate(service.createdAt, 'UTC')}</p>
      <p><strong>Дата последнего изменения (ваша временная зона):</strong> {formatDate(service.updatedAt, userTimeZone)}</p>
      <p><strong>Дата последнего изменения (UTC):</strong> {formatDate(service.updatedAt, 'UTC')}</p>
      <Link to="/catalog" className="back-link">Вернуться в каталог</Link>
    </div>
  );
};

export default ItemDetails;
