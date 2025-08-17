const API_KEY = "AIzaSyBeiyXNxUd_4tOCFAXvebDDCv_BPpx-jdI";

//Send the URL to the backend
async function isUrlUnsafe(url) {
  try {
    const response = await fetch("http://localhost:5000/check_url", {
      method: "POST",
      body: JSON.stringify({ url: url }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await response.json();
    return data.unsafe; // expects { "unsafe": true/false }
  } catch (err) {
    console.error("Backend error:", err);
    return false;
  }
}

// Listen for tab updates
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === "loading" && tab.url.startsWith("http")) {
    const unsafe = await isUrlUnsafe(tab.url);
    if (unsafe) {
      // Block by redirecting to a warning page
      chrome.tabs.update(tabId, { url: chrome.runtime.getURL("blocked.html") });
      chrome.notifications.create({
        type: "basic",
        iconUrl: "icon.png",
        title: "Blocked Unsafe Site",
        message: "Access to this website has been blocked for your safety.",
      });
    }
  }
});
