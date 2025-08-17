// Load the kid_analysis message from storage and show it
chrome.storage.local.get("blockedData", (data) => {
  if (data.blockedData && data.blockedData.kid_analysis) {
    const msgEl = document.getElementById("kid-message");
    msgEl.innerHTML = `🌟 ${data.blockedData.kid_analysis} 🌟`;
  }
});
