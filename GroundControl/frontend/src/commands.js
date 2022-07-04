import Typing from 'react-typing-animation';
import React from 'react';

class Command {
    constructor(keyword, fullName) {
        this.keyword = keyword;
        this.fullName = fullName;

        this.helpString = "No help text for this command. Vivian, please be sure to fix this before deploying."
    }

    call(body) {
        return 'This command exists, but does nothing. Vivian, please be sure to fix this before deploying.';
    }
}

class helpCommand extends Command{
    constructor() {
        super('help','help');

        this.helpString = "This contains basic help and usage instructions for all commands."
    }

    call(body) {
        if (body === "") {
            return (this.helpString);
        } else {
            for (let command of commandList) {
                if (body === command.keyword || body === command.fullName) {
                    return (command.helpString);
                }
            }
            return ("Unrecognized command. Use without arguments to see full list.")
        }
    }
}

class loremCommand extends Command {
    constructor() {
        super('lorem', 'loremipsum');

        this.helpString = 'Prints a lorem string.'
    }

    call(body) {
        return ('Space, the final frontier. These are the voyages of the Starship Enterprise. Its five-year mission: to explore strange new worlds, to seek out new life and new civilizations, to boldly go where no man has gone before. Many say exploration is part of our destiny, but it is actually our duty to future generations and their quest to ensure the survival of the human species.');
    }
}

const commandList = [new helpCommand(), new loremCommand()];

function sentCommand(sentCommand) {
    var commandId = sentCommand.split(" ")[0]
    var commandBody = sentCommand.split(" ").slice(1).join(' ')
    for (let command of commandList) {
        if (commandId === command.keyword || commandId === command.fullName) {
            return (<Typing className='typed-line' speed={5}>{command.call(commandBody.trim())}</Typing>);
        }
    }

    return (<Typing className='typed-line' speed={5}>Unrecognized command.</Typing>);
}

export default sentCommand