import React from 'react';
import ReactDOM from 'react-dom/client';
import * as KeyboardEventHandler from 'react-keyboard-event-handler';
import sentCommand from './commands.js'

class Terminal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            lines: [<tr className='terminal-line' key={-20}><th>-20</th><td>Welcome to BoSLOO Ground Control Console.</td></tr>, <tr className='terminal-line' key={-10}><th>-10</th><td> Time of connection: {new Date().toLocaleString('en-US')}</td></tr>],
            lastLine : '',
            waitForUser: false,
            lineNumber: 0,
            controlHeld: false,
        };
        this.charIn = this.charIn.bind(this);
        this.handleKey = this.handleKey.bind(this);

        const window = document.getRootNode();

        window.addEventListener('paste', (e) => {
            e.preventDefault();

            let paste = (e.clipboardData || window.clipboardData).getData('text');
            this.appendText(paste);
        });
    }

    addLines(newLinesArray) {
        let currLines = this.state.lines
        this.setState({
            lines: currLines.concat(newLinesArray),
        });
    }

    addCharacter(newChar) {
        this.setState({
            lastLine: JSON.parse(JSON.stringify(this.state.lastLine)) + newChar,
        });
    }

    appendText(newText) {
        this.setState({
            lastLine: JSON.parse(JSON.stringify(this.state.lastLine)) + newText,
        });
    }

    deleteCharacter() {
        this.setState({
            lastLine: this.state.lastLine.slice(0,-1),
        });
    }

    finishLine() {
        let commandBody = sentCommand(this.state.lastLine);
        this.addLines([<tr className='terminal-line' key={this.state.lineNumber}><th>{this.state.lineNumber}</th><td>{'>'}{this.state.lastLine}</td></tr>,
            <tr className='terminal-line' key={this.state.lineNumber + 10}><th>{this.state.lineNumber + 10}</th><td>{commandBody}</td></tr>]);
        this.setState({ lastLine: '', lineNumber: this.state.lineNumber+20 });
    }

    charIn(newCharObj) {
        this.setState({
            lastLine: newCharObj.target.value,
        });
    }

    handleKey(key, e) {
        if (e.key === 'Enter') {
            this.finishLine();
        } else if (e.keyCode === 8) { /*backspace*/
            this.deleteCharacter();
        } else if (e.ctrlKey) {
            return;
        } else if (e.keyCode === 32) {
            this.addCharacter(' ');
        } else if (e.keyCode >= 40) {
            this.addCharacter(e.key);
        }
    }

    displayLines() {
        return this.state.lines;
    }

    render() {
        return (
            <div className='terminal-window'>
                <table className='terminal'>
                    <tbody>
                    <KeyboardEventHandler handleKeys={['all']} onKeyEvent={this.handleKey} />
                    {this.displayLines()}
                    <tr className='terminal-line'><th>{this.state.lineNumber}</th><td>{'>'}{this.state.lastLine}<span className='blink-text'>_</span></td></tr>
                    </tbody>
                </table>
            </div>
        )
    }
}

export default Terminal