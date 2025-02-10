function showBlackOverlay() {
    const overlay = document.createElement("div");
    overlay.id = "black-overlay";
    overlay.style.position = "fixed";
    overlay.style.top = 0;
    overlay.style.left = 0;
    overlay.style.width = "100%";
    overlay.style.height = "100%";
    overlay.style.backgroundColor = "black";
    overlay.style.zIndex = 999999;
    overlay.style.pointerEvents = "none";
    document.body.appendChild(overlay);
}

showBlackOverlay();

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "hideOverlay") {
        hideBlackOverlay();
        sendResponse({ status: "overlay hidden" });
    }
});

async function hideBlackOverlay() {
    const overlay = document.getElementById("black-overlay");
    if (overlay) {
        overlay.remove();
        console.log("Overlay removed");
    }
}
