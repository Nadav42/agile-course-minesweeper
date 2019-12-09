import React from "react";

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Board from './components/minesweeper/Board'

import './css/main.css'

// Call it once in your app. At the root of your app is the best place
toast.configure()

// App
class App extends React.Component {
	state = {};

	componentDidMount() {
	}

	render() {

		return (
			<div>
				<div className="mb-5"></div>
				<div className="container text-center">
					<h1>Minesweeper</h1>
				</div>
				<div className="container text-center mx-auto">
					<Board />
				</div>

				<ToastContainer />
			</div>
		);
	}
}

export default App;