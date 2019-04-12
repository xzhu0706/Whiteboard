import React, {Component} from 'react';
import cookie from 'react-cookies';
import {Jumbotron, Container, Row, Col} from 'reactstrap';

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

		fetch('/api/courses/' + userID)
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
								<h2 
									onClick={(e) => {window.location = '/course/' + course.courseID}} 
									style={{cursor: 'pointer'}}
									key={course.courseID} 
									// className="" for styling later
								>
									{course.courseName} {course.semester} {course.year} 
								</h2>
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
				<Jumbotron fluid style={{height: '280px', backgroundColor: '#eae4c5'}}>
					<Container>
							<h1 className="course-name" style={{fontWeight: 'bold'}}> 
								Welcome to your home page, {this.state.firstName} {this.state.lastName}!
							</h1>
					</Container>
        </Jumbotron>
				<div className="text-center" >
     			<text style = {{fontSize:40, color: '#1a0dab', textDecorationLine: 'underline',}}>
      			{this.state.courses.length === 0 ? (<text style ={{fontSize: 35}}>No Courses Found</text>) : this.state.courses }
     			</text>
				</div>
			</div>
		);
	}
}

export default HomePage;