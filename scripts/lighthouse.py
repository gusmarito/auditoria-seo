#!/usr/bin/env python3
"""Lighthouse local, mobile e desktop, para quando o PageSpeed Insights estiver sem cota (HTTP 429).

Uso:
  py -3 scripts/lighthouse.py --url https://www.cliente.com.br/ --dominio cliente.com.br

Usa o Edge instalado no Windows (ou o Chrome, se CHROME_PATH estiver definido).
Grava entregas/<dominio>/extra/lh_<estrategia>.json e imprime notas, Core Web Vitals,
os maiores arquivos e scripts injetados pela máquina (antivírus), que contaminam a medição.
No slide, a fonte diz "Lighthouse 12.2.1 rodado pela V4" e registra a contaminação, se houver.
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SUSPEITOS = ("kaspersky", "avast", "avg", "norton", "mcafee", "eset", "bitdefender", "trendmicro")
METRICAS = ["first-contentful-paint", "largest-contentful-paint", "total-blocking-time",
            "cumulative-layout-shift", "speed-index", "total-byte-weight"]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--dominio", required=True)
    a = ap.parse_args()
    out = os.path.join(ROOT, "entregas", a.dominio.replace("www.", ""), "extra")
    os.makedirs(out, exist_ok=True)
    env = dict(os.environ)
    if "CHROME_PATH" not in env and os.path.exists(EDGE):
        env["CHROME_PATH"] = EDGE
    for est in ["mobile", "desktop"]:
        path = os.path.join(out, f"lh_{est}.json")
        cmd = ["npx", "-y", "lighthouse@12.2.1", a.url, "--quiet", "--output=json", f"--output-path={path}",
               "--only-categories=performance,seo,accessibility,best-practices", "--chrome-flags=--headless=new"]
        if est == "desktop":
            cmd.insert(4, "--preset=desktop")
        subprocess.run(cmd, env=env, shell=(os.name == "nt"), check=False)
        if not os.path.exists(path):
            print(est, "falhou")
            continue
        d = json.load(open(path, encoding="utf-8"))
        au = d["audits"]
        print(f"== {est}", {k: round(v["score"] * 100) for k, v in d["categories"].items() if v["score"] is not None})
        for m in METRICAS:
            print("  ", m, au[m].get("displayValue"))
        reqs = au.get("network-requests", {}).get("details", {}).get("items", [])
        for r in sorted(reqs, key=lambda x: -x.get("transferSize", 0))[:6]:
            print("   pesado", round(r["transferSize"] / 1024), "KB", r.get("resourceType"), r["url"][:100])
        tp = au.get("third-party-summary", {}).get("details", {}).get("items", [])
        for it in tp:
            nome = str(it.get("entity", "")).lower()
            if any(s in nome for s in SUSPEITOS):
                print(f"   ATENÇÃO: script injetado pela máquina ({it.get('entity')}), {round(it.get('blockingTime', 0))} ms de bloqueio. Registrar na fonte do slide.")


if __name__ == "__main__":
    main()
