import React from 'react';
// import {
//   useParams
// } from "react-router-dom";
import $ from "jquery";


class Event extends React.Component {
  constructor(props) {
    super(props)  
    this.state = { eventDetails: {} }
  }

  componentDidMount() {
    let eventId = this.props.match.params.eventId;
    let apiUrl = `/events/${eventId}`
    $.get(apiUrl, response => this.setState({eventDetails: response}))
  }

  render() {
    let eventDetails = this.state.eventDetails;

    return (
      <div>
        <h1>{eventDetails.title}</h1>
        <p>Start Time and Date: {eventDetails.start_on}</p>
        <p>End Time and Date: {eventDetails.end_on}</p>
      </div>
    );
  }
}

export default Event;