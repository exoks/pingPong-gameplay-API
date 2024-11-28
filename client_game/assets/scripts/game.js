import Game from './entities/Game.js'

const chosenColor = JSON.parse(localStorage.getItem("chosenColor"));
const gameMode = JSON.parse(localStorage.getItem("mode"));
const defaultColor = "#1E90FF";

const canvas = document.getElementById('canvas');

const game = new Game(20, 100, canvas.height, canvas.width, 3, chosenColor === null ? defaultColor : chosenColor, gameMode);

game.startGame();
