// envelope.js: Envelope animation and tear sound
(function(){
  function playTear(){
    try{
      const AC = window.AudioContext || window.webkitAudioContext;
      const ctx = new AC();
      const dur = 0.12;
      const sr = ctx.sampleRate;
      const buffer = ctx.createBuffer(1, Math.floor(sr*dur), sr);
      const data = buffer.getChannelData(0);
      for(let i=0;i<data.length;i++){
        const t = i/data.length;
        const env = (1-t);
        data[i] = (Math.random()*2-1) * env * 0.6;
      }
      const src = ctx.createBufferSource();
      src.buffer = buffer;
      const filter = ctx.createBiquadFilter();
      filter.type = 'highpass';
      filter.frequency.value = 800;
      const gain = ctx.createGain();
      gain.gain.value = 0.35;
      src.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      src.start();
      setTimeout(()=>ctx.close(), 250);
    }catch(e){}
  }

  function createEnvelope(to, from, message){
    const env = document.createElement("div");
    env.className = "envelope";
    // Message only shown on card, not in envelope
    const messageHtml = '';
    // Animated To/From on envelope
    const toFromHtml = (to || from) ? `
      <div class="envelope-tofrom">
        <div class="envelope-tofrom-to">${to ? `To: <b>${escapeHtml(to)}</b>` : ''}</div>
        <div class="envelope-tofrom-from">${from ? `From: <b>${escapeHtml(from)}</b>` : ''}</div>
      </div>
    ` : '';
    const badgeText = to ? `To: ${escapeHtml(to)}` : 'Sealed envelope';
    env.innerHTML = `
      <div class="envelope-shell">
        <div class="envelope-back"></div>
        <div class="envelope-paper">
          <div class="envelope-badge">${badgeText}</div>
          ${toFromHtml}
          ${messageHtml}
        </div>
        <div class="envelope-flap"></div>
        <div class="envelope-front">
          ${toFromHtml}
        </div>
      </div>
    `;
    return env;
  }
  
  function escapeHtml(text){
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function openEnvelope(envEl, cardContainerEl){
    if(!envEl) return;
    envEl.classList.add("envelope-open");
    if(cardContainerEl) cardContainerEl.classList.add("revealed");
    playTear();
  }

  function closeEnvelope(envEl){
    if(!envEl) return;
    envEl.classList.remove("envelope-open");
  }

  window.EV_ENVELOPE = {
    create: createEnvelope,
    open: openEnvelope,
    close: closeEnvelope,
    playTear
  };
})();
