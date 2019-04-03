import React, { Component } from 'react';
import { Button } from 'reactstrap';
import CreateAnnouncementModal from './modals/CreateAnnouncementModal.js';


class CreateAnnouncement extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modal: false
    };

    this.toggle = this.toggle.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  toggle() {
    this.setState({
      modal: !this.state.modal
    });
  }


  handleSubmit(event) {
      //event.preventDefault();

      // const loginData = {
      //     EmailAddress: event.target.EmailAddress.value,
      //     UniquePassword:event.target.UniquePassword.value
			// };
			const data = {
				courseID: this.props.courseID,
				announcement: event.target.Announcement.value
			}
      console.log(data);

      fetch('http://localhost:5000/api/createAnnouncement', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(data)
      }).then((res) => {

        console.log(res)
        if(res.ok) {
          res.json().then(data => ({
            data: data,
            status: res.status
          })).then(res => {
						console.log(res);
          });
        }
        else{
					// window.location.replace("/error");
					console.log('error while posting announcement')
        }

      });

      //this.closeModal();

  }

  render() {
    return (
      <div>
        <CreateAnnouncementModal
          isOpen={this.state.modal}
          toggle={this.toggle}
          closeModal = {this.closeModal}
          handleSubmit = {this.handleSubmit}
        />
      <Button color="primary" onClick={this.toggle}>
          {this.props.label}
        </Button>
      </div>
    );
  }
}

export default CreateAnnouncement;
