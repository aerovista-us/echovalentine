// router.js: hash router: #/boxes , #/box/<id> , #/compose?pack=...&card=... , #/open?token=...
(function(){
  function parseHash(){
    const raw = location.hash || "#/boxes";
    const [path, qs] = raw.replace(/^#/, "").split("?");
    const parts = path.split("/").filter(Boolean);
    const params = new URLSearchParams(qs || "");
    return { raw, path: "/" + parts.join("/"), parts, params };
  }
  function go(hash){ location.hash = hash; }
  window.EV_ROUTER = { parseHash, go };
})();
