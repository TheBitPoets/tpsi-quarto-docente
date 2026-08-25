# Note docente — debug e regressione

## Difetti intenzionali

Lo starter contiene due errori di confine correlati:

1. `fill_samples` usa `i <= n`: con un array allocato per `n` elementi l'indice `n` è fuori limite. ASan deve fornire evidenza diretta sul percorso eseguito.
2. `summarize` usa `i < n - 1`: l'ultimo campione non entra nella somma/min/max per `n > 1`.

La soluzione corregge entrambi in `i < n`.

## Perché due difetti

L'obiettivo è mostrare che:

- un test di output può trovare un errore funzionale;
- un sanitizer può trovare un difetto di memoria anche quando un output sembra plausibile;
- strumenti diversi rispondono a domande diverse.

Il caso `N=1` è particolarmente utile: il riepilogo appare corretto, ma l'accesso fuori limite resta presente. Quindi “ho provato un input ed è giusto” non basta.

## Sequenza consigliata

1. baseline senza sanitizer (`1`, `2`, `5`);
2. tabella atteso/osservato;
3. build ASan/UBSan;
4. ipotesi sugli indici validi;
5. fix di una condizione alla volta se si vuole osservare l'effetto;
6. regressione scelta in base alla causa;
7. suite finale e input negativo.

## Controllo rapido della causa

Per un array di `n` elementi gli indici validi sono:

```text
0 .. n-1
```

Quindi:

```c
for (int i = 0; i < n; ++i)
```

è la forma naturale per visitarli tutti una volta.

## Rubrica

- 2 punti: riproduzione/casi limite;
- 2 punti: uso e interpretazione sanitizer;
- 2 punti: causa radice;
- 2 punti: fix minimo + test finali;
- 2 punti: regression report.

## Errori da non premiare come soluzione completa

- aumentare l'allocazione a `n + 1` senza correggere il dominio logico;
- ridurre il numero di campioni elaborati per evitare il crash;
- rimuovere il caso che fallisce;
- disabilitare sanitizer;
- copiare la soluzione senza una causa radice coerente;
- descrivere la regressione come “adesso passa” senza collegarla al bug.

## Domande orali

- Perché `N=1` può ingannare se guardi solo stdout?
- Qual è la differenza tra l'oracolo del test e il sanitizer?
- Quale test rappresenta meglio la causa del bug funzionale?
- Perché allocare `n+1` sarebbe un workaround e non il fix corretto?
- Che cosa dimostra e che cosa non dimostra una corsa ASan senza errori?
