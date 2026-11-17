(() => {
  const hero = document.querySelector('.hero');
  const art = hero?.querySelector('.hero-art');
  const print = hero?.querySelector('.wall-print');
  if (!art || !print) return;

  // Projected TL / TR / BR / BL of the approved Blender wall guide.
  // Use twice the guide's physical height to fit the title and navigation.
  // The calibrated camera is level, so vertical projection is linear at each edge.
  const artW = 1913;
  const artH = 822;
  const guide = [[230.018,244.987],[605.038,273.726],[605.038,339.573],[230.018,323.343]];
  const area = guide.map((p, i) => i < 2 ? p : p.map((v, k) => 2 * v - guide[3 - i][k]));
  const wide = matchMedia('(min-width: 701px)');
  const planeW = 425, planeH = 190;

  function position() {
    const {width, height} = hero.getBoundingClientRect();
    const iw = art.naturalWidth || Number(art.getAttribute('width'));
    const ih = art.naturalHeight || Number(art.getAttribute('height'));
    if (!wide.matches || !width || !height || !iw || !ih) {
      hero.classList.remove('has-wall-plane');
      return;
    }

    // Match the image's object-fit: cover and object-position, not viewport ratios.
    const scale = Math.max(width / iw, height / ih);
    const drawW = iw * scale, drawH = ih * scale;
    const css = getComputedStyle(art);
    const [offsetXPct, offsetYPct] = css.objectPosition.split(' ').map(parseFloat);
    const offsetX = (width - drawW) * offsetXPct / 100;
    const offsetY = (height - drawH) * offsetYPct / 100;
    const q = area.map(([x, y]) => [offsetX + x / artW * drawW, offsetY + y / artH * drawH]);
    if (q.some(([x, y]) => !Number.isFinite(x+y) || x < 12 || x > width - 12 || y < 12 || y > height - 12)) {
      hero.classList.remove('has-wall-plane');
      return;
    }

    const [[x0,y0],[x1,y1],[x2,y2],[x3,y3]] = q;
    const x13=x1-x2, x23=x3-x2, xsum=x0-x1+x2-x3;
    const y13=y1-y2, y23=y3-y2, ysum=y0-y1+y2-y3;
    const det=x13*y23-x23*y13;
    if (Math.abs(det) < 1e-6) {
      hero.classList.remove('has-wall-plane');
      return;
    }
    const g=(xsum*y23-x23*ysum)/det, h=(x13*ysum-xsum*y13)/det;
    const matrix = [
      (x1 - x0 + g*x1)/planeW, (y1 - y0 + g*y1)/planeW, 0, g/planeW,
      (x3 - x0 + h*x3)/planeH, (y3 - y0 + h*y3)/planeH, 0, h/planeH,
      0,0,1,0, x0,y0,0,1,
    ];
    print.style.setProperty('--wall-transform', `matrix3d(${matrix.join(',')})`);
    hero.classList.add('has-wall-plane');
  }

  position();
  art.addEventListener('load', position);
  wide.addEventListener('change', position);
  new ResizeObserver(position).observe(hero);
})();
