
import React from "react";
// react plugin used to create google maps
import { GoogleMap, Marker, withGoogleMap, withScriptjs } from "react-google-maps";
// core components
var iconBase = 'http://maps.google.com/mapfiles/kml/pal4/';


const MapWithAMarker = withScriptjs(
  withGoogleMap(props =>
    <GoogleMap
      defaultZoom={14}
      defaultCenter={{ lat: 40.631637, lng: -8.657376 }}
    >
      {props.markers.map((props, index) => {
          return (
            <Marker position={{ lat: props.lat, lng: props.lng }}
              key={index}
              id={index}
              icon={iconBase + 'icon15.png'}
              onClick={(() => {
              }
              )}
              
            />
          )
        }
      )}
    </GoogleMap>
  ));

class Maps extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      lat: 0,
      lng: 0
    }
  }
  /*
  componentDidMount(){
    Promise.all([this.get_my_location()]).then((value) => {
      this.setState(
        {
          lat: value[0].coords.latitude,
          lng: value[0].coords.longitude
        })})
  }*/

  get_my_location = () => {
    if (navigator.geolocation) {
      return new Promise(
        (resolve, reject) => navigator.geolocation.getCurrentPosition(resolve, reject)
      )
    } else {
      return new Promise(
        resolve => resolve({})
      )
    }
  }

  render() {
    return (<MapWithAMarker
      googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyB3BkFB0RAIAef8cm-H9bwQSlVraeLAAuI&v=3.exp&libraries=geometry,drawing,places"
      loadingElement={<div style={{ height: `100%` }} />}
      containerElement={<div style={{ height: `800px` }} />}
      mapElement={<div style={{ height: `100%` }} />}
      markers={this.props.markers}
      options={{
        gestureHandling: 'greedy',
        zoomControlOptions: { position: 9 },
        streetViewControl: false,
        fullscreenControl: true,
      }}
    />);
  }
}

export default Maps;