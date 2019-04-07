import React, { Component } from 'react';
import { Button } from 'reactstrap';

class Card extends Component {
  constructor(props) {
    super(props);
    this.state = {

    };
    this.handleInputChange = this.handleInputChange.bind(this);
  }

  componentDidMount() {

  }

  handleInputChange(e) {
    console.log(e.target.value);
    this.setState({
      inputGrade: e.target.value
    })
  }

  render() {
    if (this.props.isAssignment) { // for assignment
      if (this.props.isProf) { // for professor
        return (
          <div 
            className="card smallcard" 
            onClick={(e) => this.props.onClick(e, this.props.id)}
            style = {{
              backgroundColor: this.props.bgColor, 
              borderColor: this.props.borderColor,
            }}
          >
            <div className="header thumbnail d-flex">
              <Button className="jutify-content-sm-end" onClick={(e) => {this.props.handleSeeSubmissions(e, this.props.id)}}>Submissions</Button>
            </div>
            <div className="card-title">
              {this.props.title}
            </div>
            <div className="card-body">
              <h5 className="card-text">{this.props.body}</h5>
              <div className="card-text text-muted d-flex justify-content-between">
                <h6 className="">Grade Total: {this.props.gradeTotal}</h6>
                <h6 className="">{this.props.time}</h6>
              </div>
            </div>
          </div>
        );
      } else { //for student
        let bgColor = '';
        let note = '';
        if (this.props.isSubmitted) {
          if (this.props.isLate) {
            bgColor = "#edf464"; //yellow
            note = 'Late';
          } else {
            bgColor = "#88ea8b"; //green
            note = 'Submitted'
          }
        } else if (this.props.pastDue) {
          bgColor = "#ff7787";   //red
          note = 'Past Due'
        }
        return (
          <div 
            className="card smallcard" 
            onClick={(e) => this.props.onClick(e, this.props.id)}
            style = {{
              backgroundColor: bgColor, 
              borderColor: this.props.borderColor,
            }}
          >
            <div className="header thumbnail d-flex justify-content-between">
              <Button color={this.props.isSubmitted ? "secondary" : "info"} onClick={!this.props.isSubmitted ? this.props.handleSubmitAssign : (e) => {}}>Submit</Button>
              <h5 style={{color: 'red', fontWeight: 'bold'}}>{note}</h5>
              <Button color="secondary" onClick={(e) => {this.props.handleDownload(e, this.props.id)}}>Download</Button>
            </div>
            <div className="card-title">
              {this.props.title}
            </div>
            <div className="card-body">
              <h5 className="card-text">{this.props.body}</h5>
              <div className="card-text text-muted d-flex justify-content-between">
                <h6 className="">Grade Total: {this.props.gradeTotal}</h6>
                <h6 className="">{this.props.time}</h6>
              </div>            
            </div>
          </div>
        );
      }
    } else if (this.props.isSubmission) { // for submission page
      return (
        <div 
          className="card smallcard" 
          style = {{
            backgroundColor: this.props.bgColor, 
            borderColor: this.props.borderColor,
          }}
        >
          <div className="header thumbnail d-flex justify-content-between">
            <h4 style={{color: '#133263', fontWeight: 'bold', marginLeft: 20+'px'}}>{this.props.studentName}</h4>
            <form onSubmit={(e) => {this.props.handleGradeSubmission(e, this.props.id)}}>
              <div className="form-group row">
                <input
                  name="grade"
                  type="number"
                  step="any" 
                  min={0}
                  max={this.props.gradeTotal}
                  style={{marginTop: 5+'px'}}
                  className="form-control-sm" 
                  placeholder={this.props.grade}
                  onChange={this.handleInputChange}
                  required
                  //TODO: if have time, can make a message box for this field
                /><p style={{marginTop: 10+'px'}}>/{this.props.gradeTotal}</p>
                <Button 
                  color="danger" 
                  style={{marginRight: 20+'px', marginLeft: 5+'px', marginBottom: 5+'px'}}
                >
                  Enter
                </Button>
              </div>
            </form>
          </div>
          <div className="card-body">
            <textarea disabled 
              className="form-control"
              style={{height: 100+'px'}}
            >
              {this.props.body}
            </textarea>
            <div className="d-flex justify-content-between">
              <h6 className="card-text text-muted text-left">{this.props.time === null ? this.props.time : ''}</h6>
              <Button>Download</Button>
            </div>
          </div>
        </div>
      );
    } else if (this.props.isGrade) {
      return (
        <div
          className="card smallcard"
          style = {{
            backgroundColor: this.props.bgColor, 
            borderColor: this.props.borderColor,
          }}
        >
          <div className="card-body card-text d-flex justify-content-between">
            <div className="">
              {this.props.title}
            </div>
            <div className="">
              {this.props.grade ? this.props.grade : '-'}/{this.props.gradeTotal}
            </div>
          </div>
        </div>
      )
    }
    else {
      return (
        <div 
          className="card smallcard" 
          onClick={(e) => this.props.onClick(e, this.props.id)}
          style = {{
            backgroundColor: this.props.bgColor, 
            borderColor: this.props.borderColor,
          }}
        >
          <div className="header thumbnail">
            {this.props.header}
          </div>
          <div className="card-body">
            <h5 className="card-text">{this.props.body}</h5>
            <h6 className="card-text text-muted text-right">{this.props.time}</h6>
          </div>
        </div>
      );
    }
  }
};

export default Card;