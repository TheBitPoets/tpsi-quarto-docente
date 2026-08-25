# Activity — debug e regressione

Il programma compila, ma non è corretto. Il tuo compito non è cambiare righe a caso: devi produrre una spiegazione riproducibile della causa e una regressione che impedisca il ritorno del difetto.

## 1. Costruisci una baseline

```bash
gcc -Wall -Wextra -Wpedantic -std=c17 main.c -o app
printf '1\n' | ./app
printf '2\n' | ./app
printf '5\n' | ./app
```

Confronta sempre output atteso e reale. Il caso `N=1` da solo è insufficiente.

## 2. Usa i valori limite

Il dominio è `1..1000`. Prova almeno:

```text
1, 2, 5, 1000
```

Chiediti quale indice è l'ultimo valido per un array di `N` elementi.

## 3. Esegui i sanitizer

```bash
gcc -Wall -Wextra -Wpedantic -std=c17 \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  main.c -o app_asan
printf '5\n' | ./app_asan
```

Non limitarti a scrivere “ASan dà errore”: individua funzione, accesso e relazione con la dimensione allocata.

## 4. Formula l'ipotesi prima del fix

Scrivi in `REGRESSION.md`:

```text
sintomo -> evidenza -> ipotesi -> prova che può confermarla/smentirla
```

Poi applica la modifica minima.

## 5. Verifica il contratto finale

Per `N=5`:

```text
Somma: 15
Min: 1
Max: 5
```

Per `N=100`:

```text
Somma: 5050
Min: 1
Max: 100
```

L'input non valido deve continuare a produrre:

```text
Input non valido
```

con exit non-zero.

## 6. Aggiungi la regressione concettuale

Nel report identifica almeno un caso che:

- falliva prima;
- passa dopo;
- è scelto perché esercita proprio la causa radice.

Un caso casuale che passa non è una buona regressione.

## Checklist

- [ ] Ho una riproduzione prima del fix.
- [ ] Ho usato più di un valore limite.
- [ ] Ho eseguito ASan/UBSan.
- [ ] So indicare l'indice massimo valido di un array con `N` elementi.
- [ ] Ho scritto l'ipotesi prima di descrivere la correzione.
- [ ] Il fix è minimo e non cambia il contratto.
- [ ] I casi dichiarati passano.
- [ ] Il sanitizer non segnala errori nei percorsi provati dopo il fix.
- [ ] `REGRESSION.md` collega il test alla causa radice.
