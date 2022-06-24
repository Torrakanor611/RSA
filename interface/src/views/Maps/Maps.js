import React, {useState,useEffect} from "react";
// react plugin used to create google maps
// reactstrap components
import {Card, Container, Row} from "reactstrap";
// core components
import Maps from "./Maps_Component.js";
import Alert from 'react-bootstrap/Alert'

const call_time = 500;


const Maps_Page = () => {

  const [markers, setMarkers] = useState([]);
  const [msg, setMsg] = useState('');
  const [show, setShow] = useState(true);

  useEffect(() => {
    const interval = setInterval(
      () => {
        getDataCam().then((value) => {
          setMarkers(value);
        });
        
        getDataDenm().then((value) => {
          setShow(true)
          if (value == ''){
            setShow(true);
          } else {
            setMsg(value)
            setShow(true)
          }
        })
      }, call_time);

      return () => clearInterval(interval)
    },[]
  )

  const getDataCam = async () => {
    let response = await fetch(
      `http://localhost:5000/api/datacam`);
      // console.log(response)
    let result = await response.json();
    let data = [];
    // console.log("Results: ")
    // console.log(result)
    for (var obu in result) {
      data.push(
        {
          lat: result[obu]["lat"],
          lng: result[obu]["lng"],
          stationId : result[obu]["stationID"]
        }
      )
    }
    return data;
  }

  const getDataDenm = async () => {
    let response = await fetch(
      `http://localhost:5000/api/datadenm`);
      // console.log(response)
    let result = await response.json();
    console.log("DENM: ");
    console.log(result);
    if (result == {}){
      return ''
    }
    return result['msg'];
  }

  return(
      <>
        {/* Page content */}
          <Row>
            <div className="col">
              <Card className="shadow border-0">
                <Maps
                  markers={markers}
                  zoom = {10}
                  mapElement={
                    <div style={{ height: `100%`, borderRadius: "inherit" }} />
                  }
                />
              </Card>
            </div>
          </Row>
          <Alert variant="danger">
          <Alert.Heading>{msg}</Alert.Heading>
          </Alert>
      </>
    );
  }

export default Maps_Page;
