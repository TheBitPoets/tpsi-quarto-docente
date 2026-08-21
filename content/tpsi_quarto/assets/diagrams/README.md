# Standard dei diagrammi TPSI quarto

Questa cartella contiene **27 diagrammi originali**, creati per il corso e non ricavati né ricalcati dalle immagini del libro adottato.

## Formato

- sorgente: SVG testuale versionabile;
- area di disegno consigliata: `1400 × 700` o proporzione equivalente;
- sfondo chiaro incorporato, così il diagramma resta leggibile anche fuori dalla dashboard;
- nessun font esterno: `system-ui`, `Segoe UI`, `Arial`, sans-serif;
- nessuna dipendenza da script o risorse remote;
- testo italiano incorporato nell'SVG;
- `<title>` e `<desc>` obbligatori;
- `role="img"` e `aria-labelledby` obbligatori;
- frecce, etichette e forme devono comunicare il significato anche senza affidarsi soltanto al colore.

## Palette

| Ruolo | Colore |
| --- | --- |
| testo principale | `#0F172A` |
| testo secondario | `#334155` |
| sfondo | `#F8FAFC` |
| pannelli | `#FFFFFF` |
| azione/flusso | `#2563EB` |
| stato positivo/coordinato | `#0F766E` |
| attenzione/attesa | `#B45309` |
| errore/conflitto | `#B91C1C` |
| concetto alternativo | `#7C3AED` |

## Inserimento nei Markdown

Quando un SVG sostituisce una vera ASCII art nel modulo principale, il diagramma è la rappresentazione primaria e il blocco originario resta in un `<details>` per accessibilità, copia e consultazione senza immagini.

````md
![Descrizione completa del diagramma](assets/diagrams/nome-diagramma.svg)

<details>
<summary>Versione testuale del diagramma</summary>

```text
...
```

</details>
````

Gli altri diagrammi sono raccolti nelle sei guide sotto `content/tpsi_quarto/visuals/`. Questa separazione evita di interrompere continuamente teoria, codice e pseudocodice nei moduli principali.

L'`alt text` deve descrivere il significato e non limitarsi a ripetere il titolo.

## Convenzione dei nomi

```text
<modulo>-<concetto>.svg
```

Esempi:

```text
01-process-lifecycle.svg
02-producer-consumer-buffer.svg
03-requirements-traceability.svg
04-git-workflow.svg
05-debug-cycle.svg
06-responsible-ai.svg
```

## Cosa trasformare in immagine

Trasformare:

- macchine a stati;
- confronti temporali;
- topologie di comunicazione;
- cicli di attesa e deadlock;
- architetture a livelli;
- catene di tracciabilità;
- mappe concettuali.

Lasciare come testo o codice:

- comandi da copiare;
- output atteso;
- formule e invarianti brevi;
- pseudocodice destinato alla modifica;
- identificatori di activity;
- diagrammi Mermaid già versionabili e semanticamente corretti.

## Struttura delle guide

```text
content/tpsi_quarto/visuals/
  01_PROCESSI_E_CONCORRENZA.md
  02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md
  03_REQUISITI_SOFTWARE.md
  04_DOCUMENTAZIONE_VERSIONAMENTO.md
  05_TESTING_DEBUGGING.md
  06_CITTADINANZA_DIGITALE.md
```

Ogni guida:

- collega il modulo teorico;
- incorpora tutti i diagrammi del relativo nucleo;
- usa alt text descrittivi;
- spiega quali elementi restano testuali e perché.

## Controlli locali

Non esistono workflow GitHub Actions nel repository privato. I controlli si eseguono localmente:

```bash
python -m pytest tests/test_visual_diagrams.py
```

La suite verifica:

- XML SVG valido;
- `title`, `desc`, `role` e `aria-labelledby`;
- assenza di script, font e risorse remote;
- set esatto dei 27 SVG;
- corrispondenza fra inventario, guide e file;
- riferimenti Markdown a file esistenti;
- alt text significativo;
- fallback testuale per le ASCII art sostituite;
- assenza di file in `.github/workflows`.
