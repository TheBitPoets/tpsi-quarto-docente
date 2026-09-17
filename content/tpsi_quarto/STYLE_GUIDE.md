# Formattazione delle dispense TPSI quarto

Il formato dei sei moduli segue due riferimenti letti il 14 settembre 2026:

- [TPSI quinto — Web Platform e HTML moderno](https://github.com/TheBitPoets/tpsi-quinto-docente/blob/main/content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md), per orientamento, icone e componenti editoriali;
- [2cornot2c — Il processo di compilazione](https://github.com/TheBitPoets/2cornot2c/blob/main/README.md#il-processo-di-compilazione), per la cornice completa, i paragrafi giustificati e la convivenza di HTML e codice Markdown.

Queste regole sono obbligatorie per tutte le lezioni del corso, presenti e future: pannello iniziale con icone canoniche, formattazione HTML e riquadri delle definizioni. La prosa delle dispense è normalizzata in HTML. Titoli, metadati, identificatori e blocchi di codice restano nel formato originale; immagini e didascalie mantengono i collegamenti del Visual System.

## Orientamento della sezione

Il pannello è una tabella centrata che contiene `details`. La bussola **🧭** identifica il pannello; la mappa **🗺** identifica il contesto. Sono funzioni diverse.

| Campo | Icona | Entità HTML |
|---|---|---|
| Orientamento della sezione | 🧭 | `&#129517;` |
| Contesto | 🗺 | `&#128506;` |
| Prerequisiti | 🛠 | `&#128736;` |
| Obiettivi | 🎯 | `&#127919;` |
| Richiamo | 🔁 | `&#128257;` |
| Anticipazione | 👀 | `&#128064;` |
| Prossimo passo | ➡ | `&#10145;` |
| Rimando | 🔗 | `&#128279;` |
| Domande guida, quando utili | ❓ | `&#10067;` |

Nei sei moduli la cornice usa i sette campi del Course Design: contesto, prerequisiti, obiettivi, richiamo, anticipazione, prossimo passo e riferimenti. I rimandi contengono collegamenti cliccabili. Le domande guida della quinta sono un'estensione possibile, da compilare in modo specifico per l'argomento.

Il pannello viene inserito subito dopo il titolo `## In questa unità impareremo`, come nella lezione di riferimento della quinta. Gli obiettivi dettagliati e i prerequisiti della dispensa rimangono visibili.

Template:

```html
<!-- visual-orientation -->
<table align="center">
<tr>
<td>
<details>
<summary>&#129517; <strong>Orientamento della sezione</strong></summary>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#128506;</span> Contesto:</strong>
Collegamento specifico fra questo argomento e il percorso.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#128736;</span> Prerequisiti:</strong>
Conoscenze e abilità richieste per affrontare la lezione.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#127919;</span> Obiettivi:</strong>
Risultati osservabili al termine della lezione.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#128257;</span> Richiamo:</strong>
Concetti già affrontati da riattivare.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#128064;</span> Anticipazione:</strong>
Concetti che saranno sviluppati in seguito.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#10145;</span> Prossimo passo:</strong>
Attività concreta da svolgere dopo la spiegazione.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#128279;</span> Rimando:</strong>
<a href="#fonti-e-note-di-revisione">Fonti e note della lezione</a>.
</p>

</details>
</td>
</tr>
</table>
```

## Testo, liste e tabelle

La prosa usa `<p align="justify">`. Dentro un blocco HTML usare `strong`, `em`, `code` e `a href` al posto dei rispettivi marcatori Markdown. Le liste usano `ul` o `ol` con `li`; le tabelle di confronto usano `table align="center"`, `thead`, `tbody`, `tr`, `th` e `td`.

```html
<p align="justify">
Un <strong>processo</strong> è un'esecuzione attiva.
La chiamata <code>fork()</code> crea un processo figlio.
</p>

<ul>
  <li>identità del processo;</li>
  <li>memoria e risorse;</li>
  <li>stato di esecuzione.</li>
</ul>
```

I titoli restano Markdown per conservare gli anchor. Non trasformare un titolo dentro un esempio di README in una vera sezione della dispensa.

## Riquadri didattici

| Funzione | Icona | Entità |
|---|---|---|
| Definizione: Importante | ❗ | `&#10071;` |
| Idea chiave | 💡 | `&#128161;` |
| Attenzione | ⚠ | `&#9888;` |
| Laboratorio | 💻 | `&#128187;` |
| Verifica rapida | ✅ | `&#9989;` |

Ogni definizione usa il formato del [README di 2cornot2c](https://github.com/TheBitPoets/2cornot2c/blob/main/README.md), ricontrollato il 17 settembre 2026: tabella centrata, intestazione **❗ Importante**, testo giustificato e termine definito in grassetto. Il riquadro resta visibile, senza `details`. Usare questo template:

```html
<!-- definition -->
<table align="center">
<tr><td>
&#10071; <strong>Importante</strong>
<p align="justify">
Un <strong>processo</strong> è un'esecuzione attiva di un programma,
con uno stato che cambia nel tempo.
</p>
</td></tr>
</table>
<!-- /definition -->
```

I commenti `definition` non sono visibili al lettore: delimitano il riquadro per i controlli automatici. Il vecchio formato «📖 Definizione» è sostituito da questo template in tutto il corso.

Isolare la frase che definisce il concetto; lasciare motivazioni, esempi, codice e approfondimenti nei paragrafi successivi. La definizione deve essere comprensibile anche nel riquadro: esplicitare il termine invece di iniziare soltanto con «È» o «Descrive». Definizioni strettamente collegate possono condividere un riquadro; un elenco HTML può restare dentro se completa la definizione. Non annidare altre tabelle.

Applicare il riquadro quando si introduce o si formalizza un concetto. Un semplice richiamo, un esempio applicativo, una domanda o un riepilogo non richiedono un nuovo riquadro. Mantenere distinti i pannelli per idee chiave, avvertenze, laboratori e verifiche.

## Codice e immagini

I fenced code block restano Markdown fuori dai contenitori HTML. Dentro un pannello HTML, quando si inserisce nuovo codice, usare `<pre lang="c"><code>…</code></pre>` ed effettuare l'escape di `&`, `<` e `>`. Non racchiudere un fenced code block in una tabella HTML.

Le immagini rimangono locali, centrate, con testo alternativo e didascalia:

```html
<!-- figure:identificatore-stabile -->
<p align="center">
  <img src="../../assets/tpsi4/nome-figura.svg"
       alt="Relazioni e risultato che lo studente deve comprendere."
       width="960">
</p>
<p align="center"><em>Didascalia coerente con la spiegazione.</em></p>
```

Ogni immagine è registrata in [figure-index.json](../../assets/tpsi4/visual-system/figure-index.json). Gli oggetti e le scene sono descritti nel [Visual System](../../assets/tpsi4/visual-system/README.md). Non introdurre CSS o font remoti nelle dispense.

Le animazioni GIF possono affiancare le figure statiche quando il tempo o il movimento sono parte della spiegazione. Usare lo stesso pannello centrato, alt descrittivo e didascalia; dichiarare tempi simulati e ripetizione. Conservare una figura statica e una spiegazione testuale della sequenza. Registrare le GIF nella chiave `animations` del registro e mantenerne il generatore nel repository.

## Normalizzazione e verifica

Il [normalizzatore](../../scripts/format_tpsi4_lessons.py) deriva da quello della quinta e comprende tutte le lezioni con nome `NN_*.md` nella cartella del corso, incluse quelle future. Conserva l'HTML già presente, comprese le cornici personalizzate; non genera il testo dell'orientamento e non modifica gli esempi di codice. Il suo ambito è il sottoinsieme Markdown delle dispense: prosa, liste semplici, citazioni e tabelle semplici. Per strutture più complesse usare direttamente HTML.

Il controllo verifica anche i marcatori e il template delle definizioni, il testo giustificato e la presenza di un termine in grassetto; segnala il vecchio formato «Definizione». Non può riconoscere semanticamente una definizione rimasta nella prosa: questa verifica resta parte della revisione editoriale.

Per applicare intenzionalmente la formattazione:

```bash
python scripts/format_tpsi4_lessons.py --write
```

Controlli senza modificare file:

```bash
python scripts/format_tpsi4_lessons.py --check
python -m unittest discover -s tests -p test_format_tpsi4_lessons.py
python scripts/build_course_diagrams.py --check
python -m unittest discover -s tests -p test_course_diagrams.py
git diff --check
```

La Quality esegue i controlli di formattazione su Windows e Ubuntu. Verificare anche la resa visiva: allineamento, apertura del pannello, icone, tabelle, immagini e codice copiabile. La validazione HTML non sostituisce una revisione tecnica o didattica dei contenuti.
