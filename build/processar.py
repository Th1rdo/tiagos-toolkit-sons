# -*- coding: utf-8 -*-
"""Trata os sons do Tiago (~/Downloads/sound effects) para o Forge: só o áudio (sem capa nem metadados), silêncio
cortado no início e no fim, todos ao mesmo volume percebido (-16 LUFS, pico -1 dB; loudnorm em duas passagens).
Os que têm picos que travam o loudnorm (porta, passos) sobem com um limitador suave — ver o fim do ficheiro.
Saída: build/saida/*.mp3 → enviar com forge-enviar.py para MAIN/AKRASIA/Sons/Efeitos/. Não vão no repositório."""
import subprocess, json, os, glob
SRC=os.path.expanduser("~/Downloads/sound effects")
NOMES={"heavy steps":"passos-pesados","punch":"soco","man death scream":"grito-de-morte","flesh being cut":"carne-cortada",
 "footsteps":"passos","electric discharge":"descarga-eletrica","opening door":"abrir-porta","flesh growing":"carne-a-crescer",
 "slash and swing":"golpe-de-lamina","pistol":"pistola"}
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"saida"); os.makedirs(OUT, exist_ok=True)
CORTE="silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08,areverse"
for f in sorted(glob.glob(os.path.join(SRC,"*.mp3"))):
    base=os.path.splitext(os.path.basename(f))[0]; out=os.path.join(OUT, NOMES[base]+".mp3")
    r=subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",f,"-map","0:a","-af",CORTE+",loudnorm=I=-16:TP=-1:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True).stderr
    m=json.loads(r[r.rindex("{"):r.rindex("}")+1])
    ln=f"loudnorm=I=-16:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    subprocess.run(["ffmpeg","-v","error","-y","-i",f,"-map","0:a","-map_metadata","-1","-af",CORTE+","+ln+",aresample=44100",
                    "-c:a","libmp3lame","-q:a","2","-id3v2_version","0",out],check=True)
    print(f"{base:22s} → {out}")

# 2.ª volta: quem ficou longe de -16 LUFS sobe/desce com limitador (duas vezes chega)
import re
def lufs(f):
    r=subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",f,"-af","ebur128","-f","null","-"],capture_output=True,text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
for _ in range(2):
    for f in sorted(glob.glob(os.path.join(OUT,"*.mp3"))):
        g=round(-16-lufs(f),2)
        if abs(g)<=0.4: continue
        t=f+".t.mp3"
        subprocess.run(["ffmpeg","-v","error","-y","-i",f,"-af",f"volume={g}dB,alimiter=limit=0.89:attack=3:release=60:level=disabled",
                        "-c:a","libmp3lame","-q:a","2","-id3v2_version","0",t],check=True)
        os.replace(t,f)
for f in sorted(glob.glob(os.path.join(OUT,"*.mp3"))): print(f"{os.path.basename(f):24s} {lufs(f):6.1f} LUFS")
