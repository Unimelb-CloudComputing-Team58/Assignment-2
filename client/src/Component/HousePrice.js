import React, {useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import Map from "react-map-gl";
import '../App.css';

function HousePrice() {

  const {viewport, setViewport} = useState({
    longitude: 	144.946457,
    latitude: 	-37.840935,
    zoom: 10
  })

  return (
    <div>
      <div className="twomaps">
        <Map
          //defulat location 
          {...viewport}
          style={{width: '500px', height: '500px'}}
          mapStyle="mapbox://styles/frogtuna/cl29bv18u00by14mtnwzmyga3"
          mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        />
      </div>
      <div className="twomaps">
      <Map
          //defulat location 
          {...viewport}
          style={{width: '500px', height: '500px'}}
          mapStyle="mapbox://styles/frogtuna/cl29bv18u00by14mtnwzmyga3"
          mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        />
      </div>
    </div>
  );
  
} 

export default HousePrice;
