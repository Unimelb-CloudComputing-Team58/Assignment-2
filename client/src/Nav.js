import React from 'react';
import {Link} from "react-router-dom";
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function Nav() {

  return (
    <div>
      <div className="Heading">
        <h1>Melbourne livability analytics</h1>
      </div>
      <div className="inline-buttons">
          <Link to="/"><Button variant="primary">Home</Button></Link>
          <Link to="/Food"><Button variant="primary">Food</Button></Link>
          <Link to="/Park"><Button variant="primary">Park</Button></Link>
      </div>
    </div>
  );
  
} 

export default Nav;
