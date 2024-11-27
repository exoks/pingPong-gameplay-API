// Get the Button object
const matchButton = document.getElementById("btn");
const userInput = document.getElementById("txtView");

const rankInput = document.createElement("input");
rankInput.type = "number";

const form = document.getElementById("form");
form.append(document.createElement("br"));
form.append(rankInput);

// const displayView = document.createElement('p')
// form.appen(p)

// Launch the game
matchButton.addEventListener(
  "click",
  (eMouse) => {
//  const url = `ws://${window.location.host}/ws/matchmaking/`;
    const url = `ws://${window.location.host}/ws/entrance/`;

    playerSocket = new WebSocket(url);

    playerSocket.onopen = () => {
      console.log("[WS: ClientSocket]: open socket connection");
      playerSocket.send(
        JSON.stringify({
          id: userInput.value,
          rank: rankInput.value,
        }),
      );
    };

    playerSocket.onmessage = (event) => {
      console.log("[WS: ClientSocket]: data is recieved");
      console.log(event);
      const data = JSON.parse(event.data);
      console.log(data);
      // displayView.innerText(data.player_id + " vs " + data.opponent_id)
    };

    playerSocket.onclose = () => {
      console.log("[WS: ClientSocket]: socket is closed");
    };

    playerSocket.onerror = function(mouseEvent) {
      console.log("[WS: ClientSocket]: An error happend");
    };
  },
  //  { once: true },
);
