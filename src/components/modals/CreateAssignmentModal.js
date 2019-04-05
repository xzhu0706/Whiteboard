import React, { Component } from 'react';
import {Col, Form, FormGroup, Label, Input, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class CreateAssignmentModal extends Component {
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
                    <FormGroup>
                      <Label for="title" sm={2}>Title</Label>
                      <Col lg={10}>
                        <Input required type="text" name="title" />
                      </Col>
										</FormGroup>
										<FormGroup>
											<Label for="task" sm={10}>Task Description</Label>
                      <Col lg={10}>
                        <textarea required type="text" name="task" className="form-control" style={{height: 100+'px'}}  />
                      </Col>
										</FormGroup>
										{/* <FormGroup>
                      <Col lg={10}>
												<Label for="gradeTotal" sm={8}>Grade Total</Label>
                        <Input sm={4} type="text" name="gradeTotal" />
                      </Col>
                    </FormGroup> */}
										<FormGroup>
											<Label for="gradeTotal" sm={6}>Grade Total</Label>
											<Col sm={6}>
												<Input required type="number" min={1} name="gradeTotal" placeholder="" />
											</Col>
										</FormGroup>
										<FormGroup>
											<Label for="deadline" lg={6}>Deadline (Enter number of days)</Label>
											<Col sm={6}>
												<Input required type="number" min={1} name="deadline" placeholder="" />
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

export default CreateAssignmentModal;