import React from 'react';
import ReactDOM from 'react-dom/client';
import Typing from 'react-typing-animation';
import ClickableDiv from 'react-clickable-div';
import KeyboardEventHandler from 'react-keyboard-event-handler'
import './index.css';
import logos from './BoSLOO logo.json';
import Terminal from './terminal.js'

class Console extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            bodyObj: <span><SelfTest /><KeyboardEventHandler handleKeys={['all']} onKeyEvent={(key, e) => { this.replaceBody(<Terminal />); this.setState({ init: true }) }} /></span>,
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

    render() {
        return (
            <div className='console'>
                {this.state.bodyObj}
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
        const final = <span className='logo'>{logos.logo} < br /><br /><br /><Typing speed={5}>Press any key to continue...<br />{'>'} <span className='blink-text'>_</span></Typing></span>;
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
root.render(<Console />);