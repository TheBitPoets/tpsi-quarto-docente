# Riferimento docente — Mini-SRS MonitorMisure

Questo file mostra **una** soluzione coerente, non l'unica possibile. Va usato per calibrare la rubrica e discutere le scelte, non come testo da riprodurre.

## Esempio di contesto

MonitorMisure è un prototipo didattico che acquisisce una sequenza di misure simulate, le trasferisce a una componente di elaborazione e produce un riepilogo verificabile della sessione. L'iterazione corrente deve essere dimostrabile offline e non usa dati personali.

## Stakeholder di esempio

| Stakeholder | Bisogno | Rischio se ignorato |
| --- | --- | --- |
| tecnico di laboratorio | avviare una sessione e capire se procede | sessioni inutilizzabili o non diagnosticabili |
| docente | verificare quantità acquisite/elaborate | impossibilità di valutare la correttezza |
| manutentore | riprodurre errori e avere evidenze | difetti intermittenti non correggibili |
| scuola | evitare dati/credenziali reali | rischio privacy e sicurezza |

## Requisiti funzionali di esempio

- **RF-01 / Must** — Il sistema deve permettere all'operatore di avviare una sessione specificando il numero di misure simulate da acquisire entro il dominio ammesso.
- **RF-02 / Must** — Durante una sessione il sistema deve trasferire ogni misura acquisita alla componente di elaborazione senza duplicazioni intenzionali.
- **RF-03 / Must** — Al termine di una sessione il sistema deve produrre un riepilogo con numero di misure acquisite, numero di misure elaborate ed esito della sessione.
- **RF-04 / Should** — Se una sessione non può essere completata, il sistema deve terminare con un esito di errore distinguibile dal completamento corretto.

## Requisiti non funzionali di esempio

- **RNF-01 / Must — correttezza:** in una prova con una sequenza nota, il numero di misure elaborate deve coincidere con quello delle misure acquisite e l'evidenza non deve mostrare perdite o duplicazioni.
- **RNF-02 / Should — riproducibilità:** a parità di input simulato e configurazione, il riepilogo finale deve contenere gli stessi valori logici indipendentemente dall'ordine di scheduling dei worker.
- **RNF-03 / Must — privacy/sicurezza:** output, file di prova ed errori non devono contenere nomi reali di studenti, credenziali o token.

## Vincoli di esempio

- **V-01** — La demo deve funzionare offline sugli strumenti disponibili nel laboratorio scolastico.
- **V-02** — Nell'iterazione corrente la sorgente delle misure può essere simulata; non è richiesto hardware sensore.

Notare che `pthread`, la capacità esatta del buffer o una particolare struttura dati non diventano automaticamente requisiti del prodotto. Possono essere vincoli didattici di una specifica implementazione, ma la SRS deve dichiararne la fonte se li impone.

## Caso d'uso di esempio

**UC-01 — Eseguire una sessione di acquisizione**  
**Attore primario:** tecnico di laboratorio  
**Precondizioni:** prototipo disponibile; nessuna sessione già attiva; input nel formato previsto.  
**Trigger:** l'operatore richiede l'avvio della sessione.

### Flusso principale

1. L'operatore specifica il numero di misure simulate.
2. Il sistema valida la richiesta.
3. Il sistema avvia acquisizione ed elaborazione.
4. Tutte le misure previste vengono acquisite ed elaborate.
5. Il sistema conclude la sessione.
6. Il sistema presenta il riepilogo finale.

### Alternative

- **A1 — input fuori dominio:** il sistema rifiuta la richiesta, non avvia la sessione e restituisce un errore comprensibile.
- **A2 — errore durante la sessione:** il sistema termina in stato di errore e produce evidenza sufficiente a distinguere la sessione fallita da una completata.

### Postcondizioni

Per una sessione completata è disponibile un riepilogo coerente; per una sessione fallita è disponibile un esito di errore senza dati sensibili.

## Criteri di accettazione di esempio

- **AC-01 / RF-01:** dato un numero valido di misure, quando l'operatore avvia la sessione, allora il sistema accetta la richiesta e avvia il lavoro.
- **AC-02 / RF-01:** dato un input fuori dominio, quando viene richiesto l'avvio, allora la sessione non parte ed è restituito un errore.
- **AC-03 / RF-02 + RNF-01:** data una sequenza nota di 100 misure, al completamento risultano 100 acquisite e 100 elaborate, senza duplicazioni nell'evidenza prevista.
- **AC-04 / RF-03:** al termine corretto il riepilogo contiene conteggi ed esito.
- **AC-05 / RF-04:** simulando un errore supportato dal piano di prova, l'esito è diverso dal completamento corretto.
- **AC-06 / RNF-02:** ripetendo almeno tre volte la stessa prova, i valori logici del riepilogo coincidono.
- **AC-07 / RNF-03:** una scansione manuale degli output/evidence della prova non contiene dati personali, token o credenziali.

## Tracciabilità di esempio

| Requisito | Fonte | Criterio | Evidenza |
| --- | --- | --- | --- |
| RF-01 | tecnico | AC-01, AC-02 | transcript prova input valido/non valido |
| RF-02 | docente/tecnico | AC-03 | report conteggi |
| RF-03 | docente | AC-04 | riepilogo sessione |
| RF-04 | manutentore | AC-05 | exit/esito errore |
| RNF-01 | docente | AC-03 | report sequenza nota |
| RNF-02 | manutentore | AC-06 | confronto tre esecuzioni |
| RNF-03 | scuola | AC-07 | checklist privacy |

## Won't now di esempio

- **WN-01** — collegamento a sensori fisici: escluso perché la sorgente simulata basta a validare il flusso didattico.
- **WN-02** — interfaccia grafica: esclusa perché non necessaria per validare acquisizione, elaborazione e riepilogo.

## Come correggere

### 1. Contesto, stakeholder, glossario — 2 punti

Cercare coerenza interna. Un elenco lungo non compensa stakeholder privi di bisogno o termini definiti in modo circolare.

### 2. Requisiti — 3 punti

Penalizzare soprattutto:

- frasi vaghe (`veloce`, `facile`, `sicuro`) senza criterio;
- più requisiti indipendenti fusi nella stessa riga;
- dettagli implementativi presentati come bisogno senza fonte;
- RF/RNF impossibili da osservare o misurare.

### 3. Caso d'uso — 2 punti

Il caso d'uso deve descrivere l'obiettivo dell'attore, non la sequenza interna di funzioni C. Le alternative devono essere veri percorsi diversi, non parafrasi del main flow.

### 4. Accettazione e tracciabilità — 2 punti

Controllare in entrambe le direzioni:

- ogni RF/RNF ha fonte e criterio/evidenza;
- ogni riga della matrice punta a un ID esistente;
- il criterio prova davvero il requisito indicato.

### 5. Priorità e confine — 1 punto

Premiare una motivazione reale delle priorità. `Won't now` non significa requisito fallito: definisce ciò che l'iterazione non promette.

## Domande orali rapide

- Quale tuo requisito era inizialmente troppo vago e come lo hai reso verificabile?
- Quale elemento hai classificato come vincolo invece che requisito e perché?
- Mostrami una catena stakeholder -> requisito -> criterio -> evidenza.
- Se cambia un requisito, quali righe della matrice devi riesaminare?
- Perché una scelta come `pthread_cond_wait` non è automaticamente un requisito del sistema?
