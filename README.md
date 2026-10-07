# Tiago's Toolkit: Sons

Compêndio **Tiago's Toolkit — Sons**: macros de um clique que tocam um som para toda a mesa.
Arrasta do compêndio para a hotbar e clica.

Pistola · Soco · Golpe de lâmina · Carne cortada · Carne a crescer · Descarga elétrica · Grito de morte ·
Abrir porta · Passos · Passos pesados

Os sons são os do Tiago, tratados por `build/processar.py` (só o áudio, silêncio cortado no início e no fim,
todos a −16 LUFS) e guardados no Forge dele (`MAIN/AKRASIA/Sons/Efeitos/`). **Não vão no módulo**: as macros
tocam-nos de lá, e o módulo pré-carrega-os ao entrar no mundo. Noutra mesa, as macros não têm som.

## Instalar
Manifest: `https://github.com/Th1rdo/tiagos-toolkit-sons/releases/latest/download/module.json`

## Acrescentar um som
1. Pôr o ficheiro em `~/Downloads/sound effects`, dar-lhe um nome em `NOMES` (`build/processar.py`) e correr
   `python3 build/processar.py` → `build/saida/`.
2. `python3 ~/tiagos-toolkit-ferramentas/forge-enviar.py build/saida "MAIN/AKRASIA/Sons/Efeitos"`.
3. Acrescentar a linha em `SONS` (`build/gerar.py`) → `npm run build`.

O `id` do módulo é `tiagos-toolkit-sons` (nunca muda).
