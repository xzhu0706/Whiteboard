import React, {Component} from 'react';
import cookie from 'react-cookies';
import Announcements from './Annoucements.js';
import SideBar from './SideBar.js';

class CoursePage extends Component {
	constructor(props) {
		super(props);

		this.state = {
			userID: 0,
			userType: 3,
			professorID: 0,
			courseName: '',
			semester: '',
			year: '',
			professorEmail: '',
			professorName: '',
			announcements: []
			// maybe more stuff...
		}

	}

	async componentDidMount() {
		let userID = cookie.load('userID');
		let userType = cookie.load('userType');
		const params = this.props.match.params; // get params from url
		let courseID = params.courseID;
		this.setState({ userID, userType, courseID });

    console.log(params);

		await fetch('http://localhost:5000/api/courseInfo/' + params.courseID)
			.then((res) => {
				console.log(res);
				if (res.ok) {
					res.json().then(data => ({
						data: data,
						status: res.status
					})).then(res => {
						console.log(res);
						let key;
						for (key in res.data) {
							this.setState({ [key]: res.data[key] });
						}
					});
				} else {
						console.log('error while fetching courseInfo');
					}
			})

		await fetch('http://localhost:5000/api/announcement/' + params.courseID)
			.then((res) => {
				console.log(res);
				if (res.ok) {
					res.json().then(data => ({
						data: data,
						status: res.status
					})).then(res => {
						console.log(res);
						const announcements = (
							<Announcements 
								isProf={this.state.userType} 
								announcements={res.data}
								courseID={this.state.courseID} 
							/>
						);
						this.setState({ announcements });
					});
				} else {
						console.log('error while fetching announcement');
					}
			});


		// if (userType == 1) {   // userType = 1 = professor
		// 	if (userID != this.state.professorID) {
		// 		window.location = '/home/' + this.state.userID;
		// 	}
		// 	// TODO: for professor
		// }

		// // TODO: for student
	}



	render() {
		return (
			<div className="container-fluid">

				<h1 className="course-page-header"> 
					{this.state.courseName} {this.state.semester} {this.state.year} 
				</h1>

				<div className="professor-contact-info">
					<h3>{this.state.professorName}</h3>
					<h3>{this.state.professorEmail}</h3>
				</div>

				<div className="row">
					<div className="col-sm-4 d-flex justify-content-end">
						<SideBar />
					</div>
					<div className="col-sm-8">
						{this.state.announcements}
					</div>
				</div>



			</div>

		);
	}
}

export default CoursePage;