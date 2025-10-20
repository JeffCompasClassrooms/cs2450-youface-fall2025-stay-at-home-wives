const phrases = ["Share Treasure","Find Crew","Chart Connections"];
const typingElement = document.getElementById("typing");
const cursor = document.getElementById("cursor");
const typingSpeed = 100;
const erasingSpeed = 100;
const pauseTime = 3000;

let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;

function type() {
  const currentPhrase = phrases[phraseIndex];

  if (isDeleting) {
    cursor.classList.add("typing");
    typingElement.textContent = currentPhrase.substring(0, charIndex--);
    if (charIndex < 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      setTimeout(type, typingSpeed);
    } else {
      setTimeout(type, erasingSpeed);
    }
  } else {
    cursor.classList.add("typing");
    typingElement.textContent = currentPhrase.substring(0, charIndex++);
    if (charIndex > currentPhrase.length) {
      cursor.classList.remove("typing"); // resume blinking on pause
      isDeleting = true;
      setTimeout(type, pauseTime);
    } else {
      setTimeout(type, typingSpeed);
    }
  }
}

type();
