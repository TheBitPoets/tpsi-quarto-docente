---
marp: true
paginate: true
size: 16:9
title: 04 — Documentazione e controllo di versione
---

# 04 — Documentazione e controllo di versione

UDA 14 — Progettazione del software

---

# Richiamo

Un requisito senza storia può diventare presto ambiguo:

- chi lo ha cambiato?
- perché?
- quale codice lo implementa?
- quale test lo verifica?

La documentazione e il versionamento servono a preservare **contesto e intenzione**.

---

# Obiettivi

Alla fine dovrai saper:

- distinguere documentazione per pubblici diversi;
- scrivere un README operativo;
- documentare decisioni e contratti;
- usare Git con commit intenzionali;
- lavorare con branch, conflitti e pull request;
- collegare requisito, modifica, review e test;
- conservare provenance delle fonti.

---

# Documentazione ≠ commenti ovunque

La domanda è:

> Quale informazione serve, a chi, in quale momento?

Esempi:

- README → chi deve usare/eseguire il progetto;
- commento → dettaglio locale non ovvio;
- ADR → perché abbiamo scelto una soluzione;
- API/contratto → come interagiscono componenti;
- issue/PR → perché esiste una modifica.

---

# README operativo

Un buon README permette di rispondere rapidamente:

```text
che cos'è?
come si prepara?
come si esegue?
come si testa?
quali limiti ha?
dove si trovano le evidenze?
```

Se serve chiedere oralmente ogni passaggio, il repository non è ancora riproducibile.

---

# Documentare un contratto

Per una funzione/processo/protocollo descrivi ciò che conta:

```text
input
output
precondizioni
postcondizioni
errori
ownership / risorse
ordering / concorrenza
```

Non riscrivere il codice in prosa.

---

# Decision record leggero

Esempio:

```text
Decisione: ordinare sempre lock A → B
Contesto: deadlock osservato tra T1/T2
Alternative: timeout, trylock, redesign
Scelta: ordine globale
Conseguenze: tutti i call site devono rispettarlo
```

La decisione resta comprensibile anche mesi dopo.

---

# Git: snapshot con intenzione

Un commit utile dovrebbe essere:

- piccolo abbastanza da capire;
- coerente con un obiettivo;
- verificabile;
- accompagnato da un messaggio che spiega l'intenzione.

```text
Fix pipe EOF handling in parent
```

è più informativo di:

```text
modifiche varie
```

---

# Branch

Il branch isola una linea di lavoro:

```text
main ─────●────────●
           \      /
            ●──●──   feature/fix
```

Permette di sviluppare e verificare prima di integrare.

---

# Pull request

Una PR è una **unità di review**, non soltanto un pulsante per fare merge.

Dovrebbe spiegare:

- problema/obiettivo;
- cosa cambia;
- cosa non cambia;
- come è stato verificato;
- rischi/limiti.

---

# Review

Una buona review controlla più livelli:

```text
correttezza
leggibilità
contratti
error handling
concorrenza
sicurezza
provenance
test
```

Il reviewer non deve ricostruire l'intenzione dal diff.

---

# Conflitti

Un conflitto Git non significa “Git è rotto”.

Significa:

> due storie hanno modificato la stessa zona e serve una decisione umana.

Risolvi comprendendo entrambe le intenzioni, poi riesegui i test.

---

# Provenance

Quando incorpori un'idea/esempio esterno registra almeno:

- fonte;
- versione/commit quando rilevante;
- licenza/diritti;
- cosa è stato riusato o solo consultato.

Una URL senza contesto non è sempre sufficiente per una build riproducibile.

---

# Errore tipico

> Un commit enorme con refactor, feature, fix e documentazione insieme.

Effetti:

- review difficile;
- rollback rischioso;
- causa di un bug meno evidente;
- tracciabilità debole.

Separare intenzioni riduce il costo della manutenzione.

---

# Checkpoint

Hai questo messaggio:

```text
fix
```

Il diff modifica chiusura delle pipe e aggiunge un test su EOF.

Proponi:

1. titolo commit migliore;
2. descrizione PR in 3 righe;
3. evidenza da allegare;
4. requisito o bug da collegare.

---

# Collegamento al progetto concorrente

Per una modifica reale del progetto crea una mini-catena:

```text
REQ-xx / BUG-xx
      ↓
branch
      ↓
commit
      ↓
PR
      ↓
test/evidenza
```

La storia deve essere leggibile senza spiegazione orale aggiuntiva.

---

# Recap

- documentare significa preservare informazioni utili;
- Git conserva storia, ma la qualità della storia dipende da noi;
- branch/PR rendono la modifica reviewable;
- provenance fa parte della qualità;
- documentazione e codice devono evolvere insieme.

---

# Prossimo passo

Una PR ben documentata non è ancora una prova che il software sia corretto.

→ **Testing e debugging**.