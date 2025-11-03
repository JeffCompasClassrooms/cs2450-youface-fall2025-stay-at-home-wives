const mouseQueue = [];
mouseQueue.actualLength = 0;
const resolutionScale = 5;

const mapCanvas = document.querySelector("#map");
let rect = mapCanvas.getBoundingClientRect();
mapCanvas.width = rect.width;
mapCanvas.height = rect.height;
mapCanvas.style.width = "" + rect.width + "px";
mapCanvas.style.height = "" + rect.height + "px";
const mapContext = mapCanvas.getContext("2d");

function weight(optimalValue, strength) {
    return {optimalValue, strength};
}

let weightTypes = [
    "land", // land
    "shore", // specifically land near water
    "body", // Any placed body (ships, creatures, etc.)
    "beast" // Sea creatures
];

let weightGrid = {
    cellSize: 10,
    cells: {},
};

function positionToGridKey(x, y) {
    [x, y] = canvasToGrid(x, y);
    return (Math.floor(x) & 0xffff) | ((Math.floor(y) & 0xffff) << 16);
}

function canvasToGrid(x, y) {
    return [Math.floor(x / weightGrid.cellSize), Math.floor(y / weightGrid.cellSize)];
}

function gridToCanvas(x, y) {
    return [x * weightGrid.cellSize, y * weightGrid.cellSize];
}

function getWeights(x, y) {
    return weightGrid.cells[positionToGridKey(x, y)];
}

function disperseWeight(weight, center, falloff) {
}

function findOptimal(weight, center, budget) {
}

function createDeferred() {
    let resolve;
    let promise = new Promise(res => {resolve = res;});
    return {promise, resolve};
}

let canvasDraws = [];
let availableDraw = createDeferred();

function queueCanvasDraw(func, args) {
    canvasDraws.push([func, args]);
    availableDraw.resolve();
}

let drawCanvasDaemon = async () => {
    while (true) {
        await availableDraw.promise;
        availableDraw = createDeferred();
        while (canvasDraws.length > 0) {
            let [func, args] = canvasDraws.shift();
            mapContext.save();
            await func(...args);
            mapContext.restore();
        }
    }
}

drawCanvasDaemon();

function drawCompass() {
    let compassRose = new Image();
    compassRose.src = "css/assets/compassRose.png";
    compassRose.onload = () => {
        queueCanvasDraw(
            async () => {
                let x = mapCanvas.width * (3 / 15);
                let y = mapCanvas.height * (8 / 10);
                mapContext.drawImage(compassRose, x, y, 150, 150);
            },
            []
        );
    };
}

function distBetween(p1, p2) {
    return Math.hypot(p2[0] - p1[0], p2[1] - p1[1]);
}

function angleBetween(p1, p2) {
    return Math.atan2(p2[1] - p1[1], p2[0] - p1[0]);
}

function angleDiff(a, b) {
    const twoPi = Math.PI * 2;
    let diff = (b - a) % twoPi;
    if (diff < 0) diff += twoPi;
    if (diff > Math.PI) diff -= twoPi;
    return [Math.abs(diff), diff > 0 ? 1 : -1];
}

function generateIslandPoints(center, shorePointCount, baseMagnitude, noisiness) {
    let points = [];
    let angleInterval = (Math.PI * 2) / shorePointCount;
    let magnitude = baseMagnitude
    let skew = Math.random() * (Math.PI * 2);
    for (let angle = 0; angle < (Math.PI * 2); angle += angleInterval) {
        magnitude += ((Math.random() * noisiness) - noisiness / 2);
        let point = [center[0] + Math.cos(angle + skew) * magnitude, center[1] + Math.sin(angle + skew) * magnitude];
        points.push(point);
    }
    return points;
}

function circleAt(x, radius) {
    return Math.sqrt(-(x*x) + radius*radius);
}

// bias an angle toward a different one via an increasing effect with their difference
function biasAngle(angle, dest, maxDifference) {
    // magnitude is the correction that would be applied to `angle` with `direction` to fully correct it
    // we will apply some fraction of magnitude based on how far it is from maxDifference
    let [magnitude, direction] = angleDiff(angle, dest);
    let x = Math.min(1, magnitude / maxDifference);
    let proportion = -circleAt(x, 1) + 1;
    return (angle + (magnitude * proportion * direction));
}

