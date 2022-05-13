import React from 'react';
import './App.css';
import {BrowserRouter as Router,Routes,Route} from "react-router-dom";
import Nav from "./Nav"
import Food from './Component/Food';
import Home from './Component/Home';
import Park from './Component/Park';
import Test from './Component/Test';

function App() {


  return (
    
    <div className="body">
      <Router>
        <Nav />
        <Routes>
          <Route path="/" element={<Home />}/>
          <Route path="/Food" element={<Food />}/>
          <Route path="/Park" element={<Park />}/>
          <Route path="/Test" element={<Test />}/>
        </Routes>   
      </Router>
    </div>
    

  );
  
} 

export default App;
