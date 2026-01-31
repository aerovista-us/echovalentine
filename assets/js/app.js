// app.js: EchoValentines Viral — single addictive loop
(function(){
  const S = {
    packs: [],       // [{id, packPath, pack}]
    packIndex: {},   // id -> pack
    dataCache: {},   // id -> {cards, stickers, tracks}
    renderSeq: 0,    // Race condition guard for async renders
  };

const { app, h, toast, confettiBurst, installUmami, track } = window.EV_UI;

  function esc(s){ return String(s||"").replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }
  function qs(obj){
    const p = new URLSearchParams();
    Object.entries(obj||{}).forEach(([k,v])=>{ if(v!==undefined && v!==null) p.set(k, v); });
    return p.toString();
  }

  function setStreakPill(){
    const el = document.getElementById("streakText");
    if(!el) return;
    const s = window.EV_STORE.getStats();
    el.textContent = `${s.punched||0} punched`;
  }

  function randPick(arr){
    if(!arr || arr.length===0) return null;
    return arr[Math.floor(Math.random()*arr.length)];
  }

  function getCardImage(card){
    // Handle both front_svg (old format) and src (new format)
    return card.front_svg || card.src || "";
  }

  function getPackDir(packId){
    const packEntry = S.packs.find(p => p.id === packId);
    return packEntry?.packDir || packId;
  }

  async function ensurePackData(packId){
    if(S.dataCache[packId]) return S.dataCache[packId];
    const pack = S.packIndex[packId];
    const packDir = getPackDir(packId);
    const data = await window.EV_LOADER.loadPackData(packDir, pack);
    S.dataCache[packId] = data;
    return data;
  }

  // Shared Card Stage Renderer - used by both Compose and Open
  function clamp01(n){ return Math.max(0, Math.min(1, n)); }

  function normalizeSticker(st, meta){
    // Supports multiple formats:
    // - percent: xp/yp in [0..1]
    // - percent100: xp/yp in [0..100]
    // - px: x/y with meta.cw/ch available
    if(!st) return null;

    // Percent format
    if(typeof st.xp === "number" && typeof st.yp === "number"){
      const xp = st.xp > 1 ? st.xp/100 : st.xp;
      const yp = st.yp > 1 ? st.yp/100 : st.yp;
      return {
        ...st,
        xp: clamp01(xp),
        yp: clamp01(yp),
        sp: typeof st.sp === "number" ? st.sp : 1,
        rot: typeof st.rot === "number" ? st.rot : 0
      };
    }

    // Pixel format + compose stage width/height in payload
    if(typeof st.x === "number" && typeof st.y === "number" && meta && meta.cw && meta.ch){
      return {
        ...st,
        xp: clamp01(st.x / meta.cw),
        yp: clamp01(st.y / meta.ch),
        sp: typeof st.s === "number" ? st.s : (typeof st.sp === "number" ? st.sp : 1),
        rot: typeof st.rot === "number" ? st.rot : 0
      };
    }

    // Fallback guess: treat x/y as 0..1 if it looks like it
    if(typeof st.x === "number" && typeof st.y === "number" && st.x <= 1.2 && st.y <= 1.2){
      return {...st, xp: clamp01(st.x), yp: clamp01(st.y), sp: st.sp ?? 1, rot: st.rot ?? 0};
    }

    return null;
  }

  function renderCardStage({ cardSrc, stickers = [], meta = {}, stageId = "", packDir = "", interactive = false }){
    const img = h("img", { src: cardSrc, alt: "Card preview" });

    const stage = h("div", { class: interactive ? "cardStage composeStage" : "cardStage", id: stageId }, [
      img,
      h("div", { class: "stickerLayer" }, [])
    ]);

    const layer = stage.querySelector(".stickerLayer");

    // Set stage aspect ratio from real image dimensions
    img.addEventListener("load", () => {
      const w = img.naturalWidth, ht = img.naturalHeight;
      if(w && ht) stage.style.aspectRatio = `${w} / ${ht}`;
    });

    // Render stickers
    stickers
      .map(st => normalizeSticker(st, meta))
      .filter(Boolean)
      .forEach(st => {
        // Determine sticker path
        const stickerPath = st.packId 
          ? `packs/sticker_packs/${st.packId}/${st.src || st.url || st.path}`
          : `packs/${packDir}/${st.src || st.url || st.path}`;

        const el = h("img", {
          class: "stickerEl",
          src: stickerPath,
          alt: "Sticker",
          draggable: "false"
        });

        // xp/yp are normalized; sp is scale; rot degrees
        el.style.left = `${st.xp * 100}%`;
        el.style.top  = `${st.yp * 100}%`;

        // IMPORTANT: translate(-50%,-50%) keeps scaling centered.
        el.style.transform =
          `translate(-50%,-50%) rotate(${st.rot || 0}deg) scale(${st.sp || 1})`;

        // Use percent-based base size for better cross-device consistency
        el.style.width = `clamp(34px, ${(st.wv || 9)}vw, 110px)`;

        if(interactive){
          el.style.cursor = "move";
          el.style.filter = "drop-shadow(0 10px 22px rgba(0,0,0,.5))";
        }

        layer.appendChild(el);
      });

    return stage;
  }

  async function render(appEl){
    const mySeq = ++S.renderSeq;

    const r = window.EV_ROUTER.parseHash();
    const route = r.parts[0] || "boxes";

    // Clear immediately
    appEl.innerHTML = "";

    // Small loading card for async routes (prevents "blank" feeling)
    const showLoading = () => {
      if(mySeq !== S.renderSeq) return;
      appEl.innerHTML = "";
      appEl.appendChild(h("div",{class:"card"},[
        h("div",{class:"inner"},[
          h("div",{class:"h1", html:"Loading…"}),
          h("p",{class:"p", html:"Warming up the card composer."})
        ])
      ]));
    };

    try{
      if(route === "boxes") return renderBoxes(appEl);

      // Async routes: show loading immediately
      if(route === "box"){
        showLoading();
        await renderBox(appEl, decodeURIComponent(r.parts[1]||""));
        return;
      }
      if(route === "compose"){
        showLoading();
        await renderCompose(appEl, r.params);
        return;
      }
      if(route === "open"){
        showLoading();
        await renderOpen(appEl, r.params);
        return;
      }

      if(route === "about") return renderAbout(appEl);
      return renderNotFound(appEl);

    } catch(err){
      console.error("Route render failed:", route, err);
      if(mySeq !== S.renderSeq) return;
      appEl.innerHTML = "";
      appEl.appendChild(h("div",{class:"card"},[
        h("div",{class:"inner"},[
          h("div",{class:"h1", html:"Render error"}),
          h("p",{class:"p", html: esc(String(err && err.message ? err.message : err))}),
          h("div",{style:"height:10px"}),
          h("button",{class:"btn primary", onclick:()=>location.hash="#/boxes"},[
            document.createTextNode("Go home")
          ])
        ])
      ]));
    }
  }

  function renderBoxes(appEl){
    const prefs = window.EV_STORE.getPrefs();

    const hero = h("div",{class:"card"},[
      h("div",{class:"inner"},[
        h("div",{class:"row spread"},[
          h("div",{},[
            h("div",{class:"h1", html:"Pick a box. Punch a card."}),
            h("p",{class:"p", html:"One screen to choose. One button to share. Receiver opens instantly."})
          ]),
          h("div",{},[
            h("span",{class:"badge", html:`<span class="dot"></span> ${esc(S.packs.length)} boxes`})
          ])
        ]),
        h("div",{class:"hr"}),
        h("div",{class:"row"},[
          h("button",{class:"btn primary", onclick:()=>shuffleAndCompose(prefs.lastPack)},[
            document.createTextNode("Shuffle a card")
          ]),
          h("span",{class:"small", html:`Tip: hit <span class="kbd">Shuffle</span> until it feels right.`})
        ])
      ])
    ]);

    const shelf = h("div",{class:"shelf", style:"margin-top:14px;"});
    for(const p of S.packs){
      const cardCount = p.pack.cards_count || (p.pack.data?.cards ? "" : "");
      const coverImage = p.pack.assets?.box_art ? `packs/${p.packDir}/${p.pack.assets.box_art}` : null;
      const b = h("div",{class:"pack-box", onclick:()=>location.hash=`#/box/${encodeURIComponent(p.id)}`},[
        h("div",{class:"pack-cover-wrapper"},[
          coverImage ? h("img",{src: coverImage, alt: p.pack.name || p.id, class:"pack-cover"}) : h("div",{class:"pack-cover-placeholder"}),
          h("div",{class:"pack-overlay"})
        ]),
        h("div",{class:"pack-info"},[
          h("div",{class:"pack-header"},[
            h("div",{class:"pack-badge", html:`<span class="dot"></span> Ready`}),
            cardCount ? h("div",{class:"pack-count", html: `${esc(cardCount)} cards`}) : null
          ]),
          h("div",{class:"pack-title", html: esc(p.pack.name || p.id)}),
          h("div",{class:"pack-tagline", html: esc(p.pack.tagline || "")}),
          h("div",{class:"pack-actions"},[
            h("button",{class:"btn", onclick:(e)=>{e.stopPropagation(); shuffleAndCompose(p.id);}},[
              document.createTextNode("Shuffle")
            ]),
            h("button",{class:"btn primary", onclick:(e)=>{e.stopPropagation(); quickStartPack(p.id);}},[
              document.createTextNode("Start")
            ])
          ])
        ])
      ]);
      shelf.appendChild(b);
    }

    appEl.appendChild(hero);
    appEl.appendChild(shelf);
  }

  async function renderBox(appEl, packId){
    appEl.innerHTML = ""; // ✅ ensures loading card disappears
    if(!packId || !S.packIndex[packId]) return renderNotFound(appEl);
    const pack = S.packIndex[packId];
    const packDir = getPackDir(packId);

    const data = await ensurePackData(packId);
    const cards = (data.cards?.cards || []);

    window.EV_STORE.setPrefs({ lastPack: packId });

    const header = h("div",{class:"card"},[
      h("div",{class:"inner"},[
        h("div",{class:"row spread"},[
          h("div",{},[
            h("div",{class:"h1", html: esc(pack.name || packId)}),
            h("p",{class:"p", html: esc(pack.tagline || "Pick a card. Write one line. Punch & copy.")})
          ]),
          h("div",{class:"row"},[
            h("button",{class:"btn", onclick:()=>location.hash="#/boxes"},[document.createTextNode("Back")]),
            h("button",{class:"btn primary", onclick:()=>shuffleAndCompose(packId)},[document.createTextNode("Shuffle")])
          ])
        ])
      ])
    ]);

    // Gallery: Only show cards (no stickers, tracks, or other items)
    const gallery = h("div",{class:"card", style:"margin-top:14px;"},[
      h("div",{class:"inner"},[
        h("div",{class:"h2", html:"Choose a card"}),
        h("p",{class:"p", html:"Tap any card to personalize it. Keep it short. Keep it punchy."}),
        h("div",{class:"hr"}),
        (function(){
          const g = h("div",{class:"gallery"});
          // Only iterate through cards - stickers and tracks are available on compose page
          for(const c of cards){
            const cardImage = `packs/${packDir}/${getCardImage(c)}`;
            const t = h("div",{class:"card-thumb", onclick:()=>location.hash=`#/compose?${qs({pack:packId, card:c.id})}`},[
              h("div",{class:"card-image-wrapper"},[
                h("img",{src: cardImage, alt: c.title ? `Card: ${c.title}` : "Card", class:"card-cover"}),
                h("div",{class:"card-overlay"})
              ]),
              h("div",{class:"card-text"},[
                h("div",{class:"card-title", html: esc(c.title || c.id)})
              ])
            ]);
            g.appendChild(t);
          }
          return g;
        })()
      ])
    ]);

    appEl.appendChild(header);
    appEl.appendChild(gallery);
  }

  function templates(){
    return [
      "You’re my favorite glitch in the matrix.",
      "I choose you. Every timeline.",
      "If this is a simulation… keep me in yours.",
      "Your vibe? Unreasonably elite.",
      "I’d fight a bear for you (politely).",
      "You + me = soft chaos, perfect.",
      "Here’s a tiny spell: be kind to yourself."
    ];
  }

  async function shuffleAndCompose(preferPackId){
    const packId = preferPackId && S.packIndex[preferPackId] ? preferPackId : randPick(S.packs)?.id;
    if(!packId) return;
    const data = await ensurePackData(packId);
    const card = randPick(data.cards?.cards || []);
    if(!card) return;

    const t = randPick(templates()) || "";
    const prefs = window.EV_STORE.getPrefs();
    // Put a default message template only if blank
    if(!prefs || (!prefs.to && !prefs.from)){
      // no-op
    }
    window.EV_STORE.setPrefs({ lastPack: packId, lastCard: card.id });

    // route to compose with a template query flag
    location.hash = `#/compose?${qs({ pack: packId, card: card.id, t: t })}`;
  }

  function quickStartPack(packId){
    // open pack page (gallery) — or jump to last card if exists
    const prefs = window.EV_STORE.getPrefs();
    if(prefs.lastPack === packId && prefs.lastCard){
      location.hash = `#/compose?${qs({ pack: packId, card: prefs.lastCard })}`;
    } else {
      location.hash = `#/box/${encodeURIComponent(packId)}`;
    }
  }

  async function renderCompose(appEl, params){
    appEl.innerHTML = ""; // ✅ ensures loading card disappears
    const packId = params.get("pack");
    const cardId = params.get("card");
    if(!packId || !cardId) return renderNotFound(appEl);
    const pack = S.packIndex[packId];
    if(!pack) return renderNotFound(appEl);
    const packDir = getPackDir(packId);

    const data = await ensurePackData(packId);
    const card = (data.cards?.cards || []).find(x => String(x.id) === String(cardId));
    if(!card) return renderNotFound(appEl);

    // Load sticker packs
    const stickerPacks = await window.EV_LOADER.loadStickerPacks();

    window.EV_STORE.setPrefs({ lastPack: packId, lastCard: cardId });

    const prefs = window.EV_STORE.getPrefs();
    const state = {
      to: prefs.to || "",
      from: prefs.from || "",
      msg: params.get("t") || "",
      stickers: [], // Array of {src, x, y, w, h, packId}
      track: "",
      selectedStickerPack: null // Currently selected sticker pack ID
    };

    // Use shared card stage renderer for base structure
    const cardSrc = `packs/${packDir}/${getCardImage(card)}`;
    const stage = renderCardStage({
      cardSrc,
      stickers: [],
      meta: {},
      stageId: "composeStage",
      packDir,
      interactive: true
    });
    
    // Get the sticker layer for interactive editing
    const stickerLayer = stage.querySelector(".stickerLayer");
    
    // Make sure sticker layer is interactive in compose mode
    if(stickerLayer) stickerLayer.style.pointerEvents = "auto";

    function createStickerElement(stickerData){
      // Determine sticker path based on whether it's from a sticker pack or pack stickers
      const stickerPath = stickerData.packId 
        ? `packs/sticker_packs/${stickerData.packId}/${stickerData.src}`
        : `packs/${packDir}/${stickerData.src}`;
      
      const el = h("div",{class:"stickerElement"},[
        h("img",{src:stickerPath, alt:"Sticker", style:"width:100%; height:100%; object-fit:contain"}),
        h("div",{class:"stickerResizer"})
      ]);
      
      const rect = stage.getBoundingClientRect();
      // Convert percent to pixels for interactive editing
      const xPx = (stickerData.xp || 0) * rect.width;
      const yPx = (stickerData.yp || 0) * rect.height;
      const sizePx = (stickerData.wv || 9) * (rect.width / 100); // Convert vw to px
      
      el.style.position = "absolute";
      el.style.left = xPx + "px";
      el.style.top = yPx + "px";
      el.style.width = sizePx + "px";
      el.style.height = sizePx + "px";
      el.style.transform = `translate(-50%,-50%) rotate(${stickerData.rot || 0}deg) scale(${stickerData.sp || 1})`;
      el.style.cursor = "move";
      el.style.zIndex = "10";
      el.style.filter = "drop-shadow(0 10px 22px rgba(0,0,0,.5))";
      
      window.EV_DRAGDROP.attachDrag(el, el);
      window.EV_DRAGDROP.attachResize(el, el.querySelector(".stickerResizer"));
      
      el.addEventListener("dblclick", ()=>{
        const idx = state.stickers.findIndex(s => s.el === el);
        if(idx >= 0){
          state.stickers.splice(idx, 1);
          el.remove();
          sync();
        }
      });
      
      stickerData.el = el;
      return el;
    }

    function sync(){
      window.EV_STORE.setPrefs({ to: state.to, from: state.from });
      // Update sticker positions as percentages
      const rect = stage.getBoundingClientRect();
      state.stickers.forEach(s => {
        if(s.el){
          const elRect = s.el.getBoundingClientRect();
          const stageRect = stage.getBoundingClientRect();
          // Calculate center position as percentage
          s.xp = clamp01((elRect.left + elRect.width/2 - stageRect.left) / stageRect.width);
          s.yp = clamp01((elRect.top + elRect.height/2 - stageRect.top) / stageRect.height);
          // Store scale and size
          s.sp = s.sp || 1;
          s.rot = s.rot || 0;
          // Store size as viewport width percentage for responsive scaling
          s.wv = (elRect.width / stageRect.width) * 100;
        }
      });
    }

    function addSticker(stickerSrc, stickerPackId = null){
      const rect = stage.getBoundingClientRect();
      const stickerData = {
        src: stickerSrc,
        packId: stickerPackId, // null for pack stickers, pack ID for sticker pack stickers
        xp: Math.random() * 0.6 + 0.2, // 20-80% of stage width
        yp: Math.random() * 0.6 + 0.2, // 20-80% of stage height
        sp: 1,
        rot: 0,
        wv: 9 // 9vw base size
      };
      state.stickers.push(stickerData);
      const el = createStickerElement(stickerData);
      if(stickerLayer) stickerLayer.appendChild(el);
      sync();
    }

    function randomSticker(){
      // Combine pack stickers and sticker pack stickers for random selection
      const packStickerList = (data.stickers?.stickers || []).map(s => ({...s, packId: null}));
      const allStickerList = [...packStickerList];
      
      // Add all sticker pack stickers
      (stickerPacks || []).forEach(sp => {
        (sp.stickers || []).forEach(s => {
          allStickerList.push({...s, packId: sp.id});
        });
      });
      
      const s = randPick(allStickerList);
      if(s && s.src){
        addSticker(s.src, s.packId || null);
        toast("Sparkle added ✨", "good");
        track("sticker_random", { pack: packId, stickerPack: s.packId || "pack" });
      } else {
        toast("No stickers available", "bad");
      }
    }

    function clearStickers(){
      state.stickers.forEach(s => {
        if(s.el) s.el.remove();
      });
      state.stickers = [];
      sync();
      toast("Sparkles cleared", "good");
    }

    function selectSticker(stickerSrc, stickerPackId = null){
      addSticker(stickerSrc, stickerPackId);
      toast("Sticker added", "good");
    }

    function selectTrack(trackId){
      state.track = trackId;
      sync();
      toast("Track selected", "good");
    }

    async function punchAndCopy(){
      // Get stage dimensions for backward compatibility
      const rect = stage.getBoundingClientRect();
      
      // Convert stickers to percent format
      const stickerPayload = state.stickers.length > 0 ? JSON.stringify(state.stickers.map(s => ({
        src: s.src,
        packId: s.packId || null,
        xp: s.xp || 0,
        yp: s.yp || 0,
        sp: s.sp || 1,
        rot: s.rot || 0,
        wv: s.wv || 9
      }))) : "";

      const payload = {
        v: 1,
        pack: packId,
        card: cardId,
        to: (state.to||"").slice(0, 42),
        from: (state.from||"").slice(0, 42),
        msg: (state.msg||"").slice(0, 160),
        sticker: stickerPayload,
        track: state.track || "",
        cw: Math.round(rect.width), // Store for backward compat
        ch: Math.round(rect.height), // Store for backward compat
        ts: Date.now()
      };
      const token = window.EV_SHARE.encode(payload);
      // Use production URL from config, or fall back to current location for local dev
      const baseUrl = (window.EV_CONFIG && window.EV_CONFIG.BASE_URL) || `${location.origin}${location.pathname}`;
      const url = `${baseUrl}#/open?token=${token}`;

      try{
        await navigator.clipboard.writeText(url);
        const s = window.EV_STORE.bumpPunch();
        setStreakPill();
        confettiBurst();
        toast("Punched! Link copied.", "good");
        track("punch_copy", { pack: packId, card: cardId });
      } catch(e){
        toast("Couldn't copy — link shown below.", "bad", 1800);
        track("punch_copy_fail", { pack: packId, card: cardId });
      }
      out.value = url;
      outWrap.style.display = "block";
    }

    const outWrap = h("div",{style:"display:none"},[
      h("div",{class:"small", html:"Share link"}),
      h("input",{class:"input", id:"outLink", readonly:true, value:""})
    ]);
    const out = outWrap.querySelector("#outLink");

    // Sticker picker - combine pack stickers and sticker packs
    const packStickers = (data.stickers?.stickers || []);
    const allStickerPacks = stickerPacks || [];
    
    // Build sticker picker UI with tabs for each pack
    let stickerPicker = null;
    if(packStickers.length > 0 || allStickerPacks.length > 0){
      const tabs = [];
      const contents = [];
      
      // Function to update sticker picker tabs and content visibility
      function updateStickerPicker(){
        const tabsEl = document.querySelector(".pickerTabs");
        const contentsEl = document.querySelector(".pickerContents");
        if(!tabsEl || !contentsEl) return;
        
        // Update tab active states
        const tabButtons = tabsEl.querySelectorAll(".pickerTab");
        tabButtons.forEach((tab, idx) => {
          let shouldBeActive = false;
          if(packStickers.length > 0){
            if(idx === 0){
              shouldBeActive = !state.selectedStickerPack;
            } else {
              shouldBeActive = state.selectedStickerPack === allStickerPacks[idx - 1]?.id;
            }
          } else {
            shouldBeActive = state.selectedStickerPack === allStickerPacks[idx]?.id;
          }
          tab.classList.toggle("active", shouldBeActive);
        });
        
        // Update content visibility
        const contentDivs = contentsEl.querySelectorAll(".pickerContent");
        contentDivs.forEach((content, idx) => {
          let shouldBeActive = false;
          if(packStickers.length > 0){
            if(idx === 0){
              shouldBeActive = !state.selectedStickerPack;
            } else {
              shouldBeActive = state.selectedStickerPack === allStickerPacks[idx - 1]?.id;
            }
          } else {
            shouldBeActive = state.selectedStickerPack === allStickerPacks[idx]?.id;
          }
          content.style.display = shouldBeActive ? "" : "none";
          content.classList.toggle("active", shouldBeActive);
        });
      }
      
      // Pack stickers tab (if available)
      if(packStickers.length > 0){
        const isActive = !state.selectedStickerPack;
        tabs.push(h("button",{
          class:`pickerTab ${isActive ? "active" : ""}`,
          onclick:()=>{
            state.selectedStickerPack = null;
            updateStickerPicker();
          }
        },[document.createTextNode("Pack")]));
        
        contents.push(h("div",{
          class:`pickerContent ${isActive ? "active" : ""}`,
          style: !isActive ? "display:none" : ""
        },[
          h("div",{class:"pickerGrid"}, packStickers.slice(0, 12).map(s => 
        h("div",{class:"pickerItem", onclick:()=>selectSticker(s.src)},[
          h("img",{src:`packs/${packDir}/${s.src}`, alt:"Sticker"})
        ])
      ))
        ]));
      }
      
      // Sticker pack tabs
      allStickerPacks.forEach((sp, idx) => {
        const isActive = state.selectedStickerPack === sp.id || (!state.selectedStickerPack && packStickers.length === 0 && idx === 0);
        tabs.push(h("button",{
          class:`pickerTab ${isActive ? "active" : ""}`,
          onclick:()=>{
            state.selectedStickerPack = sp.id;
            updateStickerPicker();
          }
        },[document.createTextNode(sp.name || sp.id)]));
        
        contents.push(h("div",{
          class:`pickerContent ${isActive ? "active" : ""}`,
          style: !isActive ? "display:none" : ""
        },[
          h("div",{class:"pickerGrid"}, (sp.stickers || []).slice(0, 12).map(s => 
            h("div",{class:"pickerItem", onclick:()=>selectSticker(s.src, sp.id)},[
              h("img",{src:`packs/sticker_packs/${sp.id}/${s.src}`, alt:"Sticker"})
            ])
          ))
        ]));
      });
      
      stickerPicker = h("div",{class:"pickerSection"},[
        h("div",{class:"small", html:"Stickers"}),
        tabs.length > 1 ? h("div",{class:"pickerTabs"}, tabs) : null,
        h("div",{class:"pickerContents"}, contents)
      ]);
    }

    // Track picker
    const tracks = (data.tracks?.tracks || []);
    const trackPicker = tracks.length > 0 ? h("div",{class:"pickerSection"},[
      h("div",{class:"small", html:"Track (optional)"}),
      h("select",{class:"input", onchange:(e)=>{state.track=e.target.value;sync();}},[
        h("option",{value:"", html:"No track"}),
        ...tracks.map(t => h("option",{value:t.id || t.title || "", html:t.title || t.name || "Untitled"}))
      ])
    ]) : null;

    // Build the top action bar
    const actionBar = h("div",{class:"actionBar"},[
      h("div",{class:"row wrap"},[
        h("button",{class:"btn", onclick:randomSticker},["Random ✨"]),
        h("button",{class:"btn", onclick:clearStickers},["Clear"]),
        h("button",{class:"btn", onclick:()=>shuffleAndCompose(packId)},["Shuffle card"])
      ]),
      h("button",{class:"btn primary", id:"btnPunch", onclick:punchAndCopy},[
        "Punch & Copy Link"
      ])
    ]);

    const left = h("section",{class:"card"},[
      h("div",{class:"inner"},[
        h("div",{class:"row spread"},[
          h("div",{},[
            h("div",{class:"h1", html:"Compose"}),
            h("p",{class:"p", html:"One line. One link. Maximum impact."})
          ]),
          h("button",{class:"btn", onclick:()=>location.hash=`#/box/${encodeURIComponent(packId)}`},[
            document.createTextNode("Back")
          ])
        ]),
        h("div",{class:"hr"}),
        actionBar,
        outWrap,
        h("div",{class:"hr"}),
        h("label",{class:"small", html:"To"}),
        h("input",{class:"input", placeholder:"Name", value: state.to, oninput:(e)=>{state.to=e.target.value;sync();}}),
        h("div",{style:"height:10px"}),
        h("label",{class:"small", html:"From"}),
        h("input",{class:"input", placeholder:"Name", value: state.from, oninput:(e)=>{state.from=e.target.value;sync();}}),
        h("div",{style:"height:10px"}),
        h("label",{class:"small", html:"Message"}),
        (function(){
          const ta = h("textarea",{class:"input", placeholder:"Keep it short…", value: state.msg || "", oninput:(e)=>{state.msg=e.target.value;sync();}});
          return ta;
        })(),
        trackPicker ? h("div",{style:"height:10px"}) : null,
        trackPicker,
        trackPreviewEl,
        h("div",{class:"hr"}),
        stickerPicker
      ])
    ]);
    
    // Initialize track preview if track is already selected
    if(state.track) updateTrackPreview();

    const right = h("section",{class:"card"},[
      h("div",{class:"inner"},[
        h("div",{class:"h2", html:"Preview"}),
        h("p",{class:"p", html:"Drag stickers to position. Double-click to remove."}),
        h("div",{class:"hr"}),
        stage,
        h("div",{style:"height:10px"}),
        h("div",{class:"small", html:`Pack: <b>${esc(pack.name || packId)}</b> • Card: <b>${esc(card.title || cardId)}</b>`})
      ])
    ]);

    // Enable drop zone for stickers
    window.EV_DRAGDROP.enableDropZone(stage, (item, e) => {
      if(item.type === "sticker" && item.src){
        const rect = stage.getBoundingClientRect();
        const xp = (e.clientX - rect.left) / rect.width;
        const yp = (e.clientY - rect.top) / rect.height;
        const stickerData = {
          src: item.src,
          packId: item.packId || null,
          xp: clamp01(xp),
          yp: clamp01(yp),
          sp: 1,
          rot: 0,
          wv: 9
        };
        state.stickers.push(stickerData);
        const el = createStickerElement(stickerData);
        if(stickerLayer) stickerLayer.appendChild(el);
        sync();
      }
    });

    appEl.appendChild(h("div",{class:"grid two"},[left, right]));
    sync();

    // First-run tutorial
    (function maybeTutorial(){
      const prefs = window.EV_STORE.getPrefs();
      if(prefs.tutorialDismissed) return;

      const steps = [
        {t:"Write it", b:"Fill To/From and a short message."},
        {t:"Add stickers", b:"Use Random ✨ or choose stickers. Drag to move. Double-click to remove."},
        {t:"Add a track (optional)", b:"Pick a track under the message box (if this pack includes music)."},
        {t:"Send it", b:"Hit Punch & Copy Link, paste it into text/social, and they open instantly."}
      ];

      let i = 0;

      const overlay = h("div",{class:"tourOverlay"},[]);
      const card = h("div",{class:"tourCard"},[]);
      overlay.appendChild(card);

      function draw(){
        card.innerHTML = "";
        card.appendChild(h("div",{class:"tourTitle", html: esc(steps[i].t)}));
        card.appendChild(h("div",{class:"tourBody", html: esc(steps[i].b)}));

        const dont = h("label",{class:"tourCheck"},[
          h("input",{type:"checkbox", id:"tourDont"}),
          "Don't show again"
        ]);

        const btnNext = h("button",{class:"btn primary", onclick:()=>{
          const checked = !!card.querySelector("#tourDont")?.checked;
          if(checked) window.EV_STORE.setPrefs({tutorialDismissed:true});

          if(i < steps.length-1){ i++; draw(); }
          else overlay.remove();
        }},[ i < steps.length-1 ? "Next" : "Got it" ]);

        const btnSkip = h("button",{class:"btn", onclick:()=>{
          const checked = !!card.querySelector("#tourDont")?.checked;
          if(checked) window.EV_STORE.setPrefs({tutorialDismissed:true});
          overlay.remove();
        }},["Skip"]);

        card.appendChild(h("div",{class:"tourRow"},[
          dont,
          h("div",{class:"row", style:"gap:10px;"},[
            btnSkip,
            btnNext
          ])
        ]));
      }

      draw();
      document.body.appendChild(overlay);

      overlay.addEventListener("click",(e)=>{
        if(e.target === overlay) overlay.remove();
      });
    })();
  }

  async function renderOpen(appEl, params){
    appEl.innerHTML = ""; // ✅ ensures loading card disappears
    // Show splash screen for card opening
    if(window.EV_SPLASH){
      window.EV_SPLASH.show();
    }
    
    const token = params.get("token");
    if(!token){
      if(window.EV_SPLASH) window.EV_SPLASH.markContentReady();
      const c = h("div",{class:"card"},[
        h("div",{class:"inner"},[
          h("div",{class:"h1", html:"Open a link"}),
          h("p",{class:"p", html:"Paste your EchoValentines link to open it."}),
          h("div",{class:"hr"}),
          h("button",{class:"btn primary", onclick:async()=>{ await pasteAndGo(); }},[document.createTextNode("Paste from clipboard")])
        ])
      ]);
      appEl.appendChild(c);
      return;
    }

    let payload;
    try{ payload = window.EV_SHARE.decode(token); }
    catch(e){
      if(window.EV_SPLASH) window.EV_SPLASH.markContentReady();
      appEl.appendChild(h("div",{class:"card"},[h("div",{class:"inner"},[
        h("div",{class:"h1", html:"Invalid link"}),
        h("p",{class:"p", html:"That token doesn't look right."})
      ])]));
      return;
    }

    const packId = payload.pack;
    const cardId = payload.card;
    const pack = S.packIndex[packId];
    if(!pack){
      if(window.EV_SPLASH) window.EV_SPLASH.markContentReady();
      return renderNotFound(appEl);
    }
    const packDir = getPackDir(packId);

    const data = await ensurePackData(packId);
    const card = (data.cards?.cards || []).find(x => String(x.id) === String(cardId));
    if(!card){
      if(window.EV_SPLASH) window.EV_SPLASH.markContentReady();
      return renderNotFound(appEl);
    }

    // Build playlist from tracks
    const packTracks = (data.tracks?.tracks || []);
    if(packTracks.length > 0){
      window.EV_PLAYER.buildPlaylist(packTracks, packDir);
      // Select specific track if specified in payload
      if(payload.track){
        const trackIndex = packTracks.findIndex(t => (t.id || t.title || "") === payload.track);
        if(trackIndex >= 0){
          window.EV_PLAYER.currentIndex = trackIndex;
          window.EV_PLAYER.loadTrack(packTracks[trackIndex], packDir);
        }
      }
    }

    // Use shared card stage renderer
    const cardSrc = `packs/${packDir}/${getCardImage(card)}`;
    
    // Handle stickers - support both old format (single string) and new format (JSON array)
    let stickers = [];
    if(payload.sticker){
      try{
        const parsed = JSON.parse(payload.sticker);
        if(Array.isArray(parsed)){
          stickers = parsed;
        } else {
          // Old format - single sticker string
          stickers = [{src: payload.sticker, x: 0, y: 0, w: 84, h: 84}];
        }
      } catch(e){
        // Old format - single sticker string
        stickers = [{src: payload.sticker, x: 0, y: 0, w: 84, h: 84}];
      }
    }

    // Meta for backward compatibility with pixel-based stickers
    const meta = {
      cw: Number(payload.cw || 0),
      ch: Number(payload.ch || 0)
    };

    const stage = renderCardStage({
      cardSrc,
      stickers,
      meta,
      stageId: "openStage",
      packDir,
      interactive: false
    });

    // Text panel (single source of truth - not stamped on card)
    const panel = h("div",{class:"openTextPanel"},[
      h("div",{class:"line"},[
        h("span",{class:"label"},["To:"]),
        h("span",{},[ payload.to || "—" ])
      ]),
      h("div",{class:"line"},[
        h("span",{class:"label"},["From:"]),
        h("span",{},[ payload.from || "—" ])
      ]),
      payload.msg ? h("div",{class:"msg"},[
        document.createTextNode(payload.msg)
      ]) : null
    ]);

    const replyPack = packId;
    const replyCard = cardId;

    const replyParams = {
      pack: replyPack,
      card: replyCard
    };

    // swap to/from for reply
    const to = payload.from || "";
    const from = payload.to || "";

    window.EV_STORE.setPrefs({ to, from, lastPack: replyPack, lastCard: replyCard });

    // Create envelope with message inside (hidden until opened)
    const envelopeEl = window.EV_ENVELOPE.create(payload.to || "", payload.from || "", payload.msg || "");
    let envelopeOpen = false;

    // Player UI
    const playerEl = packTracks.length > 0 ? h("div",{class:"player"},[
      h("div",{class:"player-controls"},[
        h("button",{class:"player-btn", id:"playerPrev", onclick:()=>window.EV_PLAYER.playPrev(), title:"Previous"},[document.createTextNode("⟨")]),
        h("button",{class:"player-btn", id:"playerPlay", onclick:()=>window.EV_PLAYER.togglePlay(), title:"Play/Pause"},[document.createTextNode("▶")]),
        h("button",{class:"player-btn", id:"playerNext", onclick:()=>window.EV_PLAYER.playNext(), title:"Next"},[document.createTextNode("⟩")]),
        h("div",{class:"player-info"},[
          h("div",{class:"player-title", id:"playerTitle"},[document.createTextNode("No track")]),
          h("div",{class:"player-time", id:"playerTime"},[document.createTextNode("0:00 / 0:00")])
        ]),
        h("input",{type:"range", class:"player-vol", min:"0", max:"100", value:"80", oninput:(e)=>{window.EV_PLAYER.setVolume(e.target.value/100);}, title:"Volume"})
      ])
    ]) : null;

    // Wrap stage in envelope container - card hidden until envelope opens
    // Text panel (single source of truth - not stamped on card)
    const panel = h("div",{class:"openTextPanel"},[
      h("div",{class:"line"},[
        h("span",{class:"label"},["To:"]),
        h("span",{},[ payload.to || "—" ])
      ]),
      h("div",{class:"line"},[
        h("span",{class:"label"},["From:"]),
        h("span",{},[ payload.from || "—" ])
      ]),
      payload.msg ? h("div",{class:"msg"},[
        document.createTextNode(payload.msg)
      ]) : null
    ]);

    const cardContainer = h("div",{class:"cardContainer"},[stage]);
    
    // Create top action bar
    const topActions = h("div",{class:"actionBar"},[
      h("div",{class:"row wrap"},[
        h("button",{class:"btn primary", onclick:()=>location.hash=`#/compose?${qs(replyParams)}`},[
          "Punch one back"
        ]),
        h("button",{class:"btn", onclick:()=>location.hash="#/boxes"},[
          "Browse boxes"
        ])
      ])
    ]);

    const innerEl = h("div",{class:"inner"},[
      h("div",{class:"h1 openTitle", html: esc(pack.name || "EchoValentines")}),
      h("div",{class:"small", style:"margin-bottom:14px;", html:`You have a sealed envelope`}),
      topActions,
      h("div",{class:"hr"}),
      h("div",{class:"envelopeWrapper", style:"position:relative;"},[
        envelopeEl,
        cardContainer
      ]),
      // Text panel - always visible, not on card
      panel,
      // Player UI - always visible when tracks exist
      playerEl,
      h("div",{class:"row", style:"margin-top:14px;"},[
        h("button",{class:"btn primary", id:"openEnvelopeBtn", onclick:()=>{
          if(!envelopeOpen){
            window.EV_ENVELOPE.open(envelopeEl, cardContainer);
            envelopeOpen = true;
            // Text panel is always visible, no need to show/hide elements on card
            // Hide the button after opening
            const btn = document.getElementById("openEnvelopeBtn");
            if(btn) btn.style.display = "none";
          }
        }},[document.createTextNode("Open envelope")])
      ]),
    ]);

    const cardEl = h("div",{class:"card"},[innerEl]);

    appEl.appendChild(cardEl);
    track("open", { pack: packId, card: cardId });
    
    if(window.EV_SPLASH){
      window.EV_SPLASH.markContentReady();
    }
  }

  function renderAbout(appEl){
    appEl.appendChild(h("div",{class:"card"},[
      h("div",{class:"inner"},[
        h("div",{class:"h1", html:"About"}),
        h("p",{class:"p", html:"EchoValentines is a tiny, fast Valentine sharing ritual: pick a box, pick a card, write one line, punch & copy. The receiver opens instantly — no logins, no accounts."}),
        h("div",{class:"hr"}),
        h("div",{class:"p", html:"Privacy: your message travels inside the link. Don’t put anything sensitive in it."}),
        h("div",{style:"height:10px"}),
        h("button",{class:"btn", onclick:()=>location.hash="#/boxes"},[document.createTextNode("Back")])
      ])
    ]));
  }

  function renderNotFound(appEl){
    appEl.appendChild(h("div",{class:"card"},[
      h("div",{class:"inner"},[
        h("div",{class:"h1", html:"Not found"}),
        h("p",{class:"p", html:"That page doesn’t exist."}),
        h("div",{style:"height:10px"}),
        h("button",{class:"btn primary", onclick:()=>location.hash="#/boxes"},[document.createTextNode("Go home")])
      ])
    ]));
  }

  async function pasteAndGo(){
    try{
      const t = await navigator.clipboard.readText();
      if(!t) return toast("Clipboard empty", "bad");
      const m = t.match(/#\/open\?token=([^\s]+)/);
      if(m && m[1]){
        location.hash = `#/open?token=${m[1]}`;
        return;
      }
      toast("No token found in clipboard", "bad");
    } catch(e){
      toast("Clipboard access blocked", "bad");
    }
  }

  async function boot(){
    installUmami();

    // header hooks
    document.getElementById("brandBtn")?.addEventListener("click", ()=>location.hash="#/boxes");
    document.getElementById("pasteLinkBtn")?.addEventListener("click", ()=>location.hash="#/open");
    setStreakPill();

    // load packs
    const manifest = await window.EV_LOADER.loadManifest();
    const items = manifest.packs || [];
    const packs = [];

    for(const it of items){
      try {
        const id = it.id;
        const packPath = it.packPath;
        if(!id || !packPath){
          console.warn("Skipping pack: missing id or packPath", it);
          continue;
        }
        const pack = await window.EV_LOADER.loadPack(packPath);
        // Extract directory from packPath (e.g., "anti_love/pack.json" -> "anti_love")
        const packDir = packPath.split("/")[0];
        packs.push({ id, packPath, pack, packDir });
        S.packIndex[id] = pack;
      } catch(e){
        console.error(`Failed to load pack ${it.id}:`, e);
        // Continue loading other packs instead of crashing
      }
    }

    S.packs = packs;

    // router
    window.addEventListener("hashchange", ()=>render(app()));
    if(!location.hash) location.hash = "#/boxes";
    render(app());
  }

  window.EV_APP = { boot };
})();
