import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import Map, { Source, Layer } from "react-map-gl";
import { CartesianGrid,BarChart, Bar, XAxis, YAxis, Legend, Tooltip,LineChart,Line,ReferenceLine } from 'recharts';
import ReactLoading from 'react-loading';
import '../App.css';


// 

function Food() {

  const {viewport, setViewport} = React.useState({
    longitude: 	144.946457,
    latitude: 	-37.840935,
    zoom: 10
  })

  const [rawdata, setRawData] = useState()
  const [loading, setLoading] = useState(true)

    console.log(process.env.REACT_APP_URL)


    useEffect( () => {

       fetch(process.env.REACT_APP_URL + "/food")
       .then(response => response.json())
       .then(data => {
         setRawData(data.results)
         setLoading(false)   
       })
    
    },[]);



  
  const layerStyle = {
    id:   'Point',
    type: 'circle',
    paint: {
      'circle-radius': 2,
      'circle-color': '#00BFFF'
    }
  };
 
  if(loading){
    return (
      <div className="loading">
          <ReactLoading type={"spin"} color={"#ffffff"} height={65} width={300} />
      </div>
    )
  }
  else{ 
    const geojson = {
      type: 'FeatureCollection',
      features: []
    };
    rawdata.coordinates.forEach(element => {
      geojson.features.push({type: 'Feature', geometry: {type: 'Point', coordinates: element}})
    }); 
    console.log(geojson)

  return (

    <div className="component">
      <div className="link">
      <a href="/htmls/median_house_price.html" target="_blank">House price</a>
      <a href="/htmls/median_household_income.html" target="_blank">Househod income</a>
      <a href="/htmls/sa3_venues.html" target="_blank">Number of licenced venues by SA3 (food)</a>
      </div>


      <div className="heading">
        <h1>Food</h1>
      </div>
      <div className="chart-container">
        <div className="charts">
        <BarChart width={500} height={300} data={rawdata.num_tweets}>
        <CartesianGrid stroke="#eee" strokeDasharray="2 2" />
          <XAxis dataKey="area" fontSize="10"  interval={0} angle={-12} textAnchor="end" />
          <YAxis dataKey="num_tweets" label={{value: 'TweetCount', angle: -90, position: 'insideLeft'}}/>
          <Tooltip cursor={false}/>
          <Legend verticalAlign="top" height={40} />
          <Bar name="tweet count" dataKey="num_tweets" barSize={30} fill="#7B69D9"/>
        </BarChart>
        <h6>Area</h6>
      </div>




      
      <div className="charts">
      <BarChart
          width={500}
          height={300}
          data={rawdata.sentiments}
        >
          <CartesianGrid stroke="#eee" strokeDasharray="2 2" />
          <XAxis dataKey="area" fontSize="10"  interval={0} angle={-12} textAnchor="end" />
          <YAxis label={{value: 'TweetCount', angle: -90, position: 'insideLeft' }}/>
          <Legend verticalAlign="top" height={40}/>
          <Tooltip cursor={false}/>
          <Bar dataKey="num_positive" fill="#2D6BCF" />
          <Bar dataKey="num_neutral" fill="#068E04" />
          <Bar dataKey="num_negative" fill="#EC4817" />
        </BarChart>
        <h6>Area</h6>
      </div>







      </div>
      <div className="chart-container">
        <div className="charts">
        <BarChart width={500} height={300} data={rawdata.incomes}>
        <CartesianGrid stroke="#eee" strokeDasharray="2 2" />
          <XAxis dataKey="area" fontSize="10"  interval={0} angle={-12} textAnchor="end" />
          <YAxis dataKey="income" label={{value: 'Income', angle: -90, position: 'insideLeft'}}/>
          <Tooltip cursor={false}/>
          <Legend verticalAlign="top" height={36} />
          <Bar name="Median household income of Greater Melbourne SA4s" dataKey="income" barSize={30} fill="#4D5B7F"
           />
        </BarChart>
        <h6>Area</h6>
      </div>




      <div className="charts">
        <LineChart width={500} height={300} data={rawdata.relationships}>
        <CartesianGrid stroke="#eee" strokeDasharray="2 2" />
          <XAxis dataKey= "income" fontSize="10"  interval={0} angle={-9} textAnchor="end"/>
          <YAxis label={{value: 'Proportion', angle: -90, position: 'insideLeft'}} />
          <Tooltip cursor={false}/>
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey="negativePercentage" stroke="#730202" />
          <Line type="monotone" dataKey="positivePercentage" stroke="#00681B" />
        </LineChart>
        <h6>Income</h6>
      </div>
      </div>








      <div className="twomaps">
        <Map
          {...viewport}
          style={{width: '80vw', height: '60vh'}}
          mapStyle="mapbox://styles/frogtuna/cl29bv18u00by14mtnwzmyga3"
          mapboxAccessToken="pk.eyJ1IjoiZnJvZ3R1bmEiLCJhIjoiY2wyOTlsdjhrMGhhaDNrbnpqNnp1eWZleSJ9.3gYSSvMmoQK0iv85aSWjEQ"
        >
      <Source id="my-data" type="geojson" data={geojson}>
        <Layer {...layerStyle} />
      </Source>
        </Map>
      </div>
    </div>
  );
  }
  
} 

export default Food;
