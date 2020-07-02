class ProgramAction {

    static ACTION_START = 'START';
    static ACTION_OUTPUT = 'OUTPUT';
    static ACTION_OUTPUT_ERROR = 'OUTPUT_ERROR';
    static ACTION_INPUT = 'INPUT';
    static ACTION_END = 'END';

    constructor(action, data) {
        this.action = action;
        this.data = data;
    }

    send = () => {
        return JSON.stringify({action: this.action, data: this.data})
    };

    static received = (obj) => {
        const jsonData = JSON.parse(obj);
        return new ProgramAction(jsonData.action, jsonData.data);
    };


}

const WS_START = window.location.protocol === 'https:' ? 'wss://' : 'wss://';
let ENDPOINT;
let SOCKET;
let isProgramRunning = false;

// components
let runButton;
let stopButton;
let restartButton;

let outputConsole;
let inputConsole;

//status components
let runningComponent;
let errorComponent;
let finishRunningComponent;
let emptyStatusComponent;
let infoComponent;

//data
let lastInputConsoleData;
let inputConsoleData;

//components flags
let isErrorDisplay;
let isRunningDisplay;
let isRunningEndDisplay;


socketReceived = (e) => {
    if (e.action === ProgramAction.ACTION_OUTPUT) {
        addTextToOutputConsole(e.data);
    } else if (e.action === ProgramAction.ACTION_START) {
        displayRunningComponent(true);
        isProgramRunning = true;
        inputConsole.disabled = false;
    } else if (e.action === ProgramAction.ACTION_OUTPUT_ERROR) {
        addTextToOutputConsole(e.data);
        displayErrorComponent(true);
        setTimeout(() => {
            stopRunning();
        }, 1000);
    } else if (e.action === ProgramAction.ACTION_END) {
        setTimeout(() => {
            stopRunning();
        }, 1000);
    }
};

stopRunning = () => {
    SOCKET.close();
    isProgramRunning = false;
    inputConsole.disabled = true;
    displayRunningComponent(false);
    displayRunningEndComponent(true);
};

socketOpen = (e) => {
};

socketError = (e) => {
};

socketClose = (e) => {
};

loader = (id) => {
    ENDPOINT = `${window.location.host}/live-console/${id}`;
};

sendDataToSocket = (programAction) => {
    SOCKET.send(programAction.send());
};

runProgram = () => {
    if (!isProgramRunning) {
        displayRunningEndComponent(false);
        displayErrorComponent(false);
        displayRunningComponent(true);
        displayInfoComponent(false);
        clearInputConsole();
        clearOutputConsole();
        SOCKET = new WebSocket(WS_START + ENDPOINT);
        SOCKET.onmessage = (e) => {
            if (e.data) {
                socketReceived(ProgramAction.received(e.data));
            }
        };
        SOCKET.onopen = (e) => {
            if (e.data) {
                socketOpen(ProgramAction.received(e.data));
            }
        };
        SOCKET.onerror = (e) => {
            if (e.data) {
                socketError(ProgramAction.received(e.data));
            }
        };
        SOCKET.onclose = (e) => {
            if (e.data) {
                socketClose(ProgramAction.received(e.data));
            }
        };
    }

};

addTextToOutputConsole = (text) => {
    outputConsole.value = outputConsole.value + text;
};

sendData = (data) => {
    sendDataToSocket(new ProgramAction(ProgramAction.ACTION_INPUT, data));
};

consoleInputHandler = (e) => {
    let value = '';
    if (isProgramRunning) {
        if (e.keyCode === 13) {
            sendInputData();
            const valueToWrite = lastInputConsoleData;
            setTimeout(() => outputConsole.value += valueToWrite + '\n', 1);
            inputConsoleData += lastInputConsoleData + '\n> ';
            lastInputConsoleData = '';
            value = inputConsoleData;
        } else if (e.keyCode === 8) {
            lastInputConsoleData = lastInputConsoleData.substr(0, lastInputConsoleData.length - 1);
            value = inputConsoleData + lastInputConsoleData;
        } else if (e.key.length === 1) {
            lastInputConsoleData += e.key;
            value = inputConsoleData + lastInputConsoleData.substr(0, lastInputConsoleData.length);
        } else {
            value = inputConsoleData + lastInputConsoleData.substr(0, lastInputConsoleData.length);
        }
        setTimeout(() => inputConsole.value = value, 1);
    } else {
        setTimeout(() => inputConsole.value = inputConsoleData, 1);
    }
};

consoleInputRead = () => {
    return lastInputConsoleData;
};

consoleInputRead = () => {
    return lastInputConsoleData;
};

sendInputData = () => {
    sendData(consoleInputRead());
};

setupViewComponent = () => {
    runningComponent = $('#running-program-view')[0];
    errorComponent = $('#error-program-view')[0];
    emptyStatusComponent = $('#no-program-status')[0];
    displayRunningComponent(false);
    displayErrorComponent(false);
    runButton = $('#run-button')[0];
    runButton.addEventListener('click', runProgram);
    stopButton = $('#stop-button')[0];
    stopButton.addEventListener('click', stopRunning);
    restartButton = $('#restart-button')[0];
    infoComponent = $('#app-information')[0];
    restartButton.addEventListener('click', () => {
        stopRunning();
        runProgram();
    });
    outputConsole = $('#output-console')[0];
    inputConsole = $('#input-console')[0];
    finishRunningComponent = $('#finish-program-view')[0]
    $('#output-console-clear')[0].addEventListener('click', clearOutputConsole);
    $('#input-console-clear')[0].addEventListener('click', clearInputConsole);
    inputConsole.addEventListener('keydown', consoleInputHandler);
    clearOutputConsole();
    clearInputConsole();
    inputConsoleData = '> ';
    lastInputConsoleData = '';
    inputConsole.value = inputConsoleData;
};

clearOutputConsole = () => {
    outputConsole.value = '';
};

clearInputConsole = () => {
    inputConsole.value = '> ';
    lastInputConsoleData = '';
    inputConsoleData = '> ';
};

displayRunningComponent = (flag) => {
    isRunningDisplay = flag;
    runningComponent.style.display = flag ? 'flex' : 'none';
    emptyStatusComponent.style.display = !isRunningDisplay && !isErrorDisplay && !isRunningEndDisplay ? 'block' : 'none';
};

displayErrorComponent = (flag) => {
    isErrorDisplay = flag;
    errorComponent.style.display = flag ? 'flex' : 'none';
    emptyStatusComponent.style.display = !isRunningDisplay && !isErrorDisplay && !isRunningEndDisplay ? 'block' : 'none';
};

displayRunningEndComponent = (flag) => {
    isRunningEndDisplay = flag;
    finishRunningComponent.style.display = flag ? 'flex' : 'none';
    emptyStatusComponent.style.display = !isRunningDisplay && !isErrorDisplay && !isRunningEndDisplay ? 'block' : 'none';
};

displayInfoComponent = (flag) => {
    infoComponent.style.display = flag ? 'block' : 'none';
};

setupViewComponent();