import React, {Component} from 'react';
import '../styling/CoursePageHeader.css';


class CoursePageHeader extends Component {

	render() {
		return(
			<div className="course-page-header-container">
				<h2 className="course-name"> 
					{this.props.courseInfo.courseName} {this.props.courseInfo.semester} {this.props.courseInfo.year} 
				</h2>

				<div className="professor-contact-info">
					<h2>Professor {this.props.courseInfo.professorName}</h2>
					<h2>{this.props.courseInfo.professorEmail}</h2>
				</div>
			</div>
		);
	}
}

export default CoursePageHeader;