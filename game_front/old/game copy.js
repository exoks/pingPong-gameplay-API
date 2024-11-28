import Game from '../assets/scripts/entities/Game.js'

const chosenColor = JSON.parse(localStorage.getItem("chosenColor"));
const gameMode = "multiplayer";
const defaultColor = "#1E90FF";

const canvas = document.getElementById('canvas');

localStorage.setItem("gameData", JSON.stringify({socketUrl: "", x: 10}));

const game = new Game(20, 100, canvas.height, canvas.width, 3, chosenColor === null ? defaultColor : chosenColor, gameMode);

game.startGame();
