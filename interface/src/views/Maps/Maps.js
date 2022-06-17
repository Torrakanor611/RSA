/*!
=========================================================
* Argon Dashboard React - v1.1.0
=========================================================
* Product Page: https://www.creative-tim.com/product/argon-dashboard-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard-react/blob/master/LICENSE.md)
* Coded by Creative Tim
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/
import React, {useState,useEffect} from "react";
// react plugin used to create google maps
// reactstrap components
import {Card, Container, Row} from "reactstrap";
// core components
import Maps from "./Maps_Component.js";
import mqtt from 'mqtt/dist/mqtt';

const call_time = 200;

const Maps_Page = () => {

  const [markers, setMarkers] = useState([]);
  const [leader, setLeader] = useState([]);

  var options = {
    keepalive: 30,
  };
  
  var client  = mqtt.connect('192.168.98.50', options);

  var note;
  client.on('message', function (topic, message) {
    note = message.toString();
    // Updates React state with message 
    setMarkers(note);
    // console.log(note);
    // client.end(); // ?
  });


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