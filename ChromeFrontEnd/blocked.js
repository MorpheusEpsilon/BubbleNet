//Loads the IA explanation into the warning page the child sees
// Falls to "No details..." if the analysis is missing
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
