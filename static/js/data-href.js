let processDataHref = () => {
  document.querySelectorAll("[data-href]").forEach((item) => {
    item.classList.add("cursor-pointer");
    item.addEventListener("click", (e) => {
      e.preventDefault();
      let href = item.getAttribute("data-href");
      window.location.href = href;
    });
  });
};
processDataHref();