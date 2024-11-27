localStorage.removeItem("chosenColor");
localStorage.removeItem("mode");

const choiceButtons = document.getElementsByClassName("choiceButton");
for (let i = 0; i < choiceButtons.length; i++) {
    choiceButtons[i].addEventListener('click', (e) => {
        const choice = e.target.value;
        if (choice !== "tournament") {
            window.location.href = "matchQueue.html";
            localStorage.setItem("mode", JSON.stringify(choice));
        } else {
            window.location.href = "tournament.html";
        }
    })
}



