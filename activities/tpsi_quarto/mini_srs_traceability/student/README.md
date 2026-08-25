# Activity — Mini-SRS e tracciabilita dei requisiti

## Il brief: MonitorMisure

Un laboratorio scolastico usa un piccolo sistema per acquisire misure numeriche da una sorgente e salvarle per una successiva analisi. L'esperienza del modulo precedente ha mostrato un modello produttore/consumatore: una parte del sistema acquisisce dati, un'altra li elabora o salva.

Gli stakeholder hanno espresso queste esigenze iniziali:

- il **tecnico di laboratorio** vuole avviare una sessione e sapere se l'acquisizione procede correttamente;
- il **docente** vuole poter verificare quante misure sono state acquisite e quante elaborate senza leggere log tecnici complessi;
- il **manutentore** vuole che gli errori siano diagnosticabili e che il comportamento sia riproducibile;
- la **scuola** vuole evitare dati personali, credenziali o informazioni sensibili nei file di prova.

Vincoli già noti del progetto scolastico:

- il prototipo deve poter essere realizzato con strumenti disponibili nel laboratorio;
- il lavoro deve essere dimostrabile offline;
- per questa iterazione non è richiesta un'interfaccia grafica;
- non è richiesto il collegamento a sensori fisici reali: una sorgente simulata è sufficiente per la demo.

Il brief è volutamente incompleto. Devi trasformarlo in requisiti verificabili senza inventare una soluzione dettagliata prima del necessario.

## Obiettivo

Produrre due file coerenti:

- `SRS.md`: una specifica leggera dei requisiti;
- `TRACEABILITY.csv`: la matrice che collega requisiti, fonte/stakeholder, criterio di accettazione ed evidenza prevista.

Non esiste una sola SRS corretta. La qualità dipende da chiarezza, verificabilita, coerenza e tracciabilita.

## Minimo richiesto

La SRS deve contenere:

1. scopo e contesto;
2. almeno 3 stakeholder con bisogno e rischio;
3. almeno 2 attori;
4. glossario di almeno 5 termini;
5. almeno 4 requisiti funzionali `RF-*`;
6. almeno 3 requisiti non funzionali `RNF-*`;
7. almeno 2 vincoli;
8. un caso d'uso con main flow e almeno 2 alternative;
9. almeno un criterio di accettazione/evidenza per ogni RF/RNF;
10. almeno 2 elementi `Won't now` motivati;
11. questioni aperte/rischi;
12. matrice di tracciabilita coerente con tutti gli ID.

## Da richiesta vaga a requisito verificabile

Troppo vago:

```text
Il sistema deve essere veloce.
```

Meglio, se il contesto lo giustifica:

```text
RNF-02 Durante una sessione di prova con 1.000 misure simulate, il sistema deve
completare l'elaborazione senza perdere campioni e terminare entro il limite
definito nel piano di prova del laboratorio.
```

Ancora meglio: nella tua SRS specifica anche **come** raccoglierai l'evidenza e quale ambiente di prova userai.

## Non confondere requisito e soluzione

Questa frase e troppo implementativa se il brief non l'ha imposta:

```text
RF-01 Il sistema deve usare pthread_cond_wait e un array di 4 interi.
```

Può diventare un requisito di comportamento:

```text
RF-01 Il sistema deve acquisire e processare tutte le misure della sessione,
mantenendo identificabile il numero di campioni prodotti e consumati.
```

Se una tecnologia è davvero obbligatoria per ragioni didattiche o operative, dichiarala come **vincolo** e spiegane la fonte.

## Criteri di accettazione

Esempio Given/When/Then:

```text
Dato che una sessione contiene 100 misure simulate
Quando la sessione termina senza errore
Allora il riepilogo indica 100 misure acquisite e 100 misure elaborate
E non risultano campioni mancanti.
```

Copri anche percorsi negativi: input non valido, errore di acquisizione, sessione interrotta, dati fuori dominio, a seconda dei requisiti che hai scelto.

## Matrice di tracciabilita

Ogni requisito deve avere una riga logica in `TRACEABILITY.csv`:

```text
requirement_id,source_or_stakeholder,acceptance_criterion,evidence
RF-01,tecnico di laboratorio,AC-01,report della prova guidata
```

La matrice serve a rispondere a quattro domande:

- Perche esiste questo requisito?
- Chi lo ha chiesto o da quale vincolo deriva?
- Come sapremo se e soddisfatto?
- Quale evidenza conserveremo?

## Priorita MoSCoW

Usa:

- `Must` per cio che rende inutile il rilascio se manca;
- `Should` per cio che e importante ma ammette una soluzione temporanea;
- `Could` per miglioramenti non essenziali;
- `Won't now` per elementi deliberatamente fuori dall'iterazione corrente.

Non mettere tutto in `Must`: la priorita deve aiutare a prendere decisioni.

## Checklist finale

- [ ] Ogni RF/RNF descrive una sola proprieta principale.
- [ ] Ogni requisito e comprensibile senza conoscere la soluzione tecnica.
- [ ] Ogni requisito e verificabile con una prova o osservazione.
- [ ] Gli ID della SRS e della matrice coincidono.
- [ ] Ogni requisito ha fonte/stakeholder, priorita e criterio/evidenza.
- [ ] Il caso d'uso ha almeno due alternative reali.
- [ ] I `Won't now` definiscono il confine, non promesse nascoste.
- [ ] Non hai inserito nomi reali di studenti, credenziali o dati personali.
- [ ] Sai spiegare almeno un caso in cui hai trasformato una richiesta vaga in un requisito migliore.
