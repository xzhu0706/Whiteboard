import React, { Component } from 'react';
import Card from './Card.js';
import { Button } from 'reactstrap';

class Submissions extends Component {
  constructor(props) {
    super(props);
    this.state = {
			submissions: [],
			selectedSubmission: '',
		};
		
		this.handleDownloadSubmission = this.handleDownloadSubmission.bind(this);
		this.handleGradeSubmission = this.handleGradeSubmission.bind(this);
	}

	componentDidMount() {
		console.log('props for Submission component', this.props);
		if (this.props.submissions.length > 0) {
			const submissions = this.props.submissions.map((submission) => {
				return (
					<Card 
						id={submission.submissionID}
						studentName={submission.studentName}
						isSubmission={true}
						isSubmitted={submission.isSubmitted}
						isLate={submission.isLate}
						pastDue={submission.pastDue}
						// isGraded={submission.isGraded}
						grade={submission.assignmentGrade}
						gradeTotal={submission.gradeTotal}
						body={submission.content}
						time={submission.submitTime}
						// onClick={this.handleOnClickSubmission}
						handleGradeSubmission={this.handleGradeSubmission}
						handleDownload={this.handleDownloadSubmission}
					/>
				);
			})
			this.setState({ submissions });
		}
	}
	
	// handleOnClickSubmission(e, submissionID) {
	// 	console.log(submissionID);
	// 	this.setState({
	// 		selectedSubmission: submissionID
	// 	});
	// 	// console.log(this.state.selectedSubmission);
	// 	if (this.props.submissions.length > 0) {
	// 		const submissions = this.props.submissions.map((submission) => {
	// 			return (
	// 				<Card 
	// 					id={submission.submissionID}
	// 					isProf={this.props.isProf}
	// 					isSubmission={true}
	// 					notSubmitted={true} //need to modify later, need this from backend
	// 					body={submission.task}
	// 					time={"Deadline: " + submission.deadline}
	// 					onClick={this.handleOnClickSubmission}
	// 					bgColor={submissionID === submission.submissionID ? '#ea8383' : '' }
	// 					borderColor={submissionID === submission.submissionID ? 'red' : ''}
	// 					handleSubmitAssign={this.toggleSubmitSubmissionModal}
	// 					handleSeeSubmissions={this.handleSeeSubmissions}
	// 				/>
	// 			);
	// 		})
	// 		this.setState({ submissions });
	// 	}
	// }

	handleGradeSubmission(e, submissionID) {
		// e.preventDefault();
		console.log('enter grade for', submissionID);
		if (e.target.grade.value >= 0) {
			const data = {
				submissionID: submissionID,
				assignmentGrade: e.target.grade.value,
			}
			console.log('data', data);
			fetch('http://localhost:5000/api/gradeSubmission', {
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
						if (res.data.update === false) {
							alert('Fail to enter grade because no submission received. Please go to Grade Book to enter grade for non-received assignment.')
						}
					});
				}
				else {
					// window.location.replace("/error");
					console.log('error while grading Submission')
				}
			});
		}
	}

	handleDownloadSubmission(e, submissionID) {
		console.log('download submission', submissionID);
		alert('Download feature is currently not avialable.');
		window.location.reload()
		//TODO: if we implement uploading&downloading files 
	}

  render() {
		return (
			<div className="card submission-section">

				<div className="header thumbnail">
					Submissions
				</div>

				<div className="card-body">
					{this.state.submissions}
				</div>
				
			</div>
		);
	}
};

export default Submissions;