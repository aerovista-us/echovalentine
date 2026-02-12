// Interactive Hero SVG Handler
(function(){
  'use strict';
  
  // Load and inject SVG
  function initHero(){
    const container = document.getElementById('heroSvgContainer');
    if(!container) return;
    
    fetch('assets/img/hero-interactive.svg')
      .then(r => r.text())
      .then(svgText => {
        container.innerHTML = svgText;
        const svg = document.getElementById('heroSvg');
        if(svg) setupInteractivity(svg);
      })
      .catch(e => console.log('Could not load interactive SVG:', e));
  }
  
  function setupInteractivity(svg){
  
  const svgNS = 'http://www.w3.org/2000/svg';
  const particles = document.getElementById('particles');
  const clickableHearts = document.querySelectorAll('.clickable-heart');
  
  // Create particle on click
  function createParticle(x, y, color){
    const circle = document.createElementNS(svgNS, 'circle');
    circle.setAttribute('cx', x);
    circle.setAttribute('cy', y);
    circle.setAttribute('r', '4');
    circle.setAttribute('fill', color);
    circle.setAttribute('opacity', '1');
    
    const animX = Math.random() * 200 - 100;
    const animY = Math.random() * 200 - 100;
    const duration = 1 + Math.random();
    
    const animateX = document.createElementNS(svgNS, 'animateTransform');
    animateX.setAttribute('attributeName', 'transform');
    animateX.setAttribute('type', 'translate');
    animateX.setAttribute('values', `0,0; ${animX},${animY}`);
    animateX.setAttribute('dur', `${duration}s`);
    animateX.setAttribute('fill', 'freeze');
    
    const animateOpacity = document.createElementNS(svgNS, 'animate');
    animateOpacity.setAttribute('attributeName', 'opacity');
    animateOpacity.setAttribute('values', '1;0');
    animateOpacity.setAttribute('dur', `${duration}s`);
    animateOpacity.setAttribute('fill', 'freeze');
    
    const animateScale = document.createElementNS(svgNS, 'animateTransform');
    animateScale.setAttribute('attributeName', 'transform');
    animateScale.setAttribute('type', 'scale');
    animateScale.setAttribute('values', '1;0');
    animateScale.setAttribute('dur', `${duration}s`);
    animateScale.setAttribute('additive', 'sum');
    animateScale.setAttribute('fill', 'freeze');
    
    circle.appendChild(animateX);
    circle.appendChild(animateOpacity);
    circle.appendChild(animateScale);
    particles.appendChild(circle);
    
    setTimeout(() => circle.remove(), duration * 1000);
  }
  
  // Heart click handler
  clickableHearts.forEach(heart => {
    heart.addEventListener('click', function(e){
      const rect = svg.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Create burst of particles
      for(let i = 0; i < 12; i++){
        setTimeout(() => {
          const colors = ['#ff4fd8', '#ff5a9a', '#7cf8ff', '#ff8fe7', '#fff'];
          createParticle(x, y, colors[Math.floor(Math.random() * colors.length)]);
        }, i * 30);
      }
      
      // Pulse animation
      const scaleAnim = document.createElementNS(svgNS, 'animateTransform');
      scaleAnim.setAttribute('attributeName', 'transform');
      scaleAnim.setAttribute('type', 'scale');
      scaleAnim.setAttribute('values', '1;1.5;1');
      scaleAnim.setAttribute('dur', '0.5s');
      scaleAnim.setAttribute('fill', 'freeze');
      this.appendChild(scaleAnim);
      
      setTimeout(() => scaleAnim.remove(), 500);
    });
    
    // Hover effect
    heart.addEventListener('mouseenter', function(){
      this.style.opacity = '1';
      this.style.transition = 'opacity 0.2s';
    });
    
    heart.addEventListener('mouseleave', function(){
      this.style.opacity = '0.7';
    });
  });
  
  // Mouse move parallax effect
  let mouseX = 600, mouseY = 300;
  svg.addEventListener('mousemove', function(e){
    const rect = svg.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = e.clientY - rect.top;
    
    // Move floating hearts slightly based on mouse position
    const hearts = document.querySelectorAll('#floatingHearts .heart');
    hearts.forEach((heart, i) => {
      const dx = (mouseX - 600) * 0.01 * (i % 2 === 0 ? 1 : -1);
      const dy = (mouseY - 300) * 0.01 * (i % 2 === 0 ? 1 : -1);
      heart.style.transform = `translate(${dx}px, ${dy}px)`;
    });
  });
  
  // Create random floating particles
  function createFloatingParticle(){
    const x = Math.random() * 1200;
    const y = 600;
    const size = 2 + Math.random() * 3;
    const speed = 1 + Math.random() * 2;
    const colors = ['#ff4fd8', '#7cf8ff', '#ff8fe7', '#fff'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    const circle = document.createElementNS(svgNS, 'circle');
    circle.setAttribute('cx', x);
    circle.setAttribute('cy', y);
    circle.setAttribute('r', size);
    circle.setAttribute('fill', color);
    circle.setAttribute('opacity', '0.4');
    
    const animateY = document.createElementNS(svgNS, 'animate');
    animateY.setAttribute('attributeName', 'cy');
    animateY.setAttribute('values', `${y};-50`);
    animateY.setAttribute('dur', `${speed * 3}s`);
    animateY.setAttribute('fill', 'freeze');
    
    const animateX = document.createElementNS(svgNS, 'animate');
    animateX.setAttribute('attributeName', 'cx');
    animateX.setAttribute('values', `${x};${x + (Math.random() - 0.5) * 100}`);
    animateX.setAttribute('dur', `${speed * 3}s`);
    animateX.setAttribute('fill', 'freeze');
    
    const animateOpacity = document.createElementNS(svgNS, 'animate');
    animateOpacity.setAttribute('attributeName', 'opacity');
    animateOpacity.setAttribute('values', '0.4;0.8;0');
    animateOpacity.setAttribute('dur', `${speed * 3}s`);
    animateOpacity.setAttribute('fill', 'freeze');
    
    circle.appendChild(animateY);
    circle.appendChild(animateX);
    circle.appendChild(animateOpacity);
    particles.appendChild(circle);
    
    setTimeout(() => circle.remove(), speed * 3000);
  }
  
  // Create floating particles periodically
  setInterval(createFloatingParticle, 2000);
  
    // Initial burst
    setTimeout(() => {
      for(let i = 0; i < 5; i++){
        setTimeout(createFloatingParticle, i * 400);
      }
    }, 500);
  }
  
  // Initialize on DOM ready
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initHero);
  } else {
    initHero();
  }
})();
