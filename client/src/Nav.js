/* University of Melbourne                      
COMP90024 Cluster and Cloud Computing        
2022 Semester 1 Assignment 2                 

Team 58:                                     
- (Sam)    Bin Zhang,    895427 @ Melbourne  
- (Joe)    Tianhuan Lu,  894310 @ Melbourne  
- (Leo)    Yicong Li,   1307323 @ Melbourne  
- (Peter)  Weiran Zou,  1309198 @ Melbourne  
- (Thomas) Chenhao Gu,  1147534 @ Melbourne   */




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
