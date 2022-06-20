import React, {useState,useEffect} from "react";
// react plugin used to create google maps
// reactstrap components
import {Card, Container, Row} from "reactstrap";
// core components
import Maps from "./Maps_Component.js";

const call_time = 500;


const Maps_Page = () => {

  const [markers, setMarkers] = useState([]);

  useEffect(() => {
    const interval = setInterval(
      () => {
        getLocations().then((value) => {
          setMarkers(value)
        });
      }, call_time);

      return () => clearInterval(interval)
    },[]
  )

  const getLocations = async () => {
    let response = await fetch(
      `http://localhost:5000/api/getLocations`);
      console.log(response)
    let result = await response.json();
    let all_locations = [];
    console.log("Results: ")
    console.log(result)
    for (var obu in result) {
      all_locations.push(
        {
          lat: result[obu]["lat"],
          lng: result[obu]["lng"],
          stationId : result[obu]["stationID"]
        }
      )
    }
    // console.log(all_locations)
    return all_locations;
  }

  return(
      <>
        {/* Page content */}
        <Container className="mt--7" fluid>
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
        </Container>
      </>
    );
  }

export default Maps_Page;
