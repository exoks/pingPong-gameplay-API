import Player from './Player.js'
import Ball from './Ball.js'
import Net from './Net.js';

const BALL_RADIUS = 10;
const BALL_SPEED = 2;

class Game {
    static PAUSE_DURATION = 500;
    static MAX_SCORE = 6;
    static canvas = document.getElementById('canvas');
    static ctx = canvas.getContext('2d');
    static spanScore = document.getElementById('score');

    constructor(width, height, canvasHeight, canvasWidth, speed, color = "#1E90FF", status) {
        // online props
        this.emitter = new EventTarget();
        this.roomId = null;
        this.playerId = null;
        this.socket = null;

        if (status === "multiplayer") {
            this.initSocket();
        } 

        this.clientPlayer = new Player(width, height, canvasHeight, canvasWidth, speed, color);
        this.adversaryPlayer = new Player(width, height, canvasHeight, canvasWidth, speed, color);
        this.ball = new Ball(BALL_RADIUS, (canvas.width / 2 - 5), (canvas.height / 2 - 5), BALL_SPEED, BALL_SPEED, 1, canvasHeight, canvasWidth, color);
        

        this.canvasHeight = canvasHeight;
        this.canvasWidth = canvasWidth;
        this.gameMode = status;
        this.gameEnd = false;
        this.pause = false;
    };

    initSocket() {
        const gameData = JSON.parse(localStorage.getItem("gameData"));
        if (!gameData) {
            alert("problem encountered, please try again");
            window.location.href = "index.html"
        }
        const {roomId, playerId, adversaryId} = gameData;
        this.roomId = roomId;
        this.playerId = playerId;
        this.adversaryId = adversaryId;
        this.socket = new WebSocket(`ws://localhost:8001/ws/game/${this.roomId}/`);
    }

    initSocketEvents () {
        // this.socket.onopen = () => {
        //     console.log("[WS: Clientthis.]: open socket connection");
        //     this.socket.send(
        //         JSON.stringify({
        //             player_id: this.playerId,
        //         }),
        //     );
        // };

        this.socket.onmessage = (event) => {
            // console.log("[WS: ClientSocket]: data is recieved");
            const data = JSON.parse(event.data);
            console.log(data);
            if (data.event === "gameplay_init") {
                this.initRemotePlayersSide(data.paddle_x);
                this.emitter.dispatchEvent(new CustomEvent('startGame'));
            } 
            else if (data.event === "ball_state") {
                // console.log("entered ball event")
                this.ball.x = data.ball[0];
                this.ball.y = data.ball[1];
            } else if (data.event === "paddle_state") {
                console.log("received data");
                this.adversaryPlayer.y = data.paddle_y;
            }
        };
    }

    pauseGame() {
        this.pause = true;
        setTimeout(() => {
            this.pause = false;
        }, Game.PAUSE_DURATION);
    }

    startGame () {
        if (this.gameMode === "local") {
            this.initLocalPlayersSide();
            this.registerKeys();
            this.localGame();
        } 
        else if (this.gameMode === "multiplayer") {
            this.emitter.addEventListener('startGame', () => {
                this.registerKeys();
                this.remoteGame();
            });
            this.initSocketEvents();
        }
    }

    localGame() {
        if (!this.gameEnd) {
            if (!this.pause) {
                Game.ctx.clearRect(0, 0, canvas.width, canvas.height);
                // this.net.drawNet(Game.ctx);
                this.ball.drawBall(Game.ctx);
                this.clientPlayer.drawPaddle(Game.ctx);
                this.adversaryPlayer.drawPaddle(Game.ctx);
                this.clientPlayer.movePaddle();
                this.adversaryPlayer.movePaddle();
                this.ball.moveBall(this);
                if (this.clientPlayer.score > Game.MAX_SCORE || this.adversaryPlayer.score > Game.MAX_SCORE) {
                    this.gameEnd = true;
                }
            }
            this.displayScore();
            requestAnimationFrame(this.localGame.bind(this));
        }
    }

    remoteGame() {
        if (!this.gameEnd) {
            if (!this.pause) {
                Game.ctx.clearRect(0, 0, canvas.width, canvas.height);
                this.ball.drawBall(Game.ctx);
                this.clientPlayer.drawPaddle(Game.ctx);
                this.adversaryPlayer.drawPaddle(Game.ctx);
                this.clientPlayer.movePaddle(this.socket);
        //         // if (this.clientPlayer.score > Game.MAX_SCORE || this.adversaryPlayer.score > Game.MAX_SCORE) {
        //         //     this.gameEnd = true;
        //         // }
            }
            this.displayScore();
            requestAnimationFrame(this.remoteGame.bind(this));
        }
    }

    registerKeys () {
        // always register client player keys based on position
        if (this.clientPlayer.canvasSide === "left") {
            this.clientPlayer.registerKeys("w", "s");
        } else {
            this.clientPlayer.registerKeys("ArrowUp", "ArrowDown");
        }

        // only register adversary keys if it's a local game
        if (this.gameMode === "local") {
            if (this.adversaryPlayer.canvasSide === "left") {
                this.adversaryPlayer.registerKeys("w", "s");
            } else {
                this.adversaryPlayer.registerKeys("ArrowUp", "ArrowDown");
            }
        }
    }

    initLocalPlayersSide () {
        this.clientPlayer.initPlayerSide("left");
        this.adversaryPlayer.initPlayerSide("right");
    }

    initRemotePlayersSide (x) {
        this.clientPlayer.initPlayerSide(x > this.canvasWidth / 2 ? "right" : "left");
        this.adversaryPlayer.initPlayerSide(x > this.canvasWidth / 2 ? "left" : "right");
    }

    reinitComponentsCoordinates () {
        this.ball.reinitCoordinates();
        this.clientPlayer.reinitCoordinates();
        this.adversaryPlayer.reinitCoordinates();
    }

    displayScore() {
        if (!this.gameEnd)
            Game.spanScore.textContent = `Left player score: ${this.clientPlayer.score} || Right player score: ${this.adversaryPlayer.score}`;
        else
            Game.spanScore.textContent = this.clientPlayer.score > Game.MAX_SCORE ? "Left player wins" : "Right player wins";
    }
}

export default Game;