//Send the URL to the backend
async function isUrlUnsafe(url) {
  try {
    const response = await fetch("http://127.0.0.1:8000/check_url", {
      method: "POST",
      body: JSON.stringify({ url: url }),
      headers: { "Content-Type": "application/json" },
    });

    //Debugging
    if (!response.ok) {
      console.error("Backend returned error:", response.status);
      return false;
    }

    const data = await response.json();
    console.log("Backend response:", data); // Debug log
    return data.unsafe; // expects { "unsafe": true/false }
  } catch (err) {
    console.error("Backend error:", err);
    return false;
  }
}

// Listen for tab updates
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === "loading" && tab.url.startsWith("http")) {
    console.log("Checking URL:", tab.url);

    const unsafe = await isUrlUnsafe(tab.url);

    if (unsafe) {
      console.warn("Blocked unsafe site:", tab.url);

      //Redirect to a warning page
      chrome.tabs.update(tabId, { url: chrome.runtime.getURL("blocked.html") });

      //notify user
      chrome.notifications.create({
        type: "basic",
        iconUrl: "icon.jpg",
        title: "Blocked Unsafe Site",
        message: "Access to this website has been blocked for your safety.",
      });
    }
  }
});
