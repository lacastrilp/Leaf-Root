(function(){
  function renderStars(container, rating){
    const stars = container.querySelectorAll('.star');
    for(let i=1;i<=5;i++){
      const icon = stars[i-1];
      icon.classList.remove('bi-star-fill','bi-star-half','bi-star');
      if (rating >= i){
        icon.classList.add('bi-star-fill');
      } else if (rating >= i - 0.5){
        icon.classList.add('bi-star-half');
      } else {
        icon.classList.add('bi-star');
      }
    }
  }

  function setup(container){
    if (!container) return;
    // Build stars
    container.innerHTML='';
    for(let i=1;i<=5;i++){
      const s=document.createElement('i');
      s.className='bi star bi-star';
      s.dataset.index=String(i);
      container.appendChild(s);
    }
    const hidden = document.getElementById('ratingInput');
    let current = parseFloat(hidden && hidden.value || '0') || 0;
    renderStars(container, current);

    // Desktop hover preview
    container.addEventListener('mousemove', (e)=>{
      const target = e.target.closest('.star');
      if(!target) return;
      const rect = target.getBoundingClientRect();
      const half = (e.clientX - rect.left) < rect.width/2 ? 0.5 : 1.0;
      const idx = parseInt(target.dataset.index,10);
      const temp = idx - (half===0.5?0.5:0);
      renderStars(container, temp);
    });
    container.addEventListener('mouseleave', ()=>{
      renderStars(container, current);
    });
    container.addEventListener('click', (e)=>{
      const target = e.target.closest('.star');
      if(!target) return;
      const rect = target.getBoundingClientRect();
      const half = (e.clientX - rect.left) < rect.width/2 ? 0.5 : 1.0;
      const idx = parseInt(target.dataset.index,10);
      current = idx - (half===0.5?0.5:0);
      const hidden = document.getElementById('ratingInput');
      if (hidden) hidden.value = current.toFixed(1);
      renderStars(container, current);
    });

    // Mobile (touch) support: preview on move, set value on end
    const touchPreview = (clientX, clientY) => {
      const el = document.elementFromPoint(clientX, clientY);
      if(!el) return;
      const target = el.closest && el.closest('.star');
      if(!target) return;
      const rect = target.getBoundingClientRect();
      const half = (clientX - rect.left) < rect.width/2 ? 0.5 : 1.0;
      const idx = parseInt(target.dataset.index,10);
      const temp = idx - (half===0.5?0.5:0);
      renderStars(container, temp);
      return { idx, half };
    };

    container.addEventListener('touchstart', (e)=>{
      if (!e.touches || !e.touches[0]) return;
      const t = e.touches[0];
      touchPreview(t.clientX, t.clientY);
    }, { passive: true });

    container.addEventListener('touchmove', (e)=>{
      if (!e.touches || !e.touches[0]) return;
      const t = e.touches[0];
      touchPreview(t.clientX, t.clientY);
    }, { passive: true });

    container.addEventListener('touchend', (e)=>{
      if (!e.changedTouches || !e.changedTouches[0]) return;
      const t = e.changedTouches[0];
      const res = touchPreview(t.clientX, t.clientY);
      if (res) {
        const { idx, half } = res;
        current = idx - (half===0.5?0.5:0);
        const hidden = document.getElementById('ratingInput');
        if (hidden) hidden.value = current.toFixed(1);
        renderStars(container, current);
      }
    }, { passive: true });
  }

  window.initStarRating = function(){
    const el = document.getElementById('starRating');
    if (el) setup(el);
  };

  document.addEventListener('DOMContentLoaded', function(){
    if (document.getElementById('starRating')) window.initStarRating();
  });
})();
