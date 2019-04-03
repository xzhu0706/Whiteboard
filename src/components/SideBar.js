import React, { Component } from 'react';
import { Button } from 'reactstrap';

class SideBar extends Component {
	constructor(props) {
		super(props);
		this.state = {

		}
	}

	componentDidMount() {

	}

	render() {
		return (
			<div className="side-bar border border-secondary">
				<Button className="side-bar-button">Home</Button>
				<div></div>
				<Button className="side-bar-button" color="success">Materials</Button>
				<Button className="side-bar-button" color="primary">Assignments</Button>
				<Button className="side-bar-button" color="danger">GradeBook</Button>
				<Button className="side-bar-button">Log Out</Button>
			</div>
		)
	}

}

export default SideBar;