import React, { Component } from 'react';
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table';
import '../../node_modules/react-bootstrap-table/dist/react-bootstrap-table-all.min.css';

class GradeBookTable extends Component {

  constructor(props) {
    super(props);
    this.state = {
      columns: [<TableHeaderColumn width='110' dataField='ID' isKey={ true }>Student ID</TableHeaderColumn>,
      <TableHeaderColumn dataField='name' editable={false} tdStyle={ { whiteSpace: 'normal' } } >Student Name</TableHeaderColumn>],
      percentage: [],
    }

    this.onAfterSaveCell = this.onAfterSaveCell.bind(this);
  }

  componentDidMount() {
    console.log('props for table', this.props);

    let percentage = [
      <h5 className="card-text">Assignments: {this.props.data.percentage.assignmentPercentage}%</h5>
    ]
    let columns = this.state.columns;
    for (let key in this.props.data.title) {
      columns.push(
        <TableHeaderColumn 
          dataField={key}
          editable={ { validator: (val) => {if (val > this.props.data.gradeTotal[key]) {return 'Cannot exceed grade total ' + this.props.data.gradeTotal[key] + '!' ;} else if (val < 0) {return 'Cannot enter negative number!';} return true;} } }
        >
          {this.props.data.title[key]}
        </TableHeaderColumn>
      );
      if (key.substring(0, 2) == 'ex') {
        percentage.push(
          <h5 className="card-text">{this.props.data.title[key]}: {this.props.data.percentage[key]}%</h5>
        )
      }
    }
    columns.push(
      <TableHeaderColumn dataField='final' editable={false} >Est. Final Grade</TableHeaderColumn>
    )
    this.setState({ columns, percentage });
  }

  onAfterSaveCell(row, cellName, cellValue) {  
    console.log(row, cellName.substring(0,2), cellValue);
    if (cellName.substring(0,2) === 'as') {
      // call grade assignment api
      const data = {
        studentID: row['ID'],
        assignmentID: cellName.substring(2, cellName.length),
        assignmentGrade: cellValue
      }
      console.log('data', data);
      fetch('/api/gradeAssignment', {
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
              alert(`Entered grade ${this.props.data.title[cellName]}: ${cellValue} for ${row.name}.`);
              console.log(res);
              window.location.reload();
            });
          }
          else{
            // window.location.replace("/error");
            console.log('error while grading assignment')
          }
        });
    } else {
      // call grade exam api 
      const data = {
        studentID: row['ID'],
        examID: cellName.substring(2, cellName.length),
        examGrade: cellValue
      }
      console.log('data', data);
      fetch('/api/gradeExam', {
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
              alert(`Entered grade ${this.props.data.title[cellName]}: ${cellValue} for ${row.name}.`);
              console.log(res);
              window.location.reload();
            });
          }
          else{
            // window.location.replace("/error");
            console.log('error while grading Exam')
          }
        });
    };
  }

  render() {
    const cellEditProp = {
      mode: 'click', // click cell to edit
      afterSaveCell: this.onAfterSaveCell,  // a hook for after saving cell
    };
    let colWidth = (100 + Object.keys(this.props.data.gradeTotal).length * 11).toString() + '%'
    return (
      <div className="">
        <div 
          className="card smallcard" 
          style = {{
            backgroundColor: '#eae4c5', 
            width: 400+'px',
            margin: 0+' auto'
          }}
        >
          {/* <div className="percentage-header">
            <h4 style={{fontWeight: 'bold'}}>Percentage</h4>
          </div> */}
          <div className="card-body">
            {this.state.percentage}
          </div>
        </div>

        <div id="scrolltable">
        <BootstrapTable data = {this.props.data.data} cellEdit={ cellEditProp } striped version='4' containerStyle={{width: colWidth, overflowX: 'scroll'}}>
          {this.state.columns}
        </BootstrapTable>
        </div>
      </div>
    );
  }
}

export default GradeBookTable;