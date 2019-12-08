import React from 'react';
import socketIOClient from "socket.io-client";

import { url, getMinesweeperBoard, postBoardClick, postBoardFlagClick, postBoardReset } from '../../api/rest_api'

function CellMine(props) {
    return (
        <div className="game-cell mine">
        </div>
    );
}

function CellFlag(props) {

    // in flag mode normal click calls flag click
    const flagModeClick = () => {
        props.handleCellClick(props.rowNum, props.colNum);
    }

    // right click (or hold in android)
    const flagRightClick = (e) => {
        props.handleCellFlagClick(props.rowNum, props.colNum);
        e.preventDefault();
    }

    if (props.flagMode) {
        return <div className="game-cell flag" onClick={flagModeClick}></div>;
    }
    else {
        return <div className="game-cell flag" onContextMenu={flagRightClick}></div>;
    }


}

function CellNumber(props) {
    let numberClass = `num-${props.number}`;

    return (
        <div className="game-cell">
            <span className={`cell-value ${numberClass}`}>{props.number}</span>
        </div>
    );
}

function FlatCell(props) {
    return (
        <div className="game-cell"></div>
    );
}

function ClickableCell(props) {
    const cellClick = () => {
        props.handleCellClick(props.rowNum, props.colNum);
    }

    const flagClick = (e) => {
        props.handleCellFlagClick(props.rowNum, props.colNum);
        e.preventDefault();
    }

    return (
        <div className="game-cell filled" onClick={cellClick} onContextMenu={flagClick}></div>
    );
}

function Cell(props) {
    let rowNum = props.rowNum;
    let colNum = props.colNum;

    if (rowNum === undefined || colNum === undefined) {
        return null;
    }

    if (props.number) {
        return <CellNumber number={props.number} />;
    }
    else if (props.flag) {
        return <CellFlag rowNum={props.rowNum} colNum={props.colNum} handleCellClick={props.handleCellClick} handleCellFlagClick={props.handleCellFlagClick} flagMode={props.flagMode} />;
    }
    else if (props.mine) {
        return <CellMine />;
    }

    if (props.flat) {
        return <FlatCell />;
    }

    return <ClickableCell rowNum={props.rowNum} colNum={props.colNum} handleCellClick={props.handleCellClick} handleCellFlagClick={props.handleCellFlagClick} />;
}

function Row(props) {
    let cells = [];

    if (!props.rowData || props.rowNum === undefined) {
        return null;
    }

    // {"clicked": ..., "flag": ..., "mine": ..., "adjacentMines": ...}
    let rowData = props.rowData;
    let rowNum = props.rowNum;
    let handleCellClick = props.handleCellClick;
    let handleCellFlagClick = props.handleCellFlagClick;

    for (let i = 0; i < rowData.length; i++) {
        let cellData = rowData[i];

        // mark data
        let flag = false;
        let flat = false;
        let mine = false;
        let number = undefined;

        if (!cellData.clicked && cellData.flag) {
            flag = true;
        }
        else if (cellData.clicked && cellData.adjacentMines !== undefined) {
            if (cellData.adjacentMines > 0) {
                number = cellData.adjacentMines;
            }
            else {
                flat = true; // number = 0 => show flat cell
            }
        }
        else if (cellData.mine) {
            mine = true;
        }

        // add cell
        cells.push(<Cell key={`col-${i}`} rowNum={rowNum} colNum={i} flag={flag} flat={flat} mine={mine} number={number} handleCellClick={handleCellClick} handleCellFlagClick={handleCellFlagClick} flagMode={props.flagMode} />)
    }

    return (
        <div className="game-row">
            {cells}
        </div>
    );

    // <Cell></Cell>
    //     <Cell flat></Cell>
    //     <CellMine></CellMine>
    //     <CellFlag></CellFlag>
}

function GameFinishMessage(props) {
    let finished = props.finished;
    let won = props.won;

    if (!finished) {
        return null;
    }

    if (won) {
        return <h3 className="text-success">You win!</h3>
    }
    else {
        return <h3 className="text-danger">You lost!</h3>
    }
}

function FlagModeButton(props) {
    let activeClass = "";

    if (props.flagMode) {
        activeClass = "active";
    }

    return (
        <div className="d-md-none">
            <div className={`flag-mode-container ${activeClass}`} onClick={props.handleFlagModeClick}>
                <div className="flag-mode-button"></div>
            </div>
        </div>
    );
}

function Difficulty(props) {

    let probToOneMine = (1 / (props.boardSize));
    return (
        <div className="my-3">
            <input type="range" className="custom-range" id="customRange1" min={probToOneMine * 8} max={probToOneMine * 30} step={probToOneMine} value={props.value} onChange={props.mineProbabilityChanged} />
        </div>
    );
}

class Board extends React.Component {
    state = { boardData: null, flagMode: false, mine_probability: 11 / (this.props.rows * this.props.cols) }

    constructor(props) {
        super(props);

        this.socket = socketIOClient(url);
    }

    componentDidMount() {
        this.updateBoardData();

        this.socket.on("boardChanged", this.updateBoardData);
    }

    componentWillUnmount() {
        this.socket.off("boardChanged", this.updateBoardData);
    }

    updateBoardData = async () => {
        let data = await getMinesweeperBoard();
        this.setState({ boardData: data });

        console.log(this.state);
    }


    handleCellClick = (row, col) => {
        // if flag mode is active then normal click actually calls flag click (mobile support)
        if (this.state.flagMode) {
            this.handleCellFlagClick(row, col);
            return;
        }

        // normal click
        postBoardClick(row, col, this.updateBoardData);
    }

    handleCellFlagClick = (row, col) => {
        postBoardFlagClick(row, col, this.updateBoardData);
    }

    handleBoardReset = () => {
        let rows = this.props.rows;
        let cols = this.props.cols;
        let mine_probability = this.state.mine_probability;

        postBoardReset(rows, cols, mine_probability, this.updateBoardData);
    }

    mineProbabilityChanged = (e) => {
        this.setState({ mine_probability: e.target.value });
    }

    handleFlagModeClick = () => {
        this.setState({ flagMode: !this.state.flagMode });
    }
    render() {
        if (!this.state.boardData || !this.state.boardData.board) {
            return null;
        }

        let boardData = this.state.boardData;
        let board = boardData.board;

        let rowElements = []

        for (let i = 0; i < board.length; i++) {
            rowElements.push(<Row key={`row-${i}`} rowNum={i} rowData={board[i]} handleCellClick={this.handleCellClick} handleCellFlagClick={this.handleCellFlagClick} flagMode={this.state.flagMode} />)
        }

        return (
            <div>
                <div className="game-board">
                    {rowElements}
                </div>
                <div className="slidecontainer" >
                    <p>Difficulty:</p>
                    <Difficulty boardSize={this.props.rows * this.props.cols} mineProbabilityChanged={this.mineProbabilityChanged} />
                </div>

                <div className="mb-3"></div>
                <GameFinishMessage finished={boardData.finished} won={boardData.won} />
                <button type="button" className="btn btn-secondary" onClick={this.handleBoardReset}>Reset Game</button>

                <FlagModeButton flagMode={this.state.flagMode} handleFlagModeClick={this.handleFlagModeClick} />
            </div>
        );
    }
}

export default Board;
