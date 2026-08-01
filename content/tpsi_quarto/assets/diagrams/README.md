# Standard dei diagrammi TPSI quarto

Questa cartella contiene diagrammi **originali**, creati per il corso e non ricavati dalle immagini del libro adottato.

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

Il diagramma è la rappresentazione principale; il blocco testuale originario viene conservato in un `<details>` per accessibilità, copia e consultazione senza immagini.

```md
![Descrizione completa del diagramma](assets/diagrams/nome-diagramma.svg)

<details>
<summary>Versione testuale del diagramma</summary>

```text
...
```

</details>
```

L'`alt text` deve descrivere il significato e non limitarsi a ripetere il titolo.

## Convenzione dei nomi

```text
<modulo>-<concetto>.svg
```

Esempi:

```text
01-process-lifecycle.svg
01-execution-models.svg
02-producer-consumer-buffer.svg
02-deadlock-cycle.svg
03-requirements-traceability.svg
04-architecture-layers.svg
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
