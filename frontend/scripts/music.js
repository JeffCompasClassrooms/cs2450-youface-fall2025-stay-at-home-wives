let waves = new Audio("css/assets/sounds/" + wavesSound);
waves.volume = 0.4;
waves.loop = true;
let playing = false;
function startWaves() {
    if (playing !== (playing = true)) waves.play()
}
