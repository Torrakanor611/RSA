
import React from "react";
// react plugin used to create google maps
import { GoogleMap, Marker, withGoogleMap, withScriptjs } from "react-google-maps";
// core components
var iconBase = 'http://maps.google.com/mapfiles/kml/pal4/';


const MapWithAMarker = withScriptjs(
  withGoogleMap(props =>
    <GoogleMap
      defaultZoom={17}
      defaultCenter={{ lat: 25.20044250034451,  lng: 55.27789341692669 }}
    >
      {props.markers.map((props, index) => {
          console.log(props)
          if (props.stationId == "3") {
            return (
              <Marker position={{ lat: props.lat, lng: props.lng }}
                key={index}
                id={index}
                // veiculo amarelo, é o que tem reconhecimento de vídeo
                icon={iconBase + 'icon31.png'}
                onClick={(() => {
                }
                )}
              />
            )
          } else if (props.stationId == "1") {
            return (
              <Marker position={{ lat: props.lat, lng: props.lng }}
                key={index}
                id={index}
                // veiculo vermelho, acidentado
                icon={iconBase + 'icon15.png'}
                onClick={(() => {
                }
                )}
                
              />
            )
          } else {
            return (
              <Marker position={{ lat: props.lat, lng: props.lng }}
                key={index}
                id={index}
                // veiculo verde, veiculo comum
                icon={iconBase + 'icon62.png'}
                onClick={(() => {
                }
                )}
                
              />
            )
          }
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
      containerElement={<div style={{ height: `750px` }} />}
      mapElement={<div style={{ height: `100%` }} />}
      markers={this.props.markers}
      options={{
        gestureHandling: 'greedy',
        zoomControlOptions: { position: 9 },
        streetViewControl: false,
        fullscreenControl: false,
      }}
    />);
  }
}

export default Maps;