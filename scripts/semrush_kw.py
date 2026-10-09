#!/usr/bin/env python3
"""Estudo de palavras-chave e concorrência via API REST do SEMrush.

A chave sai de .cursor/mcp.json, a mesma do coletar.mjs. Banco padrão: br.
Tudo é gravado em entregas/<dominio>/extra/.

Subcomandos:
  dominio      domain_organic completo, histórico de 36 meses, ranks por banco,
               domínios de referência e perfil de Authority Score
               py -3 scripts/semrush_kw.py dominio --dominio cliente.com.br

  descobrir    correspondência ampla por semente (phrase_fullsearch)
               py -3 scripts/semrush_kw.py descobrir --dominio cliente.com.br --sementes "barragem;drenagem"

  volumes      volume, dificuldade e intenção de uma lista curada
               arquivo: uma linha por termo no formato  LINHA|tipo|termo
               tipo = servico (fundo de funil) ou conteudo (topo de funil)
               py -3 scripts/semrush_kw.py volumes --dominio cliente.com.br --arquivo kw.txt

  serp         top 10 do Google para termos de serviço, com contagem de domínios
               py -3 scripts/semrush_kw.py serp --dominio cliente.com.br --termos "dam break;macrodrenagem"

  concorrentes ranks e Authority Score de domínios que apareceram nas SERPs
               py -3 scripts/semrush_kw.py concorrentes --dominio cliente.com.br --lista "a.com.br,b.com"

Cada chamada consome unidades da conta. Um estudo completo fica em torno de
10 sementes, 150 termos, 15 a 20 SERPs e 6 a 8 concorrentes.
"""
import argparse
import collections
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.semrush.com/"
API_BL = "https://api.semrush.com/analytics/v1/"


def key():
    txt = open(os.path.join(ROOT, ".cursor", "mcp.json"), encoding="utf-8").read()
    m = re.search(r"Apikey (\w+)", txt)
    if not m:
        sys.exit("Chave SEMrush ausente em .cursor/mcp.json")
    return m.group(1)


def call(params, base=API):
    p = dict(params)
    p["key"] = key()
    raw = urllib.request.urlopen(base + "?" + urllib.parse.urlencode(p), timeout=120).read()
    try:
        t = raw.decode("utf-8")
    except UnicodeDecodeError:
        t = raw.decode("latin-1")
    t = t.replace("\r", "")
    if t.startswith("ERROR"):
        return {"error": t.strip()}
    lines = [l for l in t.strip().split("\n") if l]
    hdr = lines[0].split(";")
    return [dict(zip(hdr, l.split(";"))) for l in lines[1:]]


def outdir(dominio):
    d = os.path.join(ROOT, "entregas", dominio.replace("www.", ""), "extra")
    os.makedirs(d, exist_ok=True)
    return d


def save(dominio, name, data):
    path = os.path.join(outdir(dominio), name)
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("gravado", path)


def cmd_dominio(a):
    d = a.dominio
    save(d, "sem_organic_full.json", call({"type": "domain_organic", "domain": d, "database": a.db, "display_limit": 100,
                                           "display_sort": "tr_desc", "export_columns": "Ph,Po,Pp,Nq,Cp,Ur,Tr,Kd,Co"}))
    save(d, "sem_history.json", call({"type": "domain_rank_history", "domain": d, "database": a.db, "display_limit": 36,
                                      "export_columns": "Dt,Rk,Or,Ot,Oc"}))
    save(d, "sem_ranks_alldb.json", call({"type": "domain_ranks", "domain": d, "export_columns": "Db,Dn,Rk,Or,Ot,Oc"}))
    save(d, "sem_refdomains.json", call({"type": "backlinks_refdomains", "target": d, "target_type": "root_domain", "display_limit": 60,
                                         "display_sort": "domain_ascore_desc", "export_columns": "domain_ascore,domain,backlinks_num"}, API_BL))
    save(d, "sem_ascore_profile.json", call({"type": "backlinks_ascore_profile", "target": d, "target_type": "root_domain"}, API_BL))
    save(d, "sem_tld.json", call({"type": "backlinks_tld", "target": d, "target_type": "root_domain", "display_limit": 15,
                                  "export_columns": "zone,domains_num,backlinks_num"}, API_BL))


def cmd_descobrir(a):
    out = {}
    for s in [x.strip() for x in a.sementes.split(";") if x.strip()]:
        out[s] = call({"type": "phrase_fullsearch", "phrase": s, "database": a.db, "display_limit": a.limite,
                       "display_sort": "nq_desc", "export_columns": "Ph,Nq,Kd,In,Cp"})
        n = len(out[s]) if isinstance(out[s], list) else out[s]
        print(s, n)
    save(a.dominio, "sem_descoberta.json", out)


