# Mappe visive — Testing e debugging

Questa guida affianca [`05_TESTING_DEBUGGING.md`](../05_TESTING_DEBUGGING.md). Comandi, output, bug report e casi di test restano in testo copiabile.

## Verifica e validazione

![La verifica confronta prodotto e specifica, mentre la validazione confronta prodotto e bisogno dello stakeholder](../assets/diagrams/05-verification-validation.svg)

## Livelli di test

![Scala dai test unitari ai test di integrazione, sistema e accettazione con contesto e costo crescenti](../assets/diagrams/05-test-levels.svg)

## Ciclo di vita dei contenuti

![Una bozza passa a reviewed, approved, assigned e closed, con percorsi verso correzione o versione superseded](../assets/diagrams/05-content-lifecycle.svg)

## Ciclo del debugging

![Riproduzione, riduzione, osservazione, ipotesi, esperimento, correzione, regressione e verifica più ampia formano un ciclo](../assets/diagrams/05-debug-cycle.svg)

## Pipeline di qualità locale

![Validatori, pytest, toolchain e prova reale producono evidenze per la review senza usare GitHub Actions private](../assets/diagrams/05-quality-pipeline.svg)

## Uso didattico

- derivare i test dai requisiti;
- scegliere il livello adatto alla domanda;
- correggere soltanto dopo aver raccolto evidenze;
- ricordare che una suite verde non dimostra l'assenza di ogni difetto.
