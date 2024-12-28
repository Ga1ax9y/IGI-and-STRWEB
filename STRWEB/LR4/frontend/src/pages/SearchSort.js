import React from 'react';

const SearchSort = ({ searchTerm, setSearchTerm, sortOption, setSortOption }) => (
  <div className="search-sort-container">
    <input
      type="text"
      placeholder="Search services..."
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
    />
    <select value={sortOption} onChange={(e) => setSortOption(e.target.value)}>
      <option value="title">Sort by Title</option>
      <option value="price">Sort by Price</option>
    </select>
  </div>
);

export default SearchSort;
