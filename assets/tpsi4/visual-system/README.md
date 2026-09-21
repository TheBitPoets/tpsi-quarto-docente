# TPSI quarto — Visual System

Libreria vettoriale del corso, derivata dal sistema della quinta e adattata a processi, concorrenza e progettazione. [Audit e collocazioni](../../../doc/VISUAL_AUDIT.md).

## Cataloghi degli oggetti

Aprire le tavole per scegliere un oggetto e leggere il suo ID:

![Oggetti comuni](catalog/catalog-1.svg)

![Processi, memoria e sincronizzazione](catalog/catalog-2.svg)

![Progetto, controllo e tecnologie](catalog/catalog-3.svg)

## Sorgenti e file generati

| File | Ruolo |
|---|---|
| [components.svg](components.svg) | 27 simboli; modificare qui la forma degli oggetti. |
| [tokens.json](tokens.json) | Palette, tipografia e dimensioni di riferimento. |
| [component-inventory.json](component-inventory.json) | Nomi e origine degli oggetti. |
| [scenes/](scenes/) | Scene SVG sorgente: posizioni, testi e relazioni. |
| [figure-index.json](figure-index.json) | Registro delle 32 figure statiche, delle 2 animazioni e delle collocazioni nelle dispense. |
| [catalog/](catalog/) | Tre tavole generate; non modificarle a mano. |
| [Generatore](../../../scripts/build_course_diagrams.py) | Incorpora i simboli e risolve i token in SVG autonomi. |

Gli SVG finali sono in `assets/tpsi4/*.svg`. Non richiedono rete, font scaricati o collegamenti alla libreria durante la lettura. Le scene dichiarano `data-output` e contengono `<defs id="visual-kit-components"/>`, secondo il modello della quinta.

## Rigenerazione

Dalla root del repository, con Python 3.11 o successivo:

```bash
python scripts/build_course_diagrams.py
python scripts/build_course_diagrams.py --check
python -m unittest discover -s tests -p test_course_diagrams.py
```

La build controlla tutte le scene prima di scrivere. Rifiuta simboli inesistenti, ID duplicati, riferimenti esterni, output duplicati e destinazioni fuori dalle cartelle degli SVG generati. `--check` confronta i byte senza scrivere file.

## Grammatica visiva

- Canvas 1920 × 1080, margine di sicurezza 64 px, fondo blu scuro, pannelli chiari.
- Testi in italiano; titolo 48 px, etichette generalmente 28–32 px, note almeno 24 px.
- Blu: processi; turchese: thread e comunicazione; indaco: memoria/dati; ambra: attesa e disponibilità; viola: test; rosso: accesso protetto.
- Il colore accompagna sempre un'etichetta. Un mutex turchese e un lucchetto di sicurezza rosso hanno significati diversi.
- Freccia: flusso o transizione, con verbo o legenda quando il significato non è evidente. Linea senza punta: associazione. Tratteggio: relazione indiretta da spiegare.
- Ogni figura ha `title`, `desc`, `role="img"` e un alt nel Markdown. La didascalia esplicita la relazione centrale.
- Programma ≠ processo; processo ≠ thread; monitor software ≠ schermo. Non usare icone ambigue per queste distinzioni.

## Comporre una nuova figura

1. Cercare prima l'oggetto nei cataloghi. Padre e figlio sono varianti etichettate dello stesso processo.
2. Creare una scena `*.scene.svg` copiando la struttura di una scena vicina; usare `<use href="#tpsi-process" x="…" y="…" width="…" height="…"/>`.
3. Mantenere una relazione didattica principale; dividere una scena troppo densa.
4. Usare token come `{{canvas}}`, `{{surface}}`, `{{ink}}` e `{{family}}` nelle nuove scene. Le coordinate restano decisioni della composizione.
5. Aggiungere il record in `figure-index.json`, con sezione esatta, alt, didascalia e componenti.
6. Inserire la figura nella dispensa secondo la [guida editoriale](../../../content/tpsi_quarto/STYLE_GUIDE.md).
7. Rigenerare, aprire gli SVG e controllare leggibilità, etichette, frecce e corrispondenza con la spiegazione.
8. Eseguire i controlli e aggiornare l'audit. Il controllo strutturale non sostituisce la revisione didattica.

Per un nuovo oggetto: aggiungere il symbol in `components.svg`, registrarlo nell'inventario e inserirlo in una scena catalogo. I badge C, POSIX e Java sono etichette didattiche, non loghi ufficiali.

## Provenienza

Riferimento letto il 14 settembre 2026: [Visual System TPSI5](https://github.com/TheBitPoets/tpsi-quinto-docente/tree/main/assets/tpsi5/visual-system). Riutilizzati i simboli user, document, terminal, repository, lock, test, artifact, server e database. I restanti 18 simboli e tutte le scene della quarta sono nuovi. Il generatore riprende il contratto scene/defs della quinta con controlli aggiuntivi.

L'[audit](../../../doc/VISUAL_AUDIT.md) distingue le fonti consultate dal confronto ancora pendente con le immagini interne del libro bSmart.


## Animazioni di I/O e concorrenza

Le due GIF della lezione 01 affiancano le figure statiche. Usano palette e simboli
del kit, testo italiano, didascalia e descrizione alternativa. Sono registrate
nella chiave `animations` di [figure-index.json](figure-index.json); la chiave
`figures` continua a descrivere le scene SVG statiche.

Il [generatore delle animazioni](../../../scripts/build_course_animations.py)
contiene una sequenza di eventi deterministica e il disegno dei fotogrammi.
Rasterizza i simboli `tpsi-cpu`, `tpsi-server` e `tpsi-terminal` direttamente
da `components.svg`, usando Chrome/Chromium locale. I testi usano Arial, oppure
Liberation Sans/DejaVu Sans se Arial non è disponibile. La resa binaria può
variare con browser e font; gli eventi e i tempi restano gli stessi.

| Animazione | Sequenza |
|---|---|
| Un solo thread, 12 s | Attesa sensore fino a 4 s; attesa invio fino a 9 s; poi aggiornamento GUI e gestione dei clic accumulati. |
| Tre thread, 22 s | Un dato in invio e coda di quattro posti; nuove misure ogni 2 s fino a 8 s; sensore in attesa da 9 a 16 s; invii completati ogni 2 s da 10 s; nuove misure a 16 e 18 s. |

La GUI concorrente usa una copia dell'ultimo campione, distinta dalla coda.
Durante la pausa del sensore segnala l'età del dato, mentre continua a gestire
i clic. La coda non perde né duplica misure. Lo scenario raggiunge la capacità
senza superarla: la scelta di cosa fare in caso di ulteriore arrivo è discussa
nel testo. L'invio completato non equivale all'elaborazione completata sul server.

Per rigenerare, con Python 3.11 o successivo e Chrome/Chromium installato:

```bash
python -m pip install -r scripts/requirements-animations.txt
python scripts/build_course_animations.py
python -m unittest discover -s tests -p test_course_animations.py
```

Il generatore accetta `--browser PERCORSO` e `--font-dir CARTELLA` se necessari.
Pillow serve soltanto alla generazione; i test del modello e del registro usano
la libreria standard. Le GIF sono 1200 × 675, a 8 fotogrammi al secondo:
durate di 120 e 130 ms alternate rispettano i tempi del formato GIF.
La riproduzione è ciclica e i tempi sono didattici, diversi da quelli degli SVG
statici. Le figure statiche e il testo restano disponibili per una lettura senza
movimento. Versionare le GIF come file binari.


### Versione con Avvia e Reset

[01-io-animazioni.html](../01-io-animazioni.html) contiene entrambe le GIF e i
fotogrammi iniziali, incorporati nel file. Non parte nulla automaticamente.
Ogni animazione ha controlli indipendenti: Avvia parte dall'inizio; Reset
interrompe la riproduzione e torna al fotogramma zero. Un nuovo avvio usa un
nuovo URL Blob per evitare che la cache riprenda la GIF da un punto precedente.

Il file è utilizzabile offline: da GitHub scaricarlo e aprirlo nel browser.
La vista dei file su GitHub non esegue JavaScript; i pulsanti non possono
essere inseriti direttamente nella GIF o attivati nella dispensa Markdown.

La sorgente dell'interfaccia è [io-player.template.html](io-player.template.html).
La build delle GIF rigenera anche il file HTML. Per aggiornare solo il player:

```bash
python scripts/build_course_animations.py --player-only
```

Questo comando richiede Pillow, ma non Chrome. I dati incorporati devono
corrispondere alle GIF versionate; i test verificano tale corrispondenza.
