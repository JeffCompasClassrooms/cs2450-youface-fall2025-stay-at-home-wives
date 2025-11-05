  (function(){
    const bg = document.querySelector('#overlay');
    if(!bg) return;

    const ripple = document.createElement('div');
    ripple.className = 'ripple';
    bg.appendChild(ripple);

    let timeout;
    function ping(e){
      const rect = bg.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top)  / rect.height) * 100;
      ripple.style.setProperty('--rx', x + '%');
      ripple.style.setProperty('--ry', y + '%');
      ripple.classList.add('show');
      clearTimeout(timeout);
      timeout = setTimeout(()=>ripple.classList.remove('show'), 500);
    }

    bg.addEventListener('mousemove', ping);
    bg.addEventListener('click', ping);
  })();
