import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
// import { CartesianGrid,BarChart, Bar, XAxis, YAxis, Legend, Tooltip, Line,LineChart } from 'recharts';
import '../App.css';

function Test() {


  useEffect(() => {
    fetch("http://0.0.0.0:80/test")
    .then(res => res.json())
    .then(data=>{
      console.log(data)
    })
  }, []);

  

  // const data = [{name: 'Page A', uv: 400, pv: 2400},{name: 'Page B', uv:600, pv: 2700}];


    return (
      <div>
      {/* <div className="charts">
        <LineChart width={500} height={300} data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey="pv" stroke="#4658BF" />
          <Line type="monotone" dataKey="uv" stroke="#660054" />
        </LineChart>
      </div> */}
      </div>
    );
  }

export default Test; 