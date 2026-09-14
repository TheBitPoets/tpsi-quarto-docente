# Formattazione delle dispense TPSI quarto

Il formato dei sei moduli segue due riferimenti letti il 14 settembre 2026:

- [TPSI quinto — Web Platform e HTML moderno](https://github.com/TheBitPoets/tpsi-quinto-docente/blob/main/content/tpsi5/01_WEB_PLATFORM_HTML_MODERNO.md), per orientamento, icone e componenti editoriali;
- [2cornot2c — Il processo di compilazione](https://github.com/TheBitPoets/2cornot2c/blob/main/README.md#il-processo-di-compilazione), per la cornice completa, i paragrafi giustificati e la convivenza di HTML e codice Markdown.

La prosa delle dispense è normalizzata in HTML. Titoli, metadati, identificatori e blocchi di codice restano nel formato originale; immagini e didascalie mantengono i collegamenti del Visual System.

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
| Definizione | 📖 | `&#128214;` |
| Idea chiave | 💡 | `&#128161;` |
| Attenzione | ⚠ | `&#9888;` |
| Laboratorio | 💻 | `&#128187;` |
| Verifica rapida | ✅ | `&#9989;` |

Una definizione necessaria resta visibile, dentro una tabella centrata:

```html
<table align="center">
<tr><td>
<p align="justify">
<strong><span style="font-size: 1.15em;">&#128214;</span> Definizione:</strong>
Testo breve, autonomo e preciso.
</p>
</td></tr>
</table>
```

I sei moduli contengono una prima applicazione di questi riquadri ai concetti fondamentali. Usarli quando aiutano a riconoscere la funzione del testo, senza trasformare ogni paragrafo in un'avvertenza.

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

## Normalizzazione e verifica

Il [normalizzatore](../../scripts/format_tpsi4_lessons.py) deriva da quello della quinta, adattato ai moduli 01–06. Conserva l'HTML già presente, comprese le cornici personalizzate; non genera il testo dell'orientamento e non modifica gli esempi di codice. Il suo ambito è il sottoinsieme Markdown delle dispense: prosa, liste semplici, citazioni e tabelle semplici. Per strutture più complesse usare direttamente HTML.

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
