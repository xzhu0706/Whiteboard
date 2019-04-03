import React, { Component } from 'react';
import {Col, Form, FormGroup, Label, Input, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class CreateAnnouncementModal extends Component {
  constructor(props) {
    super(props);


	}
	
	render() {
		return (
			<div>
				<Modal isOpen={this.props.isOpen} toggle={this.props.toggle} className={this.props.className}>
            <ModalHeader toggle={this.props.toggle}>{this.props.header}</ModalHeader>
            <ModalBody>
                <Form onSubmit={this.props.handleSubmit} >
                    <FormGroup row>
                      {/* <Label for="exampleEmail" sm={2}>Email</Label> */}
                      <Col lg={10}>
                        <Input type="text" name="Announcement" id="announcement"  />
                      </Col>
                    </FormGroup>
                    <FormGroup>
                      <Col sm={10}>
                        <Button color="success">Create</Button>
                      </Col>
                    </FormGroup>
                </Form>
            </ModalBody>
          </Modal>
			</div>
		);
	}
}

export default CreateAnnouncementModal;