import React, {Component} from 'react';

class CoursePageHeader extends Component {

	render() {
		return(
			<div>
				<h1 className="course-name"> 
					{this.props.courseInfo.courseName} {this.props.courseInfo.semester} {this.props.courseInfo.year} 
				</h1>

				<div className="professor-contact-info">
					<h3>{this.props.courseInfo.professorName}</h3>
					<h3>{this.props.courseInfo.professorEmail}</h3>
				</div>
			</div>
		);
	}
}

export default CoursePageHeader;