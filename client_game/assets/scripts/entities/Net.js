class Net {
    constructor(width, height, canvasHeight, canvasWidth, color) {
        this.width = width;
        this.height = height;
        this.x = (canvasWidth / 2) - (width / 2);
        this.y = 20;
        this.canvasHeight = canvasHeight;
        this.canvasWidth = canvasWidth;
        this.color = color;
    }

    drawNet (ctx) {
        for (let i = this.y; i < this.canvasHeight - 30; i += 60) {
            ctx.fillStyle = this.color;
            ctx.fillRect(this.x, i, this.width, this.height);
            ctx.fill();
        }
    }
}

export default Net;