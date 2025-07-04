document.addEventListener("DOMContentLoaded", (event) => {
  let url = window.location.href;

  // Helper function to handle URL parameter manipulation
  function updateUrlParameter(paramName, addParam) {
    // Remove existing parameter if it exists
    while (url.includes(`&${paramName}=true`)) {
      url = url.replace(`&${paramName}=true`, "");
    }
    while (url.includes(`?${paramName}=true`)) {
      url = url.replace(`?${paramName}=true`, "");
    }
    
    // Add parameter if needed
    if (addParam) {
      const separator = url.includes('?') ? '&' : '?';
      url = url + `${separator}${paramName}=true`;
    }
    
    return url;
  }

  // Helper function to setup toggle functionality
  function setupToggle(toggleId, checkedToggleId, paramName) {
    let toggleInput = document.querySelector(toggleId);

    if (toggleInput) {
      toggleInput.addEventListener("click", (event) => {
        const newUrl = updateUrlParameter(paramName, toggleInput.checked);
        window.location.href = newUrl;
      });
    } else {
      let checkedToggleInput = document.querySelector(checkedToggleId);
      if (checkedToggleInput) {
        checkedToggleInput.addEventListener("click", (event) => {
          const newUrl = updateUrlParameter(paramName, false);
          window.location.href = newUrl;
        });
      }
    }
  }

  // Setup all toggles
  setupToggle("#wifi-toggle", "#wifi-toggle-checked", "has_wifi");
  setupToggle("#sockets-toggle", "#sockets-toggle-checked", "has_sockets");
  setupToggle("#calls-toggle", "#calls-toggle-checked", "can_take_calls");
  setupToggle("#toilet-toggle", "#toilet-toggle-checked", "has_toilet");
});
