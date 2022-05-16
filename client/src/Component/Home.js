/* University of Melbourne                      
COMP90024 Cluster and Cloud Computing        
2022 Semester 1 Assignment 2                 

Team 58:                                     
- (Sam)    Bin Zhang,    895427 @ Melbourne  
- (Joe)    Tianhuan Lu,  894310 @ Melbourne  
- (Leo)    Yicong Li,   1307323 @ Melbourne  
- (Peter)  Weiran Zou,  1309198 @ Melbourne  
- (Thomas) Chenhao Gu,  1147534 @ Melbourne   */







import React, {useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import '../App.css';


function Home() {


  return (

    <div className="homecomponent">
      <h1>welcome</h1>
      <div className="test"><img src="/images/Food_v1.png" alt="food"></img></div>
      <div className="test"><img src="/images/Park_v1.png" alt="park"></img></div>
    </div>

  );
  
} 

export default Home;
