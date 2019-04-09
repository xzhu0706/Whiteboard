import React, {Component} from 'react';
import cookie from 'react-cookies';
import { Button } from 'reactstrap';
import '../styling/HomePage.css';

class HomePage extends Component {
	constructor(props) {
		super(props);

		this.state = {
			userID: 0,
			firstName: '',
			lastName: '',
			courses: []
		}

	}

	componentDidMount() {
		let userID = cookie.load('userID');
		let firstName = cookie.load('firstName');
		let lastName = cookie.load('lastName');
		this.setState({ userID, firstName, lastName });

		fetch('http://localhost:5000/api/courses/' + userID)
			.then((res) => {
				console.log(res);
				if (res.ok) {
					res.json().then(data => ({
						data: data,
						status: res.status
					})).then(res => {
						console.log(res);

						const courses = res.data.map((course) => {
							return (
								<div className="courses_nagivator">
									<Button onClick={(e) => {window.location = '/course/' + course.courseID}}
									key = {course.courseID}
									color="primary"
									>
									{course.courseName} {course.semester} {course.year}
									</Button>
								</div>
								/*
								<h2 
									onClick={(e) => {window.location = '/course/' + course.courseID}} 
									key={course.courseID} 
									// className="" for styling later
								>
									{course.courseName} {course.semester} {course.year} 
								</h2>
								*/
							)
						})
						this.setState({ courses });

					});
				} else {
						console.log('error while fetching courses');
					}
			});
	}


	render() {
		return (
			<div>
				<h1>Welcome to your home page, {this.state.firstName} {this.state.lastName}!</h1>
				
				{this.state.courses.length === 0 ? (<h5>No courses found</h5>) : this.state.courses }

			</div>
		);
	}
}

export default HomePage;