document.getElementById("openPanel").addEventListener("click", () => {
  chrome.tabs.create({ url: "https://your-parent-panel-url.com" });
});

// Example: fetch blocked count from background
chrome.runtime.sendMessage({ action: "getStats" }, (response) => {
  document.getElementById("blockedCount").innerText = response.blockedCount;
  document.getElementById("lastAlert").innerText = response.lastAlert || "None";
});
