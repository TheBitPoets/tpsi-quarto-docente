---
marp: true
paginate: true
size: 16:9
title: 01 — Processi, thread e concorrenza
---

# 01 — Processi, thread e concorrenza

UDA 11 — Sistemi concorrenti

---

# Richiamo

Nel terzo anno un programma era soprattutto:

```text
sorgente → compilazione → eseguibile → output
```

Ora aggiungiamo una domanda:

**che cosa esiste nel sistema operativo mentre l'eseguibile sta girando?**

---

# Obiettivi

Alla fine dovrai saper:

- distinguere programma, processo e thread;
- descrivere risorse e stato di un processo;
- distinguere concorrenza e parallelismo;
- leggere un process tree;
- spiegare `fork`, `exec`, `wait` in esempi controllati;
- prevedere effetti di copie e risorse condivise.

---

# Programma ≠ processo

```text
programma
file/eseguibile
      ↓ avvio
processo
codice + memoria + stato + risorse + identità
```

Lo stesso programma può essere eseguito da più processi distinti.

---

# Il processo come contenitore

Un processo possiede o riferisce:

- spazio di indirizzamento;
- registri/stato CPU;
- PID e relazioni padre/figlio;
- file descriptor;
- credenziali;
- segnali e stato di esecuzione.

Pensalo come una **istanza in esecuzione**, non come un file.

---

# Thread

Più thread nello stesso processo condividono molte risorse:

```text
processo
├─ codice          condiviso
├─ heap            condiviso
├─ file descriptor condivisi
├─ thread A → stack + registri
└─ thread B → stack + registri
```

Condivisione significa collaborazione possibile, ma anche nuove race condition.

---

# Concorrenza e parallelismo

**Concorrenza:** più attività progrediscono in intervalli sovrapposti.

**Parallelismo:** più attività eseguono realmente nello stesso istante su risorse diverse.

```text
1 core:   A A B A B B A
2 core:   A A A A
          B B B B
```

Non sono sinonimi.

---

# Interleaving

Due sequenze corrette prese separatamente possono produrre molti ordini globali.

```text
A1 A2 A3
B1 B2 B3
```

Possibili esecuzioni:

```text
A1 B1 A2 B2 B3 A3
B1 B2 A1 A2 A3 B3
...
```

La correttezza deve sopravvivere agli ordini ammessi.

---

# `fork()` — modello mentale

```c
pid_t pid = fork();
```

Dopo il `fork` esistono due processi che proseguono dallo stesso punto.

- nel padre `pid > 0`;
- nel figlio `pid == 0`;
- in errore `pid == -1`.

Non pensare “fork esegue una funzione”: **duplica il contesto di processo secondo le regole POSIX**.

---

# Prevedi prima di eseguire

```c
printf("prima\n");
pid_t pid = fork();
printf("dopo\n");
```

Domande:

1. quante volte può comparire `prima`?
2. quante volte `dopo`?
3. l'ordine padre/figlio è garantito?
4. il buffering può influenzare ciò che osservi?

---

# `exec()`

`exec` non crea automaticamente un nuovo processo.

Sostituisce il programma eseguito dal processo corrente:

```text
PID 120 / programma A
        ↓ exec
PID 120 / programma B
```

Il PID può restare lo stesso mentre cambia l'immagine del processo.

---

# `wait()` / `waitpid()`

Il padre può sincronizzarsi con la terminazione di un figlio e raccoglierne lo stato.

```c
int status;
waitpid(pid, &status, 0);
```

Non è solo “aspettare”: serve anche a gestire correttamente il ciclo di vita dei figli.

---

# Errore tipico

> “Padre e figlio eseguono sempre in quell'ordine perché sul mio PC è successo così.”

Lo scheduler non promette l'ordine che hai osservato, salvo sincronizzazione esplicita.

Una singola esecuzione non è una specifica.

---

# Checkpoint

Classifica ogni elemento come **privato**, **copiato/ereditato** o **potenzialmente condiviso** a seconda del modello discusso:

- variabile nello stack dopo `fork`;
- file descriptor ereditato;
- heap tra thread dello stesso processo;
- registri di due thread;
- PID padre e PID figlio.

Spiega il perché, non soltanto l'etichetta.

---

# Lab — `fork_pipe_square`

Obiettivo: osservare una collaborazione padre/figlio in cui il dato attraversa un boundary IPC.

Prima del codice disegna:

```text
parent --dato--> child --risultato--> parent
```

Poi collega ogni freccia a descriptor, close, read/write e gestione errori.

---

# Evidenze utili

Per il laboratorio conserva:

- process tree previsto;
- output reale;
- exit status;
- una spiegazione di chi possiede ogni estremo della pipe;
- almeno un errore riprodotto e diagnosticato.

---

# Recap

- programma e processo non sono la stessa cosa;
- thread condividono più stato;
- concorrenza ≠ parallelismo;
- l'interleaving rende pericolose le assunzioni implicite;
- `fork/exec/wait` descrivono ciclo di vita e cooperazione.

---

# Prossimo passo

Se due attività devono cooperare, servono due problemi distinti:

**come comunicano?**  
**come coordinano l'accesso e l'ordine?**

→ Comunicazione e sincronizzazione.