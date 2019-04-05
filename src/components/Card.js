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
            className="card" 
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
              <h6 className="card-text text-muted text-right">{this.props.time}</h6>
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
          }
        } else if (this.props.pastDue) {
          bgColor = "#ff7787";   //red
          note = 'Past Due'
        }
        return (
          <div 
            className="card" 
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
              <h6 className="card-text text-muted text-right">{this.props.time}</h6>
            </div>
          </div>
        );
      }
    } else if (this.props.isSubmission) {
      return (
        <div 
          className="card" 
          style = {{
            backgroundColor: this.props.bgColor, 
            borderColor: this.props.borderColor,
          }}
        >
          <div className="header thumbnail d-flex justify-content-between">
              <h4 style={{color: '#133263', fontWeight: 'bold', marginLeft: 20+'px'}}>{this.props.studentName}</h4>
              <div>
                <input 
                  type="text" 
                  className="form-control-sm" 
                  placeholder={this.props.grade}
                  onChange={this.handleInputChange}
                >
                </input>
                <Button color="danger" onClick={(e) => {this.props.handleGradeSubmission(e, this.props.id, this.state.inputGrade)}}>Enter</Button>
              </div>
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
    } else {
      return (
        <div 
          className="card" 
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