async function traceShapeNoisy(shape, stepSize, noise, threshold) {
    let points = [];
    let thisPoint = shape[0];
    let thisAngle = angleBetween(thisPoint, shape[1]);
    for (let i = 0; i < shape.length + 1; i++) {
        let dest = shape[i % shape.length];
        let distance = distBetween(thisPoint, dest);
        do {
            let angle = angleBetween(thisPoint, dest);
            thisAngle += (Math.random() * noise) - (noise / 2);
            thisAngle = biasAngle(thisAngle, angle, Math.PI * 0.5);
            let xDiff = Math.cos(thisAngle) * stepSize;
            let yDiff = Math.sin(thisAngle) * stepSize;
            thisPoint = [thisPoint[0] + xDiff, thisPoint[1] + yDiff];
            points.push([...thisPoint]);
            distance = distBetween(thisPoint, dest);
        } while (distance > threshold);
    }
    return points;
}

function drawIsland(center, shorePointCount, baseMagnitude, noisiness) {
    let islandShape = generateIslandPoints(center, shorePointCount, baseMagnitude, noisiness);
    queueCanvasDraw(
        async () => {
            islandShape = await traceShapeNoisy(islandShape, 5, 1, 6);
            for (let point of islandShape) {
                mapContext.filter = "blur(20px)";
                mapContext.fillStyle = "#662900";
                mapContext.beginPath();
                mapContext.arc(...point, 10, 0, (Math.PI * 2));
                mapContext.fill();
                mapContext.filter = "blur(2px)";
                mapContext.fillStyle = "#100005ff";
                mapContext.beginPath();
                mapContext.arc(...point, 3, 0, (Math.PI * 2));
                mapContext.fill();
            }
            mapContext.fillStyle = "#bc9b69c0";
            mapContext.beginPath();
            mapContext.moveTo(...islandShape[0]);
            for (let i = 1; i < islandShape.length + 1; i++) {
                mapContext.lineTo(...islandShape[i % islandShape.length]);
            }
            mapContext.fill();
        },
        []
    );
}

drawCompass()
drawIsland([Math.random() * rect.width, Math.random() * rect.height], 10, 300, 250);

let pointDistance = 5;

function checkInterpolation(interp, interval) {
    let i = 0;
    let prior = pointNext(interp);
    let current = null;
    let failureCount = 0;
    while (pointPeek(interp, 1) !== null) {
        current = pointNext(interp);
        let distance = distBetween(prior, current);
        let error = Math.abs(interval - distance);
        if (error > 0.1) {
            console.error("error > 0.1 on iteration", i, "with", current, "as current and", prior, "as prior");
            failureCount++;
        }
        prior = current;
        i++;
    }
    console.log("failure count:", failureCount);
}

// generate a map to get from `p1` to `p2` in the correct number of steps.
// no point, including the destination, may be more or less distant from the last than `interval`
function interpolate(p1, p2, interval) {
    let length = distBetween(p1, p2);
    let steps = Math.floor(length / interval);
    let ratio = (steps * interval) / length;
    if (steps == 0) return null;
    let xStep = (p2[0] - p1[0]) * ratio / steps;
    let yStep = (p2[1] - p1[1]) * ratio / steps;
    let stepIteration = 0;
    let base = p1;
    let target = [p1[0] + (steps * xStep), p1[1] + (steps * yStep)];
    return {base, target, steps, xStep, yStep, stepIteration};
}

function pointPeek(p, step, useCheck) {
    if (useCheck == undefined || useCheck === true) {
        if (p.stepIteration + step >= p.steps) {
            return null;
        }
    }
    let x = p.base[0] + (p.xStep * (p.stepIteration + step));
    let y = p.base[1] + (p.yStep * (p.stepIteration + step));
    return [x, y];
}

function pointNext(p) {
    let point = pointPeek(p, 0);
    p.stepIteration++;
    return point;
}

