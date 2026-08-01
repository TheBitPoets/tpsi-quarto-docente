# Mappe visive — Documentazione e controllo di versione

Questa guida affianca [`04_DOCUMENTAZIONE_VERSIONAMENTO.md`](../04_DOCUMENTAZIONE_VERSIONAMENTO.md). Comandi Git, template ADR e descrizioni di PR restano in testo copiabile.

## Architettura a livelli

![La GUI docente chiama l'API locale, che delega al service layer e alle porte storage, repository e grading o AI](../assets/diagrams/04-architecture-layers.svg)

## Flusso Git e pull request

![Issue, branch, commit e pull request passano attraverso test e review prima del merge oppure tornano alle correzioni](../assets/diagrams/04-git-workflow.svg)

## Provenienza delle fonti

![Fonte, versione, frammento, trasformazione e revisione confluiscono in un contenuto pubblicato identificabile e aggiornabile](../assets/diagrams/04-provenance.svg)

## Diagrammi come codice

Il sequence diagram Course Board–Source Catalog–Activity Service resta in Mermaid nel modulo principale per conservarne la modificabilità.

## Uso didattico

- associare ogni livello a una responsabilità;
- usare la PR come spazio di evidenze e decisioni, non soltanto come pulsante di merge;
- registrare provenienza e versione prima di riusare una fonte.
