import React from 'react';
import './App.css';
import {BrowserRouter as Router,Routes,Route} from "react-router-dom";
import Nav from "./Nav"
import Health from './Component/Health';
import Home from './Component/Home';

function App() {


  return (
    
    <div className="body">
      <Router>
        <Nav />
        <Routes>
          <Route path="/" element={<Home />}/>
          <Route path="/Health" element={<Health />}/>
        </Routes>   
      </Router>
    </div>
    

  );
  
} 

export default App;
