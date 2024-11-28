const start = () => {
    if (JSON.parse(localStorage.getItem("mode")) !== "multiplayer") {
        document.getElementById("startGame").disabled = false;
    } else {
        // wait for player to have a pair before allowing the button to be clicked
        setInterval(() => {
            document.getElementById("startGame").disabled = false;
        }, 10000);
    }
};

const choiceButtons = document.getElementsByClassName("colorButton");
for (let i = 0; i < choiceButtons.length; i++) {
    choiceButtons[i].addEventListener('click', (e) => {
        const chosenColor = e.target.value;
        localStorage.setItem("chosenColor", JSON.stringify(chosenColor));
        console.log(localStorage.getItem("chosenColor"));
    })
};

document.getElementById("startGame").addEventListener("click", (e) => {
    // send notif to server that player is ready
    e.target.disabled = "false";
    window.location.href = "game.html";
});

start();