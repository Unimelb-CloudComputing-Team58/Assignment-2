import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import mapData from "./../data/aurin_data.json";
import { MapContainer, TileLayer, useMap } from 'react-leaflet'
// import { CartesianGrid,BarChart, Bar, XAxis, YAxis, Legend, Tooltip, Line,LineChart } from 'recharts';
import '../App.css';
import 'leaflet/dist/leaflet.css';

function Test() {


  // useEffect(() => {
  //   fetch("http://0.0.0.0:80/test")
  //   .then(res => res.json())
  //   .then(data => {
  //     console.log(data)
  //   })
  // }, []);

  // const data = [{name: 'Page A', uv: 400, pv: 2400},{name: 'Page B', uv:600, pv: 2700}];


    return (
    <MapContainer center={[50.5, 30.5]} zoom={10} style={{width:'100vw',height:'100vh'}}>
    </MapContainer>
    );
  }

export default Test; 