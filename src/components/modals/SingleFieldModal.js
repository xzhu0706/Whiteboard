import React, { Component } from 'react';
import {Col, Form, FormGroup, Label, Input, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class SingleInputFieldModal extends Component {
  constructor(props) {
    super(props);


	}
	
	render() {
		return (
			<div>
				<Modal isOpen={this.props.isOpen} toggle={this.props.toggle} className={this.props.className}>
            <ModalHeader toggle={this.props.toggle}>{this.props.header}</ModalHeader>
            <ModalBody>
                <Form onSubmit={(e) => {this.props.handleSubmit(e, e.target.input.value)}} >
                    <FormGroup row>
                      {/* <Label for="exampleEmail" sm={2}>Email</Label> */}
                      <Col lg={10}>
                        <Input type="text" name="input"  />
                      </Col>
                    </FormGroup>
                    <FormGroup>
                      <Col sm={10}>
                        <Button color="success">Submit</Button>
                      </Col>
                    </FormGroup>
                </Form>
            </ModalBody>
          </Modal>
			</div>
		);
	}
}

export default SingleInputFieldModal;