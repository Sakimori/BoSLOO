import Typing from 'react-typing-animation';
import React from 'react';
import ReactDOM from 'react-dom/client';
import * as KeyboardEventHandler from 'react-keyboard-event-handler';
import command from './commands.js'

class Terminal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            lines: ['Welcome!', "Well done."],
            lastLine : '',
            waitForUser: false
        };
        this.charIn = this.charIn.bind(this);
        this.handleKey = this.handleKey.bind(this);
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

    deleteCharacter() {
        this.setState({
            lastLine: this.state.lastLine.slice(0,-1),
        });
    }

    finishLine() {
        this.addLines([">" + this.state.lastLine, command(this.state.lastLine)]);
        this.setState({ lastLine: '' });
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
        } else if (e.keyCode === 32) {
            this.addCharacter(' ');
        } else if (e.keyCode >= 40) {
            this.addCharacter(e.key);
        }
    }

    displayLines() {
        var stringOut = "";
        for (let line of this.state.lines) {
            stringOut += "\n";
            stringOut += line;
        }

        return <span>{stringOut}</span>
    }

    render() {
        return (
            <div className='terminal'>
                <KeyboardEventHandler handleKeys={['all']} onKeyEvent={this.handleKey} />
                {this.displayLines()}<br />
                {'>'}{this.state.lastLine}<span className='blink-text'>_</span>
            </div>
        )
    }
}

export default Terminal