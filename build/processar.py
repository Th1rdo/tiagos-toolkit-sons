# -*- coding: utf-8 -*-
"""Corta, filtra e normaliza as gravações em build/fontes/ → audio/*.mp3 (mono, ~-1 dB de pico).
Fontes (todas no OpenGameArt): ver CREDITOS no README. Correr antes de gerar.py quando se muda um clip."""
import os, re, subprocess, shutil

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, "build/fontes")
OUT = os.path.join(RAIZ, "audio")

def v(p): return os.path.join(F, p)

# nome -> (entradas [(ficheiro, início, duração)], filtro; "[0:a]" = 1ª entrada ... vazio = só cortar)
# o filtro termina sempre no rótulo [o]; sem filtro usa-se fade-out final automático
CLIPS = {}

PRE = 0.09  # as gravações têm ~100 ms de ar antes do disparo

def corte(nome, fonte, ini, dur, fade=0.25, filtro=""):
    CLIPS[nome] = ([(fonte, ini, dur)], f"[0:a]{filtro + ',' if filtro else ''}afade=t=out:st={dur - fade}:d={fade}[o]")

for i, t in enumerate([2.72, 4.27, 5.77], 1): corte(f"pistola-{i}", v("tabasco/cz.wav"), t + PRE, 1.0, .4)
for i, t in enumerate([3.47, 5.87, 8.77], 1): corte(f"rifle-{i}", v("tabasco/mosin.wav"), t + PRE, 1.6, .6)
for i, t in enumerate([2.22, 5.92, 7.62, 9.62], 1): corte(f"fuzil-{i}", v("tabasco/sks.wav"), t + PRE, 1.1, .5)
corte("espingarda-1", v("tabasco/shotty.wav"), 0, .7, .3)

# tiro silenciado: estalo abafado (passa-baixo) + «pff» de ar + clack mecânico — sintetizado a partir dos tiros reais
for i, t in enumerate([2.72, 4.27, 5.77], 1):
    ar = "vehicle/compressed-air-spray-01.wav" if i != 2 else "vehicle/compressed-air-spray-02.wav"
    CLIPS[f"silenciado-{i}"] = (
        [(v("tabasco/cz.wav"), t + PRE, .45), (v(ar), 0, .35), (v("vehicle/handcuffs-metal-lock-01.wav"), 0, .12)],
        "[0:a]highpass=f=140,lowpass=f=1700,volume=0.9,afade=t=out:st=0.25:d=0.2[a];"
        "[1:a]highpass=f=1800,volume=0.45,afade=t=out:st=0.2:d=0.15[b];"
        "[2:a]volume=0.35,adelay=70|70[c];"
        "[a][b][c]amix=inputs=3:normalize=0,afade=t=out:st=0.35:d=0.1[o]")

for i in range(1, 6): corte(f"soco-{i}", v(f"qubodup/qubodupPunch0{i}.ogg"), 0, .5, .1)
for i in range(1, 5): corte(f"pancada-{i}", v(f"rubberduck/hit_0{i}.ogg"), 0, .42, .1, "equalizer=f=120:g=5")
for i in range(1, 6): corte(f"lamina-{i}", v(f"vehicle/sword-clash-0{i}.wav"), 0, 1.0, .5)
corte("sacar-lamina-1", v("vehicle/knife-unsheathe-02.wav"), 0, .47, .1)
corte("sacar-lamina-2", v("vehicle/seax-unsheathe-01.wav"), 0, .49, .1)
for i in (1, 2): corte(f"corte-{i}", v(f"vehicle/tube-plastic-whoosh-0{i}.wav"), 0, .33, .08, "volume=1.4")
for i in (1, 2, 3): corte(f"facada-{i}", v(f"vehicle/apple-cut-0{i}.wav"), 0, .48, .1, "equalizer=f=140:g=6,volume=1.3")
corte("flecha-1", v("vehicle/arrow-feathers-01.wav"), 0, .53, .1)
for i in (1, 2): corte(f"taser-{i}", v(f"vehicle/paralyzer-discharge-0{i}.wav"), 0, .9, .3)
CLIPS["explosao-1"] = ([(v("rubberduck/explosion.ogg"), 0, .56)],
    "[0:a]asetrate=33075,aresample=44100,lowpass=f=3500,aecho=0.8:0.6:90|180:0.35|.2,afade=t=out:st=0.9:d=0.5[o]")

