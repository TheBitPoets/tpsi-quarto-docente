# Guida docente — TPSI quarto 2026/27

Questa guida descrive **come condurre** il corso. Il contenuto canonico resta in `content/tpsi_quarto/`; questa cartella contiene indicazioni operative e può essere corretta durante l'anno senza cambiare automaticamente il curriculum.

## Stato da tenere visibile

Il Content Pack è `0.1.0 / draft`. Le 33 settimane e UDA 10–16 costituiscono il Course Design corrente, ma il controllo docente non è ancora concluso. Una correzione di slide o di procedura è delivery; una variazione di obiettivi, prerequisiti, UDA o tecnologie obbligatorie è curriculum e va trattata separatamente.

## Sequenza annuale corrente

| UDA | Settimane | Focus | Conduzione consigliata |
|---|---:|---|---|
| 10 | 2 | Metodo, fonti, strumenti | Rendere espliciti provenance, evidenze e workflow del corso. |
| 11 | 6 | Processi/thread/concorrenza | Modello mentale → esempi POSIX → osservazione di processi reali → lab. |
| 12 | 6 | IPC e sincronizzazione | Interleaving/race → primitive → problemi classici → debug di protocolli. |
| 13 | 4 | Requisiti | Partire dai difetti osservati e trasformarli in requisiti verificabili. |
| 14 | 4 | Documentazione/versionamento | Usare il repository stesso come caso reale: commit, branch, PR, review, ADR. |
| 15 | 5 | Testing/debugging | Ipotesi → test → evidenza → debugger/sanitizer → regressione. |
| 16 | 6 | Cittadinanza/progetto finale | Applicare licenze, provenance, privacy, sicurezza e AI al progetto. |

## Struttura suggerita di una lezione

1. **Recall**: una domanda o un piccolo caso dalla lezione precedente.
2. **Modello mentale**: diagramma o timeline prima della sintassi.
3. **Esempio minimo**: una sola idea osservabile.
4. **Variazione controllata**: cambiare un elemento e prevedere il risultato.
5. **Errore tipico**: mostrare un fallimento riproducibile.
6. **Checkpoint**: domanda breve prima del lab.
7. **Lab/progetto**: produrre un'evidenza concreta.
8. **Recap + prossimo passo**.

## Demo e laboratorio

Per processi/concorrenza usare programmi piccoli e osservabili: PID, fork, wait, pipe, exit status e interleaving. Evitare esempi troppo grandi prima che gli studenti sappiano spiegare il modello.

Per sincronizzazione partire da un'invariante e da un'interleaving problematico; introdurre mutex/semaforo/condition come strumenti per preservare proprietà, non come API da memorizzare.

Per requisiti/documentazione/testing riusare lo stesso piccolo progetto concorrente: requisito → commit/PR → test → bug → regressione. In questo modo la seconda metà dell'anno non appare scollegata dalla prima.

## Activity disponibili e gap

Al momento `fork_pipe_square` è l'Activity formalizzata e viene richiamata in UDA11, UDA12 e UDA15. Gli altri moduli hanno esercizi nei contenuti, ma non tutti hanno ancora una Activity TheBitLab formalizzata. Non presentarli come autograded: usare esercizio guidato/manuale finché il contratto Activity non viene creato e validato.

## Valutazione formativa

Privilegiare evidenze brevi e frequenti:

- spiegare un output prima di eseguirlo;
- disegnare un process tree o una timeline;
- individuare una race/deadlock;
- riscrivere un requisito ambiguo;
- spiegare perché un commit è troppo grande;
- scrivere un test che riproduce un bug;
- giustificare una scelta di licenza/provenance.

## Recupero e potenziamento

Per recupero ridurre il numero di primitive/API e mantenere invariato il concetto: un solo processo padre/figlio, una sola pipe, un solo lock, un solo requisito, un solo test.

Per potenziamento aggiungere confronti POSIX/Java, proprietà safety/liveness, fault injection, sanitizer, CI, review più rigorosa e analisi della supply chain, senza renderli automaticamente obbligatori per tutta la classe.

## Aggiornamenti durante l'anno

Quando emerge un problema:

1. correggere il sorgente canonico se il problema è nel contenuto;
2. correggere il deck se il problema è nella spiegazione/proiezione;
3. correggere lab/setup se il problema è operativo;
4. aggiungere una voce a `doc/DELIVERY_CHANGELOG.md`;
5. rigenerare gli artifact quando la pipeline slide sarà attiva;
6. aprire una review curricolare solo se cambiano scope/obiettivi/prerequisiti.

## Prima della pubblicazione agli studenti

Controllare in particolare:

- stato `draft/reviewed/approved` dei materiali;
- Activity realmente disponibili;
- link e comandi eseguibili nell'ambiente scolastico;
- separazione di soluzioni/rubriche;
- diritti/provenance delle fonti;
- eventuali note di sicurezza o privacy.