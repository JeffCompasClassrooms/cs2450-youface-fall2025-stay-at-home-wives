const canvas = document.getElementById("starfield");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const stars = Array.from({length: 600}, () => ({
  x: Math.random() * canvas.width,
  y: Math.random() * canvas.height,
  r: 0.1 + Math.random() * 1.5,
  opacity: 0.8 + Math.random() * 0.2,
  twinkle: Math.random() * 0.009 + 0.035
}));

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let star of stars) {
    star.opacity += (Math.random() > 0.5 ? 1 : -1) * star.twinkle;
    star.opacity = Math.max(0.2, Math.min(1, star.opacity));

    ctx.beginPath();
    ctx.shadowBlur = 12;
    ctx.shadowColor = "white";
    ctx.arc(star.x, star.y, star.r, 0, 2 * Math.PI);
    ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
    ctx.fill();
  }
  requestAnimationFrame(draw);
}
draw();
