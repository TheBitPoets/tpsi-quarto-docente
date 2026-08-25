# Activity — capstone responsabile

## Scopo

Questa consegna riunisce il lavoro del corso. Puoi usare **MonitorMisure** oppure un progetto concorrente equivalente approvato dal docente. Non devi inventare un progetto enorme: devi rendere **verificabile e responsabile** un progetto piccolo.

## I quattro file da completare

1. `FINAL_REPORT.md` — cosa hai costruito, quali requisiti copre, architettura, verifiche, limiti.
2. `SOURCES.json` — provenienza, versione/ref, licenza-status e uso delle fonti.
3. `PRIVACY_SECURITY.md` — dati, minimizzazione, ruoli, segreti, supply-chain e rischi residui.
4. `ACCESSIBILITY_AI.md` — accessibilita, eventuale uso AI, verifiche umane, limiti dell'automazione e uso delle risorse.

## Regola principale: non dichiarare più di ciò che hai verificato

Scrivi:

```text
Ho eseguito questi test...
Non ho eseguito questi controlli...
Questa evidenza supporta questa conclusione...
Questi rischi restano aperti...
```

Evita frasi come:

```text
La CI è verde, quindi è sicuro.
L'AI ha detto che il codice è corretto.
Ho tolto il nome, quindi non ci sono dati personali.
È online, quindi posso copiarlo.
```

## Provenienza e licenze

Per ogni fonte esterna significativa registra almeno:

- autore/organizzazione o provider;
- titolo;
- URI/repository;
- versione/ref;
- licenza o stato della licenza;
- come l'hai usata;
- trasformazioni effettuate;
- cosa puoi o non puoi redistribuire.

Se il diritto di copia non è chiaro, usa il riferimento senza incorporare il contenuto.

## Privacy e segreti

Chiediti:

- serve davvero il nome completo?
- un ID pseudonimo basta?
- chi vede i risultati?
- quanto tempo servono i report?
- output/log contengono token o percorsi personali?
- quali dati posso eliminare?

Se un segreto fosse esposto, cancellarlo dall'ultimo commit non è una soluzione completa: va revocato/ruotato secondo il contesto.

## Supply-chain

Non limitarti alle librerie. Considera anche:

- compilatore/toolchain;
- action CI;
- immagini/container;
- plugin;
- repository/fonti;
- modelli/provider AI.

Per gli elementi critici indica almeno fonte e versione/ref quando possibile.

## Uso di AI

Se non hai usato AI, dichiaralo. Se l'hai usata, documenta **cosa le hai chiesto, quali dati/fonti hai fornito, cosa hai accettato e come l'hai verificato**.

L'AI non deve diventare la fonte primaria di un fatto tecnico che puoi verificare su documentazione o test.

## Accessibilita

Controlla almeno:

- heading gerarchici;
- informazioni non affidate solo al colore;
- testo alternativo quando serve;
- codice e comandi copiabili;
- prerequisiti chiari;
- uso da tastiera quando applicabile.

Accessibile non significa “più facile”: significa rimuovere barriere inutili.

## Checklist finale

- [ ] Ogni requisito importante ha una evidenza o un limite dichiarato.
- [ ] `SOURCES.json` è JSON valido e contiene fonti/versioni/licenze-status.
- [ ] Non ho copiato materiale con diritti incerti solo perché accessibile online.
- [ ] Ho minimizzato dati e separato ruoli/permessi.
- [ ] Nessun token, password o chiave compare nella consegna.
- [ ] Ho identificato dipendenze/strumenti critici della supply-chain.
- [ ] Eventuale uso AI è dichiarato e verificato; altrimenti ho scritto `AI non usata`.
- [ ] Ho svolto controlli di accessibilita.
- [ ] Ho indicato almeno due limiti dell'automazione.
- [ ] Ho distinto controlli eseguiti da controlli non eseguiti.
- [ ] Ho indicato almeno una scelta motivata sull'uso responsabile delle risorse.