def cmd_volumes(a):
    rows = []
    for line in open(a.arquivo, encoding="utf-8"):
        parts = [p.strip() for p in line.strip().split("|")]
        if len(parts) == 3 and parts[2]:
            rows.append(parts)
    vol = {}
    terms = [r[2] for r in rows]
    for i in range(0, len(terms), 100):
        res = call({"type": "phrase_these", "phrase": ";".join(terms[i:i + 100]), "database": a.db,
                    "export_columns": "Ph,Nq,Cp,Co,Kd,In,Nr"})
        if isinstance(res, list):
            for x in res:
                vol[x["Keyword"].lower()] = x
    own = {}
    org = os.path.join(outdir(a.dominio), "sem_organic_full.json")
    if os.path.exists(org):
        for x in json.load(open(org, encoding="utf-8")):
            own.setdefault(x["Keyword"].lower(), int(x["Position"]))
    serp = os.path.join(outdir(a.dominio), "sem_serps.json")
    if os.path.exists(serp):
        alvo = a.dominio.replace("www.", "")
        for termo, res in json.load(open(serp, encoding="utf-8")).items():
            if isinstance(res, list) and termo != "_contagem_dominios":
                for x in res:
                    if alvo in x.get("Domain", ""):
                        own.setdefault(termo.lower(), int(x["Position"]))
    study = collections.defaultdict(lambda: {"servico": [], "conteudo": []})
    for linha, tipo, termo in rows:
        x = vol.get(termo.lower())
        if not x:
            continue
        study[linha][tipo].append({
            "termo": termo, "volume": int(x["Search Volume"]), "kd": int(x.get("Keyword Difficulty Index") or 0),
            "intencao": x.get("Intent", ""), "cpc": x.get("CPC", ""), "posicao_cliente": own.get(termo.lower()),
        })
    resumo = {}
    for linha, d in study.items():
        for t in d:
            d[t].sort(key=lambda r: -r["volume"])
        resumo[linha] = {"termos_servico": len(d["servico"]), "volume_servico": sum(r["volume"] for r in d["servico"]),
                         "no_top10": sum(1 for r in d["servico"] if r["posicao_cliente"] and r["posicao_cliente"] <= 10)}
        print(linha, resumo[linha])
    save(a.dominio, "kw_study.json", {"linhas": study, "resumo": resumo,
                                      "sem_volume": [t for t in terms if t.lower() not in vol]})


def cmd_serp(a):
    out, cont = {}, collections.Counter()
    alvo = a.dominio.replace("www.", "")
    for t in [x.strip() for x in a.termos.split(";") if x.strip()]:
        r = call({"type": "phrase_organic", "phrase": t, "database": a.db, "display_limit": 10, "export_columns": "Dn,Ur,Po"})
        out[t] = r
        pos = None
        if isinstance(r, list):
            for x in r:
                cont[x["Domain"]] += 1
                if alvo in x["Domain"]:
                    pos = x.get("Position")
        print(t, "| cliente:", pos or "fora do top 10")
    out["_contagem_dominios"] = cont.most_common(40)
    save(a.dominio, "sem_serps.json", out)


def cmd_concorrentes(a):
    out = {}
    for d in [x.strip() for x in a.lista.split(",") if x.strip()] + [a.dominio]:
        r = call({"type": "domain_ranks", "domain": d, "database": a.db, "export_columns": "Dn,Rk,Or,Ot,Oc"})
        b = call({"type": "backlinks_overview", "target": d, "target_type": "root_domain",
                  "export_columns": "ascore,total,domains_num"}, API_BL)
        out[d] = {"ranks": r[0] if isinstance(r, list) and r else r, "backlinks": b[0] if isinstance(b, list) and b else b}
        print(d, out[d])
    save(a.dominio, "sem_concorrentes.json", out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ["dominio", "descobrir", "volumes", "serp", "concorrentes"]:
        p = sub.add_parser(name)
        p.add_argument("--dominio", required=True)
        p.add_argument("--db", default="br")
        if name == "descobrir":
            p.add_argument("--sementes", required=True)
            p.add_argument("--limite", type=int, default=25)
        if name == "volumes":
            p.add_argument("--arquivo", required=True)
        if name == "serp":
            p.add_argument("--termos", required=True)
        if name == "concorrentes":
            p.add_argument("--lista", required=True)
    a = ap.parse_args()
    {"dominio": cmd_dominio, "descobrir": cmd_descobrir, "volumes": cmd_volumes,
     "serp": cmd_serp, "concorrentes": cmd_concorrentes}[a.cmd](a)


if __name__ == "__main__":
    main()
