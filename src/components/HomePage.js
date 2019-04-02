import React, {Component} from 'react';
import cookie from 'react-cookies';

class HomePage extends Component {
	constructor(props) {
		super(props);

		this.state = {
			userID: 0,
			// maybe more stuff...
		}

	}

	componentDidMount() {
		this.setState({
			userID: cookie.load('userID')
		});
	}


	render() {
		return (
			<div>
				<h1> Home Page</h1>
				<a><h2>id: {this.state.userID ? this.state.userID : 'nothing'}</h2></a>
			</div>
		);
	}
}

export default HomePage;