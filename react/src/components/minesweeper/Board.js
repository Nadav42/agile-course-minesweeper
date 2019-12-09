import React from 'react';
import socketIOClient from "socket.io-client";

import { url, getMinesweeperBoard, getDifficultyRange, postBoardClick, postBoardFlagClick, postBoardReset } from '../../api/rest_api'

// ---------------------- sounds ----------------------
import UIfx from 'uifx'

import winningSound1 from './winningSound.wav'
const winningSound = new UIfx(winningSound1, { volume: 0.25 });
// --------------------------------------------------- //

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
        return <div className="game-cell filled flag" onClick={flagModeClick}></div>;
    }
    else {
        return <div className="game-cell filled flag" onContextMenu={flagRightClick}></div>;
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
        return <h3 className="text-success mt-4">You win!</h3>
    }
    else {
        return <h3 className="text-danger mt-4">You lost!</h3>
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
    let difficulty = props.difficulty; // 0.13 - sent from server.
    let difficultyRangeData = props.difficultyRangeData; // {min: 0.07, max: 0.37} - sent from server.

    if (!difficulty || !difficultyRangeData) {
        return null;
    }

    // slider range and steps settings
    const minDifficulty = difficultyRangeData.min;
    const maxDifficulty = difficultyRangeData.max;
    const steps = 20; // how many steps the slider should fill

    // don't touch
    const stepSize = (maxDifficulty - minDifficulty) / steps;

    return (
        <div className="my-3 text-center">
            <input type="range" className="custom-range" value={props.difficulty} min={minDifficulty} max={maxDifficulty} step={stepSize} onChange={props.handleDifficultyChange} />
        </div>
    );
}

class Board extends React.Component {
    state = { boardData: null, difficultyRangeData: null, flagMode: false, difficulty: null, rows: 9, cols: 9 }

    constructor(props) {
        super(props);

        this.lastDifficulty = null;
        this.lastRows = null;
        this.lastCols = null;

        this.socket = socketIOClient(url);
    }

    componentDidMount() {
        this.updateBoardData();
        this.updateDifficultyRange();

        this.socket.on("boardChanged", this.updateBoardData);
    }

    componentWillUnmount() {
        this.socket.off("boardChanged", this.updateBoardData);
    }

    updateBoardData = async (playWinSound) => {
        let data = await getMinesweeperBoard();
        this.setState({ boardData: data });

        // init difficulty from server, only update when server value changed.
        if (data && data.difficulty && this.lastDifficulty !== data.difficulty) {
            this.lastDifficulty = data.difficulty;

            // only update view if value changed on server
            this.setState({ difficulty: data.difficulty });
        }

        // init from server, only update when server value changed.
        if (data && data.board) {
            let rows = data.board.length;
            let cols = data.board[0].length;

            if (this.lastRows !== rows || this.lastCols !== cols) {
                this.lastRows = rows;
                this.lastCols = cols;

                this.setState({ rows: rows, cols: cols })
            }
        }

        // play sound only after the winning click
        if (playWinSound === true) {
            if (data.won) {
                winningSound.play();
            }
        }
    }

    updateDifficultyRange = async () => {
        let data = await getDifficultyRange();
        this.setState({ difficultyRangeData: data });

        console.log(this.state);
    }

    handleCellClick = (row, col) => {
        // if flag mode is active then normal click actually calls flag click (mobile support)
        if (this.state.flagMode) {
            this.handleCellFlagClick(row, col);
            return;
        }

        const updateBoardAndCheckWinSound = () => {
            this.updateBoardData(true);
            this.socket.emit("boardAction");
        }

        // normal click
        postBoardClick(row, col, updateBoardAndCheckWinSound);
    }

    handleCellFlagClick = (row, col) => {
        // send action to server, then request new board state and notify other users
        const updateBoardDataAndNotifyAction = () => {
            this.updateBoardData();
            this.socket.emit("boardAction");
        }

        postBoardFlagClick(row, col, updateBoardDataAndNotifyAction);
    }

    handleBoardReset = () => {
        let rows = this.state.rows;
        let cols = this.state.cols;
        let difficulty = this.state.difficulty;

        // send action to server, then request new board state and notify other users
        const updateBoardDataAndNotifyAction = () => {
            this.updateBoardData();
            this.socket.emit("boardAction");
        }

        postBoardReset(rows, cols, difficulty, updateBoardDataAndNotifyAction);
    }

    handleDifficultyChange = (e) => {
        this.setState({ difficulty: e.target.value });
    }

    handleRowsColsInputChange = (e) => {
        this.setState({ rows: e.target.value, cols: e.target.value });
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
            <div className="mb-5">

                <div className="game-contianer">
                    <div className="game-board">
                        {rowElements}
                    </div>
                </div>

                <hr></hr>

                <div className="form-group text-left mx-auto reset-form">
                    <div className="row text-center mt-3 mb-3">
                        <div className="col-6">
                            <label>Rows</label>
                            <input type="text" className="form-control" value={this.state.rows} onChange={this.handleRowsColsInputChange} />
                        </div>
                        <div className="col-6">
                            <label>Cols</label>
                            <input type="text" className="form-control" value={this.state.cols} onChange={this.handleRowsColsInputChange} />
                        </div>
                    </div>

                    <div className="slidecontainer" >
                        <p>Difficulty:</p>
                        <Difficulty difficulty={this.state.difficulty} difficultyRangeData={this.state.difficultyRangeData} handleDifficultyChange={this.handleDifficultyChange} />
                    </div>
                </div>



                <div className="mb-3"></div>
                <button type="button" className="btn btn-secondary" onClick={this.handleBoardReset}>Reset Game</button>

                <GameFinishMessage finished={boardData.finished} won={boardData.won} />
                <FlagModeButton flagMode={this.state.flagMode} handleFlagModeClick={this.handleFlagModeClick} />
            </div >
        );
    }
}

export default Board;
