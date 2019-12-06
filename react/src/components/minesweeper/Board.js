import React from 'react';
import { getMinesweeperBoard, postBoardClick, postBoardFlagClick, postBoardReset } from '../../api/rest_api'

function CellMine(props) {
    return (
        <div className="game-cell mine">
        </div>
    );
}

function CellFlag(props) {
    const flagClick = (e) => {
        props.handleCellFlagClick(props.rowNum, props.colNum);
        e.preventDefault();
    }

    return (
        <div className="game-cell flag" onContextMenu={flagClick}></div>
    );
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
        return <CellFlag rowNum={props.rowNum} colNum={props.colNum} handleCellFlagClick={props.handleCellFlagClick} />;
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
        cells.push(<Cell key={`col-${i}`} rowNum={rowNum} colNum={i} flag={flag} flat={flat} mine={mine} number={number} handleCellClick={handleCellClick} handleCellFlagClick={handleCellFlagClick} />)
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

class Board extends React.Component {
    state = { boardData: null }

    constructor(props) {
        super(props);

        this.updateBoardData();
    }

    updateBoardData = async () => {
        let data = await getMinesweeperBoard();
        this.setState({ boardData: data });

        console.log(this.state);
    }

    handleCellClick = (row, col) => {
        postBoardClick(row, col, this.updateBoardData);
    }

    handleCellFlagClick = (row, col) => {
        postBoardFlagClick(row, col, this.updateBoardData);
    }

    handleBoardReset = () => {
        let rows = this.props.rows;
        let cols = this.props.cols;

        postBoardReset(rows, cols, this.updateBoardData);
    }

    render() {
        let rows = this.props.rows;
        let cols = this.props.cols;

        if (!this.state.boardData || !this.state.boardData.board) {
            return null;
        }

        let boardData = this.state.boardData;
        let board = boardData.board;

        let rowElements = []

        for (let i = 0; i < board.length; i++) {
            rowElements.push(<Row key={`row-${i}`} rowNum={i} rowData={board[i]} handleCellClick={this.handleCellClick} handleCellFlagClick={this.handleCellFlagClick} />)
        }

        return (
            <div>
                <div className="game-board">
                    {rowElements}
                </div>

                <button type="button" className="btn btn-secondary mt-4" onClick={this.handleBoardReset}>Reset Game</button>
                <p>Finished: {String(boardData.finished)}</p>
                <p>Game Won: {String(boardData.won)}</p>
            </div>
        );
    }
}

export default Board;