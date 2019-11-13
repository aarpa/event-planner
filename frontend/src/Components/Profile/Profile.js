import React from 'react';
import './Profile.css';

class Profile extends React.Component {
  constructor() {
    super();
    this.state = { upcomingEventsTab: 'hosting' }
  }

  renderBio = () => {
    return (
      <div className="bio">
        <img src="profile_pic.jpg"/>
        <h1>User's name</h1>
        <p>User's email</p>
        <p>User's phone number</p>
      </div>
    );
  }

  renderHostingEvents = () => {
    return (
      <div className="hostingEvents">
        <h3>Events You're Hosting</h3>
        <p>Name of Event: Friendsgiving Potluck</p>
        <p>Start Date and Time: 11/28/19, 6:30 pm</p>
        <p>End Date and Time: 11/28/19, 11:30 pm</p>
        <p>Guests Attending</p>
        <ol>
          <li>Guest 1</li>
          <li>Guest 2</li>
          <li>Guest 3</li>
          <li>Guest 4</li>
          <li>Guest 5</li>
        </ol>
      </div>
    );
  }

  renderAttendingEvents = () => {
    return (
      <div className="attendingEvents">
        <h3>Events You're Attending</h3>
        <p>Name of Event: Christmas Potluck</p>
        <p>Start Date and Time: 12/25/19, 6:30 pm</p>
        <p>End Date and Time: 12/25/19, 11:30 pm</p>
        <p>Guests Attending</p>
        <ol>
          <li>User</li>
          <li>Guest 1</li>
          <li>Guest 2</li>
          <li>Guest 3</li>
          <li>Guest 4</li>
          <li>Guest 5</li>
        </ol>
      </div>
    );
  }

  changeTab = (tab) => {
    this.setState({ upcomingEventsTab: tab});
  }

	render() {
    let tab = this.state.upcomingEventsTab;
    let toRender;

    if (tab === 'hosting') {
      toRender = this.renderHostingEvents();
    } else {
      toRender = this.renderAttendingEvents();
    }

		return (
        <div className="profile">
          {this.renderBio()}
          <button onClick={() => this.changeTab('hosting')}>Events Hosted by You</button>
          <button onClick={() => this.changeTab('attending')}>Events Hosted by You</button>
          {toRender}
        </div>        
  		);
	}
}

export default Profile;