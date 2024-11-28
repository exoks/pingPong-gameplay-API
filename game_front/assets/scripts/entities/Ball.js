class Ball {
    constructor(radius, x, y, speed = 2, velocityX = 2, velocityY = 1, canvasHeight, canvasWidth, color = "#1E90FF") {
        this.radius = radius;
        this.x = x;
        this.y = y;
        this.speed = speed;
        this.velocityX = velocityX;
        this.velocityY = velocityY;
        this.canvasHeight = canvasHeight;
        this.canvasWidth = canvasWidth;
        this.defaultSpeed = speed;
        this.defaultVelocityX = velocityX;
        this.defaultVelocityY = velocityY;
        this.color = color;
    };

    drawBall (ctx) {
        ctx.beginPath();
        ctx.fillStyle = this.color;
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
    }

    detectCollision (p) {
        let pTop = p.y;
        let pBottom = p.y + p.height;
        let pLeft = p.x;
        let pRight = p.x + p.width;
    
        let bTop = this.y - this.radius;
        let bBottom = this.y + this.radius;
        let bLeft = this.x - this.radius;
        let bRight = this.x + this.radius;
        
        return (bBottom > pTop && bTop < pBottom && bRight > pLeft && bLeft < pRight);
    }

    moveBall(game) {
        // Ball collision with walls (left and right edges)

        if (this.x + this.radius > this.canvasWidth) {
            this.velocityX *= -1;
            game.clientPlayer.incrementScore();
            game.reinitComponentsCoordinates();
            game.pauseGame();
        } else if (this.x - this.radius < 0) {
            this.velocityX *= -1;
            game.adversaryPlayer.incrementScore();
            game.reinitComponentsCoordinates();
            game.pauseGame();
        }
        // Ball collision with top and bottom walls
        if (this.y + this.radius > this.canvasHeight || this.y - this.radius < 0) {
            this.velocityY *= -1;
        }
    
        // Ball collision with the paddle
        let player = this.x > this.canvasWidth / 2 ? game.adversaryPlayer : game.clientPlayer;
        if (this.detectCollision(player)) {
            let collidePoint = this.y - (player.y + player.height / 2);
            collidePoint = collidePoint / (player.height / 2);
    
            let direction = (this.x > this.canvasWidth / 2) ? -1 : 1;
            let angleRad = (Math.PI / 4) * collidePoint; // angle between -45 to 45 degrees
            this.velocityY = this.speed * Math.sin(angleRad);
            this.velocityX = direction * this.speed * Math.cos(angleRad);
            this.speed += 0.1; // increase speed after collision
        }
        this.x += this.velocityX;
        this.y += this.velocityY;
    }

    reinitCoordinates() {
        this.x = this.canvasWidth / 2 - 5;
        this.y = this.canvasHeight / 2 - 5;
        this.speed = this.defaultSpeed;
        this.velocityX = this.defaultVelocityX;
        this.velocityY = this.defaultVelocityY;
    };

    updateMultiplayerBall (x, y) {
        this.x = x;
        this.y = y;
    }
}

export default Ball;