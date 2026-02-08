// dragdrop.js: Drag, drop, and resize utilities for stickers
(function(){
  function attachDrag(el, handle){
    let startX = 0, startY = 0, origX = 0, origY = 0, dragging = false;
    
    const onMove = (e) => {
      if(!dragging) return;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      el.style.left = (origX + dx) + 'px';
      el.style.top = (origY + dy) + 'px';
    };
    
    const onUp = () => {
      if(!dragging) return;
      dragging = false;
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      if(el.releasePointerCapture) el.releasePointerCapture(1);
    };
    
    handle.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      dragging = true;
      bringToFront(el);
      startX = e.clientX;
      startY = e.clientY;
      origX = parseFloat(el.style.left || '0');
      origY = parseFloat(el.style.top || '0');
      if(el.setPointerCapture) el.setPointerCapture(1);
      window.addEventListener('pointermove', onMove);
      window.addEventListener('pointerup', onUp);
    });
  }
  
  function attachResize(el, resizer){
    let startX = 0, startY = 0, origW = 0, origH = 0, resizing = false;
    
    const onMove = (e) => {
      if(!resizing) return;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      const minSize = 40;
      el.style.width = Math.max(minSize, origW + dx) + 'px';
      el.style.height = Math.max(minSize, origH + dy) + 'px';
    };
    
    const onUp = () => {
      if(!resizing) return;
      resizing = false;
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
    };
    
    resizer.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      resizing = true;
      startX = e.clientX;
      startY = e.clientY;
      origW = el.getBoundingClientRect().width;
      origH = el.getBoundingClientRect().height;
      window.addEventListener('pointermove', onMove);
      window.addEventListener('pointerup', onUp);
    });
  }
  
  function bringToFront(el){
    const parent = el.parentElement;
    if(!parent) return;
    const siblings = Array.from(parent.children);
    const maxZ = Math.max(...siblings.map(s => parseFloat(s.style.zIndex) || 0));
    el.style.zIndex = String(maxZ + 1);
  }
  
  function enableDropZone(container, onDrop){
    container.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.stopPropagation();
      container.classList.add('drop-active');
    });
    
    container.addEventListener('dragleave', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if(!container.contains(e.relatedTarget)){
        container.classList.remove('drop-active');
      }
    });
    
    container.addEventListener('drop', (e) => {
      e.preventDefault();
      e.stopPropagation();
      container.classList.remove('drop-active');
      const data = e.dataTransfer.getData('application/json');
      if(data && onDrop){
        try{
          const item = JSON.parse(data);
          onDrop(item, e);
        } catch(err){
          console.warn('Invalid drop data:', err);
        }
      }
    });
  }
  
  window.EV_DRAGDROP = {
    attachDrag,
    attachResize,
    bringToFront,
    enableDropZone
  };
})();
