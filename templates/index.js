document.addEventListener("DOMContentLoaded", (event) => {
  wifiToggleInput = document.querySelector("#wifi-toggle");
  url = window.location.href;
  if (wifiToggleInput) {
    wifiToggleInput.addEventListener("click", (event) => {
      if (wifiToggleInput.checked) {
        while (url.includes("&has_wifi=true")) {
          url = url.replace("&has_wifi=true", "");
        }
        url = url + "&has_wifi=true";
        window.location.href = url;
      }
    });
  } else {
    wifiToggleCheckedInput = document.querySelector("#wifi-toggle-checked");
    wifiToggleCheckedInput.addEventListener("click", (event) => {
      if (!wifiToggleCheckedInput.checked) {
        while (url.includes("&has_wifi=true")) {
          url = url.replace("&has_wifi=true", "");
        }
        window.location.href = url;
      }
    });
  }
  socketsToggleInput = document.querySelector("#sockets-toggle");
  if (socketsToggleInput) {
    socketsToggleInput.addEventListener("click", (event) => {
      if (socketsToggleInput.checked) {
        while (url.includes("&has_sockets=true")) {
          url = url.replace("&has_sockets=true", "");
        }
        url = url + "&has_sockets=true";
        window.location.href = url;
      }
    });
  } else {
    socketsToggleCheckedInput = document.querySelector(
      "#sockets-toggle-checked"
    );
    socketsToggleCheckedInput.addEventListener("click", (event) => {
      if (!socketsToggleCheckedInput.checked) {
        while (url.includes("&has_sockets=true")) {
          url = url.replace("&has_sockets=true", "");
        }
        window.location.href = url;
      }
    });
  }
  callsToggleInput = document.querySelector("#calls-toggle");
  if (callsToggleInput) {
    callsToggleInput.addEventListener("click", (event) => {
      if (callsToggleInput.checked) {
        while (url.includes("&can_take_calls=true")) {
          url = url.replace("&can_take_calls=true", "");
        }
        url = url + "&can_take_calls=true";
        window.location.href = url;
      }
    });
  } else {
    callsToggleCheckedInput = document.querySelector("#calls-toggle-checked");
    callsToggleCheckedInput.addEventListener("click", (event) => {
      if (!callsToggleCheckedInput.checked) {
        while (url.includes("&can_take_calls=true")) {
          url = url.replace("&can_take_calls=true", "");
        }
        window.location.href = url;
      }
    });
  }
  toiletToggleInput = document.querySelector("#toilet-toggle");
  if (toiletToggleInput) {
    toiletToggleInput.addEventListener("click", (event) => {
      if (toiletToggleInput.checked) {
        while (url.includes("&has_toilet=true")) {
          url = url.replace("&has_toilet=true", "");
        }
        url = url + "&has_toilet=true";
        window.location.href = url;
      }
    });
  } else {
    toiletToggleCheckedInput = document.querySelector("#toilet-toggle-checked");
    toiletToggleCheckedInput.addEventListener("click", (event) => {
      if (!toiletToggleCheckedInput.checked) {
        while (url.includes("&has_toilet=true")) {
          url = url.replace("&has_toilet=true", "");
        }
        window.location.href = url;
      }
    });
  }
});
