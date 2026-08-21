---
marp: true
paginate: true
size: 16:9
title: 00 — TPSI quarto: orientamento, fonti e metodo
---

# 00 — TPSI quarto
## Orientamento, fonti e metodo

UDA 10 — 2 settimane

---

# Domanda iniziale

Un programma stampa il risultato giusto.

**Questo basta per dire che il software è corretto?**

Durante l'anno costruiremo una risposta sempre più precisa.

---

# Il percorso in una mappa

```text
processi / thread
      ↓
concorrenza + IPC
      ↓
sincronizzazione
      ↓
requisiti verificabili
      ↓
documentazione + Git
      ↓
test + debugging
      ↓
progetto responsabile
```

---

# Obiettivi del corso

Alla fine dovrai saper:

- ragionare su processi e thread concorrenti;
- spiegare comunicazione e sincronizzazione;
- trasformare bisogni in requisiti verificabili;
- documentare e versionare un progetto;
- progettare test e fare debugging con evidenze;
- gestire fonti, licenze, privacy e AI responsabilmente.

---

# Non studiamo blocchi isolati

Useremo lo stesso **progetto concorrente** per collegare le UDA.

Un problema tecnico può diventare:

```text
race condition
→ requisito di correttezza
→ decisione documentata
→ test di regressione
→ evidenza nel progetto finale
```

---

# Le fonti hanno ruoli diversi

- **Contenuti originali**: lezioni canoniche del corso.
- **Linux Programming**: fonte tecnica pinned per API e laboratori POSIX.
- **Indice bibliografico**: riferimento di copertura, non testo da copiare.
- **Documentazione ufficiale**: riferimento tecnico puntuale.

Sapere *da dove arriva* un'informazione è parte della competenza.

---

# Content Pack e delivery

Il Content Pack è ancora:

`0.1.0 / draft`

Significa che il docente sta ancora controllando il percorso.

Le slide possono migliorare durante l'anno senza fingere che il curriculum sia già congelato.

---

# Il ciclo di lavoro

```text
leggi
→ prevedi
→ esegui
→ osserva
→ modifica
→ testa
→ debug
→ documenta
→ consegna
```

La previsione prima dell'esecuzione è fondamentale nei sistemi concorrenti.

---

# Che cosa conta come evidenza?

Dipende dal problema:

- output e exit status;
- process tree o timeline;
- test/report;
- commit SHA;
- requisito o criterio di accettazione;
- spiegazione tecnica breve;
- provenance della fonte.

---

# Errore tipico

> “Funziona sul mio computer, quindi è corretto.”

Nei sistemi concorrenti una singola esecuzione può nascondere race e ordering diversi.

Nel software in generale un output corretto non dimostra che requisiti, errori, sicurezza e manutenzione siano sotto controllo.

---

# Checkpoint

Per ognuna delle frasi indica se parla di **codice**, **requisito**, **test** o **evidenza**:

1. “Il figlio deve terminare prima che il padre stampi il risultato.”
2. `waitpid(...)`.
3. Eseguo il programma 100 volte e controllo l'exit code.
4. Salvo il report della prova nel repository.

---

# Prima attività

Apri il README del corso e individua:

- i 6 moduli canonici;
- il Course Design;
- la matrice di copertura;
- l'Activity `fork_pipe_square`;
- la fonte Linux Programming.

Per ogni elemento scrivi **che ruolo ha**.

---

# Recap

Il corso non chiede soltanto di programmare.

Chiede di costruire una catena verificabile:

```text
idea → requisito → implementazione → prova → spiegazione
```

---

# Prossimo passo

**Processi, thread e concorrenza**.

Prima domanda: che cosa cambia davvero quando un programma in esecuzione diventa un *processo*?