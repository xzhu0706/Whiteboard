import React, { Component } from 'react';
import Card from './Card.js';
import { Button } from 'reactstrap';
import SingleInputFieldModal from './modals/SingleFieldModal.js';

class Materials extends Component {
  constructor(props) {
    super(props);
    this.state = {
			materials: 'None',
			materialsList: [],
			selectedMaterial: '',
			createMaterialModal: false,
		};
		
		this.toggleCreateMaterialModal = this.toggleCreateMaterialModal.bind(this);
		this.handleOnClickMaterial = this.handleOnClickMaterial.bind(this);
		this.handleDeleteMaterial = this.handleDeleteMaterial.bind(this);
		this.handleCreateMaterial = this.handleCreateMaterial.bind(this);
		this.handleDownloadMaterial = this.handleDownloadMaterial.bind(this);
	}

	componentDidMount() {
		console.log('props for Material component',this.props);
		this.setState({
			materialsList: this.props.materials
		})
		if (this.props.materials.length > 0) {
			const materials = this.props.materials.map((material) => {
				return (
					<Card 
						id={material.materialID}
						body={material.material}
						time={"posted at " + material.postTime}
						onClick={this.handleOnClickMaterial}
					/>
				);
			})
			this.setState({ materials });
		}
	}
	
	handleOnClickMaterial(e, materialID) {
		console.log(materialID);
		this.setState({
			selectedMaterial: materialID
		});
		console.log(this.state.selectedMaterial);
		if (this.props.materials.length > 0) {
			const materials = this.props.materials.map((material) => {
				return (
					<Card 
						id={material.materialID}
						bgColor={materialID === material.materialID ? '#ea8383' : '' }
						borderColor={materialID === material.materialID ? 'red' : ''}
						body={material.material}
						time={"posted at " + material.postTime}
						onClick={this.handleOnClickMaterial}
					/>
				);
			})
			this.setState({ materials });
		}
	}

	handleDeleteMaterial(e) {
		console.log('delete material', this.state.selectedMaterial);

		if (this.state.selectedMaterial) {
			fetch('http://localhost:5000/api/deleteMaterial/' + this.state.selectedMaterial, {
				method: 'DELETE'
			})
			.then((res) => {
				console.log(res);
				if (res.ok) {
					res.json().then(data => ({
						data: data,
						status: res.status
					})).then(res => {
						console.log(res);
					});
				} else {
						console.log('error while deleting material');
					}
			});
			window.location.reload();
		}	}

	handleCreateMaterial(event, material) {
//		event.preventDefault();
		const data = {
			courseID: this.props.courseID,
			material: material
		}
		console.log(data);

		fetch('http://localhost:5000/api/createMaterial', {
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
				console.log('error while posting Material')
			}

		});
	}

	handleDownloadMaterial(e) {
		console.log('download material', this.state.selectedMaterial);
		//TODO: if we implement uploading&downloading files 
	}

	toggleCreateMaterialModal() {
		this.setState({
			createMaterialModal: !this.state.createMaterialModal
		})
	}


  render() {
		if (this.props.isProf) {
			return (
				<div className="card material-section">

					<div className="header thumbnail">
						Materials
					</div>

					<div className="card-body">
						{this.state.materials}
					</div>

					<div className="card-footer">
						{/* for create, delete buttons */}
						<SingleInputFieldModal
							isOpen={this.state.createMaterialModal}
							toggle={this.toggleCreateMaterialModal}
							handleSubmit={this.handleCreateMaterial}
							header="New Material"
						/>
						<Button 
							className="other-button"
							color="secondary"
							onClick={this.handleDownloadMaterial}
						>
							Download
						</Button>
						<Button 
							className="other-button"
							color="info"
							onClick={this.toggleCreateMaterialModal}
						>
							Create
						</Button>
						<Button 
							className="other-button"
							color="warning"
							onClick={this.handleDeleteMaterial}
						>
							Delete
						</Button>
					</div>

				</div>
			);
		} else {
			return (
				<div className="card material-section">
					<div className="header thumbnail">
						Class Materials
					</div>
					<div className="card-body">
						{this.state.materials}
					</div>
					<Button 
						className="other-button"
						color="secondary"
						onClick={this.handleDownloadMaterial}
					>
						Download
					</Button>
				</div>
			);
		}
  }
};

export default Materials;