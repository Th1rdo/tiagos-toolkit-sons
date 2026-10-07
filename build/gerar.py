# -*- coding: utf-8 -*-
"""Gera o módulo «Tiago's Toolkit: Sons»: macros de um clique (Sequencer + PSFX) num compêndio.
Edita SONS abaixo, corre este script e depois `node build/compilar.mjs`."""
import os, re, json, shutil, hashlib, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULO_ID = "tiagos-toolkit-sons"
VERSAO = "0.3.0"
GH = "https://github.com/Th1rdo/tiagos-toolkit-sons"
FONTE_PSFX = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/foundryRevision/04 Assets/_fonte/psfx-dbpaths.txt")

# Os sons são do Tiago (pasta «sound effects»), tratados por build/processar.py e guardados no Forge dele —
# não vão no repositório (origem/licença desconhecida, como os passos do Andares). As macros apontam para lá.
FORGE = "https://assets.forge-vtt.com/66db4a14be3d73c561d3484a/MAIN/AKRASIA/Sons/Efeitos/"
COR = "#2B2B33"

# (nome da macro, glifo, ficheiro no Forge sem .mp3)
SONS = [
 ("Pistola",            "gun",       "pistola"),
 ("Soco",               "punch",     "soco"),
 ("Golpe de lâmina",    "slash",     "golpe-de-lamina"),
 ("Carne cortada",      "stab",      "carne-cortada"),
 ("Carne a crescer",    "blob",      "carne-a-crescer"),
 ("Descarga elétrica",  "lightning", "descarga-eletrica"),
 ("Grito de morte",     "scream",    "grito-de-morte"),
 ("Abrir porta",        "door-open", "abrir-porta"),
 ("Passos",             "steps",     "passos"),
 ("Passos pesados",     "steps",     "passos-pesados"),
]

