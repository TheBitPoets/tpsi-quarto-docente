# TPSI quarto anno — Sistemi concorrenti e progettazione del software

Repository docente del corso **TPSI quarto anno**, a.s. **2026/2027**, del prof. **Antonio Caristia** e dell'ITP **Antonino Pirri**.

Il percorso parte da processi, thread e comunicazione in C/POSIX, introduce confronti con Java e prosegue con requisiti, documentazione, Git, testing e cittadinanza digitale, fino a un progetto concorrente documentato e verificabile.

Questa è una **prima bozza di pianificazione**: i materiali sono in stato `draft`. L'organizzazione del README riprende il [corso di quinta](https://github.com/TheBitPoets/tpsi-quinto-docente/blob/main/README.md); UDA e settimane seguono il [Course Design della quarta](doc/course_designs/tpsi_quarto_2026_2027.json). Le assegnazioni ai docenti e le ore delle singole lezioni sono una proposta iniziale, da aggiornare durante l'anno.

## Pianificazione annuale e suddivisione in UDA

Il piano della quarta prevede **99 ore nominali: 33 settimane × 3 ore**. La proposta assegna **50 ore ad Antonio Caristia e 49 ad Antonino Pirri**, la ripartizione più vicina al 50% usando ore intere.

Come nel corso di quinta, ciascun docente conduce le lezioni assegnate, comprendendo spiegazione, esempi ed esercitazioni. Se una lezione richiede più tempo, la conclude il responsabile; gli scostamenti si compensano sulle lezioni successive o sulla riserva. Le colonne indicano ore di conduzione didattica, non un conteggio amministrativo delle eventuali compresenze.

Sono proposte **87 ore di lezioni e attività**, **4 ore per due compiti da 2 ore**, uno per quadrimestre, e **8 ore di riserva** per recupero, consolidamento, ulteriori verifiche o imprevisti. Compiti e riserva sono già inclusi nei totali delle UDA.

| UDA | Settimane | Lezioni e attività | Compiti | Riserva flessibile | Totale UDA | Antonio Caristia | Antonino Pirri |
|---|---:|---:|---:|---:|---:|---:|---:|
| UDA-10 — Avvio del percorso, strumenti e fonti | 2 | 6 | 0 | 0 | 6 | 3 | 3 |
| UDA-11 — Processi, thread e concorrenza | 6 | 17 | 0 | 1 | 18 | 9 | 9 |
| UDA-12 — Comunicazione e sincronizzazione | 6 | 15 | 2 | 1 | 18 | 11 | 7 |
| UDA-13 — Requisiti software | 4 | 11 | 0 | 1 | 12 | 6 | 6 |
| UDA-14 — Documentazione e controllo di versione | 4 | 11 | 0 | 1 | 12 | 6 | 6 |
| UDA-15 — Testing e debugging | 5 | 12 | 0 | 3 | 15 | 7 | 8 |
| UDA-16 — Cittadinanza digitale e progetto finale | 6 | 15 | 2 | 1 | 18 | 8 | 10 |
| **Totale** | **33** | **87** | **4** | **8** | **99** | **50** | **49** |

## Lezioni, materiali e docenti responsabili

Le righe seguenti suddividono le dispense esistenti in blocchi didattici: ogni blocco può occupare più incontri. Le ore comprendono le esercitazioni collegate. I titoli aprono la dispensa o la sezione pertinente; i numeri delle lezioni sono identificatori di questa proposta.

La colonna del consuntivo resta vuota (`—`) finché non vengono comunicate le lezioni effettivamente svolte. Va compilata con data e ore, senza usare le settimane previste come date già effettuate.

