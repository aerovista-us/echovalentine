// player.js: Simple audio player for pack tracks
(function(){
  let currentAudio = null;
  let currentTrack = null;
  let playlist = [];
  let currentIndex = -1;
  let isPlaying = false;
  let volume = 0.8;
  let updateInterval = null;

  function formatTime(seconds){
    if(!seconds || isNaN(seconds)) return "0:00";
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  }

  function stop(){
    if(currentAudio){
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
    if(updateInterval){
      clearInterval(updateInterval);
      updateInterval = null;
    }
    currentTrack = null;
    currentIndex = -1;
    isPlaying = false;
    updateUI();
  }

  function updateUI(){
    const playBtn = document.getElementById("playerPlay");
    const titleEl = document.getElementById("playerTitle");
    const timeEl = document.getElementById("playerTime");
    
    if(playBtn){
      playBtn.textContent = isPlaying ? "⏸" : "▶";
      playBtn.disabled = !currentTrack;
    }
    if(titleEl){
      titleEl.textContent = currentTrack?.title || currentTrack?.name || "No track";
    }
    if(timeEl && currentAudio){
      timeEl.textContent = `${formatTime(currentAudio.currentTime)} / ${formatTime(currentAudio.duration)}`;
    } else if(timeEl){
      timeEl.textContent = "0:00 / 0:00";
    }
  }

  function loadTrack(track, packDir){
    if(!track || !track.src) return;
    
    // Stop previous track and cleanup
    if(currentAudio){
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
    if(updateInterval){
      clearInterval(updateInterval);
      updateInterval = null;
    }
    
    const audio = new Audio(`packs/${packDir}/${track.src}`);
    audio.volume = volume;
    audio.addEventListener("loadedmetadata", ()=>updateUI());
    audio.addEventListener("timeupdate", ()=>updateUI());
    audio.addEventListener("ended", ()=>{
      if(currentIndex < playlist.length - 1){
        playNext();
      } else {
        stop();
      }
    });
    audio.addEventListener("error", (e)=>{
      console.warn("Audio load error:", e);
      updateUI();
    });
    
    currentAudio = audio;
    currentTrack = track;
    isPlaying = false; // Reset playing state when loading new track
    updateUI();
    
    // Update UI periodically
    updateInterval = setInterval(()=>{
      if(!currentAudio || currentAudio !== audio){
        clearInterval(updateInterval);
        updateInterval = null;
        return;
      }
      updateUI();
    }, 500);
  }

  function play(){
    if(!currentAudio || !currentTrack) return;
    currentAudio.play().then(()=>{
      isPlaying = true;
      updateUI();
    }).catch(e=>{
      console.warn("Playback failed:", e);
    });
  }

  function pause(){
    if(currentAudio){
      currentAudio.pause();
      isPlaying = false;
      updateUI();
    }
  }

  function togglePlay(){
    if(isPlaying) pause();
    else play();
  }

  function playNext(){
    if(playlist.length === 0) return;
    const wasPlaying = isPlaying;
    currentIndex = (currentIndex + 1) % playlist.length;
    const track = playlist[currentIndex];
    if(track){
      loadTrack(track.track, track.packDir);
      if(wasPlaying) setTimeout(()=>play(), 100);
    }
  }

  function playPrev(){
    if(playlist.length === 0) return;
    const wasPlaying = isPlaying;
    currentIndex = currentIndex <= 0 ? playlist.length - 1 : currentIndex - 1;
    const track = playlist[currentIndex];
    if(track){
      loadTrack(track.track, track.packDir);
      if(wasPlaying) setTimeout(()=>play(), 100);
    }
  }

  function setVolume(val){
    volume = Math.max(0, Math.min(1, val));
    if(currentAudio) currentAudio.volume = volume;
  }

  function buildPlaylist(tracks, packDir){
    playlist = [];
    if(!tracks || !Array.isArray(tracks)) return;
    
    tracks.forEach(track => {
      if(track.src && track.src.trim()){
        playlist.push({ track, packDir });
      }
    });
    
    if(playlist.length > 0){
      currentIndex = 0;
      loadTrack(playlist[0].track, playlist[0].packDir);
    } else {
      stop();
    }
  }

  window.EV_PLAYER = {
    buildPlaylist,
    play,
    pause,
    togglePlay,
    playNext,
    playPrev,
    stop,
    setVolume,
    loadTrack,
    getCurrentTrack: ()=>currentTrack,
    isPlaying: ()=>isPlaying,
    get playlist(){ return playlist; },
    set playlist(val){ playlist = val; },
    get currentIndex(){ return currentIndex; },
    set currentIndex(val){ currentIndex = val; }
  };
})();
