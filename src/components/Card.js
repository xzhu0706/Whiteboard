import React, { Component } from 'react';
import { Button } from 'reactstrap';

class Card extends Component {
  constructor(props) {
    super(props);
    this.state = {

    };
  }

  componentDidMount() {

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
              {/* {this.props.header} */}
              <Button className="jutify-content-sm-end" onClick={this.props.handleSeeSubmissions}>Submissions</Button>
            </div>
            <div className="card-body">
              <h5 className="card-text">{this.props.body}</h5>
              <h6 className="card-text text-muted text-right">{this.props.time}</h6>
            </div>
          </div>
        );
      } else { //for student
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
              {/* {this.props.header} */}
              <Button className="jutify-content-sm-end" onClick={this.props.notSubmitted ? this.props.handleSubmitAssign : (e) => {}}>Submit</Button>
            </div>
            <div className="card-body">
              <h5 className="card-text">{this.props.body}</h5>
              <h6 className="card-text text-muted text-right">{this.props.time}</h6>
            </div>
          </div>
        );
      }
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