---
marp: true
paginate: true
size: 16:9
title: 02 — Comunicazione e sincronizzazione
---

# 02 — Comunicazione e sincronizzazione

UDA 12 — Sistemi concorrenti

---

# Richiamo

Due processi o thread possono progredire in ordini diversi.

Ora separiamo due esigenze:

```text
comunicare       = trasferire dati/informazioni
sincronizzare    = imporre relazioni sull'accesso o sull'ordine
```

Spesso servono entrambe.

---

# Obiettivi

Alla fine dovrai saper:

- distinguere IPC e sincronizzazione;
- riconoscere race condition e critical section;
- spiegare mutex, semafori e condition variable;
- ragionare su produttore/consumatore e lettori/scrittori;
- riconoscere condizioni di deadlock;
- progettare un protocollo semplice basato su invarianti.

---

# Due famiglie di comunicazione

```text
memoria condivisa             message passing
A ───── shared state ───── B  A ── messaggio ──> B
```

Memoria condivisa: accesso rapido ma coordinamento esplicito.

Messaggi: il trasferimento è più visibile, ma protocollo e blocking restano da progettare.

---

# Pipe come protocollo

Una pipe non è solo una funzione di libreria.

Definisci prima:

- chi scrive;
- chi legge;
- formato del dato;
- quando si chiudono gli estremi;
- cosa significa EOF;
- come gestire errori e terminazione.

Queste sono proprietà del **protocollo**.

---

# Race condition

```c
counter = counter + 1;
```

Può sembrare una singola operazione, ma concettualmente contiene:

```text
read counter
compute +1
write counter
```

Due thread possono interleavare queste fasi e perdere aggiornamenti.

---

# Critical section

Una sezione critica manipola stato per cui vogliamo preservare un'invariante.

```text
lock
  leggi / modifica stato condiviso
unlock
```

Il lock non è il fine: serve a proteggere una **proprietà**.

---

# Mutex

Un mutex esprime esclusione mutua:

```text
al massimo un partecipante nella critical section
```

Domanda corretta:

> Quale stato protegge questo mutex?

Domanda incompleta:

> Dove posso mettere un lock per far sparire il bug?

---

# Semafori

Un semaforo rappresenta un contatore sincronizzato.

Può modellare:

- disponibilità di N risorse;
- slot liberi/pieni;
- eventi/permessi, a seconda del protocollo.

Il valore iniziale è parte della specifica.

---

# Condition variable

Una condition non “contiene” la condizione.

Il pattern è:

```text
lock
while (!predicato_sullo_stato)
    wait(condition, lock)
usa/modifica stato
unlock
```

Il predicato vive nello stato condiviso e va ricontrollato.

---

# Produttore / consumatore

In un buffer limitato vogliamo preservare proprietà come:

```text
0 <= elementi <= capacità
```

Servono due problemi:

- proteggere la struttura dati;
- coordinare pieno/vuoto.

Non basta “mettere un mutex”.

---

# Deadlock

Quattro condizioni classiche da osservare:

- mutua esclusione;
- hold and wait;
- no preemption;
- attesa circolare.

Esempio:

```text
T1 possiede A, aspetta B
T2 possiede B, aspetta A
```

---

# Prevenire con un ordine

Una strategia semplice:

```text
acquisisci sempre A prima di B
```

Se tutti rispettano un ordine globale, eliminiamo alcuni cicli di attesa.

La regola va documentata come contratto.

---

# Errore tipico

> “Aggiungo `sleep()` così i thread si eseguono nell'ordine giusto.”

`sleep` modifica probabilità e timing; non crea una relazione di sincronizzazione affidabile.

Un bug che scompare rallentando il programma può essere ancora lì.

---

# Checkpoint

Scegli lo strumento più adatto e motiva:

1. proteggere una lista condivisa;
2. rappresentare 5 connessioni disponibili;
3. aspettare finché il buffer non contiene almeno un elemento;
4. trasferire un intero tra padre e figlio;
5. evitare acquisizioni A/B in ordine opposto.

---

# Collegamento al progetto concorrente

Per ogni meccanismo aggiungi al progetto una mini-specifica:

```text
stato condiviso:
invariante:
chi modifica:
chi aspetta:
ordine di lock:
errore osservabile:
```

Questo materiale verrà riusato nei requisiti e nei test.

---

# Lab

`fork_pipe_square` permette già di osservare IPC padre/figlio.

Estensioni manuali possibili, finché non vengono formalizzate come Activity:

- pipe bidirezionale;
- gestione EOF/close errata;
- più messaggi con protocollo definito;
- buffer produttore/consumatore con thread.

---

# Recap

- comunicazione e sincronizzazione sono problemi distinti;
- race = risultato dipendente da interleaving non controllato;
- mutex/semaforo/condition implementano proprietà;
- deadlock è un problema di dipendenze, non di “programma lento”;
- il protocollo va descritto prima del codice.

---

# Prossimo passo

Le proprietà che abbiamo appena scritto possono diventare **requisiti verificabili**.

→ Requisiti software.