import React from 'react';
import './Loader.css';

function Loader() {
  function press(){
    alert("Hello React!")
 }
  return (
    <div className="loader">
      <div className="spinner" onClick={press}></div>
    </div>
  );
}

export default Loader;
