import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import Map, { Source, Layer } from "react-map-gl";
import '../App.css';

function Health() {

  const {viewport, setViewport} = React.useState({
    longitude: 	144.946457,
    latitude: 	-37.840935,
    zoom: 10
  })

  useEffect(async () => {
    const response = await fetch('/health')
    const healthJson = await response.json()  
    
  },[]);

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
    <div>
      <div className="twomaps">
        <Map
          {...viewport}
          style={{width: '500px', height: '500px'}}
          mapStyle="mapbox://styles/frogtuna/cl29bv18u00by14mtnwzmyga3"
          mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        >
      <Source id="my-data" type="geojson" data={geojson}>
        <Layer {...layerStyle} />
      </Source>
        </Map>
      </div>
      <div className="twomaps">
      <Map
          {...viewport}
          style={{width: '500px', height: '500px'}}
          mapStyle="mapbox://styles/frogtuna/cl29bv18u00by14mtnwzmyga3"
          mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        />
      </div>
    </div>
  );
  
} 

export default Health;