# glifos 64x64, traço claro sobre o cartão da pasta
GLIFOS = {
 "silencer": '<path d="M8 28h26v10H22l-2 14h-8l2-14H8z" fill="#f5f5fa" stroke-width="2"/><rect x="34" y="29" width="20" height="8" rx="2" fill="#f5f5fa" stroke-width="2"/>',
 "rifle":  '<path d="M6 40h42l6-8M16 40v10M32 40v8M6 40l5-8h14" stroke-width="5"/>',
 "shotgun":'<path d="M6 28h48M6 36h48M20 36l-4 16" stroke-width="5"/>',
 "explosion": '<path d="M32 6l6 14 15-6-6 15 14 6-14 6 6 15-15-6-6 14-6-14-15 6 6-15-14-6 14-6-6-15 15 6z" fill="#f5f5fa" stroke-width="1"/>',
 "clash":  '<path d="M12 12l40 40M52 12L12 52" stroke-width="5"/><path d="M8 16l8-8M56 16l-8-8" stroke-width="4"/>',
 "unsheathe": '<path d="M16 48l28-28" stroke-width="5"/><path d="M40 12l12 12" stroke-width="5"/><path d="M12 52l4-4" stroke-width="6"/>',
 "glass":  '<path d="M32 8l-6 16 10 4-8 14 6 4-4 10" stroke-width="4"/><path d="M14 24h10M40 20h10M44 40h8" stroke-width="3"/>',
 "bell":   '<path d="M32 10c-10 0-14 8-14 18v10l-6 8h40l-6-8V28c0-10-4-18-14-18z" stroke-width="4"/><circle cx="32" cy="54" r="3" fill="#f5f5fa"/>',
 "gong":   '<circle cx="32" cy="36" r="19" stroke-width="4"/><circle cx="32" cy="36" r="7" stroke-width="4"/><path d="M10 10h44" stroke-width="4"/>',
 "coin":   '<circle cx="32" cy="32" r="21" stroke-width="5"/><path d="M32 20v24M26 26h9a4 4 0 0 1 0 8H26" stroke-width="3"/>',
 "flame":  '<path d="M32 8c10 12 16 20 10 32a12 12 0 0 1-20 0c-4-8 4-14 6-20 2 4 4 4 4-12z" stroke-width="4"/>',
 "creak":  '<path d="M8 46h48M8 46l6-12h36l6 12M22 34v12M42 34v12" stroke-width="4"/>',
 "cuffs":  '<circle cx="20" cy="36" r="12" stroke-width="5"/><circle cx="44" cy="36" r="12" stroke-width="5"/><path d="M28 30h8" stroke-width="4"/>',
 "key":    '<circle cx="22" cy="24" r="10" stroke-width="5"/><path d="M29 31l22 22M42 44l6-6M48 50l6-6" stroke-width="5"/>',
 "scream": '<ellipse cx="32" cy="28" rx="16" ry="20" stroke-width="4"/><ellipse cx="25" cy="23" rx="3" ry="4" fill="#f5f5fa"/><ellipse cx="39" cy="23" rx="3" ry="4" fill="#f5f5fa"/><ellipse cx="32" cy="37" rx="5" ry="8" fill="#f5f5fa"/>',
 "blob":   '<path d="M20 44c-8-4-8-16 0-20 2-10 14-14 20-6 10-2 16 8 10 16 4 8-4 16-12 12-6 6-16 4-18-2z" stroke-width="4"/><circle cx="28" cy="32" r="3" fill="#f5f5fa"/><circle cx="38" cy="38" r="2" fill="#f5f5fa"/>',
 "slash":  '<path d="M14 50L50 14" stroke-width="6"/><path d="M22 54L54 22M10 42L42 10" stroke-width="3" opacity=".6"/>',
 "sword":  '<path d="M32 8v34M24 42h16M32 42v12" stroke-width="5"/><path d="M28 14l4-6 4 6" stroke-width="3"/>',
 "stab":   '<path d="M12 52L46 18" stroke-width="5"/><path d="M46 18l6-10 2 12z" fill="#f5f5fa" stroke-width="2"/>',
 "punch":  '<path d="M18 28h24a6 6 0 0 1 6 6v8a8 8 0 0 1-8 8H24a8 8 0 0 1-8-8V30z" stroke-width="4"/><path d="M26 28v-6M34 28v-8M42 28v-6" stroke-width="4"/>',
 "club":   '<path d="M20 52L44 16" stroke-width="7"/><circle cx="46" cy="14" r="8" fill="#f5f5fa" stroke-width="2"/>',
 "gun":    '<path d="M10 26h36v10H26l-2 14h-8l2-14h-8z" fill="#f5f5fa" stroke-width="2"/><path d="M50 22l6-4M52 30h6M50 38l6 4" stroke-width="3"/>',
 "burst":  '<path d="M8 20h20M8 32h28M8 44h20" stroke-width="5"/><path d="M38 18l10 14-10 14" stroke-width="5"/>',
 "reload": '<path d="M46 22a16 16 0 1 0 2 14" stroke-width="5"/><path d="M48 10v14H34" stroke-width="5"/>',
 "arrow":  '<path d="M10 54L52 12M52 12v14M52 12H38" stroke-width="5"/><path d="M10 54l-2-10M10 54l10-2" stroke-width="3"/>',
 "roar":   '<path d="M10 38c0-14 10-22 22-22s22 8 22 22M10 38l8 6 6-6 8 8 8-8 6 6 8-6" stroke-width="4"/>',
 "claws":  '<path d="M16 10l8 44M30 8l6 46M44 10l4 42" stroke-width="5"/>',
 "steps":  '<ellipse cx="24" cy="22" rx="8" ry="12" fill="#f5f5fa"/><ellipse cx="42" cy="44" rx="8" ry="12" fill="#f5f5fa"/>',
 "wings":  '<path d="M32 46C24 30 14 24 6 24c4 12 12 20 26 22zM32 46c8-16 18-22 26-22-4 12-12 20-26 22z" fill="#f5f5fa" stroke-width="2"/>',
 "burrow": '<path d="M8 46h48M14 46c0-12 8-20 18-20s18 8 18 20" stroke-width="5"/><path d="M32 26V10M24 16l8-8 8 8" stroke-width="4"/>',
 "door-open":  '<path d="M16 10h24v44H16z" stroke-width="4"/><path d="M40 12l12 6v34l-12 2" stroke-width="4"/><circle cx="34" cy="34" r="2.5" fill="#f5f5fa"/>',
 "door-close": '<path d="M16 10h32v44H16z" stroke-width="4"/><path d="M32 10v44" stroke-width="3" opacity=".6"/><circle cx="38" cy="34" r="2.5" fill="#f5f5fa"/>',
 "lock":   '<rect x="16" y="28" width="32" height="24" rx="4" fill="#f5f5fa" stroke-width="2"/><path d="M22 28v-8a10 10 0 0 1 20 0v8" stroke-width="5"/>',
 "potion": '<path d="M26 8h12M28 8v14L16 46a6 6 0 0 0 6 10h20a6 6 0 0 0 6-10L36 22V8" stroke-width="4"/><path d="M22 40h20" stroke-width="3" opacity=".7"/>',
 "thunder":'<path d="M14 40a10 10 0 0 1 2-19 14 14 0 0 1 27-2 10 10 0 0 1 5 21z" stroke-width="4"/><path d="M34 34l-6 10h8l-6 12" stroke-width="4"/>',
 "lightning": '<path d="M38 6L16 36h14l-6 22 24-32H34z" fill="#f5f5fa" stroke-width="2"/>',
}

