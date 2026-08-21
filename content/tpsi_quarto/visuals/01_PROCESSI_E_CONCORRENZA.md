# Mappe visive — Processi, thread e concorrenza

Questa guida affianca [`01_PROCESSI_E_CONCORRENZA.md`](../01_PROCESSI_E_CONCORRENZA.md). I diagrammi sono originali e non derivano dalle immagini del libro adottato.

## Ciclo di vita di un processo

![Macchina a stati con passaggi da nuovo a pronto, in esecuzione, in attesa e terminato](../assets/diagrams/01-process-lifecycle.svg)

## Modelli di esecuzione

![Confronto temporale tra esecuzione sequenziale, concorrente e parallela](../assets/diagrams/01-execution-models.svg)

## Risorse private e condivise

![Due processi con memoria isolata confrontati con due thread che condividono codice, heap e file ma conservano stack e registri propri](../assets/diagrams/01-process-thread-resources.svg)

## `fork`, `exec` e `waitpid`

![Il padre crea il figlio con fork, il figlio può sostituire il programma con exec e il padre raccoglie lo stato con waitpid](../assets/diagrams/01-fork-exec-wait.svg)

## Incremento perso

![Due thread leggono lo stesso valore, calcolano entrambi uno e producono un solo incremento osservabile](../assets/diagrams/01-lost-update.svg)

## Uso didattico

- osservare prima il diagramma;
- ricostruire il flusso con parole proprie;
- confrontarlo con gli esempi C e Java del modulo;
- usare le versioni testuali presenti nel capitolo per esercizi e modifiche.
