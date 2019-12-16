import React from "react";

import { Router, Switch, Route } from "react-router-dom";
import { createBrowserHistory } from 'history';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Board from './components/minesweeper/Board'
import LobbiesPanel from './components/lobbies/LobbiesPanel'

import './css/main.css'

// Call it once in your app. At the root of your app is the best place
toast.configure()

function LobbiesRoute(props) {
	return (
		<div>
			<div className="mb-5"></div>
			<div className="container text-center">
				<h1 className="title">Lobbies</h1>
			</div>
			<div className="container text-center mx-auto">
				<LobbiesPanel history={props.history} />
			</div>
		</div>
	);
}

function BoardRoute() {
	return (
		<div>
			<div className="mb-5"></div>
			<div className="container text-center">
				<h1 className="title">Minesweeper</h1>
			</div>
			<div className="container text-center mx-auto">
				<Board />
			</div>
		</div>
	);
}

// App
class App extends React.Component {

	constructor(props) {
		super(props);

		this.history = createBrowserHistory();
	}
	
	render() {
		return (
			<Router history={this.history}>
				<div>
					<Switch>
						<Route path="/game">
							<BoardRoute />
						</Route>
						<Route path="/">
							<LobbiesRoute history={this.history}/>
						</Route>
					</Switch>
				</div>

				<ToastContainer />
			</Router>
		);
	}
}

export default App;