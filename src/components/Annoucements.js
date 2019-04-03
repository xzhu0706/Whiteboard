import React, { Component } from 'react';
import Card from './Card.js';

class Announcements extends Component {
  constructor(props) {
    super(props);
    this.state = {
			announcements: 'None'
    };
  }

  componentDidMount() {
		console.log(this.props.announcements);
		if (this.props.announcements.length > 0) {
			const announcements = this.props.announcements.map((ancm) => {
				return (
					<Card 
						key={ancm.announcementID}
						body={ancm.announcement}
						time={ancm.postTime}
					/>
				);
			})
			this.setState({ announcements })
		}
  }

  render() {
    return (
      <div className="card announcement-section">
        <div className="header thumbnail">
          Announcements
        </div>
        <div className="card-body">
					{this.state.announcements}
        </div>
      </div>
    );
  }
};

export default Announcements;