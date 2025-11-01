const mouseQueue = [];
const resolutionScale = 5;

const canvas = document.querySelector("#mapCanvas");
let rect = canvas.getBoundingClientRect();
canvas.width = rect.width;
canvas.height = rect.height;
const ctx = canvas.getContext("2d");
let pointDistance = 3;

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
    priorPosition = point.target;
});

function distBetween(p1, p2) {
    return Math.hypot(p2[0] - p1[0], p2[1] - p1[1]);
}

function extractPoints(mouseQueue, pointCount) {
    let points = [];
    let queueCursor = 0;
    let iterationCursor = 0;
    // this function must pop only one value
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
            return point;
        }
        mouseQueue.shift();
    }
}

let dotInterval = 20;
let dotIterator = 0;

let lineColor = "#88110055";
ctx.strokeStyle = lineColor;
ctx.lineWidth = 10;

const mapDrawDaemon = setInterval(() => {
    // only mutate the mouseQueue if it actually has enough points to draw
    let points = extractPoints(mouseQueue, 3);
    if (points === null) return;
    popPoint(mouseQueue);
    if (dotIterator++ % dotInterval > (dotInterval / 2)) {
        ctx.beginPath();
        ctx.moveTo(...points[0]);
        ctx.bezierCurveTo(...points[1], ...points[1], ...points[2]);
        ctx.stroke();
    }
}, 5)
