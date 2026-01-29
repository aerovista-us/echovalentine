// loader.js: loads pack manifest + pack metadata + pack content lazily.
(function(){
  async function j(url){
    const r = await fetch(url, { cache: "no-cache" });
    if(!r.ok) throw new Error(`Failed to load ${url}: ${r.status}`);
    return await r.json();
  }

  async function loadManifest(){ return await j("packs/manifest.json"); }
  async function loadPack(packPath){ return await j(`packs/${packPath}`); }

  async function loadPackData(packId, pack){
    const base = `packs/${packId}/`;
    let cardsRaw = await j(base + pack.data.cards);
    let stickersRaw = await j(base + pack.data.stickers);
    
    // Handle both formats: { cards: [...] } or [...]
    const cards = Array.isArray(cardsRaw) ? { cards: cardsRaw } : cardsRaw;
    const stickers = Array.isArray(stickersRaw) ? { stickers: stickersRaw } : stickersRaw;
    
    let tracks = { tracks: [] };
    try{
      if(pack.data.tracks){
        let tracksRaw = await j(base + pack.data.tracks);
        // Handle both formats: { tracks: [...] } or [...]
        tracks = Array.isArray(tracksRaw) ? { tracks: tracksRaw } : tracksRaw;
      }
    } catch(_e){ /* optional */ }
    return { cards, stickers, tracks };
  }

  window.EV_LOADER = { loadManifest, loadPack, loadPackData };
})();
