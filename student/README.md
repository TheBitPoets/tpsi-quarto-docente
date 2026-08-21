# Guida studente — TPSI quarto 2026/27

Questa guida descrive il modo di lavorare nel corso. I materiali sono ancora in revisione docente: se una procedura o una slide viene aggiornata durante l'anno, fa fede la versione indicata dal docente e dal repository.

## Workflow di lavoro

```text
leggi -> prevedi -> esegui -> osserva -> modifica -> testa -> debug -> documenta -> consegna
```

L'obiettivo non è soltanto ottenere un output corretto: devi saper spiegare **perché** il programma si comporta in quel modo e quali evidenze lo dimostrano.

## Strumenti

Usa l'ambiente Linux/di laboratorio indicato dal docente. Prima di iniziare verifica gli strumenti richiesti dal modulo, ad esempio:

```bash
git --version
gcc --version
python --version
```

Per i moduli POSIX è necessario un ambiente Linux compatibile con processi, pipe, thread e primitive di sincronizzazione. Se lavori da Windows/macOS usa l'ambiente predisposto dal corso invece di sostituire arbitrariamente le API.

## Prima di un esercizio

1. apri il modulo canonico dal README root;
2. leggi obiettivi e prerequisiti;
3. osserva la slide/checkpoint del docente;
4. individua input, output e proprietà da verificare;
5. solo dopo modifica il codice.

## Quando esegui programmi concorrenti

Non fidarti di una sola esecuzione. Registra almeno:

- PID/process tree quando utile;
- ordine degli eventi osservati;
- exit status/errori;
- output di più esecuzioni se il comportamento può cambiare;
- ipotesi su cosa è condiviso e cosa è privato.

Un programma che “una volta ha funzionato” non dimostra l'assenza di race condition.

## Debugging

Quando qualcosa non funziona evita modifiche casuali. Usa questo ciclo:

```text
riproduci -> formula un'ipotesi -> raccogli evidenza -> cambia una cosa -> riesegui -> aggiungi una regressione
```

Strumenti e tecniche specifici (debugger, sanitizer, log, test) saranno introdotti nei moduli dedicati.

## Git e documentazione

Durante il corso il repository è parte del lavoro tecnico. Un buon commit dovrebbe avere un obiettivo comprensibile e non mescolare correzioni non correlate.

Prima di consegnare controlla:

- cosa hai cambiato;
- perché lo hai cambiato;
- quale requisito/bug affronta;
- come hai verificato il risultato;
- quali limiti o problemi restano.

## Activity e TheBitLab

Alcune attività possono avere un runner/grader automatico; altre saranno valutate manualmente. Se il README indica `da completare/validare`, non significa che tu debba inventare una procedura: segui il percorso indicato dal docente.

L'Activity `fork_pipe_square` è il laboratorio formalizzato attualmente collegato ai moduli su processi, IPC e testing.

## Evidenze da conservare

A seconda dell'attività possono servire:

- sorgenti;
- output del programma;
- test/report;
- screenshot solo quando davvero utili;
- diagramma/process tree/timeline;
- commit SHA;
- breve spiegazione tecnica;
- requisiti o criteri di accettazione collegati.

## Uso responsabile delle fonti e dell'AI

Distingui sempre tra materiale del corso, documentazione tecnica, esempi esterni e contenuto generato/assistito da AI. Non presentare come tuo un testo o codice che non sai spiegare. Rispetta licenze, provenance, privacy e regole indicate dal docente.

## Se una guida cambia durante l'anno

Le correzioni operative non significano automaticamente che il programma del corso è cambiato. Il docente può migliorare slide, spiegazioni, comandi o lab mantenendo invariati gli obiettivi. Le revisioni importanti vengono registrate nel Delivery Change Log.