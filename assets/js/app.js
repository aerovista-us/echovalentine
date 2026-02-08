// app.js: EchoValentines Viral - single addictive loop
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

  function isSvgPath(path){
    return typeof path === "string" && /\.svg($|\?)/i.test(path);
  }

  function isStickerCard(card){
    const id = String(card?.id || "").toLowerCase();
    const src = String(getCardImage(card) || "").toLowerCase();
    const title = String(card?.title || "").toLowerCase();
    return (
      id.includes("-st-") ||
      id.includes("_st_") ||
      id.includes("sticker") ||
      src.includes("-st-") ||
      src.includes("_st_") ||
      src.includes("sticker") ||
      title.includes("sticker")
    );
  }

  function getLaunchCards(cards){
    return (cards || []).filter(c => !isStickerCard(c));
  }

  function pickEnvelopeSeal(stickers){
    const svgStickers = (stickers || []).filter(s => isSvgPath(s?.src || ""));
    return randPick(svgStickers)?.src || "";
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

  function renderCardStage({ cardSrc, stageId = "", interactive = false }){
    const img = h("img", { src: cardSrc, alt: "Card preview" });
    const stage = h("div", { class: interactive ? "cardStage composeStage" : "cardStage", id: stageId }, [img]);

    // Set stage aspect ratio from real image dimensions
    img.addEventListener("load", () => {
      const w = img.naturalWidth, ht = img.naturalHeight;
      if(w && ht) stage.style.aspectRatio = `${w} / ${ht}`;
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
          h("div",{class:"h1", html:"Loading..."}),
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
      const cardCount = p.pack.cards_count || "";
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
          h("div",{class:"pack-description", html: esc(p.pack.description || p.pack.tagline || "")}),
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
    appEl.innerHTML = ""; // ensures loading card disappears
    if(!packId || !S.packIndex[packId]) return renderNotFound(appEl);
    const pack = S.packIndex[packId];
    const packDir = getPackDir(packId);

    const data = await ensurePackData(packId);
    const cards = getLaunchCards(data.cards?.cards || []);

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

    // Gallery: launch cards only (sticker-cards removed)
    const gallery = h("div",{class:"card", style:"margin-top:14px;"},[
      h("div",{class:"inner"},[
        h("div",{class:"h2", html:"Choose a card"}),
        h("p",{class:"p", html:"Tap any card to personalize it. Keep it short. Keep it punchy."}),
        h("div",{class:"hr"}),
        (function(){
          const g = h("div",{class:"gallery"});
          // Only iterate through launch cards
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
      "You're my favorite glitch in the matrix.",
      "I choose you. Every timeline.",
      "If this is a simulation... keep me in yours.",
      "Your vibe? Unreasonably elite.",
      "I'd fight a bear for you (politely).",
      "You + me = soft chaos, perfect.",
      "Here's a tiny spell: be kind to yourself."
    ];
  }

  async function shuffleAndCompose(preferPackId){
    const packId = preferPackId && S.packIndex[preferPackId] ? preferPackId : randPick(S.packs)?.id;
    if(!packId) return;
    const data = await ensurePackData(packId);
    const card = randPick(getLaunchCards(data.cards?.cards || []));
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
    // open pack page (gallery) - or jump to last card if exists
    const prefs = window.EV_STORE.getPrefs();
    if(prefs.lastPack === packId && prefs.lastCard){
      location.hash = `#/compose?${qs({ pack: packId, card: prefs.lastCard })}`;
    } else {
      location.hash = `#/box/${encodeURIComponent(packId)}`;
    }
  }

  async function renderCompose(appEl, params){
    appEl.innerHTML = "";
    const packId = params.get("pack");
    const cardId = params.get("card");
    if(!packId || !cardId) return renderNotFound(appEl);
    const pack = S.packIndex[packId];
    if(!pack) return renderNotFound(appEl);
    const packDir = getPackDir(packId);

    const data = await ensurePackData(packId);
    const cards = getLaunchCards(data.cards?.cards || []);
    const card = cards.find(x => String(x.id) === String(cardId));
    if(!card) return renderNotFound(appEl);

    window.EV_STORE.setPrefs({ lastPack: packId, lastCard: cardId });

    const prefs = window.EV_STORE.getPrefs();
    const state = {
      to: prefs.to || "",
      from: prefs.from || "",
      msg: params.get("t") || "",
      track: "",
      seal: pickEnvelopeSeal(data.stickers?.stickers || [])
    };
    const sealOptions = (data.stickers?.stickers || [])
      .map(s => String(s?.src || ""))
      .filter(src => isSvgPath(src));
    if(state.seal && !sealOptions.includes(state.seal)) state.seal = "";
    if(!state.seal && sealOptions.length > 0) state.seal = sealOptions[0];

    const cardSrc = `packs/${packDir}/${getCardImage(card)}`;
    const stage = renderCardStage({
      cardSrc,
      stageId: "composeStage",
      interactive: true
    });

    function sync(){
      window.EV_STORE.setPrefs({ to: state.to, from: state.from });
    }

    function sealFullSrc(sealRel){
      return sealRel ? `packs/${packDir}/${sealRel}` : "";
    }
    function sealLabel(sealRel){
      if(!sealRel) return "No seal";
      return sealRel.split("/").pop().replace(/\.[^.]+$/, "").replace(/[_-]+/g, " ");
    }

    async function punchAndCopy(){
      const payload = {
        v: 1,
        pack: packId,
        card: cardId,
        to: (state.to || "").slice(0, 42),
        from: (state.from || "").slice(0, 42),
        msg: (state.msg || "").slice(0, 160),
        track: state.track || "",
        seal: state.seal || "",
        ts: Date.now()
      };
      const token = window.EV_SHARE.encode(payload);
      const baseUrl = (window.EV_CONFIG && window.EV_CONFIG.BASE_URL) || `${location.origin}${location.pathname}`;
      const url = `${baseUrl}#/open?token=${token}`;

      try{
        await navigator.clipboard.writeText(url);
        window.EV_STORE.bumpPunch();
        setStreakPill();
        confettiBurst();
        toast("Punched! Link copied.", "good");
        track("punch_copy", { pack: packId, card: cardId });
      } catch(e){
        toast("Couldn't copy - link shown below.", "bad", 1800);
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

    const tracks = (data.tracks?.tracks || []);
    const trackPicker = tracks.length > 0 ? h("div",{class:"pickerSection"},[
      h("div",{class:"small", html:"Track (optional)"}),
      h("select",{class:"input", id:"trackPickerSelect", onchange:(e)=>{state.track=e.target.value;sync();updateTrackPreview();}},[
        h("option",{value:"", html:"No track"}),
        ...tracks.map(t => h("option",{value:t.id || t.title || "", html:t.title || t.name || "Untitled"}))
      ])
    ]) : null;

    let previewAudio = null;
    let previewBtn = null;
    let previewTitle = null;
    let previewTime = null;

    function fmtTime(sec){
      if(!isFinite(sec) || sec < 0) return "0:00";
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return `${m}:${String(s).padStart(2,"0")}`;
    }

    function stopPreview(){
      if(previewAudio){
        previewAudio.pause();
        previewAudio.currentTime = 0;
      }
      if(previewBtn) previewBtn.textContent = "Preview >";
    }

    function updateTrackPreview(){
      const trackPickerSelect = document.getElementById("trackPickerSelect");
      if(!trackPickerSelect) return;
      const trackId = trackPickerSelect.value || "";
      if(!trackId){
        stopPreview();
        if(previewTitle) previewTitle.textContent = "No track selected";
        if(previewTime) previewTime.textContent = "";
        return;
      }

      const t = (tracks || []).find(x => (x.id || x.title || "") === trackId) || null;
      if(!t){
        stopPreview();
        if(previewTitle) previewTitle.textContent = "Track not found";
        if(previewTime) previewTime.textContent = "";
        return;
      }

      const src = t.src || t.url || t.file || "";
      if(!src){
        stopPreview();
        if(previewTitle) previewTitle.textContent = t.title || t.name || trackId;
        if(previewTime) previewTime.textContent = "No audio file";
        return;
      }

      const fullSrc = src.startsWith("http") ? src : `packs/${packDir}/${src}`;

      if(!previewAudio) previewAudio = new Audio();
      if(previewAudio.src !== fullSrc){
        previewAudio.src = fullSrc;
        previewAudio.preload = "metadata";
      }

      if(previewTitle) previewTitle.textContent = t.title || t.name || trackId;
      const tick = () => {
        if(previewTime){
          previewTime.textContent = `${fmtTime(previewAudio.currentTime)} / ${fmtTime(previewAudio.duration)}`;
        }
      };
      previewAudio.ontimeupdate = tick;
      previewAudio.onloadedmetadata = tick;
      previewAudio.onended = () => { if(previewBtn) previewBtn.textContent = "Preview >"; };
    }

    const trackPreviewEl = trackPicker ? (function(){
      previewBtn = h("button",{class:"btn", type:"button", onclick: async ()=>{
        if(!previewAudio) updateTrackPreview();
        if(!previewAudio || !previewAudio.src) return;
        if(previewAudio.paused){
          try{
            await previewAudio.play();
            previewBtn.textContent = "Preview ||";
          } catch(e){
            toast("Tap again to allow audio", "bad");
          }
        } else {
          previewAudio.pause();
          previewBtn.textContent = "Preview >";
        }
      }},["Preview >"]);

      previewTitle = h("div",{class:"small", style:"font-weight:700; margin-top:8px;"},[""]);
      previewTime  = h("div",{class:"small", style:"opacity:.8"},[""]);

      window.addEventListener("hashchange", stopPreview, { once:true });

      return h("div",{class:"player", style:"margin-top:10px;"},[
        h("div",{class:"row"},[previewBtn]),
        previewTitle,
        previewTime
      ]);
    })() : null;

    let sealPreviewImg = null;
    let sealNameEl = null;
    function updateSealPicker(){
      if(sealPreviewImg){
        if(state.seal){
          sealPreviewImg.src = sealFullSrc(state.seal);
          sealPreviewImg.style.display = "";
        } else {
          sealPreviewImg.removeAttribute("src");
          sealPreviewImg.style.display = "none";
        }
      }
      if(sealNameEl){
        sealNameEl.textContent = sealLabel(state.seal);
      }
    }
    function cycleSeal(step){
      if(sealOptions.length === 0) return;
      const current = sealOptions.indexOf(state.seal);
      const start = current >= 0 ? current : 0;
      const next = (start + step + sealOptions.length) % sealOptions.length;
      state.seal = sealOptions[next];
      updateSealPicker();
      sync();
    }
    function randomSealChoice(){
      if(sealOptions.length === 0) return;
      state.seal = randPick(sealOptions) || sealOptions[0];
      updateSealPicker();
      sync();
    }
    function clearSealChoice(){
      state.seal = "";
      updateSealPicker();
      sync();
    }

    const sealPicker = (function(){
      const section = h("div",{class:"pickerSection"},[
        h("div",{class:"small", html:"Envelope seal (optional)"})
      ]);
      if(sealOptions.length === 0){
        section.appendChild(h("div",{class:"small", style:"margin-top:8px;"},[
          document.createTextNode("No SVG seals available in this pack.")
        ]));
        return section;
      }

      sealPreviewImg = h("img",{class:"sealPreviewImg", alt:"Selected envelope seal", loading:"lazy", decoding:"async"});
      sealNameEl = h("div",{class:"small", style:"font-weight:700;"},[""]);

      const row = h("div",{class:"sealPicker"},[
        h("div",{class:"sealPreviewCard"},[sealPreviewImg]),
        h("div",{style:"flex:1;"},[
          sealNameEl,
          h("div",{class:"row", style:"margin-top:8px;"},[
            h("button",{class:"btn", type:"button", onclick:()=>cycleSeal(-1)},["Prev"]),
            h("button",{class:"btn", type:"button", onclick:randomSealChoice},["Random"]),
            h("button",{class:"btn", type:"button", onclick:()=>cycleSeal(1)},["Next"]),
            h("button",{class:"btn", type:"button", onclick:clearSealChoice},["None"])
          ])
        ])
      ]);
      section.appendChild(row);
      return section;
    })();

    const actionBar = h("div",{class:"actionBar"},[
      h("div",{class:"row wrap"},[
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
        h("textarea",{class:"input", placeholder:"Keep it short...", value: state.msg || "", oninput:(e)=>{state.msg=e.target.value;sync();}}),
        trackPicker ? h("div",{style:"height:10px"}) : null,
        trackPicker,
        trackPreviewEl,
        h("div",{style:"height:10px"}),
        sealPicker
      ])
    ]);

    const right = h("section",{class:"card"},[
      h("div",{class:"inner"},[
        h("div",{class:"h2", html:"Preview"}),
        h("p",{class:"p", html:"Card art preview. Message appears in the text panel on open."}),
        h("div",{class:"hr"}),
        stage,
        h("div",{style:"height:10px"}),
        h("div",{class:"small", html:`Pack: <b>${esc(pack.name || packId)}</b> - Card: <b>${esc(card.title || cardId)}</b>`})
      ])
    ]);

    appEl.appendChild(h("div",{class:"grid two"},[left, right]));
    const trackPickerSelect = document.getElementById("trackPickerSelect");
    if(state.track && trackPickerSelect){
      trackPickerSelect.value = state.track;
      updateTrackPreview();
    }
    updateSealPicker();
    sync();

    (function maybeTutorial(){
      const prefs = window.EV_STORE.getPrefs();
      if(prefs.tutorialDismissed) return;

      const steps = [
        {t:"Write it", b:"Fill To/From and a short message."},
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
    appEl.innerHTML = "";
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

    try {
      const data = await ensurePackData(packId);
      const card = getLaunchCards(data.cards?.cards || []).find(x => String(x.id) === String(cardId));
      if(!card){
        if(window.EV_SPLASH) window.EV_SPLASH.markContentReady();
        return renderNotFound(appEl);
      }

      const packTracks = (data.tracks?.tracks || []);
      if(packTracks.length > 0){
        window.EV_PLAYER.buildPlaylist(packTracks, packDir);
        if(payload.track){
          const trackIndex = packTracks.findIndex(t => (t.id || t.title || "") === payload.track);
          if(trackIndex >= 0){
            window.EV_PLAYER.currentIndex = trackIndex;
            window.EV_PLAYER.loadTrack(packTracks[trackIndex], packDir);
          }
        }
      }

      const cardSrc = `packs/${packDir}/${getCardImage(card)}`;
      const stage = renderCardStage({
        cardSrc,
        stageId: "openStage",
        interactive: false
      });

      const panel = h("div",{class:"openTextPanel"},[
        h("div",{class:"line"},[
          h("span",{class:"label"},["To:"]),
          h("span",{},[ payload.to || "-" ])
        ]),
        h("div",{class:"line"},[
          h("span",{class:"label"},["From:"]),
          h("span",{},[ payload.from || "-" ])
        ]),
        payload.msg ? h("div",{class:"msg"},[
          document.createTextNode(payload.msg)
        ]) : null
      ]);

      const replyParams = {
        pack: packId,
        card: cardId
      };

      const to = payload.from || "";
      const from = payload.to || "";
      window.EV_STORE.setPrefs({ to, from, lastPack: packId, lastCard: cardId });

      const sealSrc = isSvgPath(payload.seal || "")
        ? ((payload.seal || "").startsWith("http") ? payload.seal : `packs/${packDir}/${payload.seal}`)
        : "";
      const envelopeEl = window.EV_ENVELOPE.create(payload.to || "", payload.from || "", payload.msg || "", sealSrc);
      let envelopeOpen = false;

      const playerEl = packTracks.length > 0 ? h("div",{class:"player"},[
        h("div",{class:"player-controls"},[
          h("button",{class:"player-btn", id:"playerPrev", onclick:()=>window.EV_PLAYER.playPrev(), title:"Previous"},[document.createTextNode("<")]),
          h("button",{class:"player-btn", id:"playerPlay", onclick:()=>window.EV_PLAYER.togglePlay(), title:"Play/Pause"},[document.createTextNode("Play")]),
          h("button",{class:"player-btn", id:"playerNext", onclick:()=>window.EV_PLAYER.playNext(), title:"Next"},[document.createTextNode(">")]),
          h("div",{class:"player-info"},[
            h("div",{class:"player-title", id:"playerTitle"},[document.createTextNode("No track")]),
            h("div",{class:"player-time", id:"playerTime"},[document.createTextNode("0:00 / 0:00")])
          ]),
          h("input",{type:"range", class:"player-vol", min:"0", max:"100", value:"80", oninput:(e)=>{window.EV_PLAYER.setVolume(e.target.value/100);}, title:"Volume"})
        ])
      ]) : null;

      const cardContainer = h("div",{class:"cardContainer"},[stage]);

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
        h("div",{class:"small", style:"margin-bottom:14px;", html:"You have a sealed envelope"}),
        topActions,
        h("div",{class:"hr"}),
        h("div",{class:"envelopeWrapper", style:"position:relative;"},[
          envelopeEl,
          cardContainer
        ]),
        panel,
        playerEl,
        h("div",{class:"row", style:"margin-top:14px;"},[
          h("button",{class:"btn primary", id:"openEnvelopeBtn", onclick:()=>{
            if(!envelopeOpen){
              window.EV_ENVELOPE.open(envelopeEl, cardContainer);
              envelopeOpen = true;
              const btn = document.getElementById("openEnvelopeBtn");
              if(btn) btn.style.display = "none";
            }
          }},[document.createTextNode("Open envelope")])
        ]),
      ]);

      const cardEl = h("div",{class:"card"},[innerEl]);

      appEl.appendChild(cardEl);
      track("open", { pack: packId, card: cardId });
    } catch(err) {
      console.error("Error rendering open page:", err);
      appEl.appendChild(h("div",{class:"card"},[h("div",{class:"inner"},[
        h("div",{class:"h1", html:"Error loading card"}),
        h("p",{class:"p", html: esc(String(err && err.message ? err.message : err))})
      ])]));
    } finally {
      if(window.EV_SPLASH){
        window.EV_SPLASH.markContentReady();
      }
    }
  }

  function renderAbout(appEl){
    appEl.appendChild(h("div",{class:"card"},[
      h("div",{class:"inner"},[
        h("div",{class:"h1", html:"About"}),
        h("p",{class:"p", html:"EchoValentines is a tiny, fast Valentine sharing ritual: pick a box, pick a card, write one line, punch & copy. The receiver opens instantly - no logins, no accounts."}),
        h("div",{class:"hr"}),
        h("div",{class:"p", html:"Privacy: your message travels inside the link. Don't put anything sensitive in it."}),
        h("div",{style:"height:10px"}),
        h("button",{class:"btn", onclick:()=>location.hash="#/boxes"},[document.createTextNode("Back")])
      ])
    ]));
  }

  function renderNotFound(appEl){
    appEl.appendChild(h("div",{class:"card"},[
      h("div",{class:"inner"},[
        h("div",{class:"h1", html:"Not found"}),
        h("p",{class:"p", html:"That page doesn't exist."}),
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
