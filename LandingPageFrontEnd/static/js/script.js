// JS for specific CTA interactions

// Target only the Download Extension button
const downloadBtn = document.querySelector('.download-btn');

if (downloadBtn) {
  downloadBtn.addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default link behavior
    alert("Thanks for your interest! Download coming soon.");
  });
}

