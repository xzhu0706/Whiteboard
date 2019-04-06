import React, { Component } from 'react';
import Card from './Card.js';
import { Button } from 'reactstrap';
// import SingleInputFieldModal from './modals/SingleFieldModal.js';
import cookie from 'react-cookies';

class GradeBook extends Component {
  constructor(props) {
    super(props);
    this.state = {
			grades: [],
		};
		
	}

	componentDidMount() {
		//TODO
		console.log('props for GradeBook component', this.props);

	}

  render() {
		//TODO
		if (this.props.isProf) {
			return (
				<div className="card gradebook-section">

					<div className="header thumbnail">
						Grade Book
					</div>

					<div className="card-body">
						{this.state.grades}
					</div>

					<div className="card-footer">
						<Button 
							className="other-button"
							color="info"
							onClick={this.toggleCreateExamModal}
						>
							Create Exam
						</Button>
					</div>

				</div>
			);
		} else {
			return (
				<div className="card gradebook-section">
					<div className="header thumbnail">
						My Grades
					</div>
					<div className="card-body">
						{this.state.grades}
					</div>
				</div>
			);
		}
  }
};

export default GradeBook;