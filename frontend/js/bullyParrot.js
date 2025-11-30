const BullyParrot = (() => {
    // ------------------ Assets ------------------
    const assets = window.PARROT_ASSETS || {};

    const pirateInsults = [
        "Ye look like a sea urchin that lost a fight",
        "Ye smell like low tide and poor decisions",
        "Ye scurvy-ridden excuse for a bilge rat",
        "I’ve met smarter oysters",
        "yer face could sink a ship",
        "Ye’ve the charm of a moldy cannonball",
        "Even me shadow refuses to stand near ye",
        "barnacle-brained buffoon",
        "I’d call ye a swashbuckler, but ye barely buckle yer boots",
        "Ye limp like a rope that’s been chewed by crabs",
        "Aye, ye’ve the personality of wet driftwood",
        "Ye walk like yer legs be on backward",
        "Yer presence lowers the value of me treasure",
        "Ye couldn’t navigate a map if X marked yer own nose",
        "Soggy bootlicker",
    ];

    const deckMessages = [
        "Squawk! Behold me DECK!",
        "Har har! Another DECK pic fer ye!",
        "Squaawk! Feast yer eyes on this fine wooden DECK!",
        "DECK"
    ];

    const silentAppearChance = 0.3;
    const jumpscareChance = 0.1;

    let parrotContainer, bubble, bubbleText;

    // Helper
    const randomItem = list => list[Math.floor(Math.random() * list.length)];

    // ------------------ Bubbles ------------------
    function showBubble(text) {
        bubbleText.textContent = text;
        bubble.classList.add("show");

        clearTimeout(bubble.hideTimeout);
        bubble.hideTimeout = setTimeout(() => {
            bubble.classList.remove("show");
        }, 4500);
    }

    // ------------------ Deck Overlay ------------------
    function bullySmileDelay() {
        const overlay = document.getElementById("deck-overlay");
        const smile = document.getElementById("parrot-deck-smile");
    
        smile.style.display = "block";
    
        setTimeout(() => {
            smile.style.display = "none";
            overlay.style.display = "none";
        }, 6000 + Math.random() * 1000);
    }

    function showDeckOverlay(message) {
        const overlay = document.getElementById("deck-overlay");
        const img = document.getElementById("deck-overlay-img");
        const closeBtn = document.getElementById("deck-close-btn");
    
        img.src = randomItem(assets.deck || []);
    
        closeBtn.textContent = message || "Close";
    
        overlay.style.display = "flex";
    
        closeBtn.onclick = () => {
            bullySmileDelay();
        };
    }

    // ------------------ Jumpscare ------------------
    function showJumpScare() {
        const jump = document.getElementById("parrot-jumpscare");
        jump.style.display = "flex";

        setTimeout(() => {
            jump.style.display = "none";
        }, 6000 + Math.random() * 1000);
    }

    // ------------------ Random Behavior ------------------
    function randomBehavior() {
        const appear = Math.random() < 0.6;

        if (appear) {
            parrotContainer.style.display = "block";

            // Silent appear
            if (Math.random() < silentAppearChance) {
                bubble.classList.remove("show");
                return;
            }

            // Jumpscare
            if (Math.random() < jumpscareChance) {
                showJumpScare();
                return;
            }

            // Deck or insult
            if (Math.random() < 0.4) {
                const deckLine = randomItem(deckMessages);
                showBubble(deckLine);
                showDeckOverlay(deckLine);
            } else {
                showBubble(randomItem(pirateInsults));
            }

        } else {
            parrotContainer.style.display = "none";
        }
    }

    // ------------------ Create Parrot ------------------
    function createParrot() {
        // Overlay + jumpscare always exist
        document.body.insertAdjacentHTML("beforeend", `
            <div id="deck-overlay">
                <img id="deck-overlay-img" class="deck-image" src="">
                <button id="deck-close-btn">Close</button>
            </div>

            <div id="parrot-jumpscare">
                <img src="${assets.jumpscare}">
            </div>

            <div id="parrot-deck-smile">
                <img id="deck-smile-img" src="${assets.reaction}">
            </div>
        `);

        // Main parrot
        parrotContainer = document.createElement("div");
        parrotContainer.id = "bully-parrot";
        parrotContainer.innerHTML = `
            <img src="${assets.idle}" id="parrot-img">
            <div id="parrot-bubble">
                <p id="parrot-text"></p>
            </div>
        `;
        document.body.appendChild(parrotContainer);

        bubble = document.querySelector("#parrot-bubble");
        bubbleText = document.querySelector("#parrot-text");

        // Clicking Bully triggers insult
        document.getElementById("parrot-img").onclick = () => {
            showBubble(randomItem(pirateInsults));
        };

        // Start behavior
        setInterval(randomBehavior, 14000);
    }

    return { createParrot };
})();

document.addEventListener("DOMContentLoaded", BullyParrot.createParrot);
