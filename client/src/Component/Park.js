import React, {useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import Map, { Source, Layer } from "react-map-gl";
import { BarChart, Bar, XAxis, YAxis, Legend } from 'recharts';
import '../App.css';


function Park() {

  const {viewport, setViewport} = useState({
    longitude: 	144.946457,
    latitude: 	-37.840935,
    zoom: 10
  })


  //const [tweetSize, setTweetSize] = useState([])
  //const [emotionAnalysis, seEmotionAnalysis] = useState([])
  //const [feature, setFeture] = useState([])



  //   useEffect(async () => {
  //   const response = await fetch('/numberoftweet')
  //   const healthJson = await response.json()  
    
  // },[]);


  //tweetSize
  const tweetSize  = [
    {
      name: 'city',
      tweetSize: 4000,
    },
    {
      name: 'beach',
      tweetSize: 3000,
    },
    {
      name: 'airport',
      tweetSize: 2000,
    }
  ];


    //tweetsAnalysis
    const NLP = [
      {
        name: 'Positive',
        poportion: 80,
      },
      {
        name: 'Negative',
        poportion: 20,
      }
    ];


  //mapbox
  const geojson = {
    type: 'FeatureCollection',
    features: [
      {type: 'Feature', geometry: {type: 'Point', coordinates: [144.946457, -37.840935]}},
      {type: 'Feature', geometry: {type: 'Point', coordinates: [144.926457, -37.840935]}}
    ]
  };

  const layerStyle = {
    id:   'Point',
    type: 'circle',
    paint: {
      'circle-radius': 5,
      'circle-color': '#00BFFF'
    }
  };
 

  return (
    <div className="component">
      <div className="chart-container">
      <div className="charts">
        <BarChart width={500} height={300} data={tweetSize}>
          <XAxis dataKey="name" />
          <YAxis dataKey="tweetSize" />
          <Legend verticalAlign="top" height={36} />
          <Bar name="tweet size" dataKey="tweetSize" barSize={30} fill="#4D5B7F"
           />
        </BarChart>
      </div>
      <div className="charts">
        <BarChart width={500} height={300} data={NLP}>
          <XAxis dataKey="name" />
          <YAxis dataKey="poportion" />
          <Legend verticalAlign="top" height={36} />
          <Bar name="emotional analysis" dataKey="poportion" barSize={30} fill="#616A6B"
           />
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

export default Park;
