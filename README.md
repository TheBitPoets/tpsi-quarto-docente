# TPSI quarto anno — Processi, progettazione e qualità del software

Repository docente del corso **TPSI quarto anno** per l'a.s. **2026/2027**.

> **Stato:** Content Pack `0.1.0 / draft`. Il percorso è strutturato su 33 settimane e UDA 10–16, ma non è ancora congelato/approved: materiali, Activity e delivery saranno rivisti dal docente durante l'anno.

## Presentazione del corso

Il corso collega due prospettive che spesso vengono insegnate separatamente. Nella prima parte gli studenti osservano **come più processi e thread cooperano realmente**: concorrenza, IPC, sincronizzazione, race condition, deadlock e primitive POSIX. Nella seconda parte trasformano questa esperienza tecnica in **progettazione e qualità del software**: requisiti verificabili, documentazione, Git e review, testing/debugging, provenienza, sicurezza e cittadinanza digitale.

Il filo pratico è un **progetto concorrente documentato e verificabile**: non basta far funzionare un programma; bisogna saper spiegare requisiti, contratti, rischi, test, versioni e responsabilità.

## Stato del percorso

- **33 settimane**, 3 ore settimanali;
- UDA **10–16**;
- **6 moduli canonici** originali;
- fonte tecnica Linux Programming pinned da `TheBitPoets/2cornot2c`;
- Content Pack v1 già adottato, ma stato editoriale ancora `draft`;
- Activity attualmente disponibile: `fork_pipe_square`, collegata ai moduli 01, 02 e 05;
- gli altri laboratori richiesti dal percorso restano da completare/validare: il README li mostra esplicitamente come gap, non come materiale inesistente “automaticamente disponibile”.

## Entrate rapide

- [Indice e stato delle slide](slides/tpsi4/README.md)
- [Guida docente](teacher/README.md)
- [Guida studente](student/README.md)
- [Delivery Change Log](doc/DELIVERY_CHANGELOG.md)
- [Content Pack v1](content/tpsi_quarto/content-pack.json)
- [Matrice di copertura](content/tpsi_quarto/COVERAGE.md)
- [Course Design 2026/27](doc/course_designs/tpsi_quarto_2026_2027.json)

## Come usare il repository in classe

1. Apri il modulo della settimana dalla tabella qui sotto.
2. Usa il deck dedicato come sequenza di spiegazione e checkpoint.
3. Passa al laboratorio/Activity quando disponibile; quando il grader non esiste, usa la modalità manuale/rubric indicata dal docente.
4. Collega ogni attività al progetto concorrente e conserva evidenze: codice, test, output, commit e breve spiegazione tecnica.
5. Le correzioni di delivery vengono annotate in `doc/DELIVERY_CHANGELOG.md`; un cambiamento di obiettivi/UDA/prerequisiti resta invece una modifica curricolare.

## Indice cliccabile del corso

| UDA | Modulo | Lezione canonica | Slide | Activity/Lab | Nucleo didattico |
|---|---:|---|---|---|---|
| UDA-10 | 00 | [Indice, fonti e metodo](content/tpsi_quarto/README.md) | [Slide 00](slides/tpsi4/modules/00_COURSE_ORIENTATION.md) | — | Fonti, provenance, percorso, evidenze e metodo di lavoro. |
| UDA-11 | 01 | [Processi, thread e concorrenza](content/tpsi_quarto/01_PROCESSI_E_CONCORRENZA.md) | [Slide 01](slides/tpsi4/modules/01_PROCESSI_E_CONCORRENZA.md) | [fork_pipe_square](activities/tpsi_quarto/fork_pipe_square/) | Processo/thread, fork/exec/wait, concorrenza, parallelismo e risorse. |
| UDA-12 | 02 | [Comunicazione e sincronizzazione](content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md) | [Slide 02](slides/tpsi4/modules/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md) | [fork_pipe_square](activities/tpsi_quarto/fork_pipe_square/) + lab da completare | IPC, race, mutex, semafori, condition, deadlock e problemi classici. |
| UDA-13 | 03 | [Requisiti software](content/tpsi_quarto/03_REQUISITI_SOFTWARE.md) | [Slide 03](slides/tpsi4/modules/03_REQUISITI_SOFTWARE.md) | da completare/validare | Requisiti, attori, casi d'uso, scenari, acceptance criteria e tracciabilità. |
| UDA-14 | 04 | [Documentazione e controllo di versione](content/tpsi_quarto/04_DOCUMENTAZIONE_VERSIONAMENTO.md) | [Slide 04](slides/tpsi4/modules/04_DOCUMENTAZIONE_VERSIONAMENTO.md) | da completare/validare | README, documentazione, ADR, Git, branch, PR, review e provenance. |
| UDA-15 | 05 | [Testing e debugging](content/tpsi_quarto/05_TESTING_DEBUGGING.md) | [Slide 05](slides/tpsi4/modules/05_TESTING_DEBUGGING.md) | [fork_pipe_square](activities/tpsi_quarto/fork_pipe_square/) + regressioni | Verifica/validazione, test, sanitizer, debugger, regressioni e CI. |
| UDA-16 | 06 | [Cittadinanza digitale](content/tpsi_quarto/06_CITTADINANZA_DIGITALE.md) | [Slide 06](slides/tpsi4/modules/06_CITTADINANZA_DIGITALE.md) | progetto finale/rubric da validare | Licenze, privacy, segreti, supply chain, accessibilità, AI e responsabilità. |

## Mappa concettuale

```text
processi / thread
      ↓
concorrenza e IPC
      ↓
sincronizzazione e proprietà di correttezza
      ↓
requisiti verificabili
      ↓
documentazione + Git + review
      ↓
test + debugging + regressioni
      ↓
progetto finale responsabile e documentato
```

## Confini e provenienza

Il riferimento bibliografico Hoepli è usato per la **copertura curricolare**, non come testo da riprodurre. I contenuti originali sono nel repository; Linux Programming è una fonte tecnica separata e pinned. Le regole complete di provenance sono nel Content Pack e nella documentazione del corso.

Questo delivery layer non promuove automaticamente il Content Pack da `draft` ad `approved` e non sostituisce il controllo docente.