//Send the URL to the backend (Blacklist)
async function isUrlUnsafe(url) {
  try {
    //Change for actual server address
    const response = await fetch("http://127.0.0.1:8000/check_url", {
      method: "POST",
      body: JSON.stringify({ url: url }),
      headers: { "Content-Type": "application/json" },
    });

    //Debugging help
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

// AI-powered check
async function isUrlUnsafeAI(url) {
  try {
    //Change for actual server adress
    const response = await fetch("http://127.0.0.1:8000/analyze-link", {
      method: "POST",
      body: JSON.stringify({ url: url }),
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      //In case of error don't block it
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
    (tab.url.startsWith("http") || tab.url.startsWith("https")) //Avoid google sites or so
  ) {
    console.log("Checking URL:", tab.url);

    const aiData = await isUrlUnsafeAI(tab.url); //Get the AI data
    const safeData = await isUrlUnsafe(tab.url); //Get the blacklist check

    //Check for both sites
    if (aiData.unsafe || safeData.unsafe) {
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
