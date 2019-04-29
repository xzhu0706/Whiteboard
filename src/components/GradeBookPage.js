import React, {Component} from 'react';
import cookie from 'react-cookies';
import GradeBook from './GradeBook.js';
import SideBar from './SideBar.js';
import CoursePageHeader from './CoursePageHeader.js';

class GradeBookPage extends Component {
	constructor(props) {
		super(props);

		this.state = {
			userID: 0,
			userType: 3,
			gradeBook: null,
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
		this.setState({ userID, userType, courseID, courseInfo });

		fetch('/api/grade/' + courseID + '/' + userID)
			.then((res) => {
				console.log(res);
				if (res.ok) {
					res.json().then(data => ({
						data: data,
						status: res.status
					})).then(res => {
						console.log(res);
						const gradeBook = (
							<GradeBook 
								gradeBook={res.data}
								courseID={courseID}
								// assignmentID={this.state.assignmentID} 
								isProf={this.state.userType === "1"}
							/>
						);
						this.setState({ gradeBook });
					});
				} else {
						console.log('error while fetching gradeBook');
					}
			});
	}



	render() {
		return (
			<div className="container-fluid">

				<CoursePageHeader courseInfo={this.state.courseInfo} />

				<div className="row">

					<div className="col-sm-3 d-flex justify-content-end">
						<SideBar />
					</div>

					<div className="col-sm-9">
						{this.state.gradeBook}
					</div>

				</div>

			</div>

		);
	}
}

export default GradeBookPage;