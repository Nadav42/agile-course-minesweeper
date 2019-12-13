import React from "react";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Board from './components/minesweeper/Board'
import LobbiesPanel from './components/lobbies/LobbiesPanel'

import './css/main.css'

// Call it once in your app. At the root of your app is the best place
toast.configure()

function LobbiesRoute() {
	return (
		<div>
			<div className="mb-5"></div>
			<div className="container text-center">
				<h1>Lobbies</h1>
			</div>
			<div className="container text-center mx-auto">
				<LobbiesPanel />
			</div>
		</div>
	);
}

function BoardRoute() {
	return (
		<div>
			<div className="mb-5"></div>
			<div className="container text-center">
				<h1>Minesweeper</h1>
			</div>
			<div className="container text-center mx-auto">
				<Board />
			</div>
		</div>
	);
}

// App
class App extends React.Component {
	
	render() {
		return (
			<Router>
				<div>
					<Switch>
						<Route path="/game">
							<BoardRoute />
						</Route>
						<Route path="/">
							<LobbiesRoute />
						</Route>
					</Switch>
				</div>

				<ToastContainer />
			</Router>
		);
	}
}

export default App;