import React, { Component } from 'react';

class Card extends Component {
  constructor(props) {
    super(props);
    this.state = {

    };
  }

  componentDidMount() {

  }

  render() {
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
};

export default Card;