import React, { Component } from 'react';
import Card from './Card.js';
import { Button } from 'reactstrap';
// import SingleInputFieldModal from './modals/SingleFieldModal.js';
import cookie from 'react-cookies';

class Submissions extends Component {
  constructor(props) {
    super(props);
    this.state = {
			submissions: [],
			selectedSubmission: '',
		};
		
		this.handleOnClickSubmission = this.handleOnClickSubmission.bind(this);
		this.handleDownloadSubmission = this.handleDownloadSubmission.bind(this);
		this.handleGradeSubmission = this.handleGradeSubmission.bind(this);
	}

	componentDidMount() {
		//TODO
		console.log('props for Submission component',this.props);
		this.setState({
			submissionsList: this.props.submissions
		})
		if (this.props.submissions.length > 0) {
			const submissions = this.props.submissions.map((submission) => {
				return (
					<Card 
						id={submission.submissionID}
						isProf={this.props.isProf}
						isSubmission={true}
						notSubmitted={true} //need to modify later, need this from backend
						body={submission.task}
						time={"Deadline: " + submission.deadline}
						onClick={this.handleOnClickSubmission}
						handleSubmitAssign={this.toggleSubmitSubmissionModal}
						handleSeeSubmissions={this.handleSeeSubmissions}
					/>
				);
			})
			this.setState({ submissions });
		}
	}
	
	handleOnClickSubmission(e, submissionID) {
		console.log(submissionID);
		this.setState({
			selectedSubmission: submissionID
		});
		// console.log(this.state.selectedSubmission);
		if (this.props.submissions.length > 0) {
			const submissions = this.props.submissions.map((submission) => {
				return (
					<Card 
						id={submission.submissionID}
						isProf={this.props.isProf}
						isSubmission={true}
						notSubmitted={true} //need to modify later, need this from backend
						body={submission.task}
						time={"Deadline: " + submission.deadline}
						onClick={this.handleOnClickSubmission}
						bgColor={submissionID === submission.submissionID ? '#ea8383' : '' }
						borderColor={submissionID === submission.submissionID ? 'red' : ''}
						handleSubmitAssign={this.toggleSubmitSubmissionModal}
						handleSeeSubmissions={this.handleSeeSubmissions}
					/>
				);
			})
			this.setState({ submissions });
		}
	}

	handleGradeSubmission(e, grade) {
		//TODO
		console.log('enter grade for', this.state.selectedSubmission);

		const data = { //TODO: may need to modify
			submissionID: this.state.selectedSubmission,
			grade: grade
		}
		console.log('data', data);
		// fetch('http://localhost:5000/api/gradeSubmission', {
		// 	method: 'POST',
		// 	headers: {'Content-Type':'application/json'},
		// 	body: JSON.stringify(data)
		// }).then((res) => {

		// 	console.log(res)
		// 	if(res.ok) {
		// 		res.json().then(data => ({
		// 			data: data,
		// 			status: res.status
		// 		})).then(res => {
		// 			console.log(res);
		// 		});
		// 	}
		// 	else{
		// 		// window.location.replace("/error");
		// 		console.log('error while grade Submission')
		// 	}
		// });
	}

	handleDownloadSubmission(e) {
		console.log('download submission', this.state.selectedSubmission);
		//TODO: if we implement uploading&downloading files 
	}

  render() {
		//TODO
		if (this.props.isProf) {
			return (
				<div className="card submission-section">

					<div className="header thumbnail">
						Submissions
					</div>

					<div className="card-body">
						{this.state.submissions}
					</div>

					<div className="card-footer">
						<Button 
							className="other-button"
							color="success"
							onClick={this.handleDownloadSubmission}
						>
							Download
						</Button>
						<Button 
							className="other-button"
							color="info"
							onClick={this.toggleCreateSubmissionModal}
						>
							Create
						</Button>
						<Button 
							className="other-button"
							color="warning"
							onClick={this.handleDeleteSubmission}
						>
							Delete
						</Button>
					</div>

				</div>
			);
		} else {
			return (
				<div className="card submission-section">
					<div className="header thumbnail">
						Class Submissions
					</div>
					<div className="card-body">
						{this.state.submissions}
					</div>
					<Button 
						className="other-button"
						color="success"
						onClick={this.handleDownloadSubmission}
					>
						Download
					</Button>
				</div>
			);
		}
  }
};

export default Submissions;