//Send the URL to the backend
async function isUrlUnsafe(url) {
  try {
    const response = await fetch("http://127.0.0.1:8000/check_url", {
      //Change for actual server IP address

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

// AI-powered deep check
async function isUrlUnsafeAI(url) {
  try {
    const response = await fetch("http://127.0.0.1:8000/analyze-link", {
      method: "POST",
      body: JSON.stringify({ url: url }),
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      console.error("AI backend returned error:", response.status);
      return {
        unsafe: false,
        score: 100,
        adult_analysis: "",
        kid_analysis: "",
      };
    }

    const data = await response.json();
    console.log("AI response:", data);
    return {
      unsafe: data.unsafe,
      score: data.safety_score,
      adult_analysis: data.adult_analysis,
      kid_analysis: data.kid_analysis,
    };
  } catch (err) {
    console.error("AI backend error:", err);
    return { unsafe: false, score: 100, adult_analysis: "", kid_analysis: "" };
  }
}

// Listen for tab updates
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (
    changeInfo.status === "loading" &&
    (tab.url.startsWith("http") || tab.url.startsWith("https"))
  ) {
    console.log("Checking URL:", tab.url);

    const aiData = await isUrlUnsafeAI(tab.url);

    if (aiData.unsafe) {
      chrome.storage.local.set({
        blockedData: {
          url: tab.url,
          adult_analysis: aiData.adult_analysis,
          kid_analysis: aiData.kid_analysis,
        },
      });

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
