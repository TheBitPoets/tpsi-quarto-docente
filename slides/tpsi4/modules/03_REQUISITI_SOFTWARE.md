---
marp: true
paginate: true
size: 16:9
title: 03 — Requisiti software
---

# 03 — Requisiti software

UDA 13 — Progettazione del software

---

# Richiamo

Nel modulo precedente abbiamo scritto proprietà come:

> Il consumatore non deve leggere da un buffer vuoto.

Questa frase è già vicina a un requisito.

La domanda diventa:

**come trasformiamo bisogni e proprietà in qualcosa che possa essere verificato?**

---

# Obiettivi

Alla fine dovrai saper:

- distinguere bisogno e requisito;
- scrivere requisiti funzionali e non funzionali;
- riconoscere ambiguità e requisiti non verificabili;
- modellare attori, casi d'uso e scenari;
- definire criteri di accettazione;
- collegare requisito → implementazione → test.

---

# Dal bisogno al requisito

```text
bisogno
“non voglio perdere dati”
      ↓ analisi
requisito
“ogni messaggio accettato deve essere consegnato una volta...”
      ↓
criterio di accettazione
“dato X, quando Y, allora Z”
```

Il requisito riduce l'ambiguità.

---

# Funzionale vs non funzionale

**Funzionale**: che cosa deve fare il sistema.

> Il padre invia un intero al figlio e riceve il quadrato.

**Non funzionale / qualità**: vincoli e proprietà.

> Se la pipe si chiude inaspettatamente il programma deve terminare con errore rilevabile, senza bloccarsi indefinitamente.

---

# Un requisito debole

> Il programma deve essere veloce.

Problemi:

- quanto veloce?
- su quale input?
- in quale ambiente?
- con quale misura?

Non sappiamo costruire un test ripetibile.

---

# Un requisito più verificabile

> Con input di 10.000 elementi, nell'ambiente di laboratorio dichiarato, l'elaborazione deve completarsi entro il limite definito dal test di accettazione.

Ora compaiono:

- contesto;
- misura;
- soglia;
- criterio osservabile.

---

# Attori e casi d'uso

Un **attore** è un ruolo esterno che interagisce col sistema.

Un caso d'uso descrive un obiettivo dell'attore:

```text
Attore: studente
Obiettivo: eseguire il job concorrente
Precondizione: input valido
Flusso: avvia → elabora → mostra evidenza
Alternative: input errato / processo figlio fallisce
```

---

# Scenario principale e alternative

Un requisito diventa più utile quando consideriamo anche i fallimenti.

```text
happy path
      +
input invalido
processo non avviabile
pipe interrotta
timeout/deadlock
```

Il software reale vive soprattutto nelle alternative.

---

# Acceptance criteria

Formato semplice:

```text
Dato ...
Quando ...
Allora ...
```

Esempio:

```text
Dato un intero 5
Quando il padre completa lo scambio col figlio
Allora mostra 25 e termina con exit code 0
```

---

# Tracciabilità

Una catena utile:

```text
REQ-07
  ↓
issue / task
  ↓
commit / PR
  ↓
test TEST-07
  ↓
evidenza
```

La tracciabilità non è burocrazia se aiuta a rispondere:

> “Come sappiamo che questo requisito è soddisfatto?”

---

# Requisiti concorrenti

I sistemi concorrenti rendono visibili requisiti spesso trascurati:

- assenza di race osservabili;
- bounded waiting;
- nessun deadlock nel protocollo previsto;
- ordinamento quando richiesto;
- gestione terminazione/errori;
- proprietà safety/liveness.

---

# Errore tipico

> Scrivere la soluzione dentro il requisito.

“Usare un mutex pthread” non è sempre il bisogno reale.

Prima chiedi:

> Quale proprietà deve essere garantita?

Poi scegli una progettazione.

---

# Checkpoint

Quali frasi sono verificabili?

1. “La UI deve essere bella.”
2. “Il padre deve stampare il risultato solo dopo la terminazione corretta del figlio.”
3. “Il codice deve essere semplice.”
4. “Input non numerici devono produrre un errore esplicito e exit code non zero.”

Per le frasi deboli proponi una riscrittura.

---

# Collegamento al progetto

Scegli un problema già osservato nel progetto concorrente e crea:

- ID requisito;
- descrizione;
- attore/stakeholder;
- precondizione;
- scenario principale;
- caso di errore;
- acceptance criterion.

Non implementare ancora la soluzione.

---

# Mini-SRS

Una specifica leggera può contenere:

```text
scopo
stakeholder
termini/glossario
requisiti RF/RNF
casi d'uso/scenari
criteri di accettazione
vincoli
tracciabilità
```

Quanto basta per rendere il lavoro discutibile e verificabile.

---

# Recap

- requisito ≠ desiderio generico;
- verificabilità è una proprietà essenziale;
- errori e alternative fanno parte della specifica;
- acceptance criteria preparano i test;
- tracciabilità collega decisioni, codice ed evidenze.

---

# Prossimo passo

Come conserviamo e facciamo evolvere requisiti, decisioni e codice senza perdere la storia?

→ **Documentazione e controllo di versione**.