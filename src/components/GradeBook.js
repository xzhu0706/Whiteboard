import React, { Component } from 'react';
import Card from './Card.js';
import { Button } from 'reactstrap';
// import SingleInputFieldModal from './modals/SingleFieldModal.js';
import cookie from 'react-cookies';

class GradeBook extends Component {
  constructor(props) {
    super(props);
    this.state = {
			assignments: [],
			exams: [],
			estFinalGrade: null,
		};
		
	}

	componentDidMount() {
		console.log('props for GradeBook component', this.props);
		if (!this.props.isProf) { // for student
			if (this.props.gradeBook.assignment.length > 0) {
				const assignments = this.props.gradeBook.assignment.map((assignment) => {
					return (
						<Card 
							id={assignment.assignmentID}
							isGrade={true}
							grade={assignment.assignmentGrade}
							gradeTotal={assignment.gradeTotal}
							type='assignment'
							title={assignment.assignmentTitle}
						/>
					);
				});
				this.setState({ assignments });
			}
			if (this.props.gradeBook.exam.length > 0) {
				const exams = this.props.gradeBook.exam.map((exam) => {
					return (
						<Card 
							id={exam.examID}
							isGrade={true}
							grade={exam.examGrade}
							gradeTotal={exam.gradeTotal}
							type='exam'
							percentage={exam.examPercentage}
							title={exam.examTitle}
						/>
					);
				});
				this.setState({ exams });
			}
			this.setState({
				estFinalGrade: this.props.gradeBook.finalGrade
			})
		} else { // for professor
			//TODO
		}
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

					<div className="card">
						<div className="card-body">
							<Card 
								// id={}
								isGrade={true}
								grade={this.state.estFinalGrade}
								gradeTotal={100}
								type='final'
								title="Estimated Final Grade"
								borderColor="red"
							/>
						</div>
					</div>

					<div className="card">
						<div className="card-body">
							<h5>Exams</h5>
							{this.state.exams}
						</div>
					</div>

					<div className="card">
						<div className="card-body">
							<h5>Assignments</h5>
							{this.state.assignments}
						</div>
					</div>

				</div>
			);
		}
  }
};

export default GradeBook;