| UDA | Lezione e materiali | Attività previste o collegate | Ore | Docente responsabile | Date e ore svolte |
|---|---|---|---:|---|---|
| UDA-10 | [00 — Presentazione del percorso, fonti e metodo](content/tpsi_quarto/README.md) | Orientamento fra moduli, obiettivi e [matrice di copertura](content/tpsi_quarto/COVERAGE.md). | 3 | Antonio Caristia | — |
| UDA-10 | [01 — Ripartenza C/Linux e strumenti](content/tpsi_quarto/01_PROCESSI_E_CONCORRENZA.md#prerequisiti) | Ripasso di compilazione, terminale, memoria e gestione degli errori; controllo dei prerequisiti. | 3 | Antonino Pirri | — |
| UDA-11 | [02 — Processi, risorse e concorrenza](content/tpsi_quarto/01_PROCESSI_E_CONCORRENZA.md) | Ciclo di vita, gerarchia, `fork`/`exec`/`wait`, tracce di esecuzione ed esercizi del modulo. | 9 | Antonio Caristia | — |
| UDA-11 | [03 — Thread POSIX e confronto Java](content/tpsi_quarto/01_PROCESSI_E_CONCORRENZA.md#da-processo-a-thread) | Thread, `Runnable`, `join`, esercizi e avvio del [laboratorio fork/pipe](activities/tpsi_quarto/fork_pipe_square/student/README.md). | 8 | Antonino Pirri | — |
| UDA-12 | [04 — Comunicazione fra processi e pipe](content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#comunicazione-tra-processi-con-pipe) | Messaggi, segnali e completamento del [laboratorio fork/pipe](activities/tpsi_quarto/fork_pipe_square/student/README.md). | 7 | Antonino Pirri | — |
| UDA-12 | [05 — Sincronizzazione e problemi classici](content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#race-condition) | Race condition, mutex, semafori, condition, deadlock e produttore/consumatore; confronto POSIX/Java. | 8 | Antonio Caristia | — |
| UDA-13 | [06 — Dai bisogni ai requisiti verificabili](content/tpsi_quarto/03_REQUISITI_SOFTWARE.md) | Requisiti funzionali e non funzionali, attori, scenari e criteri di accettazione. | 6 | Antonio Caristia | — |
| UDA-13 | [07 — Specifica e tracciabilità del progetto](content/tpsi_quarto/03_REQUISITI_SOFTWARE.md#esercizi-graduati) | Esercizi e laboratorio del modulo: mini SRS e collegamento fra requisiti e verifiche. | 5 | Antonino Pirri | — |
| UDA-14 | [08 — Documentare codice e progetto](content/tpsi_quarto/04_DOCUMENTAZIONE_VERSIONAMENTO.md) | README, contratti, documentazione architetturale, ADR e provenienza. | 5 | Antonio Caristia | — |
| UDA-14 | [09 — Git, conflitti e code review](content/tpsi_quarto/04_DOCUMENTAZIONE_VERSIONAMENTO.md#controllo-di-versione-con-git) | Commit, branch, merge e laboratorio di documentazione e versionamento di una activity. | 6 | Antonino Pirri | — |
| UDA-15 | [10 — Strategia di verifica e casi di test](content/tpsi_quarto/05_TESTING_DEBUGGING.md) | Verifica e validazione, livelli di test, classi di equivalenza, valori limite e regressioni. | 6 | Antonio Caristia | — |
| UDA-15 | [11 — Debugging e collaudo del laboratorio](content/tpsi_quarto/05_TESTING_DEBUGGING.md#debugging-come-ciclo-di-ipotesi) | Debugger, sanitizer, bug concorrenti e test del [programma fork/pipe](activities/tpsi_quarto/fork_pipe_square/student/README.md). | 6 | Antonino Pirri | — |
| UDA-16 | [12 — Cittadinanza digitale per chi progetta software](content/tpsi_quarto/06_CITTADINANZA_DIGITALE.md) | Provenienza, licenze, dati, segreti, accessibilità e uso responsabile dell'AI. | 7 | Antonio Caristia | — |
| UDA-16 | [13 — Progetto finale integrato](content/tpsi_quarto/06_CITTADINANZA_DIGITALE.md#progetto-finale-suggerito) | Progetto concorrente con requisiti, repository documentato, test, demo e relazione finale. | 8 | Antonino Pirri | — |
| **Totale** | | | **87** | | |

Il laboratorio `fork_pipe_square` è un'unica attività, ripresa con obiettivi diversi nelle UDA-11, UDA-12 e UDA-15. È attualmente l'unica activity con bundle autonomo nel repository; gli altri esercizi e laboratori si trovano nelle dispense.

## Compiti e riserva

La collocazione dei compiti nelle UDA è indicativa; le date saranno stabilite in base al calendario effettivo dei quadrimestri.

| UDA | Voce | Antonio Caristia | Antonino Pirri | Totale | Date e ore svolte |
|---|---|---:|---:|---:|---|
| UDA-11 | Riserva: consolidamento di processi e thread | 0 | 1 | 1 | — |
| UDA-12 | Compito del primo quadrimestre | 2 | 0 | 2 | — |
| UDA-12 | Riserva: recupero sulla sincronizzazione | 1 | 0 | 1 | — |
| UDA-13 | Riserva: revisione dei requisiti | 0 | 1 | 1 | — |
| UDA-14 | Riserva: documentazione e Git | 1 | 0 | 1 | — |
| UDA-15 | Riserva: recupero, debugging e ulteriori verifiche | 1 | 2 | 3 | — |
| UDA-16 | Compito del secondo quadrimestre | 0 | 2 | 2 | — |
| UDA-16 | Riserva: consolidamento e consegna finale | 1 | 0 | 1 | — |
| **Totale** | | **6** | **6** | **12** | |

## Ripartizione complessiva fra i docenti

| Docente | Lezioni e attività | Compiti | Riserva flessibile | Totale annuale |
|---|---:|---:|---:|---:|
| prof. Antonio Caristia | 44 | 2 | 4 | **50** |
| ITP Antonino Pirri | 43 | 2 | 4 | **49** |
| **Totale** | **87** | **4** | **8** | **99** |

Gli scostamenti dal preventivo vanno riportati nel consuntivo e compensati aggiornando insieme la tabella delle lezioni, quella delle UDA e il riepilogo dei docenti.

## Riferimenti del percorso

- [Indice delle dispense](content/tpsi_quarto/README.md).
- [Matrice di copertura curricolare](content/tpsi_quarto/COVERAGE.md).
- [Course Design 2026/2027](doc/course_designs/tpsi_quarto_2026_2027.json), fonte di UDA e settimane.
- [Content Pack](content/tpsi_quarto/content-pack.json), con fonti e stato dei materiali.
- [Note docente del laboratorio fork/pipe](activities/tpsi_quarto/fork_pipe_square/teacher/NOTES.md).

La dispensa integrativa `LINUX_PROGRAMMING.md` è una fonte remota del repository `TheBitPoets/2cornot2c`, identificata nel Content Pack; non è un file locale di questo repository. Il percorso la utilizza a partire dalla sezione `Linux Programming`, escludendo la sezione iniziale `Controllo dei processi`.

## Immagini e formattazione del corso

- [Audit delle figure e degli oggetti ricorrenti](doc/VISUAL_AUDIT.md).
- [Visual System e cataloghi dei 27 oggetti](assets/tpsi4/visual-system/README.md).
- [Guida di formattazione delle dispense](content/tpsi_quarto/STYLE_GUIDE.md).
- [Registro delle 26 figure](assets/tpsi4/visual-system/figure-index.json).

Le immagini sono composte da simboli SVG riutilizzabili e inserite nei sei moduli con testo alternativo e didascalia. Per rigenerare e verificare gli SVG dalla root del repository:

```bash
python scripts/build_course_diagrams.py
python scripts/build_course_diagrams.py --check
python -m unittest discover -s tests -p test_course_diagrams.py
```

Le sei dispense seguono il template HTML della quinta e di 2cornot2c: orientamento con icone canoniche, paragrafi giustificati, liste e tabelle HTML. Il controllo `python scripts/format_tpsi4_lessons.py --check` verifica la formattazione; usare `--write` per applicarla intenzionalmente.

Modificare componenti o scene sorgente; gli SVG finali e i cataloghi vengono rigenerati. Il confronto con le figure interne del libro bSmart resta da completare: stato e fonti consultate sono indicati nell'audit.
