---
marp: true
paginate: true
size: 16:9
title: 06 — Cittadinanza digitale e progetto finale
---

# 06 — Cittadinanza digitale
## Progettare software in modo responsabile

UDA 16 — Progetto e responsabilità

---

# Richiamo

Finora abbiamo chiesto:

> Il software è corretto e verificato?

Ora allarghiamo la domanda:

> È anche **responsabile, tracciabile e sicuro da usare/condividere**?

---

# Obiettivi

Alla fine dovrai saper:

- gestire licenze e provenance delle fonti;
- evitare segreti e dati personali nel repository;
- ragionare su dipendenze e supply chain;
- considerare accessibilità e sicurezza;
- usare AI in modo dichiarato e verificabile;
- produrre un progetto finale accompagnato da evidenze e responsabilità.

---

# Il codice ha una provenienza

Quando usi materiale esterno chiedi:

```text
da dove arriva?
quale versione?
con quale licenza?
posso modificarlo?
posso ridistribuirlo?
cosa ho copiato/adattato/solo consultato?
```

La provenance è parte della documentazione tecnica.

---

# Licenza ≠ “è su Internet”

Essere pubblicamente leggibile non significa automaticamente:

- dominio pubblico;
- copiabile senza condizioni;
- ridistribuibile;
- compatibile con il tuo progetto.

Leggi la licenza e conserva attribuzione quando richiesta.

---

# Segreti

Mai committare intenzionalmente:

```text
password
API key
token
chiavi private
credenziali reali
```

Usa configurazione esterna e valori di esempio non sensibili.

Un segreto finito nella history può restare recuperabile anche dopo la cancellazione dal file corrente.

---

# Privacy

Prima di raccogliere dati chiedi:

- servono davvero?
- chi può vederli?
- per quanto tempo li conserviamo?
- possiamo usare dati sintetici?
- l'evidenza di laboratorio contiene informazioni personali?

Minimizzare i dati riduce il rischio.

---

# Supply chain

Una dipendenza è codice che scegli di far entrare nel tuo sistema.

Controlla almeno:

- origine;
- versione;
- manutenzione;
- vulnerabilità note quando rilevanti;
- necessità reale;
- aggiornamenti e compatibilità.

“Installare un package” è una decisione tecnica.

---

# Accessibilità

Software utilizzabile non significa solo software che non crasha.

Considera, quando applicabile:

- input alternativi;
- messaggi comprensibili;
- contrasto/struttura semantica nelle interfacce;
- output leggibile;
- documentazione accessibile;
- errori che non dipendono soltanto dal colore.

---

# Sicurezza e least privilege

Principio utile:

> un componente dovrebbe avere soltanto i permessi necessari.

Esempi:

- non eseguire come root senza motivo;
- limitare accesso a file e dati;
- validare input al boundary;
- non fidarsi di dati esterni per definizione.

---

# AI come assistente, non fonte magica

Se usi un modello AI:

- dichiara l'uso quando richiesto;
- verifica il risultato;
- controlla API/versioni/documentazione;
- non inserire segreti o dati personali;
- non consegnare codice che non sai spiegare;
- conserva la responsabilità della scelta.

---

# Hallucination test

Un output AI afferma:

> “`fork()` condivide automaticamente tutte le variabili tra padre e figlio.”

Come lo verifichi?

1. modello concettuale;
2. documentazione POSIX/Linux;
3. esperimento minimo;
4. osservazione;
5. correzione della spiegazione.

Questo è pensiero tecnico, non fiducia nell'autorità.

---

# Provenance del progetto finale

Aggiungi un piccolo manifest:

```text
fonti consultate
snippet/adattamenti
librerie/dipendenze
licenze
strumenti AI usati
versioni rilevanti
```

Deve essere possibile capire cosa è vostro e cosa viene dall'esterno.

---

# Valutare il progetto finale

Un progetto completo dovrebbe mostrare:

```text
requisiti
architettura/protocollo concorrente
codice
versionamento/review
test + regressioni
documentazione
provenance
sicurezza/privacy
riflessione sui limiti
```

Non soltanto una demo riuscita.

---

# Errore tipico

> “Non abbiamo dati sensibili, quindi la sicurezza non ci riguarda.”

Anche un progetto didattico può avere:

- dipendenze vulnerabili;
- input non validato;
- comandi pericolosi;
- token di test reali;
- permessi eccessivi;
- provenance incerta.

---

# Checkpoint

Per ciascuna situazione indica il rischio principale:

1. una API key nel repository;
2. codice copiato da un gist senza licenza chiara;
3. dipendenza aggiunta solo per una funzione banale;
4. screenshot di test con dati personali;
5. soluzione AI che nessuno nel gruppo sa spiegare.

Proponi una mitigazione concreta.

---

# Progetto finale

Consegna non solo il software, ma una **storia verificabile**:

```text
problema
→ requisiti
→ decisioni
→ implementazione
→ test
→ evidenze
→ provenance
→ limiti
```

Questa è la sintesi dell'intero quarto anno.

---

# Recap finale

Un buon tecnico sa chiedere contemporaneamente:

- funziona?
- perché funziona?
- come lo dimostro?
- come lo mantengo?
- posso usare/ridistribuire queste fonti?
- quali rischi creo per utenti e sistema?

---

# Chiusura del percorso

Il filo dell'anno:

```text
concorrenza
→ proprietà
→ requisiti
→ storia/versionamento
→ verifica
→ responsabilità
```

Il software non è solo codice: è un sistema di **decisioni ed evidenze**.