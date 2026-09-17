# Audit delle immagini TPSI quarto

Audit iniziale del 14 settembre 2026. Copertura: le sei dispense, la matrice curricolare, il Course Design e il laboratorio fork/pipe. Il risultato è una prima serie di **22 figure originali**, composte con **27 simboli riutilizzabili**, e tre cataloghi visivi.

## Fonti e limiti del confronto

| Riferimento | Verificato | Uso nell'audit |
|---|---|---|
| [Visual System della quinta](https://github.com/TheBitPoets/tpsi-quinto-docente/tree/main/assets/tpsi5/visual-system) | README, tokens, components e generatore letti | Architettura libreria → scene → SVG autonomi; nove simboli comuni riutilizzati. |
| [Standard editoriale della quinta](https://github.com/TheBitPoets/tpsi-quinto-docente/blob/main/content/tpsi5/STYLE_GUIDE.md) | Letto | Titoli Markdown, figure locali centrate, alt e componenti HTML accessibili. |
| [Indice pubblico Hoepli, volume 2](https://www.hoeplieditore.it/scuola/articolo/tecnologie-e-progettazione-di-sistemi-informatici-e-di-telecomunicazioni-per-larticolazione-informatica--paolo-camagni/9788836015122/2012) | Indice consultabile nei risultati pubblici | Conferma i nuclei processi, sincronizzazione, requisiti, documentazione, testing e cittadinanza. |
| [Volume adottato in bSmart](https://my.bsmart.it/#/books/15068?revision=3) | **Pagine interne non consultabili da questa sessione**: il lettore mostra soltanto il caricamento | Confronto del genere e della funzione delle figure da completare; nessuna figura o pagina interna viene dichiarata esaminata. |
| [Dispense locali](../content/tpsi_quarto/README.md) e [copertura](../content/tpsi_quarto/COVERAGE.md) | Letti obiettivi, spiegazioni, schemi, tabelle ed esercizi | Fonte delle situazioni didattiche e delle collocazioni. |

Il libro è un riferimento per la copertura e, quando consultabile, per capire quali relazioni meritano una figura. Le composizioni, le etichette e gli esempi di questa serie sono originali: non riproducono impaginazione o illustrazioni del volume. Non sono stati acquisiti screenshot del libro.

## Criterio di scelta

Una figura viene inserita quando chiarisce una struttura, un confine, uno stato, un flusso o una sequenza che la sola prosa rende difficile da seguire. Tabelle di API, checklist, snippet e piccoli esempi testuali restano leggibili e copiabili. Non si aggiunge un'icona decorativa per ogni paragrafo.

I confronti usano pannelli affiancati; le strutture annidate usano confini; le tracce hanno un asse temporale esplicito; gli stati hanno transizioni etichettate. Le frecce nei casi d'uso non vengono usate per suggerire una sequenza: le associazioni sono linee senza punta.

## Inventario degli oggetti ricorrenti

Gli identificatori e l'origine sono registrati anche in [component-inventory.json](../assets/tpsi4/visual-system/component-inventory.json). Le varianti semantiche sono espresse dalle etichette della scena: padre e figlio usano lo stesso processo; produttore e consumatore lo stesso thread; README e ADR lo stesso documento.

| Simbolo | Oggetto | Origine | Figure che lo riusano |
|---|---|---|---|
| `tpsi-user` | Persona / attore | Quinta, riuso | 03-casi-uso, 06-provenienza, 06-accessi |
| `tpsi-document` | Documento | Quinta, riuso | 01-programma-processi, 03-tracciabilita, 04-documentazione, 05-statica-dinamica, 06-provenienza |
| `tpsi-terminal` | Terminale | Quinta, riuso | 03-tracciabilita, 05-debug |
| `tpsi-repository` | Repository | Quinta, riuso | 05-debug, 06-provenienza |
| `tpsi-lock` | Segreto / risorsa protetta | Quinta, riuso | Disponibile nel catalogo; nessuna scena di lezione lo richiede ancora. |
| `tpsi-test` | Test | Quinta, riuso | 03-tracciabilita, 05-statica-dinamica, 05-debug |
| `tpsi-artifact` | Artefatto | Quinta, riuso | 06-provenienza |
| `tpsi-server` | Server | Quinta, riuso | Disponibile nel catalogo; nessuna scena di lezione lo richiede ancora. |
| `tpsi-database` | Archivio dati | Quinta, riuso | Disponibile nel catalogo; nessuna scena di lezione lo richiede ancora. |
| `tpsi-process` | Processo | Quarta, nuovo | 01-programma-processi, 02-pipe, 06-progetto |
| `tpsi-thread` | Thread | Quarta, nuovo | 01-memoria-thread, 02-buffer-condition, 02-lettori-scrittori, 02-monitor |
| `tpsi-memory` | Area di memoria | Quarta, nuovo | 01-memoria-thread, 02-race, 02-lettori-scrittori |
| `tpsi-cpu` | CPU / core | Quarta, nuovo | Disponibile nel catalogo; nessuna scena di lezione lo richiede ancora. |
| `tpsi-pipe` | Pipe | Quarta, nuovo | 02-pipe |
| `tpsi-queue` | Coda / buffer | Quarta, nuovo | 02-buffer-condition, 06-progetto |
| `tpsi-message` | Messaggio | Quarta, nuovo | 02-protocollo |
| `tpsi-mutex` | Mutex | Quarta, nuovo | 02-mutex-semaforo |
| `tpsi-semaphore` | Semaforo contatore | Quarta, nuovo | 02-mutex-semaforo |
| `tpsi-condition` | Variabile di condizione | Quarta, nuovo | Disponibile nel catalogo; nessuna scena di lezione lo richiede ancora. |
| `tpsi-monitor` | Monitor software | Quarta, nuovo | 02-monitor |
| `tpsi-commit` | Commit | Quarta, nuovo | 04-git |
| `tpsi-requirement` | Requisito verificabile | Quarta, nuovo | 03-tracciabilita |
| `tpsi-debugger` | Debugger / osservazione | Quarta, nuovo | 05-debug |
| `tpsi-shield` | Controllo di accesso | Quarta, nuovo | 06-accessi |
| `tpsi-badge-c` | C | Quarta, nuovo | Disponibile nel catalogo; nessuna scena di lezione lo richiede ancora. |
| `tpsi-badge-posix` | POSIX | Quarta, nuovo | Disponibile nel catalogo; nessuna scena di lezione lo richiede ancora. |
| `tpsi-badge-java` | Java | Quarta, nuovo | Disponibile nel catalogo; nessuna scena di lezione lo richiede ancora. |

Server, database, lucchetto di sicurezza e badge C/POSIX/Java restano disponibili per scene di laboratorio e confronti successivi. Il loro uso non è obbligatorio. Non sono importati browser, smartphone, cloud, cookie, componenti UI, route, API Web o badge frontend: non servono alle figure del percorso attuale.

## Piano delle figure e collocazione

Aggiornamento: il registro comprende ora **30 figure**. La figura [Dalle pagine virtuali alle pagine fisiche](../assets/tpsi4/01-indirizzi-virtuali-mmu.svg) è inserita nella lezione 1, in “Anatomia di un processo”, nel paragrafo sullo spazio di indirizzamento. Usa pannelli e frecce della grammatica visiva esistente, senza nuovi simboli.

La versione semplificata mette al centro quattro elementi: spazio virtuale diviso in pagine, kernel con tabelle di corrispondenza e gestione dei frame, MMU, RAM suddivisa in frame. Colori e sigle permettono di seguire V1/F4, V2/F1 e V3/F6. Sono stati rimossi dalla figura e dal percorso introduttivo i dettagli su TLB, page fault, indirizzi esadecimali e strutture specifiche di Linux. Riferimenti tecnici restano [Linux Page Tables](https://docs.kernel.org/mm/page_tables.html) e [Physical Memory](https://docs.kernel.org/mm/physical_memory.html).

La figura aggiornata è stata renderizzata con Chrome headless e ispezionata: etichette, corrispondenze e frecce sono leggibili. Build, sette test del Visual System e cinque test di formattazione superati.

Tutte le figure sotto sono composte e inserite. La revisione docente resta aperta, come per le dispense in stato `draft`. Il registro strutturato è [figure-index.json](../assets/tpsi4/visual-system/figure-index.json): conserva sezione, alt, didascalia, componenti e percorsi.

| Figura | Sezione della dispensa | Domanda a cui risponde |
|---|---|---|
| [Un programma, due processi](../assets/tpsi4/01-programma-processi.svg) | [Dal programma al processo](../content/tpsi_quarto/01_PROCESSI_E_CONCORRENZA.md#dal-programma-al-processo) | Lo stesso eseguibile avvia due processi con PID diversi e spazi di memoria distinti. |
| [Il ciclo di vita di un processo](../assets/tpsi4/01-stati-processo.svg) | [Stato e ciclo di vita di un processo](../content/tpsi_quarto/01_PROCESSI_E_CONCORRENZA.md#stato-e-ciclo-di-vita-di-un-processo) | Nuovo passa a pronto; lo scheduler porta pronto in esecuzione. Attesa di I/O porta in attesa; l'evento riporta a pronto. La preemption riporta il processo da in esecuzione a pronto; l'uscita porta a terminato. |
| [Processi isolati, thread nello stesso spazio](../assets/tpsi4/01-memoria-thread.svg) | [Risorse private e risorse condivise](../content/tpsi_quarto/01_PROCESSI_E_CONCORRENZA.md#risorse-private-e-risorse-condivise) | Due processi hanno heap separati. Due thread di uno stesso processo condividono heap, globali e descrittori, ma conservano stack e registri propri. |
| [Concorrenza e parallelismo](../assets/tpsi4/01-concorrenza-parallelismo.svg) | [Sequenziale, concorrente e parallelo](../content/tpsi_quarto/01_PROCESSI_E_CONCORRENZA.md#sequenziale-concorrente-e-parallelo) | Sequenziale: A termina prima di B. Concorrente su un core: A e B alternano i passi. Parallelo su due core: A e B eseguono passi nello stesso intervallo. |
| [fork, exec e wait: tre operazioni diverse](../assets/tpsi4/01-fork-exec-wait.svg) | [Creazione di processi: `fork`, `exec` e `wait`](../content/tpsi_quarto/01_PROCESSI_E_CONCORRENZA.md#creazione-di-processi-fork-exec-e-wait) | fork crea un figlio con un PID nuovo; exec cambia il programma del figlio mantenendone il PID; waitpid nel padre raccoglie lo stato dopo la terminazione del figlio. |
| [Una pipe: dal figlio al padre](../assets/tpsi4/02-pipe.svg) | [Comunicazione tra processi con pipe](../content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#comunicazione-tra-processi-con-pipe) | Dopo pipe e fork, il figlio scrive il quadrato su fd[1] e chiude fd[0]; il padre legge fd[0] e chiude fd[1]. I dati attraversano la pipe del kernel; waitpid raccoglie il figlio. |
| [Due incrementi, un aggiornamento perso](../assets/tpsi4/02-race.svg) | [Race condition](../content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#race-condition) | Nel modello didattico A e B leggono entrambi zero, calcolano uno e scrivono uno. L'aggiornamento di un thread viene perso. |
| [Mutex e semaforo: due contratti](../assets/tpsi4/02-mutex-semaforo.svg) | [Semafori](../content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#semafori) | Un mutex protegge l'accesso esclusivo allo stato ed è rilasciato dal proprietario. Un semaforo rappresenta disponibilità: acquisire consuma un permesso, rilasciare ne restituisce uno. |
| [Produttori e consumatori](../assets/tpsi4/02-buffer-condition.svg) | [Produttori e consumatori](../content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#produttori-e-consumatori) | Il produttore attende not_full quando il buffer è pieno; il consumatore attende not_empty quando è vuoto. Inserimento e prelievo avvengono sotto mutex; ogni risveglio richiede un nuovo controllo del predicato. |
| [Lettori e scrittori](../assets/tpsi4/02-lettori-scrittori.svg) | [Lettori e scrittori](../content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#lettori-e-scrittori) | Più lettori possono leggere insieme; uno scrittore richiede accesso esclusivo, senza lettori attivi. La politica di ammissione deve evitare attese indefinite. |
| [Deadlock: un ciclo di attese](../assets/tpsi4/02-deadlock.svg) | [Deadlock](../content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#deadlock) | Il thread A possiede X e attende Y; B possiede Y e attende X. Nel grafo la freccia risorsa verso thread indica assegnazione, thread verso risorsa indica attesa. |
| [Il monitor incapsula le regole](../assets/tpsi4/02-monitor.svg) | [Monitor](../content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#monitor) | I chiamanti accedono allo stato del monitor attraverso operazioni protette. Il monitor contiene stato privato, mutua esclusione e condizioni di attesa. |
| [Un flusso di byte ha bisogno di un protocollo](../assets/tpsi4/02-protocollo.svg) | [Scambio di messaggi e protocollo](../content/tpsi_quarto/02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#scambio-di-messaggi-e-protocollo) | Un messaggio comprende versione, tipo, ID richiesta, lunghezza e payload. Il ricevente accumula i byte e valida il formato prima di elaborare la richiesta. |
| [Dal requisito all'evidenza](../assets/tpsi4/03-tracciabilita.svg) | [Tracciabilità](../content/tpsi_quarto/03_REQUISITI_SOFTWARE.md#tracciabilità) | Il requisito di capacità del buffer guida l'implementazione; un test di inserimento a buffer pieno verifica il comportamento; il report documenta l'esito. Gli identificatori collegano i quattro artefatti. |
| [Attori, obiettivi e confine del sistema](../assets/tpsi4/03-casi-uso.svg) | [Attori, casi d'uso e scenari](../content/tpsi_quarto/03_REQUISITI_SOFTWARE.md#attori-casi-duso-e-scenari) | Il docente è associato all'assegnazione del laboratorio; lo studente alla consegna e alla consultazione del feedback. I casi d'uso sono dentro il confine della piattaforma; gli attori sono esterni. |
| [La documentazione accompagna il progetto](../assets/tpsi4/04-documentazione.svg) | [Tipi di documentazione del progetto](../content/tpsi_quarto/04_DOCUMENTAZIONE_VERSIONAMENTO.md#tipi-di-documentazione-del-progetto) | Il README collega guida di avvio, documentazione architetturale e contratti del codice. I documenti rispondono a domande diverse e vengono mantenuti insieme al progetto. |
| [Branch e merge: una storia di snapshot](../assets/tpsi4/04-git.svg) | [Controllo di versione con Git](../content/tpsi_quarto/04_DOCUMENTAZIONE_VERSIONAMENTO.md#controllo-di-versione-con-git) | Da C1 parte feature con F1 e F2 mentre main avanza a C2. Dopo review, un merge crea M con genitori C2 e F2. I conflitti eventuali si risolvono prima del commit di merge. |
| [Verifica statica e dinamica](../assets/tpsi4/05-statica-dinamica.svg) | [Verifica statica](../content/tpsi_quarto/05_TESTING_DEBUGGING.md#verifica-statica) | La verifica statica esamina codice e documenti senza eseguire il programma: review, analisi e warning. La verifica dinamica esegue il programma con input e confronta risultati e comportamento attesi. |
| [Debugging: dalle osservazioni alla correzione](../assets/tpsi4/05-debug.svg) | [Debugging come ciclo di ipotesi](../content/tpsi_quarto/05_TESTING_DEBUGGING.md#debugging-come-ciclo-di-ipotesi) | Riproduci e riduci il difetto, raccogli evidenze, formula un'ipotesi e mettila alla prova. Se è smentita, formula una nuova ipotesi; se confermata, correggi e aggiungi una regressione. |
| [La provenienza resta visibile](../assets/tpsi4/06-provenienza.svg) | [Provenienza](../content/tpsi_quarto/06_CITTADINANZA_DIGITALE.md#provenienza) | Libro e documentazione sono riferimenti dichiarati. La bozza originale conserva le fonti; il docente verifica e revisiona; la versione consegnata conserva l'identità e la storia della revisione. |
| [L'autorizzazione si applica sul server](../assets/tpsi4/06-accessi.svg) | [Ruoli e autorizzazioni](../content/tpsi_quarto/06_CITTADINANZA_DIGITALE.md#ruoli-e-autorizzazioni) | La richiesta porta un'identità al server. Il server verifica ruolo, operazione e risorsa: può consentire la lettura della propria consegna oppure rifiutare l'accesso dello studente alla soluzione docente. |
| [Progetto finale: un sistema concorrente verificabile](../assets/tpsi4/06-progetto.svg) | [Progetto finale suggerito](../content/tpsi_quarto/06_CITTADINANZA_DIGITALE.md#progetto-finale-suggerito) | Un coordinatore distribuisce richieste attraverso una coda limitata a più worker. Ogni richiesta ha un'identità e un esito tracciabile; requisiti, test e documentazione accompagnano il sistema. |

## Punti tecnici controllati

- **Stati del processo:** evento → pronto → dispatch; corretta la freccia ambigua del precedente schema ASCII. Il diagramma è un modello didattico, non l'elenco completo degli stati Linux.
- **Memoria:** heap condiviso fra thread, stack e registri separati; isolamento ordinario fra processi. Fonte di riscontro: [pthreads(7)](https://man7.org/linux/man-pages/man7/pthreads.7.html).
- **fork/exec/wait:** nuovo PID alla fork; stesso PID dopo exec; stato del figlio raccolto da waitpid. La figura distingue il percorso riuscito e annota gli errori. Riscontro: [fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html).
- **Pipe:** direzione figlio → padre coerente con l'activity; chiusure delle estremità e significato di EOF; nessun confine implicito fra messaggi. Riscontro: [pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html).
- **Race:** la tabella è un modello concettuale; non promette un risultato definito per una data race C.
- **Condition:** rilascio atomico del mutex durante l'attesa, riacquisizione al ritorno e ricontrollo in while. Riscontro: [pthread_cond_wait](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3.html).
- **Deadlock:** risorsa → thread significa assegnazione; thread → risorsa significa attesa. Il caso usa due mutex esclusivi.
- **Git:** il merge illustrato ha due genitori; direzione temporale e relazione fra commit sono distinte.
- **Progetto:** coda e worker rappresentano un'architettura possibile; la consegna deve precisare protocollo, arresto e gestione degli esiti.

## Estensioni da valutare con il libro e durante la revisione

| Tema | Decisione iniziale | Quando aggiungere una figura |
|---|---|---|
| Albero PID/PPID con più generazioni | fork già illustrata; comandi ps/pstree conservati | Se l'esercizio richiede leggere una gerarchia più ampia. |
| Fork/join POSIX e Java a confronto | Tabella e codice restano il riferimento | Se si introduce una lezione autonoma sulla somma parallela. |
| Segnali e cancellazione cooperativa | Pseudocodice e regole restano leggibili | Con un laboratorio di arresto e cleanup verificabile. |
| Coda circolare con indici | Prima figura limitata a count e condizioni | Quando si sviluppa l'implementazione dell'array circolare. |
| Architettura a livelli | Conservato il diagramma Mermaid già presente | Se occorre condividerlo anche in slide SVG. |
| Livelli di test e valori limite | Testo e tabelle sono sufficienti per il primo passaggio | Se si aggiunge una matrice di test specifica del progetto. |
| Supply chain e minimizzazione | Matrice dei ruoli e figura di provenienza coprono i confini iniziali | Con un caso concreto di dipendenze o trattamento dei dati. |

Il confronto delle figure interne del libro resta **da fare**, non è un audit completato del volume. Eventuali nuove figure vanno aggiunte alla libreria e al registro senza ridisegnare gli oggetti già disponibili.

## Verifica del primo rilascio grafico

Le 22 figure e i tre cataloghi sono stati renderizzati con Chrome headless e ispezionati visivamente. Il controllo ha portato a spostare un'etichetta nel diagramma degli stati. Verificati 91 collegamenti locali dei documenti di orientamento, audit e README; titoli e blocchi di codice delle sei dispense sono preservati, salvo la sostituzione intenzionale dello schema ASCII degli stati.

La build deterministica e i sette test del Visual System passano. I controlli sono inseriti nella Quality per Windows e Ubuntu. La revisione didattica del docente e il confronto con le figure interne bSmart restano aperti.

## Semplificazione del contesto con figure

Il percorso C/assembly della lezione 1 è sostituito da tre figure originali: [registri e memoria](../assets/tpsi4/01-registri-memoria.svg), [chiamata e stack](../assets/tpsi4/01-chiamata-stack.svg), [salvataggio e ripresa](../assets/tpsi4/01-contesto-salvataggio.svg). Il testo introduce pochi registri Intel x86-64 e segue il calcolo 20 + 3 senza listati né comandi di compilazione. Gli altri esempi operativi del modulo rimangono nelle rispettive sezioni.

Riutilizzato il simbolo CPU; pannelli, frecce e palette appartengono al sistema esistente. Nessun nuovo simbolo necessario. Le scene sono state renderizzate e ispezionate visivamente; la build e i 12 test di grafica e formattazione passano.

## Stack delle chiamate annidate

La figura [main, acquisisci e converti](../assets/tpsi4/01-stack-chiamate-annidate.svg) sostituisce lo schema ASCII nel paragrafo 4 della lezione 1. Tre pannelli mostrano lo stack mentre esegue converti, dopo il ritorno ad acquisisci e dopo il ritorno a main. Colori costanti e diciture sulla cima dello stack distinguono i frame. Nessun nuovo simbolo: composizione con pannelli e frecce esistenti. Rendering ispezionato; build e 12 test superati.

## Esempio minimo collegato ai registri

Su richiesta del docente, il percorso per immagini include ora una funzione C di due assegnamenti e sei istruzioni assembly commentate. Usa RDI per il puntatore e RAX per il dato; RIP e RSP sono spiegati in relazione alla ripresa e al ritorno. Una tabella collega il risultato 23 nel registro al valore ancora 20 in memoria mostrato nella figura. Le immagini restano invariate.

## Posizione di RSP nella chiamata

La figura `01-chiamata-stack` accompagna la funzione C `somma`, chiamata da `main`: tre variabili int con a = 2, b = 3 e c = 5. Mostra 12 byte locali e 8 byte per l'indirizzo di ritorno illustrativo 0x401025. Le frecce di RSP indicano 0x1000 prima della chiamata, 0x0FEC durante somma e 0x1000 dopo il ritorno. Il testo esplicita il passaggio intermedio a 0x0FF8 e distingue gli indirizzi delle celle dal loro contenuto. La disposizione resta didattica, non un layout garantito dal compilatore. Rendering ispezionato; build e 12 test superati.

## Problema iniziale: sensore, socket e interfaccia

Due figure sostituiscono gli schemi ASCII: [I/O sequenziale](../assets/tpsi4/01-io-sequenziale.svg) mostra una linea temporale con attese illustrative di 800 e 1200 ms; [I/O concorrente](../assets/tpsi4/01-io-concorrente.svg) separa acquisizione, invio e interfaccia, con coda di misure e ultimo valore disponibile. Le attese dipendono da dati non ancora disponibili o dal buffer di invio pieno. Il testo distingue attesa da calcolo, spiega la concorrenza anche su un core e introduce il limite della coda. Riutilizzati pannelli, frecce e simboli del sistema grafico.

Entrambe le immagini sono state renderizzate con Chrome e ispezionate. Build deterministica, sette test grafici e cinque test di formattazione superati; i test grafici hanno richiesto una riesecuzione fuori dalla sandbox per accesso negato alla cartella temporanea. Riferimenti tecnici: [read(2)](https://man7.org/linux/man-pages/man2/read.2.html) e [send(2)](https://man7.org/linux/man-pages/man2/send.2.html).

## PCB e introduzione alla paginazione

La figura [PCB](../assets/tpsi4/01-pcb.svg) mostra una scheda concettuale con identificatori, pianificazione, contesto salvato, credenziali e riferimenti a relazioni, memoria e descrittori. Le frecce distinguono i riferimenti dalle strutture collegate. Il testo precisa che non si tratta del layout di Linux e distingue le risorse del processo dal contesto dei thread. Il paragrafo sullo spazio di indirizzamento parte dalla scheda e introduce le tabelle delle pagine e la paginazione. Riferimento: [Linux Page Tables](https://docs.kernel.org/mm/page_tables.html). Nessun nuovo simbolo necessario. Rendering ispezionato; build e 12 test superati.
