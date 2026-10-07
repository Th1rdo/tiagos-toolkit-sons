# -*- coding: utf-8 -*-
"""Gera o módulo «Tiago's Toolkit: Sons»: macros de um clique (Sequencer + PSFX) num compêndio.
Edita SONS abaixo, corre este script e depois `node build/compilar.mjs`."""
import os, re, json, shutil, hashlib, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULO_ID = "tiagos-toolkit-sons"
VERSAO = "0.2.0"
GH = "https://github.com/Th1rdo/tiagos-toolkit-sons"
FONTE_PSFX = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/foundryRevision/04 Assets/_fonte/psfx-dbpaths.txt")

PASTAS = {  # nome -> cor do ícone
    "Armas de fogo": "#B1161A",
    "Corpo a corpo": "#8A4B1F",
    "Criaturas": "#3F6B3A",
    "Mundo":    "#2F5D8A",
}

# camada de ficheiro:  ("a", [clips...], volume, atraso_ms)  → um clip sorteado de audio/<clip>.mp3
# camada de PSFX:      ("p", dbPath, volume, atraso_ms[, duração_ms]) → prefixo parcial sorteia variante
# regra: até 3 camadas por macro
def n(base, k): return [f"{base}-{i}" for i in range(1, k + 1)]

SONS = [
 # ---- Armas de fogo
 ("Armas de fogo", "Pistola",         "gun",      [("a", n("pistola", 3), 1, 0)]),
 ("Armas de fogo", "Revólver",        "gun",      [("p", "psfx.ranged-weapons.guns.single-fire.revolver", 1, 0)]),
 ("Armas de fogo", "Tiro silenciado", "silencer", [("a", n("silenciado", 3), 1, 0)]),
 ("Armas de fogo", "Rifle",           "rifle",    [("a", n("rifle", 3), 1, 0)]),
 ("Armas de fogo", "Fuzil",           "rifle",    [("a", n("fuzil", 4), 1, 0)]),
 ("Armas de fogo", "Espingarda",      "shotgun",  [("a", ["espingarda-1"], 1, 0)]),
 ("Armas de fogo", "Rajada",          "burst",    [("a", n("fuzil", 4), 1, 0), ("a", n("fuzil", 4), .9, 150), ("a", n("fuzil", 4), .85, 300)]),
 ("Armas de fogo", "Recarregar",      "reload",   [("p", "psfx.ranged-weapons.guns.prepare.revolver", .9, 0)]),
 ("Armas de fogo", "Explosão",        "explosion",[("a", ["explosao-1"], 1, 0)]),
 # ---- Corpo a corpo
 ("Corpo a corpo", "Soco",            "punch",    [("a", n("soco", 5), 1, 0)]),
 ("Corpo a corpo", "Pancada",         "club",     [("a", n("pancada", 4), 1, 0)]),
 ("Corpo a corpo", "Corte",           "slash",    [("a", n("corte", 2), .9, 0), ("a", n("facada", 3), .6, 90)]),
 ("Corpo a corpo", "Facada",          "stab",     [("a", n("facada", 3), 1, 0)]),
 ("Corpo a corpo", "Choque de lâminas", "clash",  [("a", n("lamina", 5), .9, 0)]),
 ("Corpo a corpo", "Sacar lâmina",    "unsheathe",[("a", n("sacar-lamina", 2), .9, 0)]),
 ("Corpo a corpo", "Flecha",          "arrow",    [("p", "psfx.ranged-weapons.longbow.v1", 1, 0), ("a", ["flecha-1"], .8, 120)]),
 ("Corpo a corpo", "Taser",           "lightning",[("a", n("taser", 2), 1, 0)]),
 # ---- Criaturas
 ("Criaturas", "Rugido",           "roar",   [("p", "psfx.creature.dragons.roar.small", 1, 0)]),
 ("Criaturas", "Garras",           "claws",  [("p", "psfx.weapon-swooshes.heavy.v1", .5, 0), ("p", "psfx.creature.dragons.attacks.rend", .9, 90)]),
 ("Criaturas", "Passos",           "steps",  [("a", n("passos", 3), .9, 0)]),
 ("Criaturas", "Asas",             "wings",  [("p", "psfx.creature.movement.flight.wings.small", .9, 0)]),
 ("Criaturas", "Emergir do chão",  "burrow", [("p", "psfx.creature.movement.burrow.breach", 1, 0)]),
 # ---- Mundo
 ("Mundo", "Abrir porta",          "door-open",  [("a", ["porta-abrir-1"], 1, 0)]),
 ("Mundo", "Fechar porta",         "door-close", [("a", n("porta-fechar", 4), 1, 0)]),
 ("Mundo", "Porta rangendo",       "door-open",  [("a", n("porta-ranger", 2), .9, 0)]),
 ("Mundo", "Trancar com chave",    "key",        [("a", n("chave", 2), 1, 0)]),
 ("Mundo", "Algemas",              "cuffs",      [("a", n("algemas", 2), 1, 0)]),
 ("Mundo", "Vidro quebrando",      "glass",      [("a", n("vidro", 5), 1, 0)]),
 ("Mundo", "Sino",                 "bell",       [("a", n("sino", 3), 1, 0)]),
 ("Mundo", "Gongo",                "gong",       [("a", n("gongo", 2), 1, 0)]),
 ("Mundo", "Beber frasco",         "potion",     [("a", ["frasco-1"], .9, 0), ("a", ["frasco-2"], .8, 450)]),
 ("Mundo", "Moedas",               "coin",       [("a", n("moedas", 2), 1, 0)]),
 ("Mundo", "Isqueiro",             "flame",      [("a", ["isqueiro-1"], 1, 0)]),
 ("Mundo", "Rangido do chão",      "creak",      [("a", ["rangido-1"], 1, 0)]),
 ("Mundo", "Trovão",               "thunder",    [("p", "psfx.cantrips.thunderclap", 1, 0)]),
 ("Mundo", "Relâmpago",            "lightning",  [("p", "psfx.impacts.magicaleffects.lightning", 1, 0), ("p", "psfx.cantrips.thunderclap", .7, 350)]),
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

def macro(nome, camadas):
    psfx = [c for c in camadas if c[0] == "p"]
    out = [f"/* {nome} — Tiago's Toolkit: Sons */"]
    if psfx:
        out += [f"const CAMINHOS = {json.dumps([c[1] for c in psfx])};", "",
                'if (!game.modules.get("sequencer")?.active)',
                '  return ui.notifications.warn("Este som precisa do módulo Sequencer ativo.");',
                'if (!game.modules.get("psfx")?.active)',
                '  return ui.notifications.warn("Este som precisa do módulo PSFX ativo.");',
                'if (!CAMINHOS.every(c => Sequencer.Database.entryExists(c)))',
                '  return ui.notifications.warn("Este som não foi encontrado no PSFX. Atualize o módulo PSFX.");', ""]
    if any(c[0] == "a" for c in camadas):
        out += [f'const PASTA = "modules/{MODULO_ID}/audio/";',
                'const sorteia = l => l[Math.floor(Math.random() * l.length)];',
                'const toca = (clips, volume) => foundry.audio.AudioHelper.play(',
                '  { src: `${PASTA}${sorteia(clips)}.mp3`, volume, autoplay: true, loop: false, channel: "interface" }, true);', ""]
    if psfx: out.append("const seq = new Sequence();")
    for c in camadas:
        if c[0] == "a":
            _, clips, vol, atraso = c
            chamada = f"toca({json.dumps(clips)}, {vol})"
            out.append(f"setTimeout(() => {chamada}, {atraso});" if atraso else chamada + ";")
        else:
            _, caminho, vol, atraso, *resto = c
            l = f'seq.sound().file("{caminho}").volume({vol})'
            if atraso: l += f".delay({atraso})"
            if resto: l += f".duration({resto[0]}).fadeOutAudio(400)"
            out.append(l + ";")
    if psfx: out.append("seq.play();")
    return "\n".join(out) + "\n"

def conferir_audio():
    for _, nome, _, camadas in SONS:
        for c in camadas:
            if c[0] == "a":
                for clip in c[1]:
                    if not os.path.exists(os.path.join(RAIZ, "audio", clip + ".mp3")):
                        raise SystemExit(f"{nome}: falta audio/{clip}.mp3")

def verificar(todos):
    if not os.path.exists(FONTE_PSFX):
        print("(sem psfx-dbpaths.txt local: verificação de dbPaths saltada)"); return
    linhas = open(FONTE_PSFX, encoding="utf-8").read().split()
    for c in todos:
        if not any(l == c or l.startswith(c + ".") for l in linhas):
            raise SystemExit(f"dbPath inexistente: {c}")
    print(f"{len(set(todos))} dbPaths conferidos contra o PSFX")

def main():
    for d in ("packs/_source/sons", "icons"):
        shutil.rmtree(os.path.join(RAIZ, d), ignore_errors=True)
        os.makedirs(os.path.join(RAIZ, d))
    src = os.path.join(RAIZ, "packs/_source/sons")
    stats = {"systemId": None, "systemVersion": None, "coreVersion": None,
             "createdTime": None, "modifiedTime": None, "lastModifiedBy": None}

    verificar([c[1] for s in SONS for c in s[3] if c[0] == "p"])
    conferir_audio()

    ids_pasta = {}
    for i, (nome, cor) in enumerate(PASTAS.items()):
        pid = foundry_id(f"{MODULO_ID}:pasta:{nome}")
        ids_pasta[nome] = pid
        doc = {"_id": pid, "name": nome, "type": "Macro", "folder": None, "sorting": "m",
               "sort": (i + 1) * 100000, "color": cor, "description": "", "flags": {},
               "_stats": stats, "_key": f"!folders!{pid}"}
        json.dump(doc, open(f"{src}/_pasta-{ascii_slug(nome)}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    for n, (pasta, nome, glifo, camadas) in enumerate(SONS):
        assert len(camadas) <= 3, nome
        slug = ascii_slug(nome)
        mid = foundry_id(f"{MODULO_ID}:{slug}")
        open(os.path.join(RAIZ, "icons", f"{slug}.svg"), "w", encoding="utf-8").write(icone(PASTAS[pasta], GLIFOS[glifo]))
        doc = {"_id": mid, "name": nome, "type": "script", "img": f"modules/{MODULO_ID}/icons/{slug}.svg",
               "scope": "global", "command": macro(nome, camadas), "folder": ids_pasta[pasta],
               "sort": (n + 1) * 1000, "ownership": {"default": 0},
               "flags": {MODULO_ID: {"slug": slug, "pasta": pasta, "versao": VERSAO}},
               "_stats": stats, "_key": f"!macros!{mid}"}
        json.dump(doc, open(f"{src}/{slug}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    modulo = {
        "id": MODULO_ID, "title": "Tiago's Toolkit: Sons",
        "description": "Compêndio de macros de um clique que tocam um som para toda a mesa: tiros (até com silenciador), socos, lâminas, portas, vidro, trovões, rugidos. Arrasta do compêndio para a hotbar e clica.",
        "version": VERSAO, "compatibility": {"minimum": "13", "verified": "14"},
        "authors": [{"name": "Th1rdo"}],
        "esmodules": ["scripts/main.js"],
        "packs": [{"name": "sons", "label": "Tiago's Toolkit — Sons", "path": "packs/sons", "type": "Macro",
                   "ownership": {"PLAYER": "OBSERVER", "TRUSTED": "OBSERVER", "ASSISTANT": "OWNER", "GAMEMASTER": "OWNER"},
                   "flags": {}}],
        "relationships": {"recommends": [{"id": "sequencer", "type": "module", "reason": "sons do PSFX (rugido, trovão…)"},
                                         {"id": "psfx", "type": "module", "reason": "sons do PSFX (rugido, trovão…)"}]},
        "url": GH, "manifest": f"{GH}/releases/latest/download/module.json",
        "download": f"{GH}/releases/download/v{VERSAO}/{MODULO_ID}.zip", "readme": f"{GH}#readme",
    }
    json.dump(modulo, open(os.path.join(RAIZ, "module.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    clips = sorted(f for f in os.listdir(os.path.join(RAIZ, "audio")) if f.endswith(".mp3"))
    os.makedirs(os.path.join(RAIZ, "scripts"), exist_ok=True)
    open(os.path.join(RAIZ, "scripts/main.js"), "w", encoding="utf-8").write(
        "// Pré-carrega os sons para o primeiro clique já sair sem atraso. (gerado por build/gerar.py)\n"
        f"const CLIPS = {json.dumps(clips)};\n"
        f"const PSFX = {json.dumps(sorted({c[1] for s in SONS for c in s[3] if c[0] == 'p'}))};\n"
        "Hooks.once(\"ready\", () => {\n"
        f"  for (const c of CLIPS) foundry.audio.AudioHelper.preloadSound(`modules/{MODULO_ID}/audio/${{c}}`).catch(() => {{}});\n"
        "  if (game.modules.get(\"sequencer\")?.active && game.modules.get(\"psfx\")?.active)\n"
        "    Sequencer.Preloader.preload(PSFX).catch(() => {});\n"
        "});\n")
    print(f"{len(SONS)} sons · {len(PASTAS)} pastas")

if __name__ == "__main__":
    main()
