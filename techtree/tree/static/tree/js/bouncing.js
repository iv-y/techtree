let resizeReset = function() {
    w = canvasBody.width = window.innerWidth;
    h = canvasBody.height = window.innerHeight;
}

const opts = { 
    particleColor: "rgb(150,150,150)",
    lineColor: "rgb(110,110,110)",
    particleAmount: 20,
    defaultSpeed: 1,
    variantSpeed: 0.8,
    defaultRadius: 2,
    variantRadius: 2,
    linkRadiusSquare: 40000,
    speedLimit: 10,
    gravity: 25,
};

window.addEventListener("resize", function(){
    deBouncer();
});

let deBouncer = function() {
    clearTimeout(tid);
    tid = setTimeout(function() {
        resizeReset();
    }, delay);
};

let checkDistanceSquare = function(x1, y1, x2, y2){ 
    return (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1);
};

let linkPoints = function(point1, hubs){ 
    for (let i = 0; i < hubs.length; i++) {
        let distance = checkDistanceSquare(point1.x, point1.y, hubs[i].x, hubs[i].y);
        let opacity = 1 - distance / opts.linkRadiusSquare;
        if (opacity > 0) { 
            drawArea.lineWidth = 0.5;
            drawArea.strokeStyle = `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${opacity})`;
            drawArea.beginPath();
            drawArea.moveTo(point1.x, point1.y);
            drawArea.lineTo(hubs[i].x, hubs[i].y);
            drawArea.closePath();
            drawArea.stroke();
        }
    }
}

Particle = function(xPos, yPos){ 
    this.x = Math.random() * w; 
    this.y = Math.random() * h;
    this.speed = opts.defaultSpeed + Math.random() * opts.variantSpeed; 
    this.directionAngle = Math.floor(Math.random() * 360); 
    this.color = opts.particleColor;
    this.radius = opts.defaultRadius + Math.random() * opts. variantRadius; 
    this.vector = {
        x: Math.cos(this.directionAngle) * this.speed,
        y: Math.sin(this.directionAngle) * this.speed
    };
    this.update = function(){ 
        this.border(); 
        this.x += this.vector.x; 
        this.y += this.vector.y; 
        let rrrr = checkDistanceSquare(this.x, this.y, w/2, h/2);
        let aaax = (-opts.gravity) * (this.x-(w/2)) / rrrr;
        let aaay = (-opts.gravity) * (this.y-(h/2)) / rrrr;
        this.vector.x += aaax;
        this.vector.y += aaay; 
        if( this.vector.x >= opts.speedLimit)
            this.vector.x = opts.speedLimit;
        if( this.vector.x <= -opts.speedLimit)
            this.vector.x = -opts.speedLimit;
        if( this.vector.y >= opts.speedLimit)
            this.vector.y = opts.speedLimit;
        if( this.vector.y <= -opts.speedLimit)
            this.vector.y = -opts.speedLimit;
    };
    this.border = function(){ 
        if (this.x >= w || this.x <= 0) { 
            this.vector.x *= -1;
        }
        if (this.y >= h || this.y <= 0) {
            this.vector.y *= -1;
        }
        if (this.x > w) this.x = w;
        if (this.y > h) this.y = h;
        if (this.x < 0) this.x = 0;
        if (this.y < 0) this.y = 0;	
    };
    this.draw = function(){ 
        drawArea.beginPath();
        drawArea.arc(this.x, this.y, this.radius, 0, Math.PI*2);
        drawArea.closePath();
        drawArea.fillStyle = this.color;
        drawArea.fill();
    };
};

function setup(){ 
    particles = [];
    resizeReset();
    for (let i = 0; i < opts.particleAmount; i++){
        particles.push( new Particle() );
    }
    window.requestAnimationFrame(loop);
}

function loop(){ 
    window.requestAnimationFrame(loop);
    drawArea.clearRect(0,0,w,h);
    for (let i = 0; i < particles.length; i++){
        particles[i].update();
        particles[i].draw();
    }
    for (let i = 0; i < particles.length; i++){
        linkPoints(particles[i], particles);
    }
}

const canvasBody = document.getElementById("index-canvas"),
drawArea = canvasBody.getContext("2d");
let delay = 200, tid,
rgb = opts.lineColor.match(/\d+/g);
resizeReset();
setup();