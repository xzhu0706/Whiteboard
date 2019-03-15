import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import LoginPage from './components/LoginPage.js';
import HomePage from './components/HomePage.js';
import { BrowserRouter as Router, Route, Switch} from 'react-router-dom';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App">
        <Router>
          <Switch>
            <Route path="/home/:userID" component={HomePage} />
            <Route path="/" exact component={LoginPage} />
            <Route path="/login" component={LoginPage} />
          </Switch>
        </Router>
      </div>
      </div>
    );
  }
}

export default App;
