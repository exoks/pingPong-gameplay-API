class Player {
    constructor(width, height, canvasSide, canvasHeight, canvasWidth, speed, color) {
        this.width = width;
        this.height = height;
        this.x = canvasSide === "left" ? 0 : canvasWidth - width;
        this.y = (canvasHeight / 2) - (height / 2)
        this.speed = speed;
        this.color = color;
        this.score = 0;
        this.keyUp = false;
        this.keyDown = false;
        this.canvasSide = canvasSide;
        this.canvasHeight = canvasHeight;
        this.canvasWidth = canvasWidth;
    };

    drawPaddle(ctx) {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    };

    movePaddle() {
        if (this.keyUp && this.y > 0) {
            this.y -= this.speed;
        }
        if (this.keyDown && this.y + this.height < this.canvasHeight) {
            this.y += this.speed;
        }
    };

    incrementScore() {
        this.score += 1;
    };

    reinitCoordinates() {
        this.x = this.canvasSide === "left" ? 0 : this.canvasWidth - this.width;
        this.y = (this.canvasHeight / 2) - (this.height / 2)
        this.speed = this.speed;
    };

    registerKeys(upKey, downKey) {
        document.addEventListener('keydown', (e) => {
            if (e.key === upKey) {
                this.keyUp = true;
            } else if (e.key === downKey) {
                this.keyDown = true;
            }
        })
        document.addEventListener('keyup', (e) => {
            if (e.key === upKey) {
                this.keyUp = false;
            } else if (e.key === downKey) {
                this.keyDown = false;
            }
        })
    };
}

export default Player;