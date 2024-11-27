const gameBtn = document.getElementById("btn");
const idInput = document.getElementById("idInput");
const groupInput = document.getElementById("groupInput");

gameBtn.addEventListener(
  "click",
  () => {
    let roomId = "oussamahamza-203944";
    const socketPlayer = new WebSocket(
      `ws://${window.location.host}/ws/game/${roomId}/`,
    );

    socketPlayer.onopen = () => {
      console.log("[CLIENT: OPEN]: > open ws connection");
      // send paddle_y only because the consumers in my backend are identied     
      socketPlayer.send(JSON.stringify({
        "paddle_y": 100
      }));
      console.log("[CLIENT: SEND]: > data has been sent");
    };

    socketPlayer.onmessage = (event) => {
      console.log("[CLIENT: MESSAGE]: > data sent");
      console.log(JSON.parse(event.data));
    };

    socketPlayer.onclose = () => {
      console.log("[CLIENT: CLOSE]: > connection closed");
    };

    socketPlayer.onerror = () => {
      console.log("[CLIENT: ERROR]: > an error has occured");
    };
  },
  { once: true },
);
