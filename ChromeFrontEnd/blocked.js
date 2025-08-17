// Recuperar datos del almacenamiento y mostrarlos en los textareas
document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get("blockedData", (result) => {
    if (result.blockedData) {
      const { kid_analysis, adult_analysis } = result.blockedData;
      document.getElementById("kid-message").value = kid_analysis || "No data";
      document.getElementById("adultBox").value = adult_analysis || "No data";
    }
  });

  // Botón "Ver más"
  document.getElementById("seeMore").addEventListener("click", () => {
    window.open("https://www.connectsafely.org/", "_blank");
  });
});
