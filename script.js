const carouselBtn = document.querySelector(".carousel-btn");
const galleryBtn = document.querySelector(".gallery-btn");
const container = document.querySelector(".container");
const tableSection = document.querySelector(".table-section");
const displaySection = document.querySelector(".display-section");

const rows = document.querySelectorAll("tr");
const galleryContainer = document.createElement("div");
const carouselContainer = document.createElement("div");
const backBtn = document.createElement("button");
backBtn.textContent = "Back";
backBtn.classList.add("back-btn");

const prev = document.createElement("div");
prev.classList.add("prev");
prev.textContent = "<";

const next = document.createElement("div");
next.classList.add("next");
next.textContent = ">";

const dotsContainer = document.createElement("div");
dotsContainer.classList.add("dots-container");

let currentSlideIndex = 0;

let data = getTableData();

popup();

createGallery(data);

createCarousel(data);

function popup() {
  rows.forEach((row) => {
    let cells = row.querySelectorAll("td");
    if (!cells[0] || !cells[1]) return;

    row.addEventListener("mousedown", () => {
      console.log("mousedown");
      let resContainer = document.createElement("div");
      resContainer.classList.add("popup-resource");
      let res = document.createElement("img");
      res.setAttribute("src", cells[0].textContent.trim());
      res.setAttribute("alt", cells[1].textContent.trim());

      resContainer.appendChild(res);
      tableSection.appendChild(resContainer);
    });

    document.addEventListener("mouseup", () => {
      const resContainer = tableSection.querySelector(".popup-resource");
      const res = tableSection.querySelector(".popup-resource img");
      if (res) resContainer.removeChild(res);
      if (resContainer) tableSection.removeChild(resContainer);
      console.log("mouseup");
    });
  });
}

carouselBtn.addEventListener("click", () => {
  tableSection.classList.add("hide-table");

  carouselContainer.classList.add("carousel-display");

  displaySection.appendChild(carouselContainer);
  displaySection.appendChild(dotsContainer);
  displaySection.appendChild(backBtn);

  showSlide(currentSlideIndex);
});

galleryBtn.addEventListener("click", () => {
  tableSection.classList.add("hide-table");

  galleryContainer.classList.add("gallery-display");

  displaySection.appendChild(galleryContainer);
  displaySection.appendChild(backBtn);
});

backBtn.addEventListener("click", () => {
  tableSection.classList.remove("hide-table");

  // Remove all child elements securely
  while (displaySection.firstChild) {
    displaySection.removeChild(displaySection.firstChild);
  }
});

function getTableData() {
  let data = [];
  let tbody = document.querySelector("tbody");
  let rows = tbody.querySelectorAll("tr");

  rows.forEach((row) => {
    let cells = row.querySelectorAll("td");
    if (cells.length >= 2) {
      let src = cells[0].textContent.trim();
      let alt = cells[1].textContent.trim();
      data.push({ src, alt });
    }
  });

  return data;
}

function createGallery(data) {
  data.forEach((d) => {
    let image = document.createElement("img");
    image.setAttribute("src", d.src);
    image.setAttribute("alt", d.alt);
    galleryContainer.appendChild(image);
  });
}

function createCarousel(data) {
  let firstSlide = true;

  data.forEach((d, index) => {
    let carouselSlide = document.createElement("div");
    carouselSlide.classList.add("carousel-slide");

    let image = document.createElement("img");
    image.setAttribute("src", d.src);
    image.setAttribute("alt", d.alt);

    let resourceText = document.createElement("div");
    resourceText.classList.add("resource-overlay");
    resourceText.textContent = "resource" + " " + (index + 1);

    let textOverlay = document.createElement("div");
    textOverlay.classList.add("text-overlay");
    textOverlay.textContent = d.alt;

    let dot = document.createElement("div");
    dot.classList.add("dot");

    dotsContainer.appendChild(dot);

    carouselSlide.appendChild(image);
    carouselSlide.appendChild(resourceText);
    carouselSlide.appendChild(textOverlay);

    if (firstSlide) {
      carouselSlide.style.display = "block";
      firstSlide = false;
    }

    carouselContainer.appendChild(carouselSlide);
    carouselContainer.appendChild(prev);
    carouselContainer.appendChild(next);
  });
}

function showSlide(index) {
  let slides = document.querySelectorAll(".carousel-slide");
  let dots = document.querySelectorAll(".dot");

  if (index >= slides.length) {
    currentSlideIndex = 0;
  } else if (index < 0) {
    currentSlideIndex = slides.length - 1;
  } else {
    currentSlideIndex = index;
  }

  slides.forEach((slide, index) => {
    slide.style.display = "none";
    dots[index].classList.remove("dot-active");
  });

  slides[currentSlideIndex].style.display = "block";
  dots[currentSlideIndex].classList.add("dot-active");
}

function changeSlide(direction) {
  showSlide(currentSlideIndex + direction);
}

prev.addEventListener("click", () => {
  changeSlide(-1);
});
next.addEventListener("click", () => {
  changeSlide(1);
});
