import "./css/styles.scss" // must be imported so rollup-plugin-postcss can run

window.addEventListener("load", function () {
  document.querySelector(".js-scroll-down").addEventListener("click", (e) => {
    e.preventDefault()

    let target = document.querySelector("#intro").scrollHeight
    window.scrollBy({ top: window.innerHeight, behavior: "smooth" })
  })
})
