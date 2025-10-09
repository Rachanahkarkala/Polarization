def get_canvas_flame():
    return """
    <canvas id="flame-canvas"></canvas>
    <style>
        /* full-viewport canvas that does not block interactions */
        #flame-canvas {
            position: fixed;
            inset: 0; /* top:0; right:0; bottom:0; left:0 */
            width: 100vw;
            height: 100vh;
            z-index: 10000;
            pointer-events: none;
            background: transparent;
        }
    </style>
    <script>
    (function(){
      const canvas = document.getElementById('flame-canvas');
      const ctx = canvas.getContext('2d', { alpha: true });

      function resize() {
        const dpr = window.devicePixelRatio || 1;
        canvas.width = window.innerWidth * dpr;
        canvas.height = window.innerHeight * dpr;
        canvas.style.width = window.innerWidth + 'px';
        canvas.style.height = window.innerHeight + 'px';
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      }
      addEventListener('resize', resize);
      resize();

      const mouse = { x: innerWidth / 2, y: innerHeight / 2 };
      addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });

      // blobs that form the lilac flame
      const N = 22;
      const blobs = [];
      for (let i = 0; i < N; i++) {
        blobs.push({
          x: mouse.x,
          y: mouse.y,
          vx: (Math.random() - 0.5) * 0.4,
          vy: (Math.random() - 0.5) * 0.4,
          size: 30 + Math.random() * 120,
          hue: 260 + Math.random() * 40, // lilac/purple
          alpha: 0.06 + Math.random() * 0.22,
          lag: 0.07 + Math.random() * 0.18
        });
      }

      let last = performance.now();
      function loop(t){
        const dt = Math.min(40, t - last);
        last = t;

        // subtle background fade to keep gentle trails
        ctx.fillStyle = 'rgba(8,6,12,0.18)';
        ctx.fillRect(0,0,innerWidth,innerHeight);

        ctx.globalCompositeOperation = 'lighter';
        for (let i = 0; i < blobs.length; i++){
          const b = blobs[i];

          const dx = mouse.x - b.x + Math.sin(t * 0.002 + i) * 10;
          const dy = mouse.y - b.y + Math.cos(t * 0.0015 + i * 1.5) * 10;
          b.vx += dx * b.lag * 0.01;
          b.vy += dy * b.lag * 0.01;

          b.vx *= 0.92;
          b.vy *= 0.92;

          b.x += b.vx * (dt * 0.06);
          b.y += b.vy * (dt * 0.06);

          const s = b.size * (0.8 + 0.2 * Math.sin(t * 0.003 + i));

          const g = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, s);
          const c1 = `hsla(${b.hue}, 85%, 65%, ${Math.min(1, b.alpha * 6)})`;
          const c2 = `hsla(${b.hue}, 65%, 45%, ${b.alpha})`;
          g.addColorStop(0, c1);
          g.addColorStop(0.15, c2);
          g.addColorStop(0.55, `hsla(${b.hue}, 60%, 20%, ${b.alpha * 0.12})`);
          g.addColorStop(1, 'rgba(0,0,0,0)');

          ctx.shadowBlur = 40;
          ctx.shadowColor = c1;
          ctx.fillStyle = g;
          ctx.beginPath();
          ctx.arc(b.x, b.y, s, 0, Math.PI * 2);
          ctx.fill();
        }

        ctx.shadowBlur = 0;
        ctx.globalCompositeOperation = 'source-over';
        requestAnimationFrame(loop);
      }

      requestAnimationFrame(loop);
    })();
    </script>
    """
