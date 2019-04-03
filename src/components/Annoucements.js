import React, { Component } from 'react';
import Card from './Card.js';
import { Button } from 'reactstrap';
import CreateAnnouncement from './CreateAnnouncement.js';

class Announcements extends Component {
  constructor(props) {
    super(props);
    this.state = {
			announcements: 'None',
			announcementsList: [],
			selectedAnnouncement: '',
		};
		
		this.handleOnClickAnnouncement = this.handleOnClickAnnouncement.bind(this);
		this.handleDeleteAnnouncement = this.handleDeleteAnnouncement.bind(this);
		this.handleCreateAnnouncement = this.handleCreateAnnouncement.bind(this);
	}

	componentDidMount() {
		console.log('props for Announcement component',this.props);
		this.setState({
			announcementsList: this.props.announcements
		})
		if (this.props.announcements.length > 0) {
			const announcements = this.props.announcements.map((ancm) => {
				return (
					<Card 
						id={ancm.announcementID}
						body={ancm.announcement}
						time={ancm.postTime}
						onClick={this.handleOnClickAnnouncement}
					/>
				);
			})
			this.setState({ announcements });
		}
  }
	
	handleOnClickAnnouncement(e, ancmID) {
		console.log(ancmID);
		this.setState({
			selectedAnnouncement: ancmID
		});
		console.log(this.state.selectedAnnouncement);
		if (this.props.announcements.length > 0) {
			const announcements = this.props.announcements.map((ancm) => {
				return (
					<Card 
						id={ancm.announcementID}
						bgColor={ancmID === ancm.announcementID ? 'yellow' : '' }
						borderColor={ancmID === ancm.announcementID ? 'red' : ''}
						body={ancm.announcement}
						time={ancm.postTime}
						onClick={this.handleOnClickAnnouncement}
					/>
				);
			})
			this.setState({ announcements });
		}
	}

	handleDeleteAnnouncement(e) {
		console.log('delete ancm', this.state.selectedAnnouncement);
		//TODO: need delete announcement API call from backend
	}

	handleCreateAnnouncement(e) {
		//TODO: 
	}


  render() {
		if (this.props.isProf) {
			return (
				<div className="card announcement-section">

					<div className="header thumbnail">
						Announcements
					</div>

					<div className="card-body">
						{this.state.announcements}
					</div>

					<div className="card-footer">
						{/* for create, delete buttons */}
						<CreateAnnouncement
							label="Create"
							courseID={this.props.courseID}
						/>
						{/* <Button 
							className="side-bar-button"
							onClick={this.handleCreateAnnouncement}
						>
							Create
						</Button> */}
						<Button 
							className="side-bar-button"
							onClick={this.handleDeleteAnnouncement}
						>
							Delete
						</Button>
					</div>

				</div>
			);
		} else {
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
  }
};

export default Announcements;