#!/usr/bin/env python3
"""QA visual do deck: captura cada slide em 1600x900, checa console, estouro,
colisão com a linha de fonte, centralização em 4 viewports e navegação.

Uso:
  py -3 scripts/qa_deck.py entregas/<dominio>/deck/index.html entregas/<dominio>/qa

Depois gere as folhas de contato:
  py -3 .cursor/skills/colli-html-ppt/scripts/make_contact_sheet.py entregas/<dominio>/qa/slides --output entregas/<dominio>/qa/sheets

Abra cada folha e cada slide denso (tabelas, 5W1H, palavras-chave) em resolução cheia.
Estouro de ".sphere" é intencional (esfera decorativa recortada). Qualquer outro, corrija.
"""
import asyncio
import json
import pathlib
import sys

from playwright.async_api import async_playwright


async def main():
    sys.stdout.reconfigure(encoding="utf-8")
    deck = pathlib.Path(sys.argv[1]).resolve()
    out = pathlib.Path(sys.argv[2]) / "slides"
    out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="msedge")
        pg = await b.new_page(viewport={"width": 1600, "height": 900})
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(deck.as_uri())
        await pg.wait_for_timeout(2500)
        n = await pg.evaluate("document.querySelectorAll('.slide').length")
        problemas = []
        for i in range(n):
            await pg.evaluate(f"goTo({i})")
            await pg.wait_for_timeout(1400)
            await pg.screenshot(path=str(out / f"s{i + 1:02d}.png"))
            o = await pg.evaluate("""() => {
              const s = document.querySelector('.slide.active'); const r = s.getBoundingClientRect(); const bad = [];
              s.querySelectorAll('*').forEach(e => { const q = e.getBoundingClientRect();
                if (q.width && !e.closest('.sphere') && (q.right > r.right + 1 || q.bottom > r.bottom + 1)) bad.push(e.className || e.tagName); });
              const src = s.querySelector('.src'); let col = null;
              if (src) { const a = src.getBoundingClientRect();
                s.querySelectorAll(':scope > *:not(.src):not(.topline):not(.sphere)').forEach(e => { const q = e.getBoundingClientRect();
                  if (q.bottom > a.top + 2 && q.top < a.top && q.height > 0) col = (e.className || e.tagName); }); }
              return {estouro: bad.slice(0, 5), colide_fonte: col}; }""")
            if o["estouro"] or o["colide_fonte"]:
                problemas.append((i + 1, o))
        print("slides", n)
        print("erros de console", errs or "nenhum")
        print("estouro ou colisão", json.dumps(problemas, ensure_ascii=False) if problemas else "nenhum")
        for w, h in [(1024, 768), (1366, 768), (1600, 900), (1920, 1080)]:
            await pg.set_viewport_size({"width": w, "height": h})
            await pg.wait_for_timeout(400)
            r = await pg.evaluate("(()=>{const r=document.getElementById('deck').getBoundingClientRect();return [r.left, innerWidth-r.right, r.top, innerHeight-r.bottom]})()")
            ok = abs(r[0] - r[1]) <= 1 and abs(r[2] - r[3]) <= 1 and min(r) >= 0
            print(f"viewport {w}x{h}", "centralizado" if ok else f"FALHOU {r}")
        await pg.set_viewport_size({"width": 1600, "height": 900})
        await pg.evaluate("goTo(0)")
        d0 = await pg.evaluate("[prevBtn.disabled, nextBtn.disabled]")
        await pg.keyboard.press("ArrowRight")
        c1 = await pg.evaluate("slideCounter.textContent")
        await pg.keyboard.press("End")
        d1 = await pg.evaluate("[prevBtn.disabled, nextBtn.disabled, progressFill.style.width]")
        print("navegação", "ok" if d0 == [True, False] and c1.startswith("02") and d1 == [False, True, "100%"] else f"FALHOU {d0} {c1} {d1}")
        await b.close()


asyncio.run(main())
