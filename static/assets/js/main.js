function toggleMode() {
  const toggleState = document.getElementById("toggle");

  if (toggleState.classList.contains("toggle-dark")) {
    toggleState.classList.remove("toggle-dark");
    toggleState.classList.add("toggle-light");

    document.documentElement.style.setProperty("--background", "#F2F2F2");
    document.documentElement.style.setProperty("--color", "#000000");
    document.documentElement.style.setProperty("--button", "#FFFFFF");
    document.documentElement.style.setProperty("--buttonhover", "#E5E5E5");
    document.documentElement.style.setProperty(
      "--feedback__color",
      "rgba(0, 0, 0, 0.25)"
    );
  } else {
    toggleState.classList.remove("toggle-light");
    toggleState.classList.add("toggle-dark");
    document.documentElement.style.setProperty("--background", "#0F0F0F");
    document.documentElement.style.setProperty("--color", "#F1F1F1");
    document.documentElement.style.setProperty("--button", "#272727");
    document.documentElement.style.setProperty("--buttonhover", "#3F3F3F");
    document.documentElement.style.setProperty(
      "--feedback__color",
      "rgba(255, 255, 255, 0.7)"
    );
  }
}

const button_id = document.querySelector("#like_dislike");

const like_button = document.getElementById("like");
const like__icon = document.getElementById("like__icon");

const dislike_button = document.getElementById("dislike");
const dislike__icon = document.getElementById("dislike__icon");

const like_count = document.getElementById("number");

function liked() {
  const like_button_status = like_button.getAttribute("data-status");

  like_button.classList.remove("touch_feedback");
  like_button.offsetWidth;
  like_button.classList.add("touch_feedback");

  switch (like_button_status) {
    case "inactive":
      like__icon.classList.add("fa-solid");
      like__icon.classList.remove("fa-regular");
      like_button.setAttribute("data-status", "active");
      like_count.innerHTML = "146";

      dislike__icon.classList.add("fa-regular");
      dislike__icon.classList.remove("fa-solid");
      dislike_button.setAttribute("data-status", "inactive");

      like__icon.classList.remove("like__animation");
      like__icon.offsetWidth;
      like__icon.classList.add("like__animation");
      break;
    case "active":
      like__icon.classList.add("fa-regular");
      like__icon.classList.remove("fa-solid");
      like_button.setAttribute("data-status", "inactive");
      like_count.innerHTML = "145";
      break;
  }
}

function disliked() {
  const dislike_button_status = dislike_button.getAttribute("data-status");

  dislike_button.classList.remove("touch_feedback");
  dislike_button.offsetWidth;
  dislike_button.classList.add("touch_feedback");

  switch (dislike_button_status) {
    case "inactive":
      like__icon.classList.add("fa-regular");
      like__icon.classList.remove("fa-solid");
      like_button.setAttribute("data-status", "inactive");
      like_count.innerHTML = "145";

      dislike__icon.classList.add("fa-solid");
      dislike__icon.classList.remove("fa-regular");
      dislike_button.setAttribute("data-status", "active");

      dislike__icon.classList.remove("dislike__animation");
      dislike__icon.offsetWidth;
      dislike__icon.classList.add("dislike__animation");
      break;
    case "active":
      dislike__icon.classList.add("fa-regular");
      dislike__icon.classList.remove("fa-solid");
      dislike_button.setAttribute("data-status", "inactive");
      break;
  }
}
