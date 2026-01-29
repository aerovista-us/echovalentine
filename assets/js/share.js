// share.js: encode/decode share payload into URL-safe base64.
(function(){
  function toB64Url(str){
    const bytes = new TextEncoder().encode(str);
    let bin = "";
    bytes.forEach(b => bin += String.fromCharCode(b));
    const b64 = btoa(bin).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
    return b64;
  }
  function fromB64Url(b64url){
    const b64 = b64url.replace(/-/g,'+').replace(/_/g,'/');
    const pad = b64.length % 4 ? '='.repeat(4 - (b64.length % 4)) : '';
    const bin = atob(b64 + pad);
    const bytes = new Uint8Array([...bin].map(ch => ch.charCodeAt(0)));
    return new TextDecoder().decode(bytes);
  }

  window.EV_SHARE = {
    encode(payload){ return toB64Url(JSON.stringify(payload)); },
    decode(token){
      const s = fromB64Url(token);
      return JSON.parse(s);
    }
  };
})();
