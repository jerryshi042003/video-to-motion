/* D3 charts for the Video to Motion write-up. Same contract as the page: hairlines, one accent, mono labels. */
(function () {
  const css = getComputedStyle(document.documentElement);
  const C = { accent: css.getPropertyValue('--accent').trim() || '#0a66d8', muted: css.getPropertyValue('--muted').trim() || '#6e6e76',
              line: css.getPropertyValue('--line').trim() || '#e4e4e8', fg: css.getPropertyValue('--fg').trim() || '#111', bad: '#b4442c', good: '#236442' };
  const mono = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace';
  const onView = (el, fn) => { const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { fn(); io.disconnect(); } }), { threshold: .35 }); io.observe(el); };

  // 1. Fastest racket spin per point, free-wrist fit vs arm solve (deg/s). Cap line at 2,600.
  function spinChart(el, rows) {
    const W = el.clientWidth, rowH = 22, m = { l: 112, r: 86, t: 18, b: 22 }, H = m.t + rows.length * rowH + m.b;
    const svg = d3.select(el).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('width', '100%');
    const x = d3.scaleLinear().domain([0, 5600]).range([m.l, W - m.r]);
    const y = d3.scaleBand().domain(rows.map(r => r.point)).range([m.t, H - m.b]).paddingInner(.45);
    svg.append('g').selectAll('text').data(rows).join('text').attr('x', m.l - 8).attr('y', d => y(d.point) + y.bandwidth() / 2 + 4)
      .attr('text-anchor', 'end').style('font', `11px ${mono}`).attr('fill', C.muted).text(d => d.label);
    svg.append('line').attr('x1', x(2600)).attr('x2', x(2600)).attr('y1', m.t - 6).attr('y2', H - m.b).attr('stroke', C.fg).attr('stroke-dasharray', '3 3').attr('stroke-width', 1);
    svg.append('text').attr('x', x(2600) + 4).attr('y', m.t - 8).style('font', `10px ${mono}`).attr('fill', C.muted).text('2,600°/s cap');
    const before = svg.append('g').selectAll('rect').data(rows).join('rect').attr('x', x(0)).attr('y', d => y(d.point)).attr('height', y.bandwidth() / 2).attr('width', 0).attr('fill', C.bad).attr('opacity', .85);
    const after = svg.append('g').selectAll('rect').data(rows).join('rect').attr('x', x(0)).attr('y', d => y(d.point) + y.bandwidth() / 2).attr('height', y.bandwidth() / 2).attr('width', 0).attr('fill', C.good);
    const lab = svg.append('g').selectAll('text').data(rows).join('text').attr('x', d => x(Math.max(d.before, d.after)) + 4).attr('y', d => y(d.point) + y.bandwidth() / 2 + 4)
      .style('font', `10px ${mono}`).attr('fill', C.muted).attr('opacity', 0).text(d => `${d3.format('.2~s')(d.before)} → ${d3.format('.2~s')(d.after)}`);
    onView(el, () => {
      before.transition().duration(900).delay((d, i) => i * 40).attr('width', d => x(d.before) - x(0));
      after.transition().duration(900).delay((d, i) => 400 + i * 40).attr('width', d => x(d.after) - x(0));
      lab.transition().delay(1400).duration(400).attr('opacity', 1);
    });
  }

  // 2. Face angle at contact, before and after the contact rule. Negative = closed, positive = open.
  function contactChart(el, rows, band) {
    const W = el.clientWidth, rowH = 13, m = { l: 118, r: 14, t: 26, b: 22 }, H = m.t + rows.length * rowH + m.b;
    const svg = d3.select(el).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('width', '100%');
    const x = d3.scaleLinear().domain([-90, 90]).range([m.l, W - m.r]);
    const y = (i) => m.t + i * rowH + rowH / 2;
    svg.append('rect').attr('x', x(band[0])).attr('width', x(band[1]) - x(band[0])).attr('y', m.t - 4).attr('height', rows.length * rowH + 4).attr('fill', C.good).attr('opacity', .12);
    svg.append('line').attr('x1', x(0)).attr('x2', x(0)).attr('y1', m.t - 6).attr('y2', H - m.b).attr('stroke', C.line);
    [-60, 0, 60].forEach(v => svg.append('text').attr('x', x(v)).attr('y', H - 6).attr('text-anchor', 'middle').style('font', `10px ${mono}`).attr('fill', C.muted).text(v < 0 ? `${-v}° closed` : v > 0 ? `${v}° open` : 'vertical'));
    svg.append('text').attr('x', (x(band[0]) + x(band[1])) / 2).attr('y', m.t - 10).attr('text-anchor', 'middle').style('font', `10px ${mono}`).attr('fill', C.good).text('allowed at contact');
    svg.append('g').selectAll('text').data(rows).join('text').attr('x', m.l - 8).attr('y', (d, i) => y(i) + 3.5).attr('text-anchor', 'end').style('font', `9.5px ${mono}`).attr('fill', C.muted).text(d => d.label);
    const lines = svg.append('g').selectAll('line').data(rows).join('line').attr('x1', d => x(d.before)).attr('x2', d => x(d.before)).attr('y1', (d, i) => y(i)).attr('y2', (d, i) => y(i)).attr('stroke', C.line);
    const dotsB = svg.append('g').selectAll('circle').data(rows).join('circle').attr('cx', d => x(d.before)).attr('cy', (d, i) => y(i)).attr('r', 3).attr('fill', C.bad);
    const dotsA = svg.append('g').selectAll('circle').data(rows).join('circle').attr('cx', d => x(d.before)).attr('cy', (d, i) => y(i)).attr('r', 3).attr('fill', C.good).attr('opacity', 0);
    onView(el, () => {
      lines.transition().delay((d, i) => 300 + i * 25).duration(700).attr('x2', d => x(d.after));
      dotsA.transition().delay((d, i) => 300 + i * 25).duration(700).attr('opacity', 1).attr('cx', d => x(d.after));
      dotsB.transition().delay(300).duration(700).attr('opacity', .35);
    });
  }

  // 3. Simple horizontal bars with a label and value (percent or px).
  function bars(el, rows, max, fmt) {
    const W = el.clientWidth, rowH = 26, m = { l: 150, r: 54, t: 6, b: 6 }, H = m.t + rows.length * rowH + m.b;
    const svg = d3.select(el).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('width', '100%');
    const x = d3.scaleLinear().domain([0, max]).range([m.l, W - m.r]);
    svg.append('g').selectAll('text').data(rows).join('text').attr('x', m.l - 8).attr('y', (d, i) => m.t + i * rowH + 16).attr('text-anchor', 'end').style('font', `11px ${mono}`).attr('fill', C.muted).text(d => d.label);
    const r = svg.append('g').selectAll('rect').data(rows).join('rect').attr('x', x(0)).attr('y', (d, i) => m.t + i * rowH + 6).attr('height', 12).attr('rx', 6).attr('width', 0).attr('fill', d => d.color || C.accent);
    const t = svg.append('g').selectAll('text').data(rows).join('text').attr('x', d => x(d.value) + 6).attr('y', (d, i) => m.t + i * rowH + 16).style('font', `11px ${mono}`).attr('fill', C.fg).attr('opacity', 0).text(d => fmt(d.value));
    onView(el, () => { r.transition().duration(900).delay((d, i) => i * 120).attr('width', d => x(d.value) - x(0)); t.transition().delay(900).duration(300).attr('opacity', 1); });
  }

  // 4. Live trace: racket angular speed per frame of the final fit, with a cursor looping at the clip's frame rate.
  function trace(el, data, label) {
    const W = el.clientWidth, H = 120, m = { l: 44, r: 10, t: 12, b: 20 };
    const svg = d3.select(el).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('width', '100%');
    const x = d3.scaleLinear().domain([0, data.speed.length]).range([m.l, W - m.r]);
    const y = d3.scaleLinear().domain([0, Math.max(2800, d3.max(data.speed))]).range([H - m.b, m.t]);
    svg.append('line').attr('x1', m.l).attr('x2', W - m.r).attr('y1', y(2600)).attr('y2', y(2600)).attr('stroke', C.fg).attr('stroke-dasharray', '3 3');
    svg.append('text').attr('x', m.l).attr('y', y(2600) - 4).style('font', `10px ${mono}`).attr('fill', C.muted).text('2,600°/s');
    svg.append('text').attr('x', W - m.r).attr('y', H - 6).attr('text-anchor', 'end').style('font', `10px ${mono}`).attr('fill', C.muted).text(label);
    [0, 1000, 2000].forEach(v => svg.append('text').attr('x', m.l - 6).attr('y', y(v) + 3).attr('text-anchor', 'end').style('font', `10px ${mono}`).attr('fill', C.muted).text(v));
    const path = svg.append('path').datum(data.speed).attr('fill', 'none').attr('stroke', C.accent).attr('stroke-width', 1.5)
      .attr('d', d3.line().x((d, i) => x(i)).y(d => y(d)).curve(d3.curveMonotoneX));
    const cursor = svg.append('line').attr('y1', m.t).attr('y2', H - m.b).attr('stroke', C.fg).attr('stroke-width', 1);
    const dot = svg.append('circle').attr('r', 3.5).attr('fill', C.fg);
    const val = svg.append('text').style('font', `10px ${mono}`).attr('fill', C.fg);
    let run = false, t0 = 0;
    function tick(now) { if (!run) return; const f = Math.floor(((now - t0) / 1000) * data.fps) % data.speed.length; const cx = x(f), cy = y(data.speed[f]);
      cursor.attr('x1', cx).attr('x2', cx); dot.attr('cx', cx).attr('cy', cy); val.attr('x', Math.min(cx + 6, W - 70)).attr('y', Math.max(cy - 8, m.t + 8)).text(`${Math.round(data.speed[f])}°/s`); requestAnimationFrame(tick); }
    const io = new IntersectionObserver(es => es.forEach(e => { run = e.isIntersecting; if (run) { t0 = performance.now(); requestAnimationFrame(tick); } }), { threshold: .2 });
    io.observe(el);
  }

  window.VTM = { spinChart, contactChart, bars, trace };
})();
