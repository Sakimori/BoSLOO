import React from 'react';
import ReactDOM from 'react-dom/client';
import Typing from 'react-typing-animation';
import ClickableDiv from 'react-clickable-div';
import KeyboardEventHandler from 'react-keyboard-event-handler'
import './index.css';
import logos from './BoSLOO logo.json';

function Square(props) {
    return (
        <button className="square" onClick={props.onClick} >
            {props.value}
        </button>
    );
}

class Board extends React.Component {
    renderSquare(i) {
        return (
            <Square
                value={this.props.squares[i]}
                onClick={() => this.props.onClick(i)}
            />
        );
    }

    render() {
        return (
            <div>
                <div className="board-row">
                    {this.renderSquare(0)}
                    {this.renderSquare(1)}
                    {this.renderSquare(2)}
                </div>
                <div className="board-row">
                    {this.renderSquare(3)}
                    {this.renderSquare(4)}
                    {this.renderSquare(5)}
                </div>
                <div className="board-row">
                    {this.renderSquare(6)}
                    {this.renderSquare(7)}
                    {this.renderSquare(8)}
                </div>
            </div>
        );
    }
}

class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            history: [{
                squares: Array(9).fill(null),
            }],
            xIsNext: true,
        };
    }

    handleClick(i) {
        const history = this.state.history;
        const current = history[history.length - 1];
        const squares = current.squares.slice();
        if (calculateWinner(squares) || squares[i]) {
            return;
        }
        squares[i] = (this.state.xIsNext ? 'X' : 'O');
        this.setState({
            history: history.concat([{
                squares: squares,
            }]),
            xIsNext: !this.state.xIsNext,
        });
    }

    render() {
        const history = this.state.history;
        const current = history[history.length - 1];
        const winner = calculateWinner(current.squares);
        let status;
        if (winner) {
            status = 'Winner: ' + winner;
        } else {
            status = 'Next: ' + (this.state.xIsNext ? 'X' : 'O');
        }

        return (
            <div className="game">
                <div className="game-board">
                    <Board
                        squares={current.squares}
                        onClick={(i) => this.handleClick(i)}
                    />
                </div>
                <div className="game-info">
                    <div>{status}</div>
                    <ol>{/* TODO */}</ol>
                </div>
            </div>
        );
    }
}

function calculateWinner(squares) {
    const lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ];
    for (let i = 0; i < lines.length; i++) {
        const [a, b, c] = lines[i];
        if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
            return squares[a];
        }
    }
    return null;
}

class Terminal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            bodyObj: <SelfTest />,
            init: false,
        }
    }

    appendToBody(newContent) {
        let bodyObj = JSON.parse(JSON.stringify(this.state.bodyObj)) + newContent;
        this.setState({
            bodyObj: bodyObj
        });
    }

    replaceBody(newContent) {
        this.setState({
            bodyObj: newContent
        });
    }

    handler() {
        const init = this.state.init;
        if (!init) { this.replaceBody('YIPPIE!'); this.setState({ init: true }); }
    }

    render() {
        return (
            <div className='terminal'>
                {this.state.bodyObj}
                <KeyboardEventHandler handleKeys={['all']}
                    onKeyEvent={(key, e) => { if (!this.state.init) { this.replaceBody('YIPPIE!'); this.setState({ init: true }); } }} />
            </div>
        );
    }
}

class SelfTest extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            logodisplay: false
        }
    }

    render() {
        const final = <span>{logos.logo} < br /><br /><br /><Typing speed={5}>Press any key to continue...<br/>> <span className='blink-text'>_</span></Typing></span>;
        return (
            <div className='power-on-self-test'>
                <Typing speed={5} onFinishedTyping={() => this.setState({logodisplay: true})}>
                BoSLOO ACPI BIOS v0.1<br />
                Sakimori Ind. 2022<br />
                Initializing cache.................................<Typing.Speed ms={200} />...<Typing.Speed ms={5} /> OK!<br />
                Initializing network.........<Typing.Speed ms={500} />....<Typing.Speed ms={5} />.................<Typing.Speed ms={300} />....<Typing.Speed ms={5} /> OK!<br />
                Initializing GPU...................................<Typing.Speed ms={1000} />...<Typing.Speed ms={5} /> <span className='fail-text'>FAIL!</span><br />
                <br />             
                </Typing>
                {this.state.logodisplay ? final : null}
            </div>
        )
    }
}

// =========================================

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Terminal />);