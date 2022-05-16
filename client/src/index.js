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
import ReactDOM from 'react-dom/client';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
