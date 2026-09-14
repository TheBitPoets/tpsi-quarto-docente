# Formattazione delle dispense TPSI quarto

Riferimento: [standard della quinta](https://github.com/TheBitPoets/tpsi-quinto-docente/blob/main/content/tpsi5/STYLE_GUIDE.md). Il primo passaggio applica orientamento, figure e didascalie ai sei moduli; una revisione editoriale completa della prosa resta distinta dal solo impaginare le immagini.

## Struttura

Mantenere titoli Markdown e identificatori esistenti: sono destinazioni della Course Board e dei link alle lezioni. Conservare codice copiabile e tabelle di confronto. Le informazioni fondamentali devono essere visibili senza aprire pannelli.

All'inizio della dispensa, dopo i metadati, un pannello di orientamento collega contesto, obiettivo, prerequisiti e prossimo passo. Le sezioni già presenti mantengono l'ordine: obiettivi, prerequisiti, problema, spiegazione, esempi, esercizi, verifica, sintesi e fonti.

## Immagini

Usare soltanto gli SVG generati dal [Visual System](../../assets/tpsi4/visual-system/README.md). Inserire la figura dopo la spiegazione del concetto, prima del successivo argomento, con una frase che renda esplicito cosa osservare.

```html
<!-- figure:identificatore-stabile -->
<p align="center">
  <img src="../../assets/tpsi4/nome-figura.svg"
       alt="Relazioni e risultato che lo studente deve comprendere."
       width="960">
</p>
<p align="center"><em>Didascalia breve, autonoma e coerente con il testo.</em></p>
```

Ogni inserimento deve essere registrato in [figure-index.json](../../assets/tpsi4/visual-system/figure-index.json). L'alt descrive il significato, non il solo aspetto: “A possiede X e attende Y” è più utile di “quattro riquadri colorati”. I dettagli della figura devono restare spiegati anche nel testo.

## Componenti editoriali

| Funzione | Etichetta |
|---|---|
| Orientamento | 🗺 Orientamento della sezione |
| Definizione | 📖 Definizione |
| Modello o relazione | 💡 Idea chiave |
| Errore o limite | ⚠ Attenzione |
| Attività | 💻 Laboratorio |
| Controllo di comprensione | ✅ Verifica rapida |

Esempio di callout visibile:

```html
<table align="center"><tr><td>
<p align="justify"><strong>💡 Idea chiave:</strong> testo breve e autonomo.</p>
</td></tr></table>
```

I pannelli `details` possono contenere orientamento, materiali accessori o approfondimenti. Non nascondere la definizione necessaria per il paragrafo successivo. Dentro HTML usare `strong`, `em` e `code`; conservare righe vuote attorno ai blocchi Markdown. Nella revisione della prosa si possono usare paragrafi HTML giustificati, come nella quinta, senza cambiare i contenuti.

## Controlli

```bash
python scripts/build_course_diagrams.py --check
python -m unittest discover -s tests -p test_course_diagrams.py
git diff --check
```

Aprire inoltre le figure a dimensione di lettura e proiezione: controllare testo, margini, frecce, etichette e significato. Le immagini restano vettoriali e non dipendono da CSS o font remoti. I controlli automatici non equivalgono alla revisione completa della dispensa.
