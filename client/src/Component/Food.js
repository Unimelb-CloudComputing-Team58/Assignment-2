import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import Map, { Source, Layer } from "react-map-gl";
import { CartesianGrid,BarChart, Bar, XAxis, YAxis, Legend, Tooltip } from 'recharts';
import ReactLoading from 'react-loading';
import '../App.css';

function Food() {

  const {viewport, setViewport} = React.useState({
    longitude: 	144.946457,
    latitude: 	-37.840935,
    zoom: 10
  })

  const [rawdata, setRawData] = useState()
  const [loading, setLoading] = useState(true)


    useEffect( () => {

       fetch('/food')
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
      <div className="chart-container">
        <div className="charts">
        <BarChart width={500} height={300} data={rawdata.num_tweets}>
        <CartesianGrid stroke="#eee" strokeDasharray="2 2" />
          <XAxis dataKey="area" fontSize="14"/>
          <YAxis dataKey="num_tweets" />
          <Tooltip cursor={false}/>
          <Legend verticalAlign="top" height={40} />
          <Bar name="tweet count" dataKey="num_tweets" barSize={30} fill="#7B69D9"/>

        </BarChart>
      </div>





      <div className="charts">
      <BarChart
          width={500}
          height={300}
          data={rawdata.sentiments}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid stroke="#eee" strokeDasharray="2 2" />
          <XAxis dataKey="area" fontSize="14"/>
          <YAxis />
          <Legend verticalAlign="top" height={40}/>
          <Tooltip cursor={false}/>
          <Bar dataKey="num_positive" fill="#2D6BCF" />
          <Bar dataKey="num_neutral" fill="#03CB00" />
          <Bar dataKey="num_negative" fill="#EC4817" />
        </BarChart>
      </div>







      </div>
      <div className="chart-container">
        <div className="charts">
        <BarChart width={500} height={300} data={rawdata.income}>
          <XAxis dataKey="area" />
          <YAxis dataKey="income" />
          <Legend verticalAlign="top" height={36} />
          <Bar name="Median household income vs. SA4" dataKey="income" barSize={30} fill="#4D5B7F"
           />
        </BarChart>
      </div>
      <div className="charts">
        <BarChart width={500} height={300} data={rawdata}>
          <XAxis dataKey="name" />
          <YAxis dataKey="poportion" />
          <Legend verticalAlign="top" height={36} />
          <Bar name="Happiness vs. income" dataKey="poportion" barSize={30} fill="#616A6B"/>
          <Bar name="tweet count" dataKey="tweetSize" barSize={30} fill="#4D5B7F"/>
        </BarChart>
      </div>
      </div>








      <div className="twomaps">
        <Map
          {...viewport}
          style={{width: '1100px', height: '500px'}}
          mapStyle="mapbox://styles/frogtuna/cl29bv18u00by14mtnwzmyga3"
          mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
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
