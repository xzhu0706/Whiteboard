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
      <div className="card">
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