# Mappe visive — Comunicazione e sincronizzazione

Questa guida affianca [`02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md`](../02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md). Pseudocodice e primitive restano nel modulo in forma copiabile.

## Produttore, buffer e consumatore

![Produttore e consumatore coordinati attraverso un buffer limitato, un mutex e due condizioni not full e not empty](../assets/diagrams/02-producer-consumer-buffer.svg)

## Pipe padre–figlio

![Il figlio scrive nella pipe dopo aver chiuso la lettura, mentre il padre legge, chiude la scrittura e attende con waitpid](../assets/diagrams/02-pipe-parent-child.svg)

## Read–modify–write

![Counter più più scomposto in lettura, calcolo e scrittura con una finestra in cui un altro thread può interferire](../assets/diagrams/02-race-read-modify-write.svg)

## Variabile di condizione

![Il thread acquisisce il mutex, controlla la condizione in while, attende rilasciando il mutex e ricontrolla dopo il risveglio](../assets/diagrams/02-condition-wait.svg)

## Deadlock

![Due thread possiedono un lock e attendono l'altro, formando un ciclo che impedisce il progresso](../assets/diagrams/02-deadlock-cycle.svg)

## Monitor

![Un monitor incapsula stato privato, metodi sincronizzati e code di attesa sulle condizioni](../assets/diagrams/02-monitor.svg)

## Proprietario unico

![Thread client inviano comandi a una coda e un solo thread database possiede e modifica la connessione](../assets/diagrams/02-single-owner.svg)

## Uso didattico

I diagrammi chiariscono struttura e responsabilità. Per implementare gli algoritmi, usare il pseudocodice e gli esempi POSIX/Java del modulo principale.
