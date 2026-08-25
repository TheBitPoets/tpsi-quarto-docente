# Note docente — produttore/consumatore con buffer limitato

## Scopo didattico

Questa Activity chiude il passaggio concettuale da mutex come semplice mutua esclusione a mutex + variabili di condizione come protocollo su uno stato condiviso.

L'invariante da rendere esplicito in classe è:

```text
0 <= count <= CAPACITY
```

La soluzione deve separare tre responsabilità:

- il mutex protegge la consistenza di `data`, `head`, `tail`, `count`;
- `not_empty` rappresenta il predicato `count > 0`;
- `not_full` rappresenta il predicato `count < CAPACITY`.

## Confine dell'automazione

I test automatici verificano compilazione e output deterministico. Non possono dimostrare, da soli, che lo studente abbia usato correttamente mutex e condition: una soluzione sequenziale potrebbe imitare l'output.

Per questo la valutazione deve mantenere i controlli manuali del contratto Activity:

1. accesso allo stato condiviso sotto mutex;
2. `pthread_cond_wait` dentro `while`;
3. assenza di busy waiting/sleep come sincronizzazione;
4. produzione e consumo effettivi attraverso il buffer;
5. `head`/`tail` circolari e invariante rispettato.

## Sequenza consigliata in laboratorio

1. Disegnare il buffer con `head`, `tail`, `count`.
2. Far simulare a mano il caso `N=5`, capacità 4.
3. Scrivere prima `buffer_push` e `buffer_pop` come pseudocodice.
4. Evidenziare che `pthread_cond_wait` rilascia il mutex e lo riacquisisce prima di ritornare.
5. Implementare producer e consumer.
6. Solo alla fine completare `pthread_create`/`pthread_join` e l'output.
7. Far spiegare a voce perché `if` non è sufficiente.

## Errori frequenti

- `count++` o `count--` fuori dal lock;
- segnale inviato ma stato non ancora coerente;
- `if` invece di `while`;
- dimenticare `% CAPACITY` su `head`/`tail`;
- usare due mutex diversi per predicati che dipendono dallo stesso stato;
- stampare dai worker, introducendo output non deterministico;
- confondere `pthread_cond_signal` con il trasferimento di dati: il dato resta nel buffer, la condition segnala soltanto che il predicato potrebbe essere cambiato.

## Rubrica operativa

- 2 punti: buffer circolare e invariante corretti;
- 2 punti: mutex sulla sezione critica;
- 2 punti: `not_empty`/`not_full` e `while` corretti;
- 2 punti: lifecycle thread e casi di test;
- 2 punti: gestione input/errori e spiegazione tecnica.

## Domande orali rapide

- Quale dato protegge il mutex?
- Che cosa significa esattamente `not_empty`?
- Perché la `wait` deve stare dentro `while`?
- Cosa accadrebbe se il produttore facesse busy waiting su `count`?
- Il segnale trasporta il valore prodotto?
- Perché `head` e `tail` devono essere aggiornati sotto lo stesso mutex di `count`?

## Estensioni facoltative, non parte del contratto base

Dopo la correzione si può discutere, senza cambiare l'Activity assegnata:

- più produttori/consumatori;
- shutdown con sentinella;
- confronto con semafori;
- confronto con `BlockingQueue` in Java;
- misure di contesa e dimensionamento del buffer.
