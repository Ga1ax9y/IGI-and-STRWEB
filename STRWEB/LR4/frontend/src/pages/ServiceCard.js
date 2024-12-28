import React from 'react';
import { Link } from 'react-router-dom';

const ServiceCard = ({ service, onEdit, onDelete, user }) => (
  <div className="service-card">
    <h2 className="service-title">{service.title}</h2>
    <p className="service-description">{service.description}</p>
    <p className="service-price">Price: ${service.price.toFixed(2)}</p>
    <Link to={`/catalog/${service._id}`} className="details-link">Details</Link>
    {user && (
      <div className="service-actions">
        <button onClick={() => onEdit(service)}>Edit</button>
        <button onClick={() => onDelete(service._id)}>Delete</button>
      </div>
    )}
  </div>
);

export default ServiceCard;
