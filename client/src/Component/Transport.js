import React, {useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import Map from "react-map-gl";
import '../App.css';

function Transport() {

  const {viewport, setViewport} = useState({
    longitude: 	144.946457,
    latitude: 	-37.840935,
    zoom: 10,
    width: '100vw',
    height: '100vh'
  })

  return (
    <div>
      <div className="twomaps">
        <Map
          //defulat location 
          initialViewState={{
          longitude: 144.946457,
          latitude: -37.840935,
          zoom: 10  
        }}
          style={{width: '500px', height: '500px'}}
          mapStyle="mapbox://styles/frogtuna/cl29bv18u00by14mtnwzmyga3"
          mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        />
      </div>
      <div className="twomaps">
      <Map
          //defulat location 
          initialViewState={{
          longitude: 144.946457,
          latitude: -37.840935,
          zoom: 10  
        }}
          style={{width: '500px', height: '500px'}}
          mapStyle="mapbox://styles/frogtuna/cl29bv18u00by14mtnwzmyga3"
          mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        />
      </div>
    </div>
  );
  
} 

export default Transport;
