# Build delle slide TPSI4

Le slide sorgente sono Markdown/Marp; HTML, PDF e PPTX sono derivati e non vanno modificati a mano.

## Controllo

```bash
python scripts/build_slides.py --check-only
```

Verifica i 7 deck `00..06`, le lezioni canoniche, i link di navigazione e il front matter Marp.

## Build completa

```bash
python scripts/build_slides.py --formats html,pdf,pptx --browser chrome
```

Output:

```text
build/tpsi4-slides/
  html/
  pdf/
  pptx/
  MANIFEST.json
  SHA256SUMS.txt
```

Marp CLI è fissato alla versione `4.5.0`. HTML/PDF vengono renderizzati in parallelo; PPTX è seriale per evitare timeout Chrome/Puppeteer osservati nel consumer TPSI quinto.

Il manifest registra esplicitamente `content_pack: 0.1.0` e `content_pack_status: draft`: la generazione delle slide non equivale ad approvazione del curriculum.