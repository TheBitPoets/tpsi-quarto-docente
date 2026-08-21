---
marp: true
paginate: true
size: 16:9
title: 05 — Testing e debugging
---

# 05 — Testing e debugging

UDA 15 — Qualità del software

---

# Richiamo

Ora abbiamo:

```text
requisito → commit/PR
```

Manca il passaggio fondamentale:

> Quale evidenza dimostra che il comportamento richiesto è davvero presente?

---

# Obiettivi

Alla fine dovrai saper:

- distinguere verifica e validazione;
- progettare casi di test da requisiti;
- distinguere test statici e dinamici;
- riprodurre un difetto prima di correggerlo;
- usare debugger/sanitizer/log come strumenti di evidenza;
- aggiungere una regressione dopo un bug;
- interpretare CI e report senza limitarti al “verde/rosso”.

---

# Verifica e validazione

Domande diverse:

**Verifica**  
> Abbiamo costruito il prodotto secondo specifica?

**Validazione**  
> La specifica/prodotto risponde davvero al bisogno?

Entrambe richiedono criteri espliciti.

---

# Dal requisito al test

Requisito:

> Input non numerico deve terminare con errore esplicito e codice non zero.

Caso di test:

```text
input: abc
expected stderr: messaggio di errore
expected exit status: != 0
```

La testabilità nasce già nella scrittura del requisito.

---

# Struttura di un test

```text
Arrange  prepara stato/input
Act      esegui l'azione
Assert   confronta risultato/proprietà
```

Nei sistemi concorrenti può servire anche osservare:

- ordering;
- timeout;
- assenza di blocco;
- ripetibilità statistica;
- cleanup di risorse.

---

# Statico vs dinamico

**Statico**: senza eseguire il programma.

- compiler warning;
- lint/static analysis;
- review;
- controllo documentazione/contratti.

**Dinamico**: osservando un'esecuzione.

- test;
- sanitizer;
- debugger;
- tracing/log.

---

# Debugging: metodo, non tentativi

```text
riproduci
→ riduci il caso
→ formula ipotesi
→ raccogli evidenza
→ cambia una cosa
→ verifica
→ aggiungi regressione
```

Modificare più cose insieme rende difficile sapere cosa ha davvero risolto il problema.

---

# Riprodurre prima di correggere

Bug report debole:

> Ogni tanto si blocca.

Bug report utile:

```text
input:
ambiente:
passi:
risultato osservato:
risultato atteso:
frequenza:
log/exit status:
```

---

# Debugger

Il debugger serve a interrogare lo stato:

- breakpoint;
- step;
- stack frame;
- variabili;
- thread;
- backtrace.

Non sostituisce il modello mentale: ti aiuta a confrontare **ipotesi e stato reale**.

---

# Sanitizer

Con toolchain compatibile puoi rilevare classi di errori difficili da vedere a occhio:

```bash
gcc -fsanitize=address,undefined -g ...
```

Per problemi di concorrenza esistono strumenti specifici, da usare quando l'ambiente li supporta.

Il report va interpretato, non soltanto copiato.

---

# Concorrenza: testare una race

Una race può non apparire in ogni esecuzione.

Strategie:

- eseguire molte volte;
- aumentare contesa;
- usare input mirati;
- aggiungere strumenti di rilevazione;
- verificare invarianti invece di un ordine accidentale.

---

# Timeout

Un test di concorrenza che può bloccarsi deve avere una politica di timeout.

```text
pass = termina correttamente entro il limite
fail = output errato / errore inatteso / timeout
```

Il timeout non “prova assenza di deadlock” in generale, ma rende il test controllabile.

---

# Regressione

Dopo aver corretto un bug:

1. conserva un test che falliva prima;
2. verifica che passi con la correzione;
3. lascialo nella suite.

Così il bug diventa conoscenza eseguibile.

---

# CI

La Continuous Integration automatizza controlli su ogni modifica.

Ma un badge verde ha valore solo se sappiamo:

- quali test esegue;
- quali ambienti copre;
- quali failure può non rilevare;
- quali artifact/evidenze produce.

---

# Errore tipico

> “Il test passa, quindi il requisito è certamente soddisfatto.”

Un test dimostra soltanto ciò che verifica nel contesto in cui è eseguito.

Test, requisito e rischio devono essere coerenti.

---

# Checkpoint

Per questo bug:

> il padre resta bloccato se il figlio chiude la pipe senza scrivere

progetta:

1. caso minimo di riproduzione;
2. evidenza da osservare;
3. timeout;
4. comportamento atteso;
5. regressione da conservare.

---

# Collegamento a `fork_pipe_square`

Usa l'Activity come caso end-to-end:

```text
requisito
→ programma padre/figlio
→ esecuzione
→ errore iniettato
→ test/regressione
→ commit con evidenza
```

Il laboratorio diventa così anche materiale per UDA15.

---

# Recap

- test nasce da proprietà/requisiti;
- debugging parte dalla riproduzione;
- strumenti raccolgono evidenze;
- bug corretto → regressione;
- CI automatizza controlli, non il ragionamento.

---

# Prossimo passo

Un progetto tecnicamente corretto può comunque essere irresponsabile se gestisce male dati, fonti, dipendenze o AI.

→ **Cittadinanza digitale e progetto finale**.