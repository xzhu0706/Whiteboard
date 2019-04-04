import React, {Component} from 'react';
import cookie from 'react-cookies';
import Materials from './Materials.js';
import SideBar from './SideBar.js';
import CoursePageHeader from './CoursePageHeader.js';

class MaterialsPage extends Component {
	constructor(props) {
		super(props);

		this.state = {
			userID: 0,
			userType: 3,
			materials: [],
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

		fetch('http://localhost:5000/api/materials/' + courseID)
			.then((res) => {
				console.log(res);
				if (res.ok) {
					res.json().then(data => ({
						data: data,
						status: res.status
					})).then(res => {
						console.log(res);
						const materials = (
							<Materials 
								isProf={this.state.userType == 1} 
								materials={res.data}
								courseID={this.state.courseID} 
							/>
						);
						this.setState({ materials });
					});
				} else {
						console.log('error while fetching materials');
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
						{this.state.materials}
					</div>

				</div>

			</div>

		);
	}
}

export default MaterialsPage;