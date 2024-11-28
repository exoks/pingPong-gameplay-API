const style = `<style>
    #avatarsContainer {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80%;
        width: 100%;
    }
    #avatarsContainer > * {
        margin: 1rem;
    }

    .avatarHeader {
        text-align: center;
        margin-bottom: 0.6rem;
    }

    .avatar {
        height: 8rem;
        width: 8rem;
        box-shadow: rgba(0, 0, 0, 0.05) 0px 0px 0px 1px;    
        border-radius: 100%;
    }
</style>`;

const template = `
${style}
<div id="avatarsContainer">
<div>
    <h3 class="avatarHeader">You</h3>
    <img class="avatar" id="userAvatar" src="./assets/images/loading.gif" alt="none">
</div>
<h3>VS</h3>
<div>
    <h3 class="avatarHeader">Adversary</h3>
    <img class="avatar" id="adversaryAvatar" src="./assets/images/loading.gif" alt="none">
</div>
</div>`;



class avatarsComponent extends HTMLElement {
    constructor () {
        super();
        this.attachShadow({mode: "open"});
    }

    render () {
        this.shadowRoot.innerHTML = template;
    }

    fetchAvatars() {
        const mode = JSON.parse(localStorage.getItem("mode"));
        let userAvatar = undefined;
        let adversaryAvatar = undefined;

        if (mode === "local") {
            userAvatar = "assets/images/avatar.png";
            adversaryAvatar = "assets/images/avatar.png";
        } else if (mode === "multiplayer") {
            // userAvatar = "assets/images/avatar.png"; fetch avatar from server
            // adversaryAvatar = "assets/images/avatar.png"; fetch avatar from server
        } else if (mode === "ai") {
            userAvatar = "assets/images/avatar.png";
            adversaryAvatar = "assets/images/ai.png";
        }
        if (userAvatar || adversaryAvatar) {
            this.shadowRoot.querySelector("#userAvatar").src = userAvatar;
            this.shadowRoot.querySelector("#adversaryAvatar").src = adversaryAvatar;
        }
    }

    connectedCallback () {
        this.render();
        this.fetchAvatars();
    }
};

customElements.define("avatars-component", avatarsComponent);

export default avatarsComponent;