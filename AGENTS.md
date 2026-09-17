# Regole editoriali del corso

Per ogni modifica alle dispense leggere e seguire
[STYLE_GUIDE.md](content/tpsi_quarto/STYLE_GUIDE.md).
Le regole valgono per tutte le lezioni, presenti e future:

- mantenere il pannello iniziale di orientamento con le sette voci e le icone canoniche;
- usare paragrafi giustificati, liste e tabelle HTML; conservare titoli e blocchi di codice in Markdown;
- presentare ogni definizione nel riquadro centrato **❗ Importante** del template di 2cornot2c, con il termine in grassetto e i marcatori `definition` della guida;
- tenere esempi e approfondimenti fuori dal riquadro, salvo gli elenchi necessari a completare la definizione; non ripetere il riquadro per semplici richiami allo stesso concetto;
- verificare la formattazione con `python scripts/format_tpsi4_lessons.py --check` e controllare la resa delle parti modificate.

La scelta di quali passaggi costituiscano una definizione richiede una revisione editoriale: il controllo automatico verifica il template dei riquadri marcati, non il significato del testo.
