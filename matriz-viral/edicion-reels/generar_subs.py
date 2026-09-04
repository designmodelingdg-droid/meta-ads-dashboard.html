# Genera subtitulos ASS estilo reel DMA sincronizados al timeline editado
# Offsets: final = src + offset por segmento (medidos de los intermedios)
AMBER = r"{\c&H4AA0E8&}"   # #E8A04A en BGR
WHITE = r"{\c&HFFFFFF&}"
POP = r"{\fscx85\fscy85\t(0,90,\fscx100\fscy100)}"

def t(sec):
    h = int(sec // 3600); m = int(sec % 3600 // 60); s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# (inicio_final, fin_final, texto)  — tiempos ya mapeados al timeline editado
# hook: H1 final=src ; H2 final=src-0.3167
# des:  D1 +6.1393 ; D2 +5.8726 ; D3 +5.5726
# cta:  C1 +19.7059 ; C2 +19.3892
lineas = [
    # HOOK
    (0.00, 1.60, f"REVIT ME ARROJÓ\\NUN {AMBER}ERROR{WHITE}"),
    (1.66, 2.56, "PERO CHATGPT"),
    (2.56, 4.46, f"ME AHORRÓ {AMBER}2 HORAS{WHITE}"),
    (4.46, 5.62, "DE TRABAJO EN BUSCAR"),
    (5.62, 6.42, "LA SOLUCIÓN"),
    # DESARROLLO
    (6.44, 7.76, "ME SALIÓ ESTE ERROR"),
    (7.76, 8.60, f"EN {AMBER}REVIT{WHITE}"),
    (8.60, 9.20, "Y EN VEZ DE"),
    (9.20, 10.26, "BUSCAR EN FOROS"),
    (10.37, 11.05, "LO QUE HICE"),
    (11.05, 12.15, f"ES PEGARLO EN {AMBER}CHATGPT{WHITE}"),
    (12.37, 13.31, "DARLE UN CONTEXTO"),
    (13.31, 14.41, "PARA QUE ME PUEDA"),
    (14.41, 15.86, "DAR LA SOLUCIÓN"),
    (15.92, 16.93, "UNA SOLUCIÓN"),
    (16.93, 17.69, "QUE ME AHORRA"),
    (17.69, 19.57, f"{AMBER}2 HORAS{WHITE} DE TRABAJO"),
    # CTA
    (19.71, 20.33, f"{AMBER}OJO:{WHITE}"),
    (20.57, 21.85, "ES IMPORTANTE QUE VALIDES"),
    (21.85, 22.73, "TODO LO QUE HAGAS"),
    (22.73, 23.33, "CON LA GUÍA"),
    (23.41, 24.81, "POR ESO SI TE INTERESA"),
    (24.81, 26.31, f"COMENTA {AMBER}“GUÍA”{WHITE}"),
    (26.31, 26.97, "Y TE ENSEÑO"),
    (26.97, 27.70, "CÓMO USARLA"),
]

hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Reel,Montserrat ExtraBold,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,1,0,1,6,2,2,60,60,460,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

with open("subs.ass", "w", encoding="utf-8-sig") as f:
    f.write(hdr)
    for s, e, txt in lineas:
        f.write(f"Dialogue: 0,{t(s)},{t(e)},Reel,,0,0,0,,{POP}{txt}\n")
print(f"subs.ass: {len(lineas)} lineas")
