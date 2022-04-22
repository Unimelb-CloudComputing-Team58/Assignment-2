import React from 'react';
import './App.css';
import {BrowserRouter as Router,Routes,Route} from "react-router-dom";
import Nav from "./Nav"
import Health from './Component/Health';
import HousePrice from './Component/HousePrice';
import Home from './Component/Home';
import Transport from './Component/Transport';

function App() {


  return (
    
    <div className="body">
      <Router>
        <Nav />
        <Routes>
          <Route path="/" element={<Home />}/>
          <Route path="/Health" element={<Health />}/>
          <Route path="/HousePrice" element={<HousePrice />}/>
          <Route path="/Transport" element={<Transport />}/>
        </Routes>   
      </Router>
    </div>
    

  );
  
} 

export default App;
