import React, { Component } from 'react';
import Card from './Card.js';
import { Button } from 'reactstrap';
import SingleInputFieldModal from './modals/SingleFieldModal.js';
import cookie from 'react-cookies';

class Assignments extends Component {
  constructor(props) {
    super(props);
    this.state = {
			assignments: 'None',
			selectedAssignment: '',
			createAssignmentModal: false,
			submitAssignmentModal: false,
		};
		
		this.toggleCreateAssignmentModal = this.toggleCreateAssignmentModal.bind(this);
		this.toggleSubmitAssignmentModal = this.toggleSubmitAssignmentModal.bind(this);
		this.handleOnClickAssignment = this.handleOnClickAssignment.bind(this);
		this.handleDeleteAssignment = this.handleDeleteAssignment.bind(this);
		this.handleCreateAssignment = this.handleCreateAssignment.bind(this);
		this.handleDownloadAssignment = this.handleDownloadAssignment.bind(this);
		this.handleSubmitAssignment = this.handleSubmitAssignment.bind(this);
		this.handleSeeSubmissions = this.handleSeeSubmissions.bind(this);
	}

	componentDidMount() {
		if (this.props.assignments.length > 0) {
			const assignments = this.props.assignments.map((assignment) => {
				return (
					<Card 
						id={assignment.assignmentID}
						isProf={this.props.isProf}
						isAssignment={true}
						isSubmitted={assignment.isSubmitted}
						isLate={assignment.isLate}
						pastDue={assignment.pastDue}
						title={assignment.title}
						body={assignment.task}
						time={"Deadline: " + assignment.deadline}
						onClick={this.handleOnClickAssignment}
						handleSubmitAssign={this.toggleSubmitAssignmentModal}
						handleSeeSubmissions={this.handleSeeSubmissions}
						handleDownload={this.handleDownloadAssignment}
					/>
				);
			})
			this.setState({ assignments });
		}
	}
	
	handleOnClickAssignment(e, assignmentID) {
		if (cookie.load('userType') == 1) {
			console.log(assignmentID);
			this.setState({
				selectedAssignment: assignmentID
			});
			// console.log(this.state.selectedAssignment);
			if (this.props.assignments.length > 0) {
				const assignments = this.props.assignments.map((assignment) => {
					return (
						<Card 
							id={assignment.assignmentID}
							isProf={this.props.isProf}
							isAssignment={true}
							pastDue={assignment.pastDue}
							title={assignment.title}
							body={assignment.task}
							time={"Deadline: " + assignment.deadline}
							onClick={this.handleOnClickAssignment}
							bgColor={assignmentID === assignment.assignmentID ? '#b0e5f4' : '' }
							handleSeeSubmissions={this.handleSeeSubmissions}
						/>
					);
				})
				this.setState({ assignments });
			}
		}
	}

	handleDeleteAssignment(e) {
		console.log('delete assignment', this.state.selectedAssignment);
		
		if (this.state.selectedAssignment) {
			fetch('http://localhost:5000/api/deleteAssignment/' + this.state.selectedAssignment, {
				method: 'DELETE'
			})
			.then((res) => {
				console.log(res);
				if (res.ok) {
					res.json().then(data => ({
						data: data,
						status: res.status
					})).then(res => {
						console.log(res);
					});
				} else {
						console.log('error while deleting assignment');
					}
			});
			window.location.reload();
		}	}

	handleCreateAssignment(event, assignment) {
		//event.preventDefault();
		// TODO*****************************************************
		const data = {
			courseID: this.props.courseID,
			task: assignment,
			title: 'title',
			deadline: 7, //need to let user choose the day
			gradeTotal: 100, //need to let user input the grade
		}
		console.log(data);

		fetch('http://localhost:5000/api/createAssignment', {
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
				console.log('error while creating Assignment')
			}

		});
	}

	handleSubmitAssignment(e, submittedAssignment) {
		console.log('submit assignment for', this.state.selectedAssignment);
		const data = {
			assignID: this.state.selectedAssignment,
			studentID: cookie.load('userID'),
			content: submittedAssignment
		}
		fetch('http://localhost:5000/api/submitAssignment', {
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
				console.log('error while posting Assignment')
			}
		});
	}

	handleSeeSubmissions(e, assignmentID) {
		console.log('see submissions for', assignmentID);
		window.location = '/submissions/' + assignmentID
	}

	handleDownloadAssignment(e, assignmentID) {
		console.log('download assignment', assignmentID);
		//TODO: if we implement uploading&downloading files 
	}

	toggleCreateAssignmentModal() {
		this.setState({
			createAssignmentModal: !this.state.createAssignmentModal
		})
	}

	toggleSubmitAssignmentModal() {
		this.setState({
			submitAssignmentModal: !this.state.submitAssignmentModal
		})
	}


  render() {
		if (this.props.isProf) {
			return (
				<div className="card assignment-section">

					<div className="header thumbnail">
						Assignments
					</div>

					<div className="card-body">
						{this.state.assignments}
					</div>

					<div className="card-footer">
						{/* for create, delete buttons */}
						<SingleInputFieldModal
							isOpen={this.state.createAssignmentModal}
							toggle={this.toggleCreateAssignmentModal}
							handleSubmit={this.handleCreateAssignment}
							header="New Assignment"
						/>
						<Button 
							className="other-button"
							color="success"
							onClick={this.handleDownloadAssignment}
						>
							Download
						</Button>
						<Button 
							className="other-button"
							color="info"
							onClick={this.toggleCreateAssignmentModal}
						>
							Create
						</Button>
						<Button 
							className="other-button"
							color="warning"
							onClick={this.handleDeleteAssignment}
						>
							Delete
						</Button>
					</div>

				</div>
			);
		} else {
			return (
				<div className="card assignment-section">
					<SingleInputFieldModal
						isOpen={this.state.submitAssignmentModal}
						toggle={this.toggleSubmitAssignmentModal}
						handleSubmit={this.handleSubmitAssignment}
						header="Submit Assignment"
					/>
					<div className="header thumbnail">
						Class Assignments
					</div>
					<div className="card-body">
						{this.state.assignments}
					</div>
					{/* <Button 
						className="other-button"
						color="success"
						onClick={this.handleDownloadAssignment}
					>
						Download
					</Button> */}
				</div>
			);
		}
  }
};

export default Assignments;