def ascii_slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def foundry_id(semente):
    n = int(hashlib.sha1(semente.encode()).hexdigest(), 16)
    alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    saida = ""
    while len(saida) < 16:
        n, r = divmod(n, len(alfabeto)); saida += alfabeto[r]
    return saida

def icone(cor, glifo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">'
            f'<rect width="64" height="64" rx="12" fill="{cor}"/>'
            f'<rect x="2.5" y="2.5" width="59" height="59" rx="10" fill="none" stroke="#ffffff" stroke-opacity=".35" stroke-width="3"/>'
            f'<g fill="none" stroke="#f5f5fa" stroke-linecap="round" stroke-linejoin="round">{glifo}</g></svg>')

def macro(nome, ficheiro):
    return f"""/* {nome} — Tiago's Toolkit: Sons */
foundry.audio.AudioHelper.play(
  {{ src: "{FORGE}{ficheiro}.mp3", volume: 0.8, autoplay: true, loop: false, channel: "interface" }}, true);
"""

def main():
    for d in ("packs/_source/sons", "icons", "audio"):
        shutil.rmtree(os.path.join(RAIZ, d), ignore_errors=True)
    for d in ("packs/_source/sons", "icons"):
        os.makedirs(os.path.join(RAIZ, d))
    src = os.path.join(RAIZ, "packs/_source/sons")
    stats = {"systemId": None, "systemVersion": None, "coreVersion": None,
             "createdTime": None, "modifiedTime": None, "lastModifiedBy": None}

    for n, (nome, glifo, ficheiro) in enumerate(SONS):
        slug = ascii_slug(nome)
        mid = foundry_id(f"{MODULO_ID}:{slug}")
        open(os.path.join(RAIZ, "icons", f"{slug}.svg"), "w", encoding="utf-8").write(icone(COR, GLIFOS[glifo]))
        doc = {"_id": mid, "name": nome, "type": "script", "img": f"modules/{MODULO_ID}/icons/{slug}.svg",
               "scope": "global", "command": macro(nome, ficheiro), "folder": None,
               "sort": (n + 1) * 1000, "ownership": {"default": 0},
               "flags": {MODULO_ID: {"slug": slug, "ficheiro": ficheiro, "versao": VERSAO}},
               "_stats": stats, "_key": f"!macros!{mid}"}
        json.dump(doc, open(f"{src}/{slug}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    os.makedirs(os.path.join(RAIZ, "scripts"), exist_ok=True)
    open(os.path.join(RAIZ, "scripts/main.js"), "w", encoding="utf-8").write(
        "// Pré-carrega os sons para o primeiro clique já sair sem atraso. (gerado por build/gerar.py)\n"
        f"const SONS = {json.dumps([FORGE + f + '.mp3' for _, _, f in SONS])};\n"
        "Hooks.once(\"ready\", () => {\n"
        "  for (const s of SONS) foundry.audio.AudioHelper.preloadSound(s).catch(() => {});\n"
        "});\n")

    modulo = {
        "id": MODULO_ID, "title": "Tiago's Toolkit: Sons",
        "description": "Compêndio de macros de um clique que tocam um som para toda a mesa: pistola, soco, lâmina, carne, descarga, grito, porta, passos. Arrasta do compêndio para a hotbar e clica.",
        "version": VERSAO, "compatibility": {"minimum": "13", "verified": "14"},
        "authors": [{"name": "Th1rdo"}],
        "esmodules": ["scripts/main.js"],
        "packs": [{"name": "sons", "label": "Tiago's Toolkit — Sons", "path": "packs/sons", "type": "Macro",
                   "ownership": {"PLAYER": "OBSERVER", "TRUSTED": "OBSERVER", "ASSISTANT": "OWNER", "GAMEMASTER": "OWNER"},
                   "flags": {}}],
        "url": GH, "manifest": f"{GH}/releases/latest/download/module.json",
        "download": f"{GH}/releases/download/v{VERSAO}/{MODULO_ID}.zip", "readme": f"{GH}#readme",
    }
    json.dump(modulo, open(os.path.join(RAIZ, "module.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{len(SONS)} sons")

if __name__ == "__main__":
    main()
