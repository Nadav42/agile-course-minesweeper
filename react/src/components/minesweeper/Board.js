import React from 'react';
import { getMinesweeperBoard } from '../../api/rest_api'

function CellMine(props) {
    return (
        <div className="game-cell mine">
        </div>
    );
}

function CellFlag(props) {
    return (
        <div className="game-cell flag">
        </div>
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

function Cell(props) {
    if (props.number) {
        return <CellNumber number={props.number} />;
    }
    else if (props.flag) {
        return <CellFlag />;
    }
    else if (props.mine) {
        return <CellMine />;
    }

    let cellClass = " filled";
    if (props.flat) {
        cellClass = "";
    }

    return (
        <div className={`game-cell ${cellClass}`}></div>
    );
}

function Row(props) {
    let cells = [];

    if (!props.rowData) {
        return null;
    }

    // {"clicked": ..., "flag": ..., "mine": ..., "adjacentMines": ...}
    let rowData = props.rowData;

    for (let i = 0; i < rowData.length; i++) {
        let cellData = rowData[i];

        if (!cellData.clicked && cellData.flag) {
            cells.push(<Cell key={`col-${i}`} flag />)
        }
        else if (cellData.clicked && cellData.adjacentMines !== undefined) {
            if (cellData.adjacentMines > 0) {
                cells.push(<Cell key={`col-${i}`} number={cellData.adjacentMines} />)
            }
            else {
                cells.push(<Cell key={`col-${i}`} flat />)
            }  
        }
        else if (cellData.mine) {
            cells.push(<Cell key={`col-${i}`} mine />)
        }
        else {
            cells.push(<Cell key={`col-${i}`} />)
        }
        
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
            rowElements.push(<Row key={`row-${i}`} rowData={board[i]} />)
        }

        return (
            <div className="game-board">
                {rowElements}
            </div>
        );
    }
}

export default Board;