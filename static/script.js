// This file is for any additional JavaScript needed across the application
function showFlashMessage(message, category) {
  const flashDiv = document.createElement("div");
  flashDiv.className = `flash flash-${category}`;
  flashDiv.innerHTML = `
        ${message}
        <span class="close-btn" onclick="this.parentElement.style.display='none'">&times;</span>
    `;
  document.body.insertBefore(flashDiv, document.body.firstChild);

  // Auto-hide after 5 seconds
  setTimeout(() => {
    if (flashDiv.parentElement) {
      flashDiv.style.display = "none";
    }
  }, 5000);
}

document.addEventListener("DOMContentLoaded", function () {
  // Close flash messages when clicked
  document.querySelectorAll(".flash").forEach((flash) => {
    flash.addEventListener("click", function () {
      this.style.display = "none";
    });
  });

  // Add animation to buttons
  document.querySelectorAll(".btn").forEach((button) => {
    button.addEventListener("mousedown", function () {
      this.style.transform = "translateY(1px)";
    });

    button.addEventListener("mouseup", function () {
      this.style.transform = "translateY(0)";
    });

    button.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
    });
  });
});
