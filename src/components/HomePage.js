import React, {Component} from 'react';
import cookie from 'react-cookies';

class HomePage extends Component {
	constructor(props) {
		super(props);

		this.state = {
			userID: 0,
			firstName: '',
			lastName: ''
			// maybe more stuff...
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
						if (res.data.found == false) {
							console.log("courses not found");
							//TODO: show no course is found for user 

						} else {
							console.log("courses found");
							//TODO: need array of objects from backend to use map function

						}
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

				{/* TODO: fetch courses and list them out */}

			</div>
		);
	}
}

export default HomePage;