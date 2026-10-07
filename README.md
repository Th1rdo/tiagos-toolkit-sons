# Tiago's Toolkit: Sons

Compêndio **Tiago's Toolkit — Sons**: macros de um clique que tocam um som (ou duas camadas) para toda a mesa.
Arrasta do compêndio para a hotbar e clica. Cada clique sorteia uma variante.

| Pasta | Sons |
|---|---|
| Armas de fogo | Pistola, Revólver, Tiro silenciado, Rifle, Fuzil, Espingarda, Rajada, Recarregar, Explosão |
| Corpo a corpo | Soco, Pancada, Corte, Facada, Choque de lâminas, Sacar lâmina, Flecha, Taser |
| Criaturas | Rugido, Garras, Passos, Asas, Emergir do chão |
| Mundo | Abrir/Fechar porta, Porta rangendo, Trancar com chave, Algemas, Vidro quebrando, Sino, Gongo, Beber frasco, Moedas, Isqueiro, Rangido do chão, Trovão, Relâmpago |

A maioria usa gravações reais incluídas no módulo (`audio/`, ~0,75 MB, pré-carregadas ao entrar no mundo).
Rugido, Garras, Asas, Emergir, Trovão, Relâmpago, Revólver, Recarregar e Flecha usam o **PSFX** (com Sequencer) —
sem esses dois módulos essas macros avisam e não tocam; as outras funcionam sozinhas.

## Instalar
Manifest: `https://github.com/Th1rdo/tiagos-toolkit-sons/releases/latest/download/module.json`

## Acrescentar um som
1. Pôr a gravação em `build/fontes/` e descrever o corte em `build/processar.py` → `python3 build/processar.py`
   (corta, tira o silêncio inicial, normaliza, gera MP3).
2. Acrescentar a linha em `SONS` em `build/gerar.py` → `npm run build`.

O `id` do módulo é `tiagos-toolkit-sons` (nunca muda).
O **Tiro silenciado** é sintetizado: tiro real da pistola filtrado (passa-baixo) + «pff» de ar comprimido + clack metálico.

## Créditos (todos do OpenGameArt)
- **Tiros** (pistola CZ-52, Mosin Nagant, SKS, espingarda) — *Gunshot Sounds*, Tabasco. A página indica CC0; o ficheiro
  incluído cita «Vincent Sevedge, CC BY 3.0» — por isso fica o crédito aqui.
- **Socos** — *Punch*, Iwan «qubodup» Gabovitch, CC0.
- **Lâminas, facas, flecha, passos, frascos, chaves, algemas, moedas, isqueiro, taser, chão** — *Fantasy Sound Effects (Tinysized SFX)*, Vehicle, CC0.
- **Portas, vidro, sinos, gongos, pancadas, explosão** — *100 CC0 SFX*, rubberduck, CC0.
