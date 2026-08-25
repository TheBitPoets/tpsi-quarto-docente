# Riferimento docente — capstone responsabile

## Obiettivo della correzione

Il capstone non premia la quantità di documenti. Premia una catena di responsabilità verificabile:

```text
bisogno/requisito
  -> decisione/implementazione
  -> verifica/evidenza
  -> provenienza e diritti
  -> dati/rischi/limiti
  -> responsabilità residua
```

Un progetto piccolo con limiti dichiarati può essere migliore di un progetto ambizioso con affermazioni non dimostrate.

## Evidenze minime accettabili

### Tecnica

- identificazione del progetto/versione;
- almeno un requisito o criterio di accettazione tracciato;
- architettura concorrente spiegata con stato condiviso/invariante quando applicabile;
- verifiche reali con ambiente/comando o procedura;
- controlli non eseguiti dichiarati.

### Provenienza

Per fonti significative:

- identificatore/titolo;
- provider o organizzazione;
- URI/repository;
- versione/ref;
- licenza o `license_status`;
- uso/trasformazione;
- nota sulla redistribuzione.

L'assenza di licenza esplicita non va trasformata in “libero”. Se i diritti sono incerti, è corretta la scelta di conservare solo il riferimento e produrre materiale originale.

### Privacy e sicurezza

Cercare:

- inventario ragionato, non una lista generica;
- minimizzazione concreta;
- separazione ruoli/permessi;
- gestione dei segreti;
- dipendenze/supply-chain con versione o provenienza;
- rischi residui.

La UI nascosta non vale come autorizzazione server-side.

### AI

Sono entrambe valide:

- `AI non usata`;
- uso AI documentato con scopo, modello/provider se noto, dati/fonti forniti, output selezionato, verifiche umane e limiti.

Penalizzare affermazioni come “l'AI ha verificato” se non esiste evidenza indipendente.

### Accessibilità e risorse

Lo studente deve mostrare almeno controlli concreti su struttura/uso dei materiali e una scelta motivata di uso responsabile delle risorse. Non richiedere ottimizzazioni simboliche: serve un trade-off reale, anche piccolo.

## Esempio di buona limitazione

```text
Ho eseguito test deterministici su Linux/gcc per gli input dichiarati. Non ho
eseguito ThreadSanitizer né prove di carico; quindi non dichiaro assenza di data
race o starvation. Il protocollo dei lock è stato inoltre revisionato manualmente.
```

È più corretto di:

```text
Tutti i test passano, quindi il programma concorrente è sicuro.
```

## Esempio di fonte

```json
{
  "source_id": "posix-pthreads-reference",
  "title": "TODO titolo reale usato dallo studente",
  "provider": "TODO",
  "uri_or_repository": "TODO",
  "ref_or_version": "TODO",
  "license_status": "reference-only-or-verified-license",
  "use_in_project": "verifica del contratto pthread_cond_wait",
  "transformation": "nessuna copia sostanziale; sintesi originale",
  "redistribution_note": "conservato il riferimento"
}
```

Non fornire agli studenti questo esempio con dati inventati come se fossero una fonte reale: serve solo a mostrare la forma dell'evidenza.

## Rubrica — 10 punti

### 1. Coerenza tecnica e tracciabilità — 2

- progetto/versione identificabile;
- catena requisito -> decisione -> verifica;
- architettura/limiti coerenti.

### 2. Provenienza e licenze — 2

- manifest completo e coerente;
- distinzione accesso/copia/redistribuzione;
- nessuna attribuzione o licenza inventata.

### 3. Privacy, sicurezza e supply-chain — 2

- minimizzazione;
- ruoli;
- segreti;
- dipendenze/versioni;
- rischi residui.

### 4. Verifiche, limiti e AI — 2

- test/controlli realmente eseguiti;
- controlli non eseguiti;
- uso AI dichiarato o assente;
- responsabilità umana esplicita.

### 5. Accessibilità e uso delle risorse — 2

- controlli concreti;
- barriere considerate;
- almeno una scelta motivata su CI/storage/AI/hardware/rete.

## Red flags

- segreti o dati personali reali nella consegna;
- licenza inventata;
- contenuto copiato integralmente con diritti incerti;
- CI verde presentata come prova di sicurezza completa;
- uso AI occultato quando è parte sostanziale del lavoro;
- metriche sugli studenti interpretate automaticamente come giudizi personali;
- rischi noti cancellati dal report per “far sembrare finito” il progetto.

## Domande orali rapide

- Mostrami una catena requisito -> evidenza.
- Quale fonte non hai copiato perché la redistribuzione non era chiara?
- Quale dato hai eliminato perché non necessario?
- Quale dipendenza o tool della supply-chain hai identificato per versione/ref?
- Che cosa NON dimostrano i tuoi test?
- Se hai usato AI, quale suo output hai verificato indipendentemente? Se non l'hai usata, dove lo dichiari?
- Quale barriera di accessibilità hai rimosso?
- Quale rischio rimane aperto dopo la consegna?
