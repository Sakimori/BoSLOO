import React from 'react';
import ReactDOM from 'react-dom/client';
import Typing from 'react-typing-animation';
import ClickableDiv from 'react-clickable-div';
import KeyboardEventHandler from 'react-keyboard-event-handler'
import './index.css';
import logos from './BoSLOO logo.json';
import Terminal from './terminal.js';
import StatusBar from './statusbar.js';

const nominal = <div><Terminal /><StatusBar /></div>;

class Console extends React.Component {
    constructor(props) {
        super(props);
        this.swapper = this.swapper.bind(this);
        this.state = {
            bodyObj: <PowerOn onClick={this.swapper} />,
            init: 0,
        }       
    }

    swapper(key, e) {
        if (this.state.init === 0) {
            this.replaceBody(<SelfTest />);
            this.playSound();
        } else if (this.state.init === 1) {
            this.replaceBody(nominal);
        }
        this.setState({ init: this.state.init + 1 });
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

    playSound() {
        var sound = document.getElementById("boot-sound")
        sound.volume = 0.1;
        sound.play();
    }

    render() {
        return (
            <div className='console'>
                <KeyboardEventHandler handleKeys={['all']} onKeyEvent={this.swapper} />
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
                <Typing speed={30} onFinishedTyping={() => this.setState({ logodisplay: true })}>
                BoSLOO ACPI BIOS v0.1<br />
                Sakimori Ind. 2022<br />
                    <Typing.Speed ms={ 5}/>Initializing cache.................................<Typing.Speed ms={200} />...<Typing.Speed ms={5} /> OK!<br />
                Initializing network.........<Typing.Speed ms={500} />....<Typing.Speed ms={5} />.................<Typing.Speed ms={300} />....<Typing.Speed ms={5} /> OK!<br />
                Initializing GPU...................................<Typing.Speed ms={1000} />...<Typing.Speed ms={5} /> <span className='fail-text'>FAIL!</span><br />
                <br />             
                </Typing>
                {this.state.logodisplay ? final : null}
            </div>
        )
    }
}

function PowerOn(props) {
    return (
        <div className="power-on-container"><div className='power-on-box'><span id='start-text' onClick={props.onClick}><span className='blink-text'>START</span></span></div></div>
    );
}

// =========================================

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Console />);