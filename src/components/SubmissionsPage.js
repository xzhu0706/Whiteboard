import React, {Component} from 'react';
import cookie from 'react-cookies';
import Submissions from './Submissions.js';
import SideBar from './SideBar.js';
import CoursePageHeader from './CoursePageHeader.js';

class SubmissionsPage extends Component {
	constructor(props) {
		super(props);

		this.state = {
			userID: 0,
			userType: 3,
			submissions: [],
			assignmentID: 0,
			courseInfo: {
				courseID: 0,
				professorID: 0,
				courseName: '',
				semester: '',
				year: '',
				professorEmail: '',
				professorName: '',
			}
			// maybe more stuff...
		}

	}

	componentDidMount() {
		const userID = cookie.load('userID');
		const userType = cookie.load('userType');
		const courseInfo = cookie.load('courseInfo');
		const courseID = courseInfo.courseID;
		const params = this.props.match.params;
		const assignmentID = params.assignmentID;
		this.setState({ userID, userType, courseID, courseInfo, assignmentID });

		fetch('http://localhost:5000/api/submissions/' + assignmentID)
			.then((res) => {
				console.log(res);
				if (res.ok) {
					res.json().then(data => ({
						data: data,
						status: res.status
					})).then(res => {
						console.log(res);
						const submissions = (
							<Submissions 
								submissions={res.data}
								assignmentID={this.state.assignmentID} 
							/>
						);
						this.setState({ submissions });
					});
				} else {
						console.log('error while fetching submissions');
					}
			});
	}



	render() {
		return (
			<div className="container-fluid">

				<CoursePageHeader courseInfo={this.state.courseInfo} />

				<div className="row">

					<div className="col-sm-4 d-flex justify-content-end">
						<SideBar />
					</div>

					<div className="col-sm-8">
						{this.state.submissions}
					</div>

				</div>

			</div>

		);
	}
}

export default SubmissionsPage;