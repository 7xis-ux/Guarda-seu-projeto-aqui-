(() => {
  const canvas = document.getElementById("particles");
  if (!(canvas instanceof HTMLCanvasElement)) return;

  const context = canvas.getContext("2d");
  if (!context) return;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const particleCount = Math.min(75, Math.floor(window.innerWidth / 18));
  const particles = [];
  let width = 0;
  let height = 0;
  let frame = 0;

  function resize() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
  }

  function createParticle() {
    return {
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 1.5 + 0.6,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      alpha: Math.random() * 0.48 + 0.18
    };
  }

  function draw() {
    context.clearRect(0, 0, width, height);
    for (let i = 0; i < particles.length; i += 1) {
      const particle = particles[i];
      particle.x += particle.vx;
      particle.y += particle.vy;
      if (particle.x < 0 || particle.x > width) particle.vx *= -1;
      if (particle.y < 0 || particle.y > height) particle.vy *= -1;

      context.beginPath();
      context.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      context.fillStyle = `rgba(174, 155, 255, ${particle.alpha})`;
      context.fill();

      for (let j = i + 1; j < particles.length; j += 1) {
        const other = particles[j];
        const dx = particle.x - other.x;
        const dy = particle.y - other.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < 112) {
          context.beginPath();
          context.moveTo(particle.x, particle.y);
          context.lineTo(other.x, other.y);
          context.strokeStyle = `rgba(143, 120, 255, ${(1 - distance / 112) * 0.16})`;
          context.lineWidth = 0.7;
          context.stroke();
        }
      }
    }

    if (!reducedMotion) frame = window.requestAnimationFrame(draw);
  }

  resize();
  for (let i = 0; i < particleCount; i += 1) particles.push(createParticle());
  draw();
  window.addEventListener("resize", () => {
    resize();
    if (reducedMotion) draw();
  });
  window.addEventListener("pagehide", () => window.cancelAnimationFrame(frame), { once: true });
})();
