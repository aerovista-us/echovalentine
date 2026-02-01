// splash.js: Simple and fun splash screen with SVG animation
(function(){
  let splashEl = null;
  let svgLoaded = false;
  let contentReady = false;
  let minWaitTime = 3000; // 3 seconds after SVG loads
  let svgLoadTime = null;
  let checkInterval = null;

  function createSplash(){
    if(splashEl) return splashEl;
    
    splashEl = document.createElement("div");
    splashEl.className = "splash-screen";
    splashEl.innerHTML = `
      <div class="splash-content">
        <div class="splash-video-container">
          <video src="assets/img/echovalentine_splash.mp4" autoplay muted loop playsinline class="splash-video" onloadeddata="window.EV_SPLASH.onSvgLoad()" onerror="window.EV_SPLASH.onSvgError()">
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
    `;
    
    return splashEl;
  }

  function checkReady(){
    if(!svgLoaded || !contentReady) return false;
    
    const now = Date.now();
    const timeSinceSvgLoad = now - svgLoadTime;
    
    if(timeSinceSvgLoad >= minWaitTime){
      return true;
    }
    
    return false;
  }

  function tryHide(){
    if(checkInterval){
      clearInterval(checkInterval);
      checkInterval = null;
    }
    
    if(checkReady()){
      hide();
    } else {
      // Check again in 100ms
      checkInterval = setInterval(() => {
        if(checkReady()){
          clearInterval(checkInterval);
          checkInterval = null;
          hide();
        }
      }, 100);
    }
  }

  function hide(){
    if(!splashEl) return;
    
    splashEl.classList.add("splash-hiding");
    
    setTimeout(() => {
      if(splashEl && splashEl.parentNode){
        splashEl.parentNode.removeChild(splashEl);
      }
      splashEl = null;
      svgLoaded = false;
      contentReady = false;
      svgLoadTime = null;
    }, 500); // Match CSS transition duration
  }

  function show(container){
    if(!container) container = document.body;
    
    const splash = createSplash();
    if(splash.parentNode) return; // Already shown
    
    container.appendChild(splash);
    
    // Reset state
    svgLoaded = false;
    contentReady = false;
    svgLoadTime = null;
    
    // Force re-check video load status (in case it's cached)
    const video = splash.querySelector(".splash-video");
    if(video && video.readyState >= 2){
      onSvgLoad();
    }
  }

  function onSvgLoad(){
    svgLoaded = true;
    svgLoadTime = Date.now();
    
    // Start checking if we can hide
    if(contentReady){
      tryHide();
    }
  }

  function onSvgError(){
    console.warn("Splash video failed to load");
    // Still mark as loaded to prevent infinite waiting
    svgLoaded = true;
    svgLoadTime = Date.now();
    if(contentReady){
      tryHide();
    }
  }

  function markContentReady(){
    contentReady = true;
    
    // Start checking if we can hide
    if(svgLoaded){
      tryHide();
    }
  }

  window.EV_SPLASH = {
    show,
    hide,
    markContentReady,
    onSvgLoad,
    onSvgError
  };
})();