function pointPeekLast(p) {
    let point = pointPeek(p, p.steps, false);
    return point;
}

let priorPosition = null;

window.addEventListener('mousemove', (event) => {
    if (priorPosition === null) {
        priorPosition = [event.clientX, event.clientY];
    }
    let point = interpolate(priorPosition, [event.clientX, event.clientY], pointDistance);
    if (point === null) {
        return;
    }
    mouseQueue.push(point);
    mouseQueue.actualLength += point.steps;
    priorPosition = point.target;
    let pointBuffer = 100;
});

function extractPoints(mouseQueue, pointCount) {
    let points = [];
    let queueCursor = 0;
    let iterationCursor = 0;
    while (points.length < pointCount) {
        if (mouseQueue.length <= queueCursor) return null;
        let base = mouseQueue[queueCursor];
        let pointCandidate = pointPeek(base, iterationCursor)
        if (pointCandidate === null) {
            queueCursor += 1;
            iterationCursor = 0;
            continue;
        }
        iterationCursor++;
        points.push(pointCandidate);
    }
    return points;
}

function popPoint(mouseQueue) {
    while (true) {
        if (mouseQueue.length < 1) return null;
        let point = pointNext(mouseQueue[0]);
        if (point !== null) {
            mouseQueue.actualLength--;
            return point;
        }
        mouseQueue.shift();
    }
}

let defaultImgHeight = 100;
let defaultImgWidth = 100;
let fadeInSeconds = 2;
let fadeInInterval = 50;
let fadeInIterations = fadeInSeconds * 1000 / fadeInInterval
let fadeInOpacity = 1 / fadeInIterations

async function newMapImage(name, scale, position) {
    const img = new Image();
    img.src = "/css/assets/mapDrawings/" + name;
    img.onload = () => {
        let imgWidth = defaultImgWidth * scale;
        let imgHeight = defaultImgHeight * scale;
        position[0] -= imgWidth / 2;
        position[1] -= imgHeight / 2;
        let count = 0;
        let fadeIn = setInterval(() => {
            queueCanvasDraw(
                async () => {
                    let opacity = 1 / fadeInIterations;
                    mapContext.globalAlpha = opacity;
                    mapContext.drawImage(img, ...position, imgHeight, imgWidth);
                    if (count >= fadeInIterations) {
                        clearInterval(fadeIn);
                    }
                    count++;
                },
                []
            );
        }, fadeInInterval);
    }
}

const strokes = [];

async function markStroke(position) {
    strokes.push(position);
    if (strokes.length % 10 == 0) {
        let length = Object.values(imageCategories).length;
        let category = Object.values(imageCategories)[Math.floor(Math.random() * length)];
        let imgName = category.images[Math.floor(Math.random() * category.images.length)];
        let scale = category.scale;
        position[0] += Math.random() * 100 - 50;
        position[1] += Math.random() * 100 - 50;
        newMapImage(imgName, scale, position);
    }
}

let dotInterval = 20;
let dotIterator = 0;

let lineColor = "#440011";

async function mapDrawOne() {
    // mutate the mouseQueue while it actually has enough points to draw
    let points;
    if ((points = extractPoints(mouseQueue, 3)) !== null) {
        queueCanvasDraw(
            () => {
                mapContext.strokeStyle = lineColor;
                mapContext.lineWidth = 10;
                popPoint(mouseQueue);
                if (dotIterator++ % dotInterval > (dotInterval / 2)) {
                    mapContext.beginPath();
                    mapContext.filter = "blur(2px)";
                    let falter = (Math.random() * 10) - 5;
                    mapContext.lineWidth += falter;
                    mapContext.moveTo(...points[0]);
                    mapContext.bezierCurveTo(...points[1], ...points[1], ...points[2]);
                    mapContext.stroke();
                }
                // The center of a stroke is halfway through the drawing interval, which is halfway through the whole interval.
                if (dotIterator % dotInterval === (Math.round(dotInterval * 3/4))) {
                    markStroke(points[1]);
                }
            },
            []
        );
        return true;
    }
    else return false;
};

let mapDrawDaemon = setInterval(mapDrawOne, 1);
