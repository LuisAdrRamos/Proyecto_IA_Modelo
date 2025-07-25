// Manejo de errores HTMX de forma simple.
document.addEventListener('htmx:afterRequest', (ev) => {
  if (ev.detail.xhr && ev.detail.xhr.status >= 400) {
    alert("Error: " + ev.detail.xhr.responseText);
  }
});
