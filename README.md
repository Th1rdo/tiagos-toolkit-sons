# Tiago's Toolkit: Sons

Compêndio **Tiago's Toolkit — Sons**: macros de um clique que tocam um som (ou duas camadas) do PSFX
para toda a mesa. Arrasta do compêndio para a hotbar e clica. Cada clique sorteia uma variante.

**Precisa de:** Sequencer + PSFX.

| Pasta | Sons |
|---|---|
| Combate | Corte, Espadada, Estocada, Soco, Pancada, Tiro, Rajada, Recarregar, Flecha |
| Criaturas | Rugido, Garras, Passos, Asas, Emergir do chão |
| Mundo | Abrir porta, Fechar porta, Trancar porta, Beber frasco, Trovão, Relâmpago |

## Instalar
Manifest: `https://github.com/Th1rdo/tiagos-toolkit-sons/releases/latest/download/module.json`

## Acrescentar um som
Editar a lista `SONS` em `build/gerar.py` (dbPaths conferidos contra o PSFX no build), depois `npm run build`.
Id do módulo: `tiagos-toolkit-sons` (nunca muda).