corte("porta-abrir-1", v("rubberduck/door_open.ogg"), 0, .45, .1)
for i in range(1, 5): corte(f"porta-fechar-{i}", v(f"rubberduck/door_close_0{i}.ogg"), 0, .85 if i == 2 else .5, .1)
corte("porta-ranger-1", v("rubberduck/door_01.ogg"), 0, 2.7, .4, "volume=3")
corte("porta-ranger-2", v("rubberduck/door_02.ogg"), 0, 2.6, .4, "volume=3.5")
corte("chave-1", v("vehicle/keyhole-lockbox-turn-01.wav"), 0, .9, .15)
corte("chave-2", v("rubberduck/key_open_01.ogg"), 0, .43, .1)
for i in (1, 2): corte(f"algemas-{i}", v(f"vehicle/handcuffs-metal-lock-0{i}.wav"), 0, .6 if i == 1 else .78, .1)
for i in range(1, 6): corte(f"vidro-{i}", v(f"rubberduck/glass_0{i}.ogg"), 0, .95 if i > 3 else .4, .1)
for i in (1, 2, 3): corte(f"sino-{i}", v(f"rubberduck/bell_0{i}.ogg"), 0, [1.29, .53, 1.78][i - 1], .3)
for i in (1, 2): corte(f"gongo-{i}", v(f"rubberduck/gong_0{i}.ogg"), 0, 1.2, .5)
corte("frasco-1", v("vehicle/vial-glass-uncork-01.wav"), 0, .5, .1)
corte("frasco-2", v("vehicle/water-pour-01.wav"), 0, 1.2, .4)
corte("moedas-1", v("vehicle/coinflip-01.wav"), 0, .35, .08)
corte("moedas-2", v("vehicle/coins-shake-01.wav"), 0, 1.1, .3)
corte("isqueiro-1", v("vehicle/lighter-light-01.wav"), 0, .32, .08)
corte("fosforo-1", v("vehicle/match-light-01.wav"), 0, .75, .2)
corte("rangido-1", v("vehicle/floor-creak-01.wav"), 0, .64, .15)
for i in (1, 2, 3): corte(f"passos-{i}", v(f"vehicle/mud-steps-0{i}.wav"), 0, [3.0, 2.4, 1.3][i - 1], .4)
corte("pagina-1", v("vehicle/book-page-01.wav"), 0, 1.4, .3)

def pico(caminho):
    s = subprocess.run(["ffmpeg", "-nostats", "-i", caminho, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = re.search(r"max_volume: (-?[\d.]+) dB", s)
    return float(m.group(1)) if m else 0.0

def main():
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    tmp = os.path.join(OUT, "_t.wav")
    for nome, (entradas, filtro) in CLIPS.items():
        cmd = ["ffmpeg", "-v", "error", "-y"]
        for f, ini, dur in entradas:
            cmd += ["-ss", str(ini), "-t", str(dur), "-i", f]
        cmd += ["-filter_complex", filtro, "-map", "[o]", "-ac", "1", "-ar", "44100", tmp]
        subprocess.run(cmd, check=True)
        ganho = -1.0 - pico(tmp)                      # pico final em -1 dB
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"volume={ganho:0.2f}dB",
                        "-c:a", "libmp3lame", "-q:a", "3", os.path.join(OUT, nome + ".mp3")], check=True)
    os.remove(tmp)
    tot = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print(f"{len(CLIPS)} clips · {tot/1e6:0.2f} MB")

if __name__ == "__main__":
    main()
