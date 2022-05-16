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
import './App.css';
import {BrowserRouter as Router,Routes,Route} from "react-router-dom";
import Nav from "./Nav"
import Food from './Component/Food';
import Home from './Component/Home';
import Park from './Component/Park';

function App() {


  return (
    
    <div className="body">
      <Router>
        <Nav />
        <Routes>
          <Route path="/" element={<Home />}/>
          <Route path="/Food" element={<Food />}/>
          <Route path="/Park" element={<Park />}/>
        </Routes>   
      </Router>
    </div>
    

  );
  
} 

export default App;
