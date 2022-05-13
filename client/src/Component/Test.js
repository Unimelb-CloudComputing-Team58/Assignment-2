import React, {useState, useEffect} from 'react';
import '../App.css';
import 'axios';

function Test() {

  const [data,setData] = useState([{}])

  useEffect(() => {
    fetch("test")
    .then(res => res.json())
    .then(data =>{
      console.log(data)
    })
  }, []);

  // useEffect(() => {
  //   fetch("http://10.12.51.39:5001/test",{
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' ,'Access-Control-Allow-Origin': '*', 'mode':'no-cors'}
  // })
  //   .then(res => res.json())
  //   .then(data =>{
  //     setData(data)
  //     console.log(data)
  //   })
  // }, []);

    return (
      <div>
        <h1>hello</h1>
      </div>
    );
  }

export default Test; 