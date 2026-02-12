# Quick Fixes Guide - Critical Issues

## 🔴 IMMEDIATE FIXES REQUIRED

### 1. Fix XSS in envelope.js
**File:** `assets/js/envelope.js:43`

**Current (VULNERABLE):**
```javascript
env.innerHTML = `
  <div class="envelope-message">
    <div class="envelope-message-to"><b>${escapeHtml(to || "To")}</b></div>
    <div class="envelope-message-text">${escapeHtml(message)}</div>
    <div class="envelope-message-from">From: <b>${escapeHtml(from || "")}</b></div>
  </div>
`;
```

**Fixed:**
```javascript
const messageDiv = document.createElement("div");
messageDiv.className = "envelope-message";

const toDiv = document.createElement("div");
toDiv.className = "envelope-message-to";
const toBold = document.createElement("b");
toBold.textContent = to || "To";
toDiv.appendChild(toBold);

const textDiv = document.createElement("div");
textDiv.className = "envelope-message-text";
textDiv.textContent = message || "";

const fromDiv = document.createElement("div");
fromDiv.className = "envelope-message-from";
fromDiv.textContent = "From: ";
const fromBold = document.createElement("b");
fromBold.textContent = from || "";
fromDiv.appendChild(fromBold);

messageDiv.appendChild(toDiv);
messageDiv.appendChild(textDiv);
messageDiv.appendChild(fromDiv);
env.appendChild(messageDiv);
```

---

### 2. Fix XSS in app.js (html attribute)
**File:** `assets/js/app.js:500-501`

**Current (VULNERABLE):**
```javascript
h("div",{html:`To: <b>${esc(payload.to || "")}</b>`}),
h("div",{html:`From: <b>${esc(payload.from || "")}</b>`})
```

**Fixed:**
```javascript
(function(){
  const toDiv = document.createElement("div");
  toDiv.textContent = "To: ";
  const toBold = document.createElement("b");
  toBold.textContent = payload.to || "";
  toDiv.appendChild(toBold);
  
  const fromDiv = document.createElement("div");
  fromDiv.textContent = "From: ";
  const fromBold = document.createElement("b");
  fromBold.textContent = payload.from || "";
  fromDiv.appendChild(fromBold);
  
  return h("div",{},[toDiv, fromDiv]);
})()
```

**OR** Update `ui.js` helper to use `textContent`:
```javascript
// ui.js:9 - Change html attribute handling
else if(k === "html") {
  // SECURITY: Use textContent for safety, or sanitize
  el.textContent = v; // Simple fix, but loses HTML formatting
  // OR use DOMPurify: el.innerHTML = DOMPurify.sanitize(v);
}
```

---

### 3. Add Path Traversal Protection
**File:** `assets/js/loader.js:10`

**Current (VULNERABLE):**
```javascript
async function loadPack(packPath){ 
  return await j(`packs/${packPath}`); 
}
```

**Fixed:**
```javascript
async function loadPack(packPath){
  // Validate packPath to prevent path traversal
  if(!packPath || typeof packPath !== 'string') {
    throw new Error('Invalid packPath');
  }
  // Remove any path traversal attempts
  const sanitized = packPath.replace(/\.\./g, '').replace(/^\/+/, '');
  // Only allow alphanumeric, underscore, hyphen, and forward slash
  if(!/^[a-zA-Z0-9_\-/]+\.json$/.test(sanitized)) {
    throw new Error('Invalid packPath format');
  }
  return await j(`packs/${sanitized}`);
}
```

**Also fix in app.js:669:**
```javascript
// Current:
const packDir = packPath.split("/")[0];

// Fixed:
const packDir = packPath.split("/")[0];
// Validate packDir
if(!packDir || packDir.includes('..') || packDir.includes('/')) {
  console.error('Invalid packDir:', packDir);
  continue;
}
```

---

### 4. Add JSON Parse Error Handling
**File:** `assets/js/share.js:20-23`

**Current:**
```javascript
decode(token){
  const s = fromB64Url(token);
  return JSON.parse(s);
}
```

**Fixed:**
```javascript
decode(token){
  try {
    const s = fromB64Url(token);
    return JSON.parse(s);
  } catch(e) {
    throw new Error('Invalid token format');
  }
}
```

**Also fix in app.js:509:**
```javascript
// Current:
const parsed = JSON.parse(payload.sticker);

// Fixed:
let parsed;
try {
  parsed = JSON.parse(payload.sticker);
} catch(e) {
  // Fallback to old format
  parsed = payload.sticker;
}
```

---

### 5. Clean Up Event Listeners
**File:** `assets/js/app.js:681`

