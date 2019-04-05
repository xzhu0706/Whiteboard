import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import LoginPage from './components/LoginPage.js';
import HomePage from './components/HomePage.js';
import CoursePage from './components/CoursePage.js';
import MaterialsPage from './components/MaterialsPage.js';
import AssignmentPage from './components/AssignmentPage.js';
import SubmissionsPage from './components/SubmissionsPage.js';
import { BrowserRouter as Router, Route, Switch} from 'react-router-dom';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App">
        <Router>
          <Switch>
            <Route path="/" exact component={LoginPage} />
            <Route path="/login" component={LoginPage} />
            <Route path="/home/:userID" component={HomePage} />
            <Route path="/course/:courseID" component={CoursePage} />
            <Route path="/materials/:courseID" component={MaterialsPage} />
            <Route path="/assignments/:courseID" component={AssignmentPage} />
            <Route path="/submissions/:assignmentID" component={SubmissionsPage} />
          </Switch>
        </Router>
      </div>
      </div>
    );
  }
}

export default App;
