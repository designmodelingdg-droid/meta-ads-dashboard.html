# Subtitulos v2: timeline con snaps, "CON LA IA" corregido
AMBER = r"{\c&H4AA0E8&}"
WHITE = r"{\c&HFFFFFF&}"
POP = r"{\fscx85\fscy85\t(0,90,\fscx100\fscy100)}"

def t(sec):
    h = int(sec // 3600); m = int(sec % 3600 // 60); s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"

lineas = [
    (0.00, 1.60, f"REVIT ME ARROJÓ\\NUN {AMBER}ERROR{WHITE}"),
    (1.66, 2.56, "PERO CHATGPT"),
    (2.56, 4.46, f"ME AHORRÓ {AMBER}2 HORAS{WHITE}"),
    (4.47, 5.63, "DE TRABAJO EN BUSCAR"),
    (5.63, 6.45, "LA SOLUCIÓN"),
    (6.45, 7.77, "ME SALIÓ ESTE ERROR"),
    (7.77, 8.53, f"EN {AMBER}REVIT{WHITE}"),
    (8.53, 9.13, "Y EN VEZ DE"),
    (9.13, 10.25, "BUSCAR EN FOROS"),
    (10.42, 10.86, "LO QUE HICE"),
    (10.86, 12.37, f"ES PEGARLO EN {AMBER}CHATGPT{WHITE}"),
    (12.47, 13.35, "DARLE UN CONTEXTO"),
    (13.35, 14.51, "PARA QUE ME PUEDA"),
    (14.51, 15.97, "DAR LA SOLUCIÓN"),
    (16.07, 17.08, "UNA SOLUCIÓN"),
    (17.08, 17.84, "QUE ME AHORRA"),
    (17.84, 19.72, f"{AMBER}2 HORAS{WHITE} DE TRABAJO"),
    (19.89, 20.51, f"{AMBER}OJO:{WHITE}"),
    (20.75, 22.03, "ES IMPORTANTE QUE VALIDES"),
    (22.03, 22.91, "TODO LO QUE HAGAS"),
    (22.91, 23.52, f"CON LA {AMBER}IA{WHITE}"),
    (23.59, 24.99, "POR ESO SI TE INTERESA"),
    (25.02, 26.52, f"COMENTA {AMBER}“GUÍA”{WHITE}"),
    (26.52, 27.18, "Y TE ENSEÑO"),
    (27.18, 27.90, "CÓMO USARLA"),
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

with open("subs2.ass", "w", encoding="utf-8-sig") as f:
    f.write(hdr)
    for s, e, txt in lineas:
        f.write(f"Dialogue: 0,{t(s)},{t(e)},Reel,,0,0,0,,{POP}{txt}\n")
print(f"subs2.ass: {len(lineas)} lineas")
