import React from "react";

import Board from './components/minesweeper/Board'

import './css/main.css'

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
					<Board rows={8} cols={8} />
				</div>
			</div>
		);
	}
}

export default App;