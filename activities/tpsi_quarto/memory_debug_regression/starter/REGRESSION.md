# Regression report

## Ambiente

- sistema operativo: TODO
- compilatore/versione: TODO
- commit o versione del laboratorio: TODO

## Sintomo riprodotto

Comando/input minimo:

```text
TODO
```

Atteso:

```text
TODO
```

Osservato:

```text
TODO
```

## Evidenza sanitizer

Comando:

```bash
gcc -Wall -Wextra -Wpedantic -std=c17 -fsanitize=address,undefined -fno-omit-frame-pointer main.c -o app_asan
```

Estratto essenziale del risultato prima del fix:

```text
TODO
```

## Ipotesi

TODO

## Causa radice

TODO: indica funzione, condizione errata e perche viola il dominio valido degli indici/casi.

## Correzione minima

TODO

## Test di regressione

- input: TODO
- perche questo caso copre la causa: TODO
- risultato dopo il fix: TODO

## Verifica finale

- [ ] build senza warning con i flag richiesti
- [ ] casi limite dichiarati corretti
- [ ] sanitizer senza segnalazioni nei percorsi provati
- [ ] input non valido ancora rifiutato
- [ ] nessun debug aggiunto a stdout
