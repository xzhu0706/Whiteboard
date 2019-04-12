import React, { Component } from 'react';
import Card from './Card.js';
import { Button } from 'reactstrap';
import SingleInputFieldModal from './modals/SingleFieldModal.js';
import cookie from 'react-cookies';
import CreateAssignmentModal from './modals/CreateAssignmentModal.js';

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
						gradeTotal={assignment.gradeTotal}
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
		// if (cookie.load('userType') == 1) {
			console.log(assignmentID);
			this.setState({
				selectedAssignment: assignmentID
			});
			// console.log(this.state.selectedAssignment);
			if (this.props.isProf) {
				console.log('isProf');
				if (this.props.assignments.length > 0) {
					const assignments = this.props.assignments.map((assignment) => {
						return (
							<Card 
								id={assignment.assignmentID}
								isProf={this.props.isProf}
								isAssignment={true}
								pastDue={assignment.pastDue}
								gradeTotal={assignment.gradeTotal}
								title={assignment.title}
								body={assignment.task}
								time={"Deadline: " + assignment.deadline}
								onClick={this.handleOnClickAssignment}
								handleSubmitAssign={this.toggleSubmitAssignmentModal}
								bgColor={assignmentID === assignment.assignmentID ? '#eae4c5' : '' }
								handleSeeSubmissions={this.handleSeeSubmissions}
								handleDownload={this.handleDownloadAssignment}
							/>
						);
					})
					this.setState({ assignments });
				}
			}
		// }
	}

	handleDeleteAssignment(e) {
		console.log('delete assignment', this.state.selectedAssignment);
		
		if (this.state.selectedAssignment) {
			fetch('/api/deleteAssignment/' + this.state.selectedAssignment, {
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
						window.location.reload();
					});
				} else {
						console.log('error while deleting assignment');
						alert('Something went wrong!');
						window.location.reload();
					}
			});
		}	}

	handleCreateAssignment(event) {
		// event.preventDefault();

		const data = {
			courseID: this.props.courseID,
			title: event.target.title.value,
			task: event.target.task.value,
			deadline: event.target.deadline.value, 
			gradeTotal: event.target.gradeTotal.value, 
		}
		 console.log(data);

		fetch('/api/createAssignment', {
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
		// e.preventDefault();
		console.log('submit assignment for', this.state.selectedAssignment);
		const data = {
			assignmentID: this.state.selectedAssignment,
			studentID: cookie.load('userID'),
			content: submittedAssignment
		}
		console.log(data);
		fetch('/api/submitAssignment', {
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
					window.location.reload();
				});
			}
			else{
				// window.location.replace("/error");
				console.log('error while posting Assignment')
				alert('Fail to submit, somthing went wrong');
			}
		});
	}

	handleSeeSubmissions(e, assignmentID) {
		console.log('see submissions for', assignmentID);
		window.location = '/submissions/' + assignmentID
	}

	handleDownloadAssignment(e, assignmentID) {
		console.log('download assignment', assignmentID);
		alert('Download feature is currently not available.');
		window.location.reload()
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
						<CreateAssignmentModal
							isOpen={this.state.createAssignmentModal}
							toggle={this.toggleCreateAssignmentModal}
							handleSubmit={this.handleCreateAssignment}
							header="New Assignment"
						/>
						<Button 
							className="other-button"
							onClick={(e) => {this.handleDownloadAssignment(e, this.state.selectedAssignment)}}
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
					<Button 
						className="other-button"
						onClick={this.handleDownloadAssignment}
					>
						Download
					</Button>
				</div>
			);
		}
  }
};

export default Assignments;