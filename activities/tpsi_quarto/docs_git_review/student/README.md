# Activity — documentare, versionare e revisionare una modifica

## Scenario

Continui il lavoro su **MonitorMisure**. Hai già una mini-SRS con requisiti identificati `RF-*` / `RNF-*`. Ora devi preparare una piccola modifica documentale/progettuale come farebbe un team reale: branch, commit intenzionali, ADR, descrizione PR, review ed evidenze.

Se non hai a disposizione la tua SRS precedente, usa come minimo questi due riferimenti:

- **RF-03:** al termine della sessione deve essere disponibile un riepilogo con conteggi ed esito;
- **RNF-03:** output ed evidenze non devono contenere dati personali o credenziali.

## Obiettivo

Alla fine non valuto soltanto *cosa hai scritto*, ma anche se riesco a ricostruire **perché** la modifica esiste, **come** è stata versionata e **quali verifiche** la sostengono.

## Workflow richiesto

1. Controlla lo stato del repository con `git status -sb`.
2. Crea un branch dedicato, per esempio `docs/monitormisure-contract`.
3. Completa `PROJECT_README.md` e `ADR-001.md`.
4. Rileggi la diff e crea un primo commit intenzionale.
5. Completa `PR_DESCRIPTION.md`, `REVIEW.md` ed `EVIDENCE.md`.
6. Esegui i controlli dichiarati.
7. Crea un secondo commit con scopo distinto.
8. Ricontrolla diff, log e stato finale.

## Comandi utili

```bash
git status -sb
git switch -c docs/monitormisure-contract
git diff
git add <file>
git diff --staged
git commit -m "docs: document MonitorMisure contract"
git log --oneline -n 5
git diff --stat BASE...HEAD
```

`BASE` è il riferimento indicato dal docente per la prova. Non copiare automaticamente `main` se il tuo laboratorio usa un'altra base.

## Cosa rende buono un commit

Un commit deve poter essere spiegato con una frase semplice. Evita:

- `update`, `fix`, `varie` senza contesto;
- file estranei inseriti per errore;
- due lavori indipendenti nello stesso commit;
- output temporanei, segreti o file generati non richiesti.

Prima di ogni commit guarda **sia** `git status` **sia** la diff staged.

## ADR: registra il perché

L'ADR non è un riassunto dei file modificati. Deve mostrare:

- contesto e forze in gioco;
- decisione;
- almeno due alternative reali;
- conseguenze positive;
- costi/conseguenze negative;
- come verificherai la decisione.

## Descrizione PR

La PR deve permettere al revisore di seguire questa catena:

```text
problema -> RF/RNF -> modifica -> verifica -> rischio/limite
```

Una frase come “ho aggiornato la documentazione” è insufficiente se non spiega cosa cambia per il progetto.

## Self-review

Nel file `REVIEW.md` inserisci almeno tre rilievi specifici. Classificali:

- `blocking`: non dovrebbe essere integrato finché non viene corretto;
- `important`: rischio significativo da risolvere o discutere;
- `suggestion`: miglioramento utile ma non bloccante;
- `style`: preferenza o coerenza editoriale senza impatto sostanziale.

La review riguarda il cambiamento, non la persona.

## Evidenze Git

`EVIDENCE.md` deve contenere output sufficienti a verificare:

- branch usato;
- stato finale;
- almeno due commit;
- diff rispetto alla base;
- collegamento tra requisito e file/modifica.

Prima di incollare output, rimuovi informazioni non necessarie e verifica che non contengano dati sensibili.

## Checklist finale

- [ ] README usabile da una persona che non ha seguito la lezione.
- [ ] ADR spiega una vera decisione e almeno due alternative.
- [ ] PR collega almeno un RF/RNF alle verifiche.
- [ ] Ho lavorato su un branch dedicato.
- [ ] Ho prodotto almeno due commit con scopi distinti.
- [ ] `git status -sb` finale è comprensibile e non mostra file casuali.
- [ ] La self-review contiene almeno tre rilievi classificati.
- [ ] Le evidenze non contengono token, credenziali o dati personali.
- [ ] So spiegare perché i miei commit sono separati in quel modo.
