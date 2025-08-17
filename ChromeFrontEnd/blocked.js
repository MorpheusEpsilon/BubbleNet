document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get("blockedData", (data) => {
    if (data.blockedData) {
      document.getElementById("kid-analysis").textContent =
        data.blockedData.kid_analysis;
    } else {
      document.getElementById("kid-analysis").textContent =
        "No details available.";
    }
  });
});
