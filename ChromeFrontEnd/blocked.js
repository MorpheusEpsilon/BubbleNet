document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get("blockedData", (data) => {
    const kidMessageElem = document.getElementById("kid-message");

    if (kidMessageElem) {
      if (data.blockedData && data.blockedData.kid_analysis) {
        kidMessageElem.textContent = data.blockedData.kid_analysis;
      } else {
        kidMessageElem.textContent = "No details available.";
      }
    }
  });
});
