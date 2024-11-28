const style = `<style>
* {
    padding: 0;
    margin: 0;
}

#choiceContainer {
    width: 40vw;
    height: 80vh;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    background: rgba(255, 255, 255, 0.25);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.choiceButton {
    width: 30%;
    height: 4rem;
    margin: 0.5rem;
    background-color: none;
    outline: none;
    border: none;
    border-radius: 0.5rem;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.25);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    color: #F0F8FF;
}

.choiceButton:hover {
    background-color: rgba(255, 255, 255, 0.107);
    cursor: pointer;
}
</style>`;

const template = `
${style}
<div id="choiceContainer">
    <button class="choiceButton" value="local" id="local" >Local</button>
    <button class="choiceButton" value="multiplayer" id="multiplayer" >Multiplayer</button>
    <button class="choiceButton" value="tournament" id="tournament" >Tournament</button>
    <button class="choiceButton" value="ai" id="ai">AI</button>
</div>`;



class indexComponent extends HTMLElement {
    constructor () {
        super();
        this.attachShadow({mode: "open"});
    }

    render () {
        this.shadowRoot.innerHTML = template;
    }

    initButtonsListener () {
        const buttons = this.shadowRoot.querySelectorAll(".choiceButton");
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].addEventListener("click", (e) => {this.redirect(e)});
        }
    }

    redirect(e) {
        const choice = e.target.value;
        if (choice !== "tournament") {
            localStorage.setItem("mode", JSON.stringify(choice));
            window.location.href = "matchMaking.html";
        } else {
            window.location.href = "tournament.html";
        }
    }

    connectedCallback () {
        this.render();
        this.resetLocalStorage();
        this.initButtonsListener();
    }

    resetLocalStorage() {
        localStorage.removeItem("mode");
        localStorage.removeItem("chosenColor");
        localStorage.removeItem("gameData");
    }
};

customElements.define("index-component", indexComponent);

export default indexComponent;