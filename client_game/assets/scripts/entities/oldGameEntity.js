import Player from './Player.js'
import Ball from './Ball.js'
import Net from './Net.js';

const BALL_RADIUS = 10;
const BALL_SPEED = 3;

class Game {
    static LOCAL = 1;
    static REMOTE = 2;
    static AI = 3;

    static PAUSE_DURATION = 500;
    static GAME_STARTED = false;
    static MAX_SCORE = 6;
    static canvas = document.getElementById('canvas');
    static ctx = canvas.getContext('2d');
    static spanScore = document.getElementById('score');

    constructor(clientId, gameId, width, height, canvasHeight, canvasWidth, speed, color, status) {
        // fetch canvas side based on status and set each player side
        this.clientSide = status === Game.LOCAL ? "left" : "left";
        this.adversarySide = status === Game.LOCAL ? "right" : "right";

        // CONSTRUCTOR ==== width, height, canvasSide, canvasHeight, canvasWidth, speed, color, status
        this.clientPlayer = new Player(width, height, this.clientSide, canvasHeight, canvasWidth, speed, color, status);
        this.adversaryPlayer = new Player(width, height, this.adversarySide, canvasHeight, canvasWidth, speed, color, status);
        this.leftPlayer = this.clientPlayer.canvasSide === "left" ? this.clientPlayer : this.adversaryPlayer;
        this.rightPlayer = this.clientPlayer.canvasSide === "left" ? this.adversaryPlayer : this.clientPlayer;
        
        // CONSTRUCTOR ==== radius, x, y, speed, velocityX, velocityY, canvasHeight, canvasWidth
        this.ball = new Ball(BALL_RADIUS, (canvas.width / 2 - 5), (canvas.height / 2 - 5), BALL_SPEED, 3, 2, canvasHeight, canvasWidth);
        
        // CONSTRUCTOR ==== width, height, canvasHeight, canvasWidth, color
        this.net = new Net(10, 30, canvasHeight, canvasWidth, color);
        
        this.clientId = clientId;
        this.gameId = gameId;
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
        console.log("works!");
        if (this.adversaryPlayer.status === Game.LOCAL && !Game.GAME_STARTED) {
            this.clientPlayer.registerKeys("w", "s");
            this.adversaryPlayer.registerKeys("ArrowUp", "ArrowDown");
            Game.GAME_STARTED = true;
        }

        if (!this.gameEnd) {
            if (!this.pause) {
                Game.ctx.clearRect(0, 0, canvas.width, canvas.height);
                this.net.drawNet(Game.ctx);
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
            requestAnimationFrame(this.startGame.bind(this));
        }
    }

    reinitComponentsCoordinates () {
        this.ball.reinitCoordinates();
        this.clientPlayer.reinitCoordinates();
        this.adversaryPlayer.reinitCoordinates();
    }

    displayScore() {
        if (!this.gameEnd)
            Game.spanScore.textContent = `Left player score: ${this.leftPlayer.score} || Right player score: ${this.rightPlayer.score}`;
        else
            Game.spanScore.textContent = this.leftPlayer.score > Game.MAX_SCORE ? "Left player wins" : "Right player wins";
    }
}





export default Game;