# Matrice di copertura TPSI quarto anno

Questa matrice controlla la fedeltà curricolare del pacchetto senza misurare la somiglianza testuale con il libro adottato.

Legenda stato:

- **baseline**: teoria, esempi, esercizi e proposta di laboratorio presenti nel modulo;
- **pilot activity**: almeno una activity assegnabile è già inclusa;
- **activity da creare**: il contenuto è presente, ma manca ancora una activity dedicata a quella specifica voce curricolare;
- **revisione docente**: è richiesta una verifica didattica o tecnica prima della pubblicazione;
- **licenza da verificare**: il frammento della fonte tecnica contiene materiale esterno da controllare o sostituire.

> **Nota sulla granularità:** la presenza di almeno una Activity canonica in un modulo non implica che ogni sua voce curricolare abbia già un laboratorio dedicato. Le righe marcate `activity da creare` restano quindi gap reali di approfondimento anche quando il modulo, nel suo complesso, è già assegnabile.

## Processi sequenziali e paralleli

| Voce curricolare | Contenuto originale | Collegamenti Linux | Attività/laboratorio | Stato |
| --- | --- | --- | --- | --- |
| Il modello a processi | `01_PROCESSI_E_CONCORRENZA.md` → Dal programma al processo; stati e ciclo di vita | `Linux Programming` → Processi; Process IDs; vedere i processi attivi | osservazione PID/PPID; albero dei processi; laboratorio `fork`/pipe | baseline, pilot activity |
| Risorse e condivisione | `01_PROCESSI_E_CONCORRENZA.md` → Spazio di indirizzamento e risorse | processi vs thread; dati specifici del thread | confronto memoria separata/condivisa; tabella delle risorse | baseline, activity da creare |
| I thread o processi leggeri | `01_PROCESSI_E_CONCORRENZA.md` → Thread e processo; confronto C/Java | I Thread; creazione, dati, join, ritorno, attributi | contatore concorrente; Java `Runnable`; debug di una race | baseline, activity da creare |
| L'elaborazione concorrente | `01_PROCESSI_E_CONCORRENZA.md` → Concorrenza, parallelismo e interleaving | thread sincroni e asincroni; processi vs thread | simulazione di interleaving; misurazione tempi | baseline, activity da creare |
| La descrizione della concorrenza | `01_PROCESSI_E_CONCORRENZA.md` → Tracce, invarianti e proprietà | sezioni critiche; race condition | diagramma degli eventi; proprietà safety/liveness | baseline, activity da creare |

## Comunicazione e sincronizzazione

| Voce curricolare | Contenuto originale | Collegamenti Linux | Attività/laboratorio | Stato |
| --- | --- | --- | --- | --- |
| La comunicazione tra processi | `02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md` → IPC e canali | `fork`, `exec`, segnali, `wait`; estensione originale su pipe | pipe padre/figlio; protocollo a messaggi | baseline, pilot collegato |
| La sincronizzazione tra processi | `02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md` → ordine, mutua esclusione e attesa | sincronizzazione e sezioni critiche; variabili di condizione | barriera concettuale; ordine di stampa deterministico | baseline, activity da creare |
| I semafori | `02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md` → contatore e operazioni atomiche | Semafori | parcheggio con posti limitati; confronto `sem_t`/`Semaphore` | baseline, activity da creare |
| Applicazione dei semafori | `02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md` → pattern di uso | Semafori; mutex e condition | turnazione, barriera, pool di risorse | baseline, activity da creare |
| Produttori/consumatori | `02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md` → buffer limitato | mutex, semafori, variabili di condizione | `tpsi4-activity-c-producer-consumer-buffer-001`: coda circolare C con mutex/condition | baseline, pilot activity |
| Lettori/scrittori | `02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md` → politiche e starvation | deadlock con più thread; mutex | registro condiviso con politica esplicita | baseline, activity da creare |
| Deadlock | `02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md` → condizioni e prevenzione | Mutex Deadlocks; Deadlocks con due o più Thread | laboratorio dei due lock; ordine globale | baseline, activity da creare |
| Monitor | `02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md` → stato protetto e condition | mutex + variabili di condizione | monitor concettuale C; classe Java sincronizzata | baseline, activity da creare |
| Scambio di messaggi | `02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md` → protocollo e ownership | segnali e processi; estensione originale IPC | mini servizio request/response | baseline, activity da creare |

## Requisiti software

| Voce curricolare | Contenuto originale | Fonte tecnica | Attività/laboratorio | Stato |
| --- | --- | --- | --- | --- |
| La specifica dei requisiti | `03_REQUISITI_SOFTWARE.md` → requisiti verificabili | documentazione interna del progetto e casi d'uso originali | `tpsi4-activity-c-mini-srs-traceability-001`: mini-SRS con RF/RNF verificabili | baseline, pilot activity |
| Raccolta e analisi dei requisiti | `03_REQUISITI_SOFTWARE.md` → stakeholder, interviste e conflitti | issue e scenari del progetto come esempi | stessa Activity: matrice stakeholder/bisogni e priorità | baseline, pilot collegato |
| Attori, casi d'uso e scenari | `03_REQUISITI_SOFTWARE.md` → use case e flussi | diagrammi Mermaid originali | stessa Activity: UC con main flow e alternative | baseline, pilot collegato |
| Documentazione dei requisiti | `03_REQUISITI_SOFTWARE.md` → SRS leggera e tracciabilità | issue, decisioni e test di accettazione | stessa Activity: `SRS.md` + `TRACEABILITY.csv` | baseline, pilot activity |

## Documentazione del software

| Voce curricolare | Contenuto originale | Fonte tecnica | Attività/laboratorio | Stato |
| --- | --- | --- | --- | --- |
| La documentazione del progetto | `04_DOCUMENTAZIONE_VERSIONAMENTO.md` → pubblico, struttura e decisioni | documentazione esistente di 2cornot2c | `tpsi4-activity-c-docs-git-review-001`: README + ADR | baseline, pilot activity |
| La documentazione del codice | `04_DOCUMENTAZIONE_VERSIONAMENTO.md` → nomi, contratti, commenti e API | esempi originali C/Java | migliorare codice poco leggibile; generare documentazione | baseline, activity da creare |
| Controllo delle versioni | `04_DOCUMENTAZIONE_VERSIONAMENTO.md` → commit, branch, merge e review | Git e GitHub; workflow del repository | stessa Activity: branch, almeno due commit, PR e self-review | baseline, pilot activity |

## Testing e debugging

| Voce curricolare | Contenuto originale | Fonte tecnica | Attività/laboratorio | Stato |
| --- | --- | --- | --- | --- |
| Verifica e validazione del software | `05_TESTING_DEBUGGING.md` → costruire bene/costruire il prodotto giusto | activity, rubriche e criteri di accettazione | derivare test dai requisiti | baseline, activity da creare |
| Verifica statica e dinamica | `05_TESTING_DEBUGGING.md` → review, warning, sanitizer, test | runner, GCC, test deterministici, sandbox | `tpsi4-activity-c-memory-debug-regression-001`: compilazione rigorosa, test e sanitizer | baseline, pilot activity |
| Debugging di un programma | `05_TESTING_DEBUGGING.md` → riproduzione, ipotesi, osservazione e fix | output runner e report | stessa Activity: bug di confine, causa radice, fix minimo e regressione | baseline, pilot activity |

## Cittadinanza digitale

| Nucleo | Contenuto originale | Attività | Stato |
| --- | --- | --- | --- |
| Licenze e uso corretto delle fonti | `06_CITTADINANZA_DIGITALE.md` | `tpsi4-activity-d-responsible-capstone-001`: manifest fonti, ref/versioni e license-status | baseline, pilot activity, revisione docente |
| Collaborazione responsabile | `06_CITTADINANZA_DIGITALE.md` | capstone + continuità con review UDA14; segnalazione responsabile da approfondire | baseline, pilot collegato |
| Privacy e dati scolastici | `06_CITTADINANZA_DIGITALE.md` | capstone: inventario dati, minimizzazione, ruoli e segreti | baseline, pilot activity |
| Sicurezza della supply chain | `06_CITTADINANZA_DIGITALE.md` | capstone: dipendenze, fonti, versioni, rischi e contromisure | baseline, pilot activity |
| Uso responsabile dell'AI | `06_CITTADINANZA_DIGITALE.md` | capstone: uso AI dichiarato o assente, verifica umana e limiti dell'automazione | baseline, pilot activity |

## Copertura minima assegnabile per modulo

Questa tabella misura un requisito diverso dalla copertura granulare sopra: verifica che **ogni modulo del Content Pack abbia almeno una Activity canonica assegnabile**. Non elimina i laboratori aggiuntivi ancora indicati come `activity da creare`.

