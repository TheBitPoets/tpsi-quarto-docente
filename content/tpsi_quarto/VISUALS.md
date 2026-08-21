# Inventario visivo TPSI quarto

Questo inventario distingue i diagrammi che migliorano realmente la comprensione dai blocchi che devono restare testo, codice o Mermaid.

## Stato

- **integrato**: SVG creato e referenziato dal modulo principale o dalla relativa guida in `visuals/`;
- **testo**: non convertire, perché deve restare copiabile o modificabile;
- **Mermaid**: mantenere come diagramma testuale versionabile.

La produzione pianificata comprende **27 diagrammi SVG originali**. Tutti sono presenti e referenziati.

## Modulo 1 — Processi, thread e concorrenza

| Concetto | Decisione | Stato | File |
| --- | --- | --- | --- |
| soluzione sequenziale e attività coordinate | mantenere testo: è pseudocodice introduttivo | testo | — |
| ciclo di vita del processo | macchina a stati SVG | integrato | `assets/diagrams/01-process-lifecycle.svg` |
| sequenziale, concorrente, parallelo | confronto temporale SVG | integrato | `assets/diagrams/01-execution-models.svg` |
| risorse di processi e thread | schema memoria privata/condivisa | integrato | `assets/diagrams/01-process-thread-resources.svg` |
| fork/exec/wait | flusso padre-figlio | integrato | `assets/diagrams/01-fork-exec-wait.svg` |
| interleaving e incremento perso | timeline di due thread | integrato | `assets/diagrams/01-lost-update.svg` |
| formula dell'invariante | mantenere testo | testo | — |

Guida: [`visuals/01_PROCESSI_E_CONCORRENZA.md`](visuals/01_PROCESSI_E_CONCORRENZA.md).

## Modulo 2 — Comunicazione e sincronizzazione

| Concetto | Decisione | Stato | File |
| --- | --- | --- | --- |
| produttore, buffer e consumatore | schema con mutex e condition | integrato | `assets/diagrams/02-producer-consumer-buffer.svg` |
| estremità della pipe | diagramma padre/figlio | integrato | `assets/diagrams/02-pipe-parent-child.svg` |
| decomposizione di `counter++` | read-modify-write e finestra di race | integrato | `assets/diagrams/02-race-read-modify-write.svg` |
| lock e sezione critica | mantenere pseudocodice | testo | — |
| `wait` su variabile di condizione | schema di rilascio, attesa e ricontrollo | integrato | `assets/diagrams/02-condition-wait.svg` |
| produttore/consumatore pseudocodice | mantenere testo modificabile | testo | — |
| deadlock a due lock | grafo circolare di attesa | integrato | `assets/diagrams/02-deadlock-cycle.svg` |
| monitor | stato privato, metodi e condizioni | integrato | `assets/diagrams/02-monitor.svg` |
| ownership del thread database | message-passing e proprietario unico | integrato | `assets/diagrams/02-single-owner.svg` |
| envelope del messaggio | mantenere struttura testuale | testo | — |

Guida: [`visuals/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md`](visuals/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md).

## Modulo 3 — Requisiti software

| Concetto | Decisione | Stato | File |
| --- | --- | --- | --- |
| bisogno, requisito, soluzione, vincolo | mappa a quattro concetti | integrato | `assets/diagrams/03-requirement-concepts.svg` |
| diagramma di contesto TheBitLab | mantenere Mermaid | Mermaid | — |
| tracciabilità bisogno → risultato | catena bidirezionale SVG | integrato | `assets/diagrams/03-requirements-traceability.svg` |
| caso d'uso | mantenere template testuale | testo | — |

Guida: [`visuals/03_REQUISITI_SOFTWARE.md`](visuals/03_REQUISITI_SOFTWARE.md).

## Modulo 4 — Documentazione e versionamento

| Concetto | Decisione | Stato | File |
| --- | --- | --- | --- |
| architettura GUI/API/service/provider | livelli e confini SVG | integrato | `assets/diagrams/04-architecture-layers.svg` |
| sequenza Course Board / catalogo / activity | mantenere Mermaid | Mermaid | — |
| flusso Git branch/commit/PR/review | diagramma di processo | integrato | `assets/diagrams/04-git-workflow.svg` |
| provenienza delle fonti | grafo fonte/versione/trasformazione/revisione | integrato | `assets/diagrams/04-provenance.svg` |

Guida: [`visuals/04_DOCUMENTAZIONE_VERSIONAMENTO.md`](visuals/04_DOCUMENTAZIONE_VERSIONAMENTO.md).

## Modulo 5 — Testing e debugging

| Concetto | Decisione | Stato | File |
| --- | --- | --- | --- |
| verifica e validazione | doppio percorso requisito/prodotto/bisogno | integrato | `assets/diagrams/05-verification-validation.svg` |
| livelli di test | scala unità → integrazione → sistema → accettazione | integrato | `assets/diagrams/05-test-levels.svg` |
| ciclo di vita `draft → closed` | macchina a stati | integrato | `assets/diagrams/05-content-lifecycle.svg` |
| ciclo del debugging | ciclo ipotesi → prova → fix → regressione | integrato | `assets/diagrams/05-debug-cycle.svg` |
| pipeline di qualità | controlli locali automatici e revisione umana | integrato | `assets/diagrams/05-quality-pipeline.svg` |
| comandi GDB, sanitizer e output | mantenere testo copiabile | testo | — |

Guida: [`visuals/05_TESTING_DEBUGGING.md`](visuals/05_TESTING_DEBUGGING.md).

## Modulo 6 — Cittadinanza digitale

| Concetto | Decisione | Stato | File |
| --- | --- | --- | --- |
| accesso, copia, modifica e redistribuzione | matrice dei diritti distinti | integrato | `assets/diagrams/06-usage-rights.svg` |
| quattro ruoli della provenienza | libro, fonte tecnica, contenuto originale, revisore | integrato | `assets/diagrams/06-provenance-roles.svg` |
| minimizzazione dei dati | triangolo scopo/durata/accesso | integrato | `assets/diagrams/06-data-minimization.svg` |
| ruoli e autorizzazioni | mantenere tabella | testo | — |
| supply chain | dipendenze → build → artefatto → distribuzione | integrato | `assets/diagrams/06-supply-chain.svg` |
| uso responsabile dell'AI | fonti → AI → revisione → pubblicazione | integrato | `assets/diagrams/06-responsible-ai.svg` |

Guida: [`visuals/06_CITTADINANZA_DIGITALE.md`](visuals/06_CITTADINANZA_DIGITALE.md).

## Regola di completamento

La fase visiva è completa quando:

1. ogni SVG supera il controllo XML e accessibilità;
2. ogni riferimento Markdown punta a un file esistente;
3. nessun comando, output o pseudocodice utile è stato sostituito da un'immagine non copiabile;
4. i diagrammi Mermaid validi restano versionabili;
5. ogni immagine ha alt text e fallback testuale quando sostituisce un'ASCII art nel modulo principale;
6. ogni diagramma restante è raccolto nella guida visiva del modulo;
7. nessun asset deriva da immagini del libro adottato;
8. il repository privato non contiene GitHub Actions.

## Stato finale della produzione

- SVG previsti: **27**;
- SVG presenti: **27**;
- guide visive: **6**;
- diagrammi del libro copiati o ricalcati: **0**;
- workflow GitHub Actions private: **0**.
