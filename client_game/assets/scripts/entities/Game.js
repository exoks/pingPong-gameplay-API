import { io } from "https://cdn.socket.io/4.8.1/socket.io.esm.min.js";
import Player from './Player.js'
import Ball from './Ball.js'
import Net from './Net.js';

const BALL_RADIUS = 10;
const BALL_SPEED = 2;

class Game {
    static PAUSE_DURATION = 500;
    static GAME_STARTED = false;
    static MAX_SCORE = 6;
    static canvas = document.getElementById('canvas');
    static ctx = canvas.getContext('2d');
    static spanScore = document.getElementById('score');

    constructor(width, height, canvasHeight, canvasWidth, speed, color = "#1E90FF", status) {
        if (status === "multiplayer") {
            const gameData = JSON.parse(localStorage.getItem("gameData"));
            // roomId - x plauer
            if (!gameData) {
                alert("problem encountered, please try again");
                window.location.href = "index.html"
            }
            const {socketUrl, x} = gameData;

            this.clientPosition = x > Game.canvas.width / 2 ? "right" : "left";
            this.adversaryPosition = x > Game.canvas.width / 2 ? "left" : "right";
            this.socket = io(socketUrl);
        } else {
            this.clientPosition = "left";
            this.adversaryPosition = "right";
        }

        this.clientPlayer = new Player(width, height, this.clientPosition, canvasHeight, canvasWidth, speed, color);
        this.adversaryPlayer = new Player(width, height, this.adversaryPosition, canvasHeight, canvasWidth, speed, color);
        
        // CONSTRUCTOR ==== radius, x, y, speed, velocityX, velocityY, canvasHeight, canvasWidth
        this.ball = new Ball(BALL_RADIUS, (canvas.width / 2 - 5), (canvas.height / 2 - 5), BALL_SPEED, BALL_SPEED, 1, canvasHeight, canvasWidth, color);
        
        // CONSTRUCTOR ==== width, height, canvasHeight, canvasWidth, color
        // this.net = new Net(10, 30, canvasHeight, canvasWidth, color);
        
        this.gameMode = status;
        this.gameEnd = false;
        this.pause = false;
    };

    pauseGame() {
        this.pause = true;
        setTimeout(() => {
            this.pause = false;
        }, Game.PAUSE_DURATION);
    }

    startGame () {
        console.log(this.gameMode);
        if (!Game.GAME_STARTED) {
            this.clientPlayer.registerKeys("w", "s");
            if (this.gameMode === "local")
                this.adversaryPlayer.registerKeys("ArrowUp", "ArrowDown");
            Game.GAME_STARTED = true;
        }

        if (this.gameMode === "local") {
            this.localGame();
            console.log("entered2");
        } 
        else if (this.gameMode === "multiplayer") {
            this.remoteGame();
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
        this.updateAdversaryEvent();
        if (!this.gameEnd) {
            Game.ctx.clearRect(0, 0, canvas.width, canvas.height);
            // this.net.drawNet(Game.ctx);
            this.ball.drawBall(Game.ctx);
            this.clientPlayer.drawPaddle(Game.ctx);
            this.adversaryPlayer.drawPaddle(Game.ctx);

            this.clientPlayer.movePaddle();
            this.updateClientEvent();
            
            this.ball.moveBall(this);
            if (this.clientPlayer.score > Game.MAX_SCORE || this.adversaryPlayer.score > Game.MAX_SCORE) {
                this.gameEnd = true;
            }
            this.displayScore();
            requestAnimationFrame(this.remoteGame.bind(this));
        }
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

    // socket events
    updateClientEvent() {
        this.socket.emit('movement', this.clientPlayer.y);
    }

    updateAdversaryEvent() {
        this.socket.on('movement', (data) => {
            this.adversaryPlayer.y = data.y;
        })
    }
}





export default Game;
