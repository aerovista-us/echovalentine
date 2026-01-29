// app_bootstrap.js
window.addEventListener("DOMContentLoaded", () => {
  // Show splash screen immediately
  if(window.EV_SPLASH){
    window.EV_SPLASH.show();
  }
  
  window.EV_APP.boot().then(() => {
    // Mark content as ready after boot completes
    if(window.EV_SPLASH){
      window.EV_SPLASH.markContentReady();
    }
  }).catch(err => {
    console.error(err);
    // Hide splash even on error
    if(window.EV_SPLASH){
      window.EV_SPLASH.markContentReady();
    }
    const el = document.getElementById("app");
    if(el){
      el.innerHTML = `<div class="card"><div class="inner"><div class="h1">Crashed</div><p class="p">${String(err)}</p></div></div>`;
    }
  });
});
