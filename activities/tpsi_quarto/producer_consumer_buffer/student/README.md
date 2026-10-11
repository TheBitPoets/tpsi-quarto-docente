# Activity — produttore e consumatore con buffer limitato

## Obiettivo

Implementare il problema produttore/consumatore con due thread POSIX e un buffer circolare condiviso di capacità 4.

Il punto centrale non è soltanto ottenere la somma corretta: devi preservare l'invariante

```text
0 <= count <= 4
```

senza busy waiting e senza accessi concorrenti non protetti allo stato del buffer.

## Contratto del programma

Il programma legge da standard input un intero `N` compreso tra 1 e 1000.

- il produttore genera i valori `1, 2, ..., N` e li inserisce nel buffer;
- il consumatore estrae esattamente `N` valori e ne calcola la somma;
- il buffer contiene al massimo 4 elementi;
- `head`, `tail`, `count` e l'array del buffer sono stato condiviso;
- un unico mutex protegge l'invariante del buffer;
- `not_empty` sveglia chi attende dati;
- `not_full` sveglia chi attende spazio.

Esempio con input:

```text
5
```

output esatto:

```text
Somma: 15
Prodotti: 5
Consumati: 5
```

Per input non valido:

```text
Input non valido
```

con codice di uscita diverso da zero.

## Regola fondamentale: `while`, non `if`

Lo schema corretto è:

```text
lock
while condizione non soddisfatta:
    cond_wait(...)
modifica lo stato condiviso
signal(...)
unlock
```

Dopo un risveglio devi ricontrollare la condizione: il fatto di essere stato svegliato non garantisce che il predicato sia ancora vero quando riottieni il mutex.

## Cosa completare

Nel file `main.c` trovi quattro punti principali:

1. `buffer_push`;
2. `buffer_pop`;
3. `producer_main`;
4. `consumer_main`;
5. creazione e `join` dei due thread nel `main`.

## Compilazione locale

Su Linux:

```bash
gcc -Wall -Wextra -Wpedantic -std=c17 -pthread main.c -o app
```

Esecuzione:

```bash
printf '10\n' | ./app
```

Output atteso:

```text
Somma: 55
Prodotti: 10
Consumati: 10
```

## Errori da evitare

- controllare `count` senza mutex;
- usare `if` intorno a `pthread_cond_wait`;
- usare `sleep` o `usleep` per "sincronizzare" i thread;
- tenere il mutex mentre si svolge lavoro che non riguarda lo stato condiviso;
- dimenticare il wrap-around di `head` e `tail`;
- segnalare `not_empty`/`not_full` prima di aver aggiornato coerentemente lo stato;
- stampare trace dai thread: renderebbero l'output non deterministico.

## Checklist prima della consegna

- [ ] Il programma compila senza warning con i flag indicati.
- [ ] `buffer_push` attende quando `count == 4`.
- [ ] `buffer_pop` attende quando `count == 0`.
- [ ] Entrambe le attese sono dentro un `while`.
- [ ] Tutti gli accessi a `head`, `tail` e `count` sono sotto mutex.
- [ ] Il produttore genera realmente `1..N`.
- [ ] Il consumatore calcola realmente la somma dei valori estratti.
- [ ] Non c'è busy waiting.
- [ ] L'output contiene soltanto le tre righe previste.
- [ ] Sai spiegare perché l'invariante `0 <= count <= 4` non può essere violato.
