import React from 'react';
import ReactDOM from 'react-dom/client';
import Typing from 'react-typing-animation';
import ClickableDiv from 'react-clickable-div';
import KeyboardEventHandler from 'react-keyboard-event-handler'
import './index.css';
import logos from './BoSLOO logo.json';

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