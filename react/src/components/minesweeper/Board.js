import React from 'react';

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

    for (let i = 0; i < props.cols; i++) {
        cells.push(<Cell key={`col-${i}`} number={i + 1} />)
    }

    return (
        <div className="game-row">
            {cells}
            <Cell></Cell>
            <Cell flat></Cell>
            <CellMine></CellMine>
            <CellFlag></CellFlag>
        </div>
    );
}

class Board extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let rows = this.props.rows;
        let cols = this.props.cols;

        let rowElements = []

        for (let i = 0; i < rows; i++) {
            rowElements.push(<Row key={`row-${i}`} cols={cols} />)
        }

        return (
            <div className="game-board">
                {rowElements}
            </div>
        );
    }
}

export default Board;