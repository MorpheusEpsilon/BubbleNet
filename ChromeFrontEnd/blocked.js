document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get("blockedData", (data) => {
    if (data.blockedData) {
      document.getElementById("blocked-url").textContent = data.blockedData.url;
      document.getElementById("adult-analysis").textContent =
        data.blockedData.adult_analysis;
      document.getElementById("kid-analysis").textContent =
        data.blockedData.kid_analysis;
    } else {
      document.getElementById("blocked-url").textContent = "Unknown site";
      document.getElementById("adult-analysis").textContent =
        "No details available.";
      document.getElementById("kid-analysis").textContent =
        "No details available.";
    }
  });
});
