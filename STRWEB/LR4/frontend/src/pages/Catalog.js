import React, { useEffect, useState } from 'react';
import axios from 'axios';
import useAuth from '../hooks/useAuth';
import './Catalog.css';
import Loader from '../extensions/Loader.js';
import ServiceCard from './ServiceCard';
import SearchSort from './SearchSort';

function Catalog() {
  const { user, loading } = useAuth();
  const [services, setServices] = useState([]);
  const [loadingServices, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newService, setNewService] = useState({
    title: '',
    description: '',
    price: 0,
  });
  const [editingServiceId, setEditingServiceId] = useState(null);

  const [searchTerm, setSearchTerm] = useState('');
  const [sortOption, setSortOption] = useState('title');

  useEffect(() => {
    axios.get('http://localhost:5000/api/services')
      .then(response => {
        setServices(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching services:', err);
        setError('Failed to load services');
        setLoading(false);
      });
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewService({
      ...newService,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const apiCall = editingServiceId
      ? axios.put(`http://localhost:5000/api/services/${editingServiceId}`, newService)
      : axios.post('http://localhost:5000/api/services', newService);

    apiCall
      .then(response => {
        if (editingServiceId) {
          setServices(services.map(service =>
            service._id === editingServiceId ? response.data : service
          ));
          alert('Service updated successfully');
          setEditingServiceId(null);
        } else {
          setServices([...services, response.data]);
          alert('Service added successfully');
        }
        setNewService({ title: '', description: '', price: 0 });
      })
      .catch(err => {
        console.error('Error saving service:', err);
        alert('Failed to save service');
      });
  };

  const handleEdit = (service) => {
    setEditingServiceId(service._id);
    setNewService({
      title: service.title,
      description: service.description,
      price: service.price,
    });
  };

  const handleDelete = (id) => {
    axios.delete(`http://localhost:5000/api/services/${id}`)
      .then(() => {
        setServices(services.filter(service => service._id !== id));
        alert('Service deleted successfully');
      })
      .catch(err => {
        console.error('Error deleting service:', err);
        alert('Failed to delete service');
      });
  };

  const filteredServices = services.filter(service =>
    service.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedServices = [...filteredServices].sort((a, b) => {
    if (sortOption === 'title') {
      return a.title.localeCompare(b.title);
    } else if (sortOption === 'price') {
      return a.price - b.price;
    }
    return 0;
  });

  if (loading) {
    return <Loader />;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="catalog-container">
      <h1>Catalog</h1>
      {user && (
        <form onSubmit={handleSubmit} className="service-form">
          <h2>{editingServiceId ? 'Update Service' : 'Add New Service'}</h2>
          <div>
            <label>
              Title:
              <input
                type="text"
                name="title"
                value={newService.title}
                onChange={handleInputChange}
                required
              />
            </label>
          </div>
          <div>
            <label>
              Description:
              <textarea
                name="description"
                value={newService.description}
                onChange={handleInputChange}
                required
              />
            </label>
          </div>
          <div>
            <label>
              Price:
              <input
                type="number"
                name="price"
                value={newService.price}
                onChange={handleInputChange}
                min="0"
                required
              />
            </label>
          </div>
          <button type="submit">{editingServiceId ? 'Update' : 'Add'}</button>
        </form>
      )}
      <SearchSort
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        sortOption={sortOption}
        setSortOption={setSortOption}
      />
      <div className="service-list">
        {sortedServices.map(service => (
          <ServiceCard
            key={service._id}
            service={service}
            onEdit={handleEdit}
            onDelete={handleDelete}
            user={user}
          />
        ))}
      </div>
    </div>
  );
}

export default Catalog;
