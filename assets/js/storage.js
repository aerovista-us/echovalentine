// storage.js: unlocks + preferences + lightweight stats (local only)
(function(){
  const UNLOCK_KEY = "ev_unlocks_v1";
  const PREF_KEY   = "ev_prefs_v1";
  const STAT_KEY   = "ev_stats_v1";

  function jget(key, fallback){
    try { return JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback)); }
    catch { return fallback; }
  }
  function jset(key, val){ localStorage.setItem(key, JSON.stringify(val)); }

  function getPrefs(){ return jget(PREF_KEY, { to:"", from:"", lastPack:"", lastCard:"" }); }
  function setPrefs(p){ jset(PREF_KEY, { ...getPrefs(), ...(p||{}) }); }

  function getStats(){ return jget(STAT_KEY, { punched:0, lastPunchTs:0 }); }
  function bumpPunch(){
    const s = getStats();
    s.punched = (s.punched||0) + 1;
    s.lastPunchTs = Date.now();
    jset(STAT_KEY, s);
    return s;
  }

  function loadUnlocks(){ return jget(UNLOCK_KEY, {}); }
  function saveUnlocks(x){ jset(UNLOCK_KEY, x); }

  window.EV_STORE = {
    // prefs
    getPrefs, setPrefs,
    // stats
    getStats, bumpPunch,
    // unlocks
    isUnlocked(packId){ const x = loadUnlocks(); return !!x[packId]; },
    unlock(packId, code){ const x = loadUnlocks(); x[packId] = { code: (code||"manual"), ts: Date.now() }; saveUnlocks(x); },
    lock(packId){ const x = loadUnlocks(); delete x[packId]; saveUnlocks(x); },
    getAllUnlocks(){ return loadUnlocks(); }
  };
})();
