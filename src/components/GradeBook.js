import React, { Component } from 'react';
import Card from './Card.js';
import { Button } from 'reactstrap';
import GradeBookTable from './GradeBookTable.js';
import createExamModal from './modals/CreateExamModal.js';
import CreateExamModal from './modals/CreateExamModal.js';


class GradeBook extends Component {
  constructor(props) {
    super(props);
    this.state = {
			assignments: [],
			exams: [],
			estFinalGrade: null,
			gradeBookTable: null,
			createExamModal: false,
		};

		this.toggleCreateExamModal = this.toggleCreateExamModal.bind(this);
		this.handleCreateExam = this.handleCreateExam.bind(this);
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
		} 
	}

	toggleCreateExamModal(e) {
		this.setState({
			createExamModal: !this.state.createExamModal
		});
	}

	handleCreateExam(event) {
		//backend TODO: sort the exams by id
		// event.preventDefault();

		const data = {
			courseID: this.props.courseID,
			examTitle: event.target.title.value,
			examPercentage: event.target.percentage.value, 
			gradeTotal: event.target.gradeTotal.value, 
		}
		 console.log(data);

		fetch('http://localhost:5000/api/createExam', {
			method: 'POST',
			headers: {'Content-Type':'application/json'},
			body: JSON.stringify(data)
		}).then((res) => {

			console.log(res)
			if(res.ok) {
				res.json().then(data => ({
					data: data,
					status: res.status
				})).then(res => {
					console.log(res);
				});
			}
			else{
				// window.location.replace("/error");
				console.log('error while creating exam')
			}

		});
	}

  render() {
		//TODO
		if (this.props.isProf) {
			return (
				<div className="card gradebook-section">
					<CreateExamModal 
						isOpen={this.state.createExamModal}
						toggle={this.toggleCreateExamModal}
						handleSubmit={this.handleCreateExam}
						header="New Exam"
					/>

					<div className="header thumbnail">
						Grade Book
					</div>

					<div className="card-body">
						{/* {this.state.grades} */}
						<GradeBookTable data={this.props.gradeBook} />
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