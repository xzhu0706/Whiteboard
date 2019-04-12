import React, { Component } from 'react';
import Card from './Card.js';
import { Button } from 'reactstrap';
import SingleInputFieldModal from './modals/SingleFieldModal.js';

class Announcements extends Component {
  constructor(props) {
    super(props);
    this.state = {
			announcements: 'None',
			announcementsList: [],
			selectedAnnouncement: '',
			createAnnouncementModal: false,
		};
		
		this.toggleCreateAnnouncementModal = this.toggleCreateAnnouncementModal.bind(this);
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
						bgColor={ancmID === ancm.announcementID ? '#eae4c5' : '' }
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
		e.preventDefault();
		// if (this.state.selectedAnnouncement) {
			fetch('/api/deleteAnnouncement/' + this.state.selectedAnnouncement, {
				method: 'DELETE'
			})
			.then((res) => {
				console.log(res);
				if (res.ok) {
					res.json().then(data => ({
						data: data,
						status: res.status
					})).then(res => {
						console.log(res);
						window.location.reload();
					});
				} else {
						console.log('error while deleting announcement');
						alert('Something went wrong!');
						window.location.reload();
					}
			});
			// window.location.reload();
		// }	
	}

	handleCreateAnnouncement(event, announcement) {
//		event.preventDefault();
		const data = {
			courseID: this.props.courseID,
			announcement: announcement
		}
		console.log(data);

		fetch('/api/createAnnouncement', {
			method: 'POST',
			headers: {'Content-Type':'application/json'},
			body: JSON.stringify(data)
		}).then((res) => {

			console.log(res)
			if(res.ok) {
				res.json().then(data => ({
					data: data,
					status: res.status
				})).then(res => {
					console.log(res);
					window.location.reload();
				});
			}
			else{
				// window.location.replace("/error");
				console.log('error while posting announcement')
				alert('Something went wrong!');
				window.location.reload();
			}

		});

	}

	toggleCreateAnnouncementModal() {
		this.setState({
			createAnnouncementModal: !this.state.createAnnouncementModal
		})
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
						<SingleInputFieldModal
							isOpen={this.state.createAnnouncementModal}
							toggle={this.toggleCreateAnnouncementModal}
							handleSubmit={this.handleCreateAnnouncement}
							header="New Announcement"
						/>
						<Button 
							className="other-button"
							color="info"
							onClick={this.toggleCreateAnnouncementModal}
						>
							Create
						</Button>
						<Button 
							className="other-button"
							color="warning"
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