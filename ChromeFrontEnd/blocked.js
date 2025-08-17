document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get("blockedData", (result) => {
    if (result.blockedData) {
      const { kid_analysis, adult_analysis } = result.blockedData;

      // Insert AI analysis into the boxes
      document.getElementById("kid-message").innerText =
        kid_analysis || "No data available";
    }
  });
});