| Modulo | Activity canoniche presenti | Stato sullo stack UDA12–UDA16 |
| --- | --- | --- |
| 01 — Processi e concorrenza | `tpsi4-activity-c-fork-pipe-square-001` | presente |
| 02 — Comunicazione e sincronizzazione | `tpsi4-activity-c-fork-pipe-square-001`; `tpsi4-activity-c-producer-consumer-buffer-001` | presente |
| 03 — Requisiti software | `tpsi4-activity-c-mini-srs-traceability-001` | presente |
| 04 — Documentazione e versionamento | `tpsi4-activity-c-docs-git-review-001` | presente |
| 05 — Testing e debugging | `tpsi4-activity-c-memory-debug-regression-001` | presente |
| 06 — Cittadinanza digitale | `tpsi4-activity-d-responsible-capstone-001` | presente |

**Esito dello stack corrente:** 6/6 moduli hanno almeno una Activity canonica. Il pacchetto resta `draft`: questo traguardo non sostituisce revisione docente, validazione dei diritti delle fonti, CI eseguibile e collaudo del flusso reale di assegnazione.

## Controllo della qualità didattica

Per ciascuna riga la revisione deve verificare:

1. corrispondenza tra obiettivi, teoria, esempio e attività;
2. presenza di almeno un errore frequente o caso limite;
3. progressione da osservazione a produzione autonoma;
4. distinzione fra concetto generale e dettaglio di una piattaforma;
5. presenza di una forma di verifica;
6. accessibilità del linguaggio e sintesi inclusiva;
7. riferimenti alle fonti e stato di licenza;
8. assenza di copie sostanziali del testo editoriale.

## Copertura `LINUX_PROGRAMMING.md`

Sezioni incluse nel lavoro di integrazione:

- Processi e Process IDs;
- visualizzazione e terminazione dei processi;
- `system`, `fork`, famiglia `exec`;
- segnali e `sigaction`;
- terminazione, `wait`, zombie e cleanup asincrono;
- thread POSIX, parametri, join, ritorno e attributi;
- cancellazione, dati specifici e cleanup handler;
- race condition e sezioni critiche;
- mutex, trylock e deadlock;
- semafori e variabili di condizione;
- implementazione Linux, `clone` e confronto processi/thread.

Sezione esclusa:

- `Controllo dei processi` e le relative slide iniziali.

Nota di licenza: gli esempi presenti nella dispensa che dichiarano una provenienza editoriale esterna devono essere controllati singolarmente. Dove la licenza non consente la redistribuzione o non è chiara, il pacchetto deve usare una nuova implementazione originale.

## Gap tecnici della piattaforma

| Gap | Impatto | Strategia iniziale |
| --- | --- | --- |
| runner Java non implementato | niente grading automatico Java | activity Java con rubrica docente e `test: false` |
| fonti remote non sincronizzate | repository privato non indicizzato automaticamente | fonte locale nel repository; migrazione futura al provider GitHub |
| content pack non ancora entità runtime | manifest non letto dalla dashboard | mantenere Markdown e activity come dati autorevoli correnti |
| collegamenti activity/UDA ancora in evoluzione | parte dei legami può essere manuale | ID stabili e `activity_ids` nel Content Pack; Course Design archiviato resta storico |
| preview asset incompleta | immagini/diagrammi possono non rendersi | testo alternativo e diagrammi sorgente leggibili |
| GitHub Actions TPSI4 non esegue i job | impossibile usare la CI hosted come prova del pacchetto | mantenere PR draft; usare validazione controllata equivalente finché il runner non torna disponibile |

## Stato del primo incremento

Il primo incremento è completo quando sono presenti:

- contratto e manifest;
- tutti i moduli Markdown di baseline;
- progetto archiviato del quarto anno;
- una activity C/POSIX end-to-end con starter e soluzione docente;
- documentazione di importazione;
- PR draft collegata a #625.

Questo traguardo storico è stato superato sullo stack corrente: oltre al pilot C/POSIX, ogni modulo 01–06 possiede almeno una Activity canonica assegnabile.

La chiusura di #625 richiede comunque la revisione docente, il controllo delle fonti/licenze, il collaudo completo dalla dashboard e gli altri criteri di accettazione dell'issue. La presenza delle Activity non autorizza da sola la promozione del pacchetto ad `approved`.
