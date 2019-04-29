import React, { Component } from 'react';
import cookie from 'react-cookies';
import { Button } from 'reactstrap';

class SideBar extends Component {
	constructor(props) {
		super(props);
		this.state = {
			courseID: 0,
			userID: 0,
		}

		this.handleLogOut = this.handleLogOut.bind(this);
	}

	componentDidMount() {
		// const courseInfo = cookie.load('courseInfo'); // get courseInfo from cookie
		// const courseID = courseInfo.courseID;
		const userID = cookie.load('userID');
		const userType = cookie.load('userType');
		this.setState({ userID, userType })
	}

	handleLogOut() {
		cookie.remove('userID');
		cookie.remove('userType');
		cookie.remove('courseInfo');
		window.location = '/';
	}

	render() {
		return (
			<div className="side-bar border border-secondary">
				<Button className="side-bar-button" color="primary" onClick={(e) => {window.location = '/home/' + this.state.userID}}>Home</Button>
				<div></div>
				<Button className="side-bar-button" color="warning" onClick={(e) => {window.location = '/course/' + cookie.load('courseInfo').courseID}}>Announcements</Button>
				<Button className="side-bar-button" color="dark" onClick={(e) => {window.location = '/materials/' + cookie.load('courseInfo').courseID}}>Materials</Button>
				<Button className="side-bar-button" color="success" onClick={(e) => {window.location = '/assignments/' + cookie.load('courseInfo').courseID}}>Assignments</Button>
				<Button className="side-bar-button" color="danger" onClick={(e) => {window.location = '/gradebook/' + cookie.load('courseInfo').courseID + '/' + this.state.userID}}>
					{this.state.userType === '1' ? 'GradeBook' : 'My Grades'}
				</Button>
				<Button className="side-bar-button" onClick={this.handleLogOut}>Log Out</Button>
			</div>
		)
	}

}

export default SideBar;