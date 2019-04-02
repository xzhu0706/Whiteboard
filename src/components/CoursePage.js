import React, {Component} from 'react';
import cookie from 'react-cookies';

class CoursePage extends Component {
	constructor(props) {
		super(props);

		this.state = {
			professorID: 3,
			userID: 0,
			userType: 3,
			// maybe more stuff...
		}

	}

	componentDidMount() {
		let userID = cookie.load('userID');
		let userType = cookie.load('userType');
		this.setState({
			userID: userID,
			userType: userType,
		});
		console.log(userType)

		// TODO: load course info from API and save to states


		if (userType == 1) {   // userType = 1 = professor
			if (userID != this.state.professorID) {
				window.location = '/home/' + this.state.userID;
			}
			// TODO: for professor
		}

		// TODO: for student
	}



	render() {
		return (
			<div>
				<h1> Course Page </h1>
				<h2> id: {this.state.userID ? this.state.userID : 'nothing'}</h2>
			</div>

		);
	}
}

export default CoursePage;