# Riferimento docente — docs-as-code, Git e review

Questa Activity valuta insieme **artefatti documentali** e **processo versionato**. Un insieme di Markdown perfetto senza una storia Git verificabile non soddisfa il contratto completo.

## Esempio di catena tracciabile

```text
RF-03: riepilogo finale verificabile
  -> PROJECT_README: documenta output/evidenza attesa
  -> ADR-001: decide dove rendere autorevole il contratto del riepilogo
  -> PR_DESCRIPTION: spiega modifica e compatibilita
  -> EVIDENCE: mostra commit/diff e verifica eseguita
```

## ADR di riferimento — idea

Una decisione plausibile è: **rendere il formato del riepilogo finale un contratto documentato e versionato, evitando di duplicarlo in più guide**.

Alternative da discutere:

1. copiare il formato in ogni documento;
2. scegliere una fonte autorevole e collegarla dagli altri documenti;
3. generare una parte della documentazione da una fonte strutturata.

Una buona risposta non deve scegliere per forza l'opzione 2, ma deve spiegare conseguenze e criterio di verifica.

## Commit di riferimento

Esempio di separazione intenzionale:

```text
1. docs: define MonitorMisure project and architecture decision
2. docs: add review evidence and PR traceability
```

Sono preferibili a un unico `update docs` perché rendono distinguibili due intenti e facilitano review/revert.

## PR di riferimento

La descrizione dovrebbe permettere di rispondere rapidamente:

- quale problema risolve?
- quale RF/RNF giustifica la modifica?
- quali file cambiano e perché?
- quale verifica è stata eseguita?
- cosa resta fuori scope?
- quali rischi o compatibilità sono rilevanti?

## Esempi di review

**Blocking**

> `PROJECT_README.md` dichiara un output diverso da quello usato come evidenza in `EVIDENCE.md`; serve scegliere una fonte autorevole e riallineare prima dell'integrazione.

**Important**

> L'ADR sceglie una soluzione ma non registra l'alternativa scartata; così il futuro manutentore non può capire perché la scelta sia stata preferita.

**Suggestion**

> La sezione di avvio rapido potrebbe includere l'output atteso della prova minima per rendere più semplice verificare la riuscita.

**Style**

> Uniformerei i titoli delle sezioni all'infinito o al sostantivo per coerenza editoriale.

## Correzione della storia Git

Verificare manualmente:

1. branch dedicato coerente con il lavoro;
2. almeno due commit reali;
3. messaggi che esprimono intenti distinti;
4. diff dei commit compatibile con la descrizione;
5. assenza di file casuali/temporanei;
6. working tree finale comprensibile;
7. nessun segreto o dato personale nelle evidenze.

Non richiedere necessariamente una storia "perfetta": l'obiettivo è che lo studente sappia motivare struttura e scelte.

## Rubrica

### README — 2 punti

- scopo e pubblico comprensibili;
- prova minima riproducibile;
- limiti e provenienza espliciti.

### ADR — 2 punti

- contesto reale;
- decisione distinta dal requisito;
- alternative;
- conseguenze positive e negative;
- verifica.

### Git — 2 punti

- branch dedicato;
- almeno due commit intenzionali;
- evidenza coerente con log/diff.

### PR — 2 punti

- problema e requisito;
- soluzione;
- verifiche;
- rischi/limiti/compatibilità.

### Review — 2 punti

- almeno tre rilievi specifici;
- classificazione sensata;
- linguaggio professionale;
- azione proposta quando necessaria.

## Domande orali rapide

- Perché hai separato i due commit?
- Qual è la fonte autorevole per il contratto che hai documentato?
- Mostrami il collegamento RF/RNF -> file -> verifica.
- Che differenza c'è tra un commento `blocking` e una preferenza `style`?
- Quale informazione dell'ADR non potrei ricostruire facilmente guardando solo il codice?
- Se la PR venisse respinta, quali evidenze conserveresti per capire la decisione?
