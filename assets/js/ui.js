// ui.js: tiny view helpers (no frameworks)
(function(){
  const app = () => document.getElementById("app");

  function h(tag, attrs={}, children=[]){
    const el = document.createElement(tag);
    for(const [k,v] of Object.entries(attrs||{})){
      if(k === "class") el.className = v;
      else if(k === "html") el.innerHTML = v;
      else if(k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2), v);
      else if(v === false || v === null || v === undefined) {}
      else if(k === "value" && (tag === "input" || tag === "textarea" || tag === "select")) el.value = v;
      else if(k === "readonly" && tag === "input") el.readOnly = v;
      else el.setAttribute(k, String(v));
    }
    (children||[]).forEach(c => el.appendChild(c));
    return el;
  }

  // Toasts
  let toastHost;
  function ensureToastHost(){
    if(toastHost) return toastHost;
    toastHost = document.createElement("div");
    toastHost.className = "toastHost";
    document.body.appendChild(toastHost);
    return toastHost;
  }

  function toast(msg, kind="good", ms=1400){
    const host = ensureToastHost();
    const t = h("div",{class:`toast ${kind}`},[
      h("span",{class:"dot", "aria-hidden":"true"}),
      h("span",{html: msg})
    ]);
    host.appendChild(t);
    setTimeout(()=>{ t.style.opacity="0"; t.style.transform="translateY(6px)"; }, ms);
    setTimeout(()=>{ try{ t.remove(); }catch{} }, ms+450);
  }

  function confettiBurst(){
    // Very lightweight: create 24 divs, animate via WAAPI
    const layer = document.createElement("div");
    layer.className = "confetti";
    document.body.appendChild(layer);

    const count = 24;
    for(let i=0;i<count;i++){
      const c = document.createElement("div");
      c.style.position="absolute";
      c.style.left = (Math.random()*100) + "vw";
      c.style.top  = (-10 - Math.random()*30) + "vh";
      c.style.width = (6 + Math.random()*10) + "px";
      c.style.height = (6 + Math.random()*14) + "px";
      c.style.borderRadius = "6px";
      c.style.opacity = "0.95";
      c.style.background = "rgba(255,255,255,.9)";
      layer.appendChild(c);

      const dx = (-20 + Math.random()*40);
      const rot = (-180 + Math.random()*360);
      const dur = (900 + Math.random()*600);

      c.animate([
        { transform:`translate(0,0) rotate(0deg)`, opacity: 1 },
        { transform:`translate(${dx}vw, 120vh) rotate(${rot}deg)`, opacity: 0.7 }
      ], { duration: dur, easing:"cubic-bezier(.2,.7,.2,1)", fill:"forwards" });
    }

    setTimeout(()=>{ try{ layer.remove(); }catch{} }, 1400);
  }

  // Optional analytics
  function installUmami(){
    const cfg = window.EV_CONFIG || {};
    if(!cfg.UMAMI_SRC || !cfg.UMAMI_WEBSITE_ID) return;
    const s = document.createElement("script");
    s.defer = true;
    s.src = cfg.UMAMI_SRC;
    s.setAttribute("data-website-id", cfg.UMAMI_WEBSITE_ID);
    document.head.appendChild(s);
  }

  function track(event, data){
    try{
      if(window.umami && typeof window.umami.track === "function"){
        window.umami.track(event, data);
      }
    } catch(_e){}
  }

  window.EV_UI = { app, h, toast, confettiBurst, installUmami, track };
})();
