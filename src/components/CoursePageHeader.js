import React, {Component} from 'react';
import {Jumbotron, Container, Row, Col} from 'reactstrap';

class CoursePageHeader extends Component {

	render() {
		return(
			<div className="course-page-header">
        <Jumbotron fluid style={{height: '280px', backgroundColor: '#eae4c5'}}>
					<Container>
							<h1 className="course-name" style={{fontWeight: 'bold'}}> 
								{this.props.courseInfo.courseName} {this.props.courseInfo.semester} {this.props.courseInfo.year} 
							</h1>
							<hr className="hr-header" />
							<div className="professor-contact-info">
								<h5>Instructor: {this.props.courseInfo.professorName}</h5>
								<h5>Email: {this.props.courseInfo.professorEmail}</h5>
							</div>
					</Container>
        </Jumbotron>
			</div>
		);
	}
}

export default CoursePageHeader;