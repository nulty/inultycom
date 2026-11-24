import "./css/styles.scss" // must be imported so rollup-plugin-postcss can run

// Contact links carry the address reversed and base64-encoded in data-email
// (main/context_processors.py), so it never appears in the HTML as text. Turn
// them into mailto: links; with data-email-text, show the address as well.
function revealEmail() {
  document.querySelectorAll("[data-email]").forEach((link) => {
    const email = atob(link.dataset.email).split("").reverse().join("")
    link.href = `mailto:${email}`
    if ("emailText" in link.dataset) link.textContent = email
  })
}

document.addEventListener("DOMContentLoaded", revealEmail)
