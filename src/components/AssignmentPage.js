import React, {Component} from 'react';
import cookie from 'react-cookies';
import Assignments from './Assignments.js';
import SideBar from './SideBar.js';
import CoursePageHeader from './CoursePageHeader.js';

class AssignmentsPage extends Component {
	constructor(props) {
		super(props);

		this.state = {
			userID: 0,
			userType: 3,
			assignments: [],
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
		const courseID = courseInfo.courseID; // get params from url
		this.setState({ userID, userType, courseID, courseInfo });

		fetch('/api/assignments/' + courseID + '/' + userID)
			.then((res) => {
				console.log(res);
				if (res.ok) {
					res.json().then(data => ({
						data: data,
						status: res.status
					})).then(res => {
						console.log(res);
						const assignments = (
							<Assignments 
								isProf={this.state.userType == 1} 
								assignments={res.data}
								courseID={this.state.courseID} 
							/>
						);
						this.setState({ assignments });
					});
				} else {
						console.log('error while fetching assignments');
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
						{this.state.assignments}
					</div>

				</div>

			</div>

		);
	}
}

export default AssignmentsPage;