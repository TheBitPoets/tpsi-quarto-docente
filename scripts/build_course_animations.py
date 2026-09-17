#!/usr/bin/env python3
"""Build the two I/O teaching GIFs from a deterministic event timeline.

Rendering needs Pillow and a local Chromium browser. The simulation and tests
use only the standard library. Palette and icons come from the course visual kit.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "assets/tpsi4/visual-system"
OUT = ROOT / "assets/tpsi4"
FPS = 8
SIZE = (1200, 675)
DURATION = {"sequenziale": 12, "concorrente": 22}
# An intentionally short pause occurs after filling the four waiting slots.
ARRIVALS = ((0, 20), (2, 21), (4, 22), (6, 23), (8, 24), (16, 25), (18, 26))
COMPLETIONS = (10, 12, 14, 16, 18, 20)
CLICKS = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21)


def concurrent_state(t: float) -> dict:
    """FIFO: one measurement in flight, four waiting; GUI reads a separate copy."""
    queue = []
    sending = None
    delivered = []
    latest, sampled = 20, 0
    events = sorted([(when, 1, value) for when, value in ARRIVALS] +
                    [(when, 0, None) for when in COMPLETIONS])
    for when, kind, value in events:
        if when > t:
            break
        if kind == 0:
            if sending is not None:
                delivered.append(sending)
                sending = None
            if queue:
                sending = queue.pop(0)
        else:
            latest, sampled = value, when
            if sending is None:
                sending = value
            else:
                queue.append(value)
    return dict(queue=queue, sending=sending, delivered=delivered,
                latest=latest, sampled=sampled, sensor_wait=9 <= t < 16,
                server_slow=t < 10, clicks=sum(c <= t for c in CLICKS))


def sequential_state(t: float) -> dict:
    """The only thread reads at t=4, finishes sending at t=9, then handles GUI."""
    phase = "sensor" if t < 4 else "send" if t < 9 else "gui"
    return dict(phase=phase, latest=19 if t < 9 else 20,
                sampled=-2 if t < 9 else 4,
                handled=0 if t < 9 else sum(c <= t for c in CLICKS),
                pending=sum(c <= t for c in CLICKS) if t < 9 else 0)


def browser_path(explicit: str | None) -> str:
    candidates = [explicit, shutil.which("chromium"), shutil.which("google-chrome"),
                  "C:/Program Files/Google/Chrome/Application/chrome.exe",
                  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
                  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    raise RuntimeError("Use --browser to select a local Chromium executable")


def icon_atlas(browser: str, directory: Path, colors: dict):
    """Rasterize the actual shared SVG symbols, rather than redraw similar icons."""
    from PIL import Image
    import xml.etree.ElementTree as ET
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ns = "{http://www.w3.org/2000/svg}"
    library = ET.parse(KIT / "components.svg").getroot()
    defs = ET.tostring(library.find(ns + "defs"), encoding="unicode")
    for key, value in colors.items():
        defs = defs.replace("{{" + key + "}}", value)
    icons = ("tpsi-cpu", "tpsi-server", "tpsi-terminal")
    uses = "".join(f'<use href="#{name}" x="{i * 120}" y="0" width="120" height="100"/>' for i, name in enumerate(icons))
    page = directory / "icons.html"
    page.write_text('<!doctype html><meta charset="utf-8"><style>body{margin:0;background:' +
                    colors["surface"] + '}</style><svg xmlns="http://www.w3.org/2000/svg" width="360" height="100">' +
                    defs + uses + '</svg>', encoding="utf-8")
    target = directory / "icons.png"
    subprocess.run([browser, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--no-first-run", "--no-default-browser-check",
                    "--user-data-dir=" + str(directory / "browser"),
                    "--screenshot=" + str(target), "--window-size=800,600",
                    page.as_uri()], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    deadline = time.monotonic() + 15
    while not target.exists() and time.monotonic() < deadline:
        time.sleep(.1)
    with Image.open(target) as atlas:
        return [atlas.crop((i * 120, 0, (i + 1) * 120, 100)).convert("RGB") for i in range(3)]


def font_paths(directory: str | None) -> tuple[str, str]:
    roots = ([Path(directory)] if directory else []) + [
        Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/liberation2"),
        Path("/usr/share/fonts/truetype/dejavu"), Path("/System/Library/Fonts/Supplemental")]
    for root in roots:
        for plain, bold in [("arial.ttf", "arialbd.ttf"), ("Arial.ttf", "Arial Bold.ttf"),
                            ("LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf"),
                            ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf")]:
            if (root / plain).is_file() and (root / bold).is_file():
                return str(root / plain), str(root / bold)
    raise RuntimeError("Use --font-dir for Arial, Liberation Sans or DejaVu Sans")


class Renderer:
    def __init__(self, icons, fonts):
        from PIL import Image, ImageDraw, ImageFont
        self.Image, self.Draw, self.Font = Image, ImageDraw, ImageFont
        self.icons, self.fonts = icons, fonts
        self.c = json.loads((KIT / "tokens.json").read_text(encoding="utf-8"))["colors"]

    @lru_cache(maxsize=None)
    def font(self, size, bold=False):
        return self.Font.truetype(self.fonts[int(bold)], size)

    def text(self, xy, text, size=20, color="ink", bold=False):
        # Fail the build for accidental overflow rather than silently clipping text.
        font = self.font(size, bold)
        if self.d.textbbox(xy, text, font=font)[2] > SIZE[0] - 20:
            raise ValueError("Text exceeds canvas: " + text)
        self.d.text(xy, text, font=font, fill=self.c.get(color, color))

    def rect(self, box, color, radius=14, outline=None, width=2):
        self.d.rounded_rectangle(box, radius, fill=self.c.get(color, color),
                                outline=self.c.get(outline, outline), width=width)

    def arrow(self, points, color="line"):
        color = self.c.get(color, color)
        self.d.line(points, fill=color, width=4)
        x, y = points[-1]
        self.d.polygon([(x, y), (x-10, y-6), (x-10, y+6)], fill=color)

    def progress(self, box, ratio, color):
        x,y,x2,y2=box
        self.rect(box, "#dce5ef", 5)
        if ratio > 0:
            self.rect((x,y,x+max(8,(x2-x)*min(1,ratio)),y2),color,5)

    def base(self, title, subtitle, t, mode):
        self.im = self.Image.new("RGB", SIZE, self.c["canvas"])
        self.d = self.Draw.Draw(self.im)
        self.text((30,20), title,32,"surface",True)
        self.text((30,64), subtitle,19,"muted")
        self.text((30,614), "Tempo simulato: %02d s" % t,19,"surface",True)
        self.text((295,614), "Tempi illustrativi e rallentati · la sequenza si ripete",18,"muted")
        self.progress((30,650,1170,658),t / DURATION[mode],"thread")

    def gui(self, t, latest, sampled, handled, pending=0, frozen=False, stale=False, sequential=False):
        # Same screen position and controls in both animations.
        self.rect((30,380,1170,593),"surface",outline="runtime" if frozen else "thread",width=4)
        self.im.paste(self.icons[2].resize((72,60)),(50,396))
        self.text((136,397),"GUI · temperatura",20,bold=True)
        self.text((136,434),str(latest)+" °C",46,bold=True)
        self.text((138,491),f"Ultima misura: t = {sampled} s",18)
        if frozen:
            self.text((350,402),"FERMA: il thread è occupato dall'I/O",24,"runtime",True)
            self.text((350,440),f"Clic in attesa: {pending}   |   Clic gestiti: 0",22)
            self.text((350,480),"Valore, animazione e comandi non si aggiornano.",19)
        else:
            self.text((350,402),"ATTIVA: i clic ricevono risposta",24,"thread",True)
            self.text((350,440),f"Clic gestiti: {handled}   |   Attesa: 0",22)
            self.text((350,480), f"Dato non aggiornato da {int(t-sampled)} s: sensore in attesa."
                      if stale else "Ora il thread può aggiornare la schermata." if sequential else
                      "Mostra l'ultima misura acquisita, senza aspettare l'invio.",19,
                      "runtime" if stale else "ink")
        pressed = any(0 <= t-c < .6 for c in CLICKS)
        self.rect((885,425,1135,478),"thread" if pressed and not frozen else "process",9)
        self.text((911,440),"Mostra dettagli",21,"surface",True)
        if pressed:
            self.text((907,397),"Utente: CLIC!",21,"runtime",True)
        # A moving dot is GUI work, not the sensor and not an OS pointer.
        self.progress((350,534,825,545), .08 if frozen else (t % 2)/2,"runtime" if frozen else "thread")
        self.text((350,555),"Indicatore della GUI fermo" if frozen else "Indicatore della GUI in movimento",17)
        self.text((897,495),"Clic simulato ogni 2 s",17)

    def sequential(self, t):
        s=sequential_state(t);phase=s["phase"]
        self.base("Un solo thread: l'attesa ferma anche la GUI",
                  "Leggi il sensore  →  invia al server  →  aggiorna la schermata",t,"sequenziale")
        for x,title,icon in [(30,"1  LEGGI",0),(425,"2  INVIA",1),(820,"3  AGGIORNA",2)]:
            self.rect((x,112,x+350,294),"surface")
            self.text((x+20,126),title,23,bold=True)
            self.im.paste(self.icons[icon].resize((84,70)),(x+15,170))
        self.arrow([(380,211),(417,211)])
        self.arrow([(775,211),(812,211)])
        self.text((141,177),"Sensore in attesa" if phase=="sensor" else "Misura: 20 °C",19,
                  "runtime" if phase=="sensor" else "thread",True)
        self.text((141,211),"Nessun dato pronto" if phase=="sensor" else "Arrivata a t = 4 s",17)
        self.text((536,177),"Non ancora avviato" if phase=="sensor" else
                  "Invio bloccato" if phase=="send" else "Invio completato",19,
                  "runtime" if phase=="send" else "ink",True)
        self.text((536,211),"Server lento; buffer pieno" if phase=="send" else
                  "Aspetta la lettura" if phase=="sensor" else "Ora tocca alla GUI",17)
        self.text((931,177),"Non raggiunta" if phase!="gui" else "Gestisce i clic",19,
                  "runtime" if phase!="gui" else "thread",True)
        self.text((931,211),"Resta al vecchio dato" if phase!="gui" else "Mostra 20 °C",17)
        for x,ratio in [(50,min(t/4,1)),(445,max(0,min((t-4)/5,1))),(840,0 if t<9 else 1)]:
            self.progress((x,265,x+310,275),ratio,"thread")
        self.rect((30,312,1170,359),"panel")
        messages={"sensor":"Il thread aspetta il sensore. Il clic arriva, ma la GUI non può gestirlo.",
                  "send":"Il thread aspetta spazio per inviare. La misura è pronta, la GUI è ancora ferma.",
                  "gui":"L'attesa è finita: solo ora la GUI aggiorna il valore e gestisce i clic accumulati."}
        self.text((48,324),messages[phase],21,"surface")
        self.gui(t,s["latest"],s["sampled"],s["handled"],s["pending"],phase!="gui",sequential=True)
        return self.im

    def concurrent(self,t):
        s=concurrent_state(t)
        self.base("Tre thread: l'I/O aspetta, la GUI risponde",
                  "A acquisisce  ·  B invia  ·  C gestisce la GUI  |  Coda FIFO: 4 posti + 1 dato in invio",t,"concorrente")
        self.rect((30,112,320,296),"surface")
        self.text((48,125),"A · SENSORE",22,bold=True)
        self.im.paste(self.icons[0].resize((66,55)),(48,166))
        self.text((125,172),"IN ATTESA" if s["sensor_wait"] else "ACQUISISCE",20,
                  "runtime" if s["sensor_wait"] else "thread",True)
        self.text((48,237),"Nessuna nuova misura" if s["sensor_wait"] else
                  f"Ultimo campione: {s['latest']} °C",20)
        self.rect((355,112,765,296),"surface")
        self.text((375,125),f"CODA PER B    {len(s['queue'])} / 4",22,bold=True)
        for i in range(4):
            x=375+i*93
            filled=i<len(s["queue"])
            self.rect((x,178,x+81,229),"data" if filled else "#e2e8f0",8)
            self.text((x+17,191),str(s["queue"][i]) if filled else "—",24,"surface" if filled else "ink",True)
        self.text((375,245),"Primo da inviare ←   |   valori in °C",17)
        self.rect((800,112,1170,296),"surface")
        self.text((820,125),"B · INVIO VIA SOCKET",22,bold=True)
        self.im.paste(self.icons[1].resize((66,55)),(821,167))
        self.text((897,177),f"In invio: {s['sending']} °C",21,bold=True)
        self.text((821,234),"Server lento; buffer pieno" if s["server_slow"] else
                  f"Invii completati: {len(s['delivered'])}",20,"runtime" if s["server_slow"] else "thread",True)
        self.arrow([(320,206),(350,206)])
        self.arrow([(765,206),(795,206)])
        self.rect((30,312,1170,359),"panel")
        message=("La coda si riempie; C legge la copia dell'ultimo valore e risponde ai clic." if t<9 else
                 "Il sensore non produce dati: la GUI resta attiva e segnala il valore non aggiornato." if t<16 else
                 "Il sensore riparte; la coda si svuota in ordine e la GUI mostra i nuovi valori.")
        self.text((48,324),message,20,"surface")
        self.gui(t,s["latest"],s["sampled"],s["clicks"],stale=s["sensor_wait"])
        self.text((55,555),"C · copia ultimo valore",17,"thread",True)
        return self.im



def build_player():
    """Embed existing GIFs and still posters in a single offline HTML file."""
    import base64
    import io
    from PIL import Image
    data = {}
    for mode, duration in DURATION.items():
        payload = (OUT / f"01-io-{mode}-animazione.gif").read_bytes()
        with Image.open(io.BytesIO(payload)) as gif:
            poster = io.BytesIO()
            gif.seek(0)
            gif.convert("RGB").save(poster, format="PNG")
        data[mode] = {
            "gif": base64.b64encode(payload).decode("ascii"),
            "poster": "data:image/png;base64," + base64.b64encode(poster.getvalue()).decode("ascii"),
            "duration": duration,
        }
    template = (KIT / "io-player.template.html").read_text(encoding="utf-8")
    page = template.replace("{{ANIMATION_DATA}}", json.dumps(data, ensure_ascii=True))
    target = OUT / "01-io-animazioni.html"
    target.write_text(page, encoding="utf-8", newline="\n")
    print(target.relative_to(ROOT), target.stat().st_size, "bytes")


def build(browser=None,font_dir=None):
    from PIL import Image
    colors=json.loads((KIT/"tokens.json").read_text(encoding="utf-8"))["colors"]
    with tempfile.TemporaryDirectory(prefix="tpsi4-animation-") as tmp:
        renderer=Renderer(icon_atlas(browser_path(browser),Path(tmp),colors),font_paths(font_dir))
        # One shared palette prevents flashing colors between frames.
        samples=Image.new("RGB",(SIZE[0]*2,SIZE[1]))
        samples.paste(renderer.sequential(6),(0,0))
        samples.paste(renderer.concurrent(13),(SIZE[0],0))
        palette=samples.quantize(colors=256)
        for mode in DURATION:
            render=renderer.sequential if mode == "sequenziale" else renderer.concurrent
            frames=[render(i/FPS).quantize(palette=palette,dither=Image.Dither.NONE)
                    for i in range(DURATION[mode]*FPS)]
            # 8 fps is exactly 125 ms in the model; GIF uses 10 ms ticks.
            # Alternate 120/130 ms to preserve exact two-second event timing.
            durations=[120 if i%2==0 else 130 for i in range(len(frames))]
            path=OUT/f"01-io-{mode}-animazione.gif"
            frames[0].save(path,save_all=True,append_images=frames[1:],duration=durations,
                           loop=0,optimize=True,disposal=1)
            print(path.relative_to(ROOT),path.stat().st_size,"bytes")


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser")
    parser.add_argument("--font-dir")
    parser.add_argument("--player-only", action="store_true", help="rebuild only the offline HTML player from existing GIFs")
    args=parser.parse_args()
    if not args.player_only:
        build(args.browser,args.font_dir)
    build_player()
