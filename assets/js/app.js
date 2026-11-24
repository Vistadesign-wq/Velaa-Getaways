/* Velaa Getaways — interactions (v3). No dependencies. */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var root = document.documentElement, LANG = root.lang || "en";
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Preloader (full once per visit) ---------- */
  var seen = false; try { seen = sessionStorage.getItem("velaa-pre") === "1"; } catch (e) {}
  var loaded = function () { root.classList.add("loaded"); try { sessionStorage.setItem("velaa-pre", "1"); } catch (e) {} };
  if (seen) loaded(); else { addEventListener("load", function () { setTimeout(loaded, 300); }); setTimeout(loaded, 2500); }

  /* ---------- Header + progress ---------- */
  var hdr = $(".hdr"), bar = $(".progress");
  var onScroll = function () {
    var y = scrollY, h = root.scrollHeight - innerHeight;
    if (hdr) hdr.classList.toggle("solid", y > 40);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? y / h : 0) + ")";
  };
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---------- Drawer ---------- */
  var drawer = $(".drawer");
  $$("[data-open]").forEach(function (b) { b.addEventListener("click", function () { drawer.classList.add("open"); document.body.classList.add("lock"); b.setAttribute("aria-expanded", "true"); }); });
  $$("[data-close]").forEach(function (b) { b.addEventListener("click", function () { drawer.classList.remove("open"); document.body.classList.remove("lock"); }); });

  /* ---------- Hero video: respect reduced motion, keep playing ---------- */
  $$(".hero video").forEach(function (v) { if (reduce) { v.removeAttribute("autoplay"); v.pause(); } else { var p = v.play(); if (p && p.catch) p.catch(function () {}); } });

  /* ---------- Hero slideshow ---------- */
  var slides = $$(".hero__slides figure");
  if (slides.length > 1) {
    var bars = $$(".hero__bars button"), cur = $("[data-cur]"), cap = $("[data-cap]"), i = 0, t;
    var show = function (n) {
      slides[i].classList.remove("on"); bars[i] && bars[i].classList.remove("on");
      bars.forEach(function (b, k) { b.classList.toggle("done", k < n); });
      i = (n + slides.length) % slides.length;
      var im = $("img", slides[i]); if (im && im.dataset.src) { im.src = im.dataset.src; im.removeAttribute("data-src"); }
      slides[i].classList.add("on");
      if (bars[i]) { bars[i].classList.remove("on"); void bars[i].offsetWidth; bars[i].classList.add("on"); }
      if (i === 0) bars.forEach(function (b) { b.classList.remove("done"); });
      if (cur) cur.textContent = "0" + (i + 1);
      if (cap) cap.textContent = slides[i].dataset.cap || "";
    };
    var play = function () { clearInterval(t); t = setInterval(function () { show(i + 1); }, 7000); };
    bars.forEach(function (b, k) { b.addEventListener("click", function () { show(k); play(); }); });
    play();
  }

  /* ---------- Reveal & counters ---------- */
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    $$(".rv, .img-rv").forEach(function (el) { io.observe(el); });
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; cio.unobserve(e.target);
        var el = e.target, end = parseInt(el.dataset.count, 10), t0 = performance.now();
        (function step(now) { var p = Math.min(1, (now - t0) / 1500); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); })(t0);
      });
    }, { threshold: 0.6 });
    $$("[data-count]").forEach(function (el) { cio.observe(el); });
  } else { $$(".rv, .img-rv").forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- Season switch ---------- */
  $$(".season").forEach(function (sw) {
    var knob = $(".knob", sw), btns = $$("button", sw);
    var place = function (b) { knob.style.width = b.offsetWidth + "px"; knob.style.transform = "translateX(" + (b.offsetLeft - 4) + "px)"; };
    var on = btns.filter(function (b) { return b.classList.contains("on"); })[0]; place(on);
    addEventListener("resize", function () { place(btns.filter(function (b) { return b.classList.contains("on"); })[0]); });
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", x === b); });
        place(b);
        $$("[data-low]").forEach(function (p) { if (p.tagName === "INPUT") return; p.textContent = p.getAttribute(b.dataset.season === "high" ? "data-high" : "data-low"); });
      });
    });
  });

  /* ---------- Modal / lightbox ---------- */
  var modal = $("#modal"), last = null;
  var openModal = function (o) {
    last = document.activeElement;
    modal.className = "modal" + (o.img ? "" : " noimg") + (o.lb ? " lb" : "");
    var mi = $(".modal__m img", modal); if (o.img) { mi.src = o.img; mi.alt = o.title || ""; }
    $(".modal__ic", modal).innerHTML = o.icon || ""; $(".modal__ic", modal).style.display = o.icon ? "" : "none";
    $(".m-kick", modal).textContent = o.kicker || ""; $("#m-title", modal).textContent = o.title || "";
    $(".modal__t", modal).innerHTML = o.html || "";
    var c = $(".m-cta", modal); if (o.cta) { c.style.display = ""; c.href = o.cta; } else c.style.display = "none";
    requestAnimationFrame(function () { modal.classList.add("open"); });
    modal.setAttribute("aria-hidden", "false"); document.body.classList.add("lock");
    setTimeout(function () { $(".modal__x", modal).focus(); }, 60);
  };
  var closeModal = function () { modal.classList.remove("open"); modal.setAttribute("aria-hidden", "true"); document.body.classList.remove("lock"); if (last) last.focus(); };
  if (modal) {
    $$("[data-x]", modal).forEach(function (b) { b.addEventListener("click", closeModal); });
    addEventListener("keydown", function (e) { if (e.key === "Escape") { closeModal(); if (drawer) { drawer.classList.remove("open"); document.body.classList.remove("lock"); } } });
  }
  $$("[data-modal]").forEach(function (el) {
    el.addEventListener("click", function (e) {
      e.preventDefault();
      var ic = $(".xp__ico svg, .why__i svg", el), d = $(".xp__detail", el);
      openModal({ img: el.dataset.img, title: el.dataset.title, kicker: el.dataset.kicker, icon: ic ? ic.outerHTML : "", html: d ? d.innerHTML : "", cta: el.dataset.cta });
    });
  });
  $$("[data-lb]").forEach(function (el) { el.addEventListener("click", function () { openModal({ img: el.dataset.lb, title: el.getAttribute("aria-label"), lb: true }); }); });

  /* ---------- Testimonials spotlight ---------- */
  $$("[data-tst]").forEach(function (w) {
    var qs = $$(".tq", w), fs = $$(".face", w), tb = $(".tbar span", w), k = 0, t;
    var go = function (n) {
      k = (n + qs.length) % qs.length;
      qs.forEach(function (q, j) { q.classList.toggle("on", j === k); });
      fs.forEach(function (f, j) { f.classList.toggle("on", j === k); });
      if (tb) { tb.classList.remove("run"); void tb.offsetWidth; tb.classList.add("run"); }
    };
    var play = function () { clearInterval(t); t = setInterval(function () { go(k + 1); }, 7000); };
    fs.forEach(function (f, j) { f.addEventListener("click", function () { go(j); play(); }); });
    var p = $("[data-prev]", w), n = $("[data-next]", w);
    if (p) p.addEventListener("click", function () { go(k - 1); play(); });
    if (n) n.addEventListener("click", function () { go(k + 1); play(); });
    w.addEventListener("mouseenter", function () { clearInterval(t); if (tb) tb.style.animationPlayState = "paused"; });
    w.addEventListener("mouseleave", function () { if (tb) tb.style.animationPlayState = ""; play(); });
    go(0); play();
  });

  /* ---------- Experience filters ---------- */
  $$(".filters").forEach(function (f) {
    var btns = $$("button", f), cards = $$(".xgrid .xp");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.classList.toggle("on", x === b); });
        cards.forEach(function (c) { var show = b.dataset.f === "*" || c.dataset.cat === b.dataset.f; c.classList.toggle("hide", !show); if (show) c.classList.add("in"); });
      });
    });
  });

  /* ---------- Booking card (home) ---------- */
  var today = new Date().toISOString().slice(0, 10);
  var pair = function (a, d) {
    if (!a || !d) return;
    a.min = today;
    a.addEventListener("change", function () {
      d.min = a.value;
      if (a.value && (!d.value || d.value <= a.value)) { var x = new Date(a.value); x.setDate(x.getDate() + 7); d.value = x.toISOString().slice(0, 10); }
      d.dispatchEvent(new Event("change", { bubbles: true }));
    });
  };
  $$("[data-book]").forEach(function (f) {
    pair(f.elements.arrival, f.elements.departure);
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = new URLSearchParams();
      ["arrival", "departure", "adults", "package"].forEach(function (k) { if (f.elements[k].value) q.set(k, f.elements[k].value); });
      location.href = f.getAttribute("action") + "?" + q.toString() + "#enquiry";
    });
  });

  /* ---------- Concierge enquiry ---------- */
  var form = $("#enquiry-form");
  if (form) {
    var D = form.dataset, steps = $$(".step", form), tabs = $$(".steps button", form), s = 0;
    var go = function (n) {
      s = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach(function (st, j) { st.classList.toggle("on", j === s); });
      tabs.forEach(function (t, j) { t.classList.toggle("on", j === s); t.classList.toggle("done", j < s); });
      var top = form.getBoundingClientRect().top + scrollY - 110; if (scrollY > top) scrollTo({ top: top, behavior: "smooth" });
    };
    tabs.forEach(function (t, j) { t.addEventListener("click", function () { go(j); }); });
    $$("[data-next-step]", form).forEach(function (b) { b.addEventListener("click", function () { go(s + 1); }); });
    $$("[data-prev-step]", form).forEach(function (b) { b.addEventListener("click", function () { go(s - 1); }); });

    $$("[data-stepper]", form).forEach(function (st) {
      var name = st.dataset.stepper, out = $("output", st), inp = form.elements[name], min = name === "adults" ? 1 : 0;
      $$("button", st).forEach(function (b) {
        b.addEventListener("click", function () { var v = Math.max(min, Math.min(20, parseInt(inp.value, 10) + parseInt(b.dataset.d, 10))); inp.value = v; out.textContent = v; update(); });
      });
    });
    pair(form.elements.arrival, form.elements.departure);

    var fmt = function (d) { try { return new Date(d).toLocaleDateString(LANG === "ru" ? "ru-RU" : "en-GB", { day: "numeric", month: "short" }); } catch (e) { return d; } };
    var num = function (v) { return parseInt(String(v || "").replace(/[^\d]/g, ""), 10) || 0; };
    var set = function (k, v) { var el = $('[data-sum="' + k + '"]'); if (el) el.textContent = v; };
    var update = function () {
      var f = form.elements, pk = $('input[name="package"]:checked', form);
      var adults = num(f.adults.value), kids = num(f.children.value);
      set("pkg", pk ? pk.dataset.name : "");
      var si = $("[data-sum-img]"); if (pk && si && si.getAttribute("src") !== pk.dataset.img) { si.style.opacity = 0; setTimeout(function () { si.src = pk.dataset.img; si.style.opacity = 1; }, 200); }
      var a = f.arrival.value, d = f.departure.value;
      set("dates", a ? fmt(a) + (d ? " → " + fmt(d) : "") : D.none);
      var nights = a && d ? Math.round((new Date(d) - new Date(a)) / 864e5) : 0;
      set("nights", nights > 0 ? nights : D.none);
      set("guests", adults + (kids ? " + " + kids : ""));
      var xs = $$('input[name="extras"]:checked', form).map(function (c) { return c.dataset.label; });
      set("xp", xs.length ? xs.length + " · " + xs.slice(0, 2).join(", ") + (xs.length > 2 ? "…" : "") : D.none);
      if (pk && pk.dataset.low) {
        var m = a ? new Date(a).getMonth() + 1 : 0, high = m && (m >= 11 || m <= 3);
        var per = num(high ? pk.dataset.high : pk.dataset.low);
        set("total", "$" + (per * adults).toLocaleString("en-US"));
        set("note", "$" + per.toLocaleString("en-US") + " " + D.note.replace("{season}", m ? (high ? D.seasonHigh : D.seasonLow) : D.seasonLow + " / " + D.seasonHigh) + (kids ? " · " + D.kids : ""));
      } else { set("total", D.quote); set("note", ""); }
    };
    form.addEventListener("change", update);

    var q = new URLSearchParams(location.search);
    if (q.has("package")) { var r = $('input[name="package"][value="' + q.get("package") + '"]', form); if (r) r.checked = true; }
    if (q.get("exp")) { var c = $('input[name="extras"][value="' + q.get("exp") + '"]', form); if (c) c.checked = true; }
    ["arrival", "departure"].forEach(function (k) { if (q.get(k)) form.elements[k].value = q.get(k); });
    if (q.get("adults")) { form.elements.adults.value = q.get("adults"); $('[data-stepper="adults"] output', form).textContent = q.get("adults"); }
    update();

    var cSel = form.elements.country, kSel = form.elements.code;
    if (cSel && kSel) cSel.addEventListener("change", function () {
      var o = cSel.options[cSel.selectedIndex], iso = o && o.dataset.iso;
      if (!iso) return;
      for (var i = 0; i < kSel.options.length; i++) if (kSel.options[i].dataset.iso === iso) { kSel.selectedIndex = i; break; }
    });
    var phone = function () {
      var f = form.elements, n = (f.phone.value || "").trim();
      if (!n) return "";
      return /^\+/.test(n) ? n : ((f.code && f.code.value ? f.code.value + " " : "") + n);
    };
    var compose = function () {
      var f = form.elements, pk = $('input[name="package"]:checked', form);
      var xs = $$('input[name="extras"]:checked', form).map(function (c) { return c.dataset.label; });
      return [D.hello, D.lName + ": " + (f.name.value || "—"), (f.country && f.country.value ? "Country: " + f.country.value : ""), (phone() ? "Phone: " + phone() : ""), D.lDates + ": " + (f.arrival.value || "—") + " → " + (f.departure.value || "—"),
        D.lGuests + ": " + f.adults.value + (num(f.children.value) ? " + " + f.children.value : ""), D.lPackage + ": " + (pk ? pk.dataset.name : "—"),
        xs.length ? D.lExtras + ": " + xs.join(", ") : "", f.message.value ? D.lMsg + ": " + f.message.value : ""].filter(Boolean).join("\n");
    };
    var status = $(".status", form);
    var valid = function () {
      var n = form.elements.name, e = form.elements.email;
      if (!n.value.trim()) { go(3); n.focus(); n.reportValidity && n.reportValidity(); return false; }
      if (!e.value.trim() || !e.checkValidity()) { go(3); e.focus(); e.reportValidity && e.reportValidity(); return false; }
      return true;
    };
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (form.elements._honey.value) return;
      if (!valid()) return;
      var f = form.elements, pk = $('input[name="package"]:checked', form);
      var xs = $$('input[name="extras"]:checked', form).map(function (c) { return c.dataset.label; });
      var payload = {
        _subject: D.subject + " — " + f.name.value, _template: "table", _captcha: "false", _replyto: f.email.value,
        Name: f.name.value, Email: f.email.value, Country: (f.country && f.country.value) || "—", "Phone / WhatsApp": phone() || "—", "Reply by": (form.querySelector('input[name="reply"]:checked') || {}).value,
        Package: pk ? pk.dataset.name : "—", Arrival: f.arrival.value || "—", Departure: f.departure.value || "—",
        Adults: f.adults.value, Children: f.children.value, Experiences: xs.join(", ") || "—",
        "Estimated total": $('[data-sum="total"]').textContent, Message: f.message.value || "—", Language: LANG.toUpperCase(), Page: location.href
      };
      status.className = "status busy"; status.textContent = D.sending;
      var btn = $('[type="submit"]', form); btn.disabled = true;
      fetch(form.action, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (!res.ok || String(res.j.success) === "false") throw new Error("x");
          status.className = "status"; steps.forEach(function (st) { st.classList.remove("on"); });
          $(".steps", form).style.display = "none"; $(".sent", form).classList.add("on");
        })
        .catch(function () {
          status.className = "status err"; status.textContent = D.err + " ";
          var a = document.createElement("a");
          a.href = "mailto:" + form.action.split("/").pop() + "?subject=" + encodeURIComponent(D.subject + " — " + f.name.value) + "&body=" + encodeURIComponent(compose() + "\nE-mail: " + f.email.value);
          a.textContent = LANG === "ru" ? "Отправить из почтового приложения →" : "Send it from your e-mail app →";
          a.style.textDecoration = "underline"; status.appendChild(a);
        })
        .then(function () { btn.disabled = false; });
    });
    $("[data-send-wa]", form).addEventListener("click", function () {
      window.open("https://wa.me/" + D.wa + "?text=" + encodeURIComponent(compose()), "_blank", "noopener");
    });
  }

  /* ---------- Language hint ---------- */
  var hint = $(".lhint");
  if (hint) {
    var key = "velaa-lang", dismissed = false; try { dismissed = localStorage.getItem(key) === "1"; } catch (e) {}
    var nav = (navigator.language || "").toLowerCase(), wants = /^(ru|uk|be|kk)/.test(nav) ? "ru" : "en";
    if (!dismissed && wants !== LANG) setTimeout(function () { hint.classList.add("on"); }, 1800);
    $$("a, button", hint).forEach(function (x) { x.addEventListener("click", function () { hint.classList.remove("on"); try { localStorage.setItem(key, "1"); } catch (e) {} }); });
  }
  $$("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });
  /* full-photo heroes: fit the whole picture in the first screen */
  var ph = $(".phero--full");
  var setHH = function () { if (ph) root.style.setProperty("--hh", Math.round(ph.getBoundingClientRect().top + scrollY) + "px"); };
  setHH(); addEventListener("resize", setHH);
  /* ---------- Carousels (photo cards, reviews, galleries) ---------- */
  $$("[data-car]").forEach(function (c) {
    var tr = $(".car__track", c), items = Array.prototype.slice.call(tr.children), dots = $(".car__dots", c),
        pv = $("[data-cprev]", c), nx = $("[data-cnext]", c), nav = $(".car__nav", c), t, rt, rs;
    var step = function () { return items.length > 1 ? (items[1].offsetLeft - items[0].offsetLeft) || tr.clientWidth : tr.clientWidth; };
    var pages = function () { var g = parseFloat(getComputedStyle(tr).columnGap) || 0, vis = Math.max(1, Math.floor((tr.clientWidth + g + 4) / step())); return Math.max(1, items.length - vis + 1); };
    var cur = function () { return Math.round(tr.scrollLeft / step()); };
    var sync = function () { var i = Math.min(cur(), pages() - 1); $$("button", dots).forEach(function (b, j) { b.classList.toggle("on", j === i); }); };
    var go = function (i) { var n = pages(); i = (i + n) % n; tr.scrollTo({ left: i * step(), behavior: reduce ? "auto" : "smooth" }); };
    var auto = c.hasAttribute("data-auto") && !reduce;
    var restart = function () { if (!auto) return; clearInterval(t); t = setInterval(function () { go(cur() + 1); }, 6500); };
    var build = function () {
      var n = pages(); dots.innerHTML = "";
      for (var i = 0; i < n; i++) {
        (function (i) { var b = document.createElement("button"); b.type = "button"; b.setAttribute("aria-label", (i + 1) + " / " + n);
          b.addEventListener("click", function () { go(i); restart(); }); dots.appendChild(b); })(i);
      }
      nav.hidden = n < 2; sync();
    };
    pv.addEventListener("click", function () { go(cur() - 1); restart(); });
    nx.addEventListener("click", function () { go(cur() + 1); restart(); });
    tr.addEventListener("scroll", function () { cancelAnimationFrame(rt); rt = requestAnimationFrame(sync); }, { passive: true });
    addEventListener("resize", function () { clearTimeout(rs); rs = setTimeout(build, 150); });
    if (auto) {
      c.addEventListener("mouseenter", function () { clearInterval(t); });
      c.addEventListener("mouseleave", restart);
      c.addEventListener("touchstart", function () { clearInterval(t); }, { passive: true });
      c.addEventListener("focusin", function () { clearInterval(t); });
    }
    build(); restart();
  });
})();
