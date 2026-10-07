# -*- coding: utf-8 -*-
"""Gera o módulo «Tiago's Toolkit: Sons»: macros de um clique (Sequencer + PSFX) num compêndio.
Edita SONS abaixo, corre este script e depois `node build/compilar.mjs`."""
import os, re, json, shutil, hashlib, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULO_ID = "tiagos-toolkit-sons"
VERSAO = "0.1.0"
GH = "https://github.com/Th1rdo/tiagos-toolkit-sons"
FONTE_PSFX = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/foundryRevision/04 Assets/_fonte/psfx-dbpaths.txt")

PASTAS = {  # nome -> (cor do ícone, cor da pasta)
    "Combate":  "#B1161A",
    "Criaturas": "#3F6B3A",
    "Mundo":    "#2F5D8A",
}

# cada camada: (dbPath do PSFX, volume, atraso em ms[, duração máx. em ms])
# regra: até 3 camadas; prefixo parcial sorteia uma variante (cada clique soa diferente)
SONS = [
 # ---- Combate
 ("Combate", "Corte",        "slash",  [("psfx.weapon-swooshes.light.v1", .7, 0), ("psfx.impacts.slashing.v1", .9, 90)]),
 ("Combate", "Espadada",     "sword",  [("psfx.weapon-swooshes.heavy.v1", .7, 0), ("psfx.weapon-attacks.sword.v1", .9, 110)]),
 ("Combate", "Estocada",     "stab",   [("psfx.weapon-attacks.spear.v1", 1, 0), ("psfx.impacts.slashing.v1", .6, 120)]),
 ("Combate", "Soco",         "punch",  [("psfx.weapon-swooshes.light.v1", .45, 0), ("psfx.impacts.bludgeoning.v1", 1, 100)]),
 ("Combate", "Pancada",      "club",   [("psfx.weapon-swooshes.heavy.v1", .6, 0), ("psfx.impacts.bludgeoning.v1", 1, 130)]),
 ("Combate", "Tiro",         "gun",    [("psfx.ranged-weapons.guns.single-fire.revolver", 1, 0)]),
 ("Combate", "Rajada",       "burst",  [("psfx.ranged-weapons.guns.single-fire.revolver.0", 1, 0),
                                       ("psfx.ranged-weapons.guns.single-fire.revolver.2", .95, 170),
                                       ("psfx.ranged-weapons.guns.single-fire.revolver.4", .9, 340)]),
 ("Combate", "Recarregar",   "reload", [("psfx.ranged-weapons.guns.prepare.revolver", .9, 0)]),
 ("Combate", "Flecha",       "arrow",  [("psfx.ranged-weapons.longbow.v1", 1, 0)]),
 # ---- Criaturas
 ("Criaturas", "Rugido",     "roar",   [("psfx.creature.dragons.roar.small", 1, 0)]),
 ("Criaturas", "Garras",     "claws",  [("psfx.weapon-swooshes.heavy.v1", .5, 0), ("psfx.creature.dragons.attacks.rend", .9, 90)]),
 ("Criaturas", "Passos",     "steps",  [("psfx.creature.movement.footsteps.outdoors.001.sequence", .9, 0, 3500)]),
 ("Criaturas", "Asas",       "wings",  [("psfx.creature.movement.flight.wings.small", .9, 0)]),
 ("Criaturas", "Emergir do chão", "burrow", [("psfx.creature.movement.burrow.breach", 1, 0)]),
 # ---- Mundo
 ("Mundo", "Abrir porta",    "door-open",  [("psfx.doors.clean.open.wooden.01", 1, 0)]),
 ("Mundo", "Fechar porta",   "door-close", [("psfx.doors.clean.close.wooden.01", 1, 0)]),
 ("Mundo", "Trancar porta",  "lock",       [("psfx.doors.clean.lock.wooden.01", 1, 0)]),
 ("Mundo", "Beber frasco",   "potion",     [("psfx.consumables.potions-vials.cork-bottle", .8, 0), ("psfx.consumables.potions-vials.drink-liquid", .9, 500)]),
 ("Mundo", "Trovão",         "thunder",    [("psfx.cantrips.thunderclap", 1, 0)]),
 ("Mundo", "Relâmpago",      "lightning",  [("psfx.impacts.magicaleffects.lightning", 1, 0), ("psfx.cantrips.thunderclap", .7, 350)]),
]

# glifos 64x64, traço claro sobre o cartão da pasta
GLIFOS = {
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

def camada_js(c):
    caminho, vol, atraso, *resto = c
    s = f'seq.sound().file("{caminho}").volume({vol})'
    if atraso: s += f'.delay({atraso})'
    if resto: s += f'.duration({resto[0]}).fadeOutAudio(400)'
    return s + ';'

def macro(nome, camadas):
    caminhos = [c[0] for c in camadas]
    return f'''/* {nome} — Tiago's Toolkit: Sons */
const CAMINHOS = {json.dumps(caminhos)};

if (!game.modules.get("sequencer")?.active)
  return ui.notifications.warn("Este som precisa do módulo Sequencer ativo.");
if (!game.modules.get("psfx")?.active)
  return ui.notifications.warn("Este som precisa do módulo PSFX ativo.");
if (!CAMINHOS.every(c => Sequencer.Database.entryExists(c)))
  return ui.notifications.warn("Este som não foi encontrado no PSFX. Atualize o módulo PSFX.");

const seq = new Sequence();
{chr(10).join(camada_js(c) for c in camadas)}
seq.play();
'''

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

    verificar([c[0] for s in SONS for c in s[3]])

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
        "description": "Compêndio de macros de um clique que tocam sons do PSFX para toda a mesa: cortes, socos, tiros, portas, trovões, rugidos. Arrasta do compêndio para a hotbar e clica.",
        "version": VERSAO, "compatibility": {"minimum": "13", "verified": "14"},
        "authors": [{"name": "Th1rdo"}],
        "packs": [{"name": "sons", "label": "Tiago's Toolkit — Sons", "path": "packs/sons", "type": "Macro",
                   "ownership": {"PLAYER": "OBSERVER", "TRUSTED": "OBSERVER", "ASSISTANT": "OWNER", "GAMEMASTER": "OWNER"},
                   "flags": {}}],
        "relationships": {"requires": [{"id": "sequencer", "type": "module", "compatibility": {}},
                                       {"id": "psfx", "type": "module", "compatibility": {}}]},
        "url": GH, "manifest": f"{GH}/releases/latest/download/module.json",
        "download": f"{GH}/releases/download/v{VERSAO}/{MODULO_ID}.zip", "readme": f"{GH}#readme",
    }
    json.dump(modulo, open(os.path.join(RAIZ, "module.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{len(SONS)} sons · {len(PASTAS)} pastas")

if __name__ == "__main__":
    main()