**Current:**
```javascript
window.addEventListener("hashchange", ()=>render(app()));
```

**Fixed:**
```javascript
let hashChangeHandler;
function boot(){
  // ... existing code ...
  
  // Store handler reference
  hashChangeHandler = () => render(app());
  window.addEventListener("hashchange", hashChangeHandler);
  
  // ... rest of boot ...
}

// Add cleanup function
function cleanup(){
  if(hashChangeHandler) {
    window.removeEventListener("hashchange", hashChangeHandler);
  }
}
```

**File:** `assets/js/player.js:53-97`

**Current:**
```javascript
function loadTrack(track, packDir){
  if(currentAudio){
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio = null;
  }
  const audio = new Audio(`packs/${packDir}/${track.src}`);
  audio.addEventListener("loadedmetadata", ()=>updateUI());
  // ... more listeners
}
```

**Fixed:**
```javascript
let audioListeners = [];

function loadTrack(track, packDir){
  // Clean up previous audio
  if(currentAudio){
    // Remove all event listeners
    audioListeners.forEach(({element, event, handler}) => {
      element.removeEventListener(event, handler);
    });
    audioListeners = [];
    
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio = null;
  }
  
  const audio = new Audio(`packs/${packDir}/${track.src}`);
  
  // Store listener references
  const handlers = [
    {element: audio, event: "loadedmetadata", handler: ()=>updateUI()},
    {element: audio, event: "timeupdate", handler: ()=>updateUI()},
    {element: audio, event: "ended", handler: ()=>{
      if(currentIndex < playlist.length - 1){
        playNext();
      } else {
        stop();
      }
    }},
    {element: audio, event: "error", handler: (e)=>{
      console.warn("Audio load error:", e);
      updateUI();
    }}
  ];
  
  handlers.forEach(({element, event, handler}) => {
    element.addEventListener(event, handler);
    audioListeners.push({element, event, handler});
  });
  
  currentAudio = audio;
  // ... rest of function
}
```

---

### 6. Fix Race Condition in Pack Loading
**File:** `assets/js/app.js:40-47`

**Current:**
```javascript
async function ensurePackData(packId){
  if(S.dataCache[packId]) return S.dataCache[packId];
  const pack = S.packIndex[packId];
  const packDir = getPackDir(packId);
  const data = await window.EV_LOADER.loadPackData(packDir, pack);
  S.dataCache[packId] = data;
  return data;
}
```

**Fixed:**
```javascript
const loadingPromises = {}; // Track in-flight requests

async function ensurePackData(packId){
  if(S.dataCache[packId]) return S.dataCache[packId];
  
  // If already loading, return the existing promise
  if(loadingPromises[packId]) {
    return loadingPromises[packId];
  }
  
  const pack = S.packIndex[packId];
  const packDir = getPackDir(packId);
  
  // Create and cache the promise
  const promise = window.EV_LOADER.loadPackData(packDir, pack)
    .then(data => {
      S.dataCache[packId] = data;
      delete loadingPromises[packId];
      return data;
    })
    .catch(err => {
      delete loadingPromises[packId];
      throw err;
    });
  
  loadingPromises[packId] = promise;
  return promise;
}
```

---

### 7. Fix Logic Error in Card Count
**File:** `assets/js/app.js:89`

**Current:**
```javascript
const cardCount = p.pack.cards_count || (p.pack.data?.cards ? "" : "");
```

**Fixed:**
```javascript
const cardCount = p.pack.cards_count || 
  (data?.cards?.cards?.length ? data.cards.cards.length : "");
```

**OR** load card count from pack data:
```javascript
// After loading pack data
const packData = await ensurePackData(p.id);
const cardCount = packData?.cards?.cards?.length || p.pack.cards_count || "";
```

---

## 📋 Testing Checklist

After applying fixes, test:

- [ ] XSS: Try injecting `<script>alert('XSS')</script>` in to/from/message fields
- [ ] Path traversal: Try `../../etc/passwd` in packPath
- [ ] Memory: Navigate between routes 50+ times, check memory usage
- [ ] Race conditions: Rapidly click shuffle button multiple times
- [ ] Error handling: Provide invalid token, malformed JSON
- [ ] Audio cleanup: Change tracks rapidly, verify no memory leaks

---

## 🚀 Priority Order

1. **Fix XSS vulnerabilities** (Security - Critical)
2. **Add path traversal protection** (Security - Critical)
3. **Clean up event listeners** (Memory - High)
4. **Fix race conditions** (Reliability - Medium)
5. **Add error handling** (Reliability - Medium)
6. **Fix logic errors** (Code Quality - Low)
