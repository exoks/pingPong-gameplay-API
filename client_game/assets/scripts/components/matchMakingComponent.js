import avatarsComponent from "./avatarsComponent.js";
import { io } from "https://cdn.socket.io/4.8.1/socket.io.esm.min.js";

const style = `<style>
* {
    padding: 0;
    margin: 0;
}

body {
    width: 100vw;
    height: 100vh;
}

#matchMakingContainer {
    width: 40vw;
    height: 80vh;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    background: rgba( 255, 255, 255, 0.25 );
    box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
    backdrop-filter: blur( 4px );
    -webkit-backdrop-filter: blur( 4px );
    border-radius: 10px;
    border: 1px solid rgba( 255, 255, 255, 0.18 );
    color: #F0F8FF;
}

#matchMakingContainer > * {
    width: 80%;
    /* height: 20%; */
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    margin: 2rem;
}

#colorHeader {
    text-align: center;
    width: 100%;
}

.colorButton {
    width: 3rem;
    height: 3rem;
    margin-right: 0.4rem;
    margin-top: 0.8rem;
    transition: 0.2s ease-in-out;
}

.colorButton {
    border: none;
    outline: none;
    border-radius: 50%;
    cursor: pointer;
}

#blue {
    background-color: #1E90FF;
}

#orange {
    background-color: #FF4500;
}

#green {
    background-color: #32CD32;
}

#gold {
    background-color: #FFD700;
}

#startGame {
    width: 50%;
    height: 4rem;
    cursor: pointer;
    background: rgba( 255, 255, 255, 0.25 );
    box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
    backdrop-filter: blur( 4px );
    -webkit-backdrop-filter: blur( 4px );
    border-radius: 10px;
    border: 1px solid rgba( 255, 255, 255, 0.18 );
    color: #F0F8FF ;
    opacity: 0.2;
}

.colorButton:hover {
    transform: scale(1.01);
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
}
</style>`;

const template = `
${style}
<div id="matchMakingContainer">
    <avatars-component></avatars-component>
    <div id="optionsContainer">
        <h3 id="colorHeader">Game's color</h3>
        <button class="colorButton" id="blue" value="#1E90FF" ></button>
        <button class="colorButton" id="orange" value="#FF4500" ></button>
        <button class="colorButton" id="green" value="#32CD32" ></button>
        <button class="colorButton" id="gold" value="#FFD700" ></button>
    </div>
    <div>
        <button id="startGame" disabled>Start game</button>
    </div>
</div>`;



class matchMakinComponent extends HTMLElement {
    constructor () {
        super();
        this.attachShadow({mode: "open"});
    }

    render () {
        this.shadowRoot.innerHTML = template;
    }

    connectedCallback () {
        this.render();
        this.pickColorEvent();
        this.matchMaking();
    }

    matchMaking () {
        if (JSON.parse(localStorage.getItem("mode")) !== "multiplayer") {
            this.shadowRoot.querySelector("#startGame").disabled = false;
            this.shadowRoot.querySelector("#startGame").style.opacity = "1";
            this.startGameEvent();
        } else {
            const url = `ws://localhost:8000/ws/entrance/`;
            const socket = new WebSocket(url);

            socket.onopen = () => {
                console.log("[WS: ClientSocket]: open socket connection");
                socket.send(
                    JSON.stringify({
                        id: (Math.floor(Math.random() * 10)).toString(),
                        rank: (Math.floor(Math.random() * 10)).toString() ,
                    }),
                );
            };

            socket.onmessage = (event) => {
                console.log("[WS: ClientSocket]: data is recieved");
                const data = JSON.parse(event.data);
                // console.log(data);
                localStorage.setItem("gameData", JSON.stringify({playerId: data.player_id, adversaryId: data.opponent_id, roomId: data.room_id}));
                this.shadowRoot.querySelector("#startGame").style.opacity = "1";
                this.shadowRoot.querySelector("#startGame").disabled = false;
                this.startGameEvent();
            };

            socket.onerror = () => {
                alert("matchmaking is down currently, try again later!");
                window.location.href = "index.html";
            }

            socket.onclose = () => {
                console.log("[WS: ClientSocket]: socket is closed");
            };

            socket.onerror = function() {
                console.log("[WS: ClientSocket]: An error happend");
            };
        }
    };

    pickColorEvent() {
        const choiceButtons = this.shadowRoot.querySelectorAll(".colorButton");
        for (let i = 0; i < choiceButtons.length; i++) {
            choiceButtons[i].addEventListener('click', (e) => {
                const chosenColor = e.target.value;
                localStorage.setItem("chosenColor", JSON.stringify(chosenColor));
                console.log(chosenColor);
            })
        };
    }

    startGameEvent() {
        this.shadowRoot.querySelector("#startGame").addEventListener("click", (e) => {
            // send notif to server that player is ready
            window.location.href = "game.html";
        });
    }

    initEventhandlers() {
        this.pickColorEvent();
        this.startGameEvent();
    }
};

customElements.define("matchmaking-component", matchMakinComponent);

export default matchMakinComponent;
