# Processi, thread e concorrenza

<!--
content_id: tpsi4-content-processi-concorrenza
status: draft
curriculum_reference: tpsi4-curriculum-hoepli-volume-2
technical_sources:
  - tpsi4-source-linux-programming
transformation: original-course-material
-->

## In questa unità impareremo

<!-- visual-orientation -->
<table align="center">
<tr>
<td>
<details>
<summary>&#129517; <strong>Orientamento della sezione</strong></summary>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#128506;</span> Contesto:</strong>
Costruisce il modello concettuale di processo, thread, risorsa, concorrenza e parallelismo, collegandolo alle sezioni operative della dispensa Linux.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#128736;</span> Prerequisiti:</strong>
C intermedio, compilazione, memoria, funzioni e puntatori di base.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#127919;</span> Obiettivi:</strong>
Distinguere programma/processo/thread, descrivere ciclo di vita e risorse, usare fork/exec/wait in esempi controllati e confrontare POSIX e Java.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#128257;</span> Richiamo:</strong>
Riprendere processo di compilazione, spazio di memoria e gestione degli errori.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#128064;</span> Anticipazione:</strong>
Prepara IPC, race condition, mutex, semafori, condition e problemi classici.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#10145;</span> Prossimo passo:</strong>
Svolgere esercizi A-D e avviare il laboratorio fork/pipe.
</p>

<p align="justify">
<strong><span style="font-size: 1.15em;">&#128279;</span> Rimando:</strong>
Modulo originale e heading pertinenti di LINUX_PROGRAMMING.md, esclusa Controllo dei processi. <a href="#fonti-e-note-di-revisione">Fonti e note della lezione</a>; <a href="COVERAGE.md">matrice di copertura</a>.
</p>

</details>
</td>
</tr>
</table>

<p align="justify">Al termine dell'unità lo studente dovrà saper:</p>

<ul>
  <li>distinguere programma, processo e thread;</li>
  <li>descrivere lo stato essenziale di un processo;</li>
  <li>spiegare che cosa sono gli otto elementi associati a un processo, come sono organizzati e perché servono;</li>
  <li>riconoscere risorse private e risorse condivise;</li>
  <li>distinguere esecuzione sequenziale, concorrente e parallela;</li>
  <li>leggere una semplice gerarchia padre-figlio;</li>
  <li>spiegare il ruolo di <code>fork</code>, <code>exec</code> e <code>wait</code> in un sistema POSIX;</li>
  <li>confrontare processi Linux, thread POSIX e thread Java;</li>
  <li>descrivere una computazione concorrente attraverso eventi, possibili interleaving e invarianti;</li>
  <li>individuare i primi rischi dovuti alla condivisione dello stato.</li>
</ul>

## Prerequisiti

<p align="justify">Sono richiesti:</p>

<ul>
  <li>funzioni e passaggio di parametri in C;</li>
  <li>array, stringhe e strutture;</li>
  <li>puntatori di base;</li>
  <li>compilazione ed esecuzione da terminale;</li>
  <li>valore di ritorno di <code>main</code>;</li>
  <li>concetti essenziali di sistema operativo, memoria e file.</li>
</ul>

<p align="justify">Per la traccia Java sono utili classi, metodi, oggetti e gestione delle eccezioni.</p>

## Problema iniziale: una sola attività o più attività coordinate?

<p align="justify">Immaginiamo un'applicazione che deve acquisire dati da un sensore, salvarli e aggiornare una schermata. Una soluzione puramente sequenziale svolge le operazioni una dopo l'altra:</p>

```text
leggi il sensore
salva il dato
aggiorna la schermata
ripeti
```

<p align="justify">Questa soluzione è semplice, ma un'operazione lenta può bloccare le altre. Se il salvataggio richiede tempo, la lettura del sensore potrebbe avvenire in ritardo. Una soluzione concorrente separa le responsabilità:</p>

```text
attività A: acquisisce i dati
attività B: salva i dati
attività C: aggiorna l'interfaccia
```

<p align="justify">La difficoltà non consiste soltanto nell'avviare più attività. Bisogna decidere:</p>

<ul>
  <li>quali dati possono essere condivisi;</li>
  <li>quando una attività deve aspettarne un'altra;</li>
  <li>come comunicano;</li>
  <li>cosa accade se una termina o fallisce;</li>
  <li>quali proprietà devono restare vere in qualunque ordine di esecuzione.</li>
</ul>

<p align="justify">Questi problemi collegano il modello a processi, i thread e la sincronizzazione.</p>

## Dal programma al processo

<table align="center">
<tr><td>
<p align="justify">
<strong><span style="font-size: 1.15em;">&#128214;</span> Definizione:</strong>
Un <strong>programma</strong> è una descrizione passiva: un file eseguibile o un insieme di istruzioni memorizzate. Un <strong>processo</strong> è un'esecuzione attiva di quel programma, con uno stato che cambia nel tempo.</p>
</td></tr>
</table>

<p align="justify">Lo stesso programma può essere eseguito in più processi. Se apriamo due terminali e avviamo due volte lo stesso comando, il codice del programma è lo stesso, ma le due esecuzioni hanno identificatori, memoria e risorse proprie.</p>

<p align="justify">Per gestire un'esecuzione, il sistema operativo deve poter rispondere a otto domande. Gli elementi elencati qui sono una mappa del percorso: li costruiremo uno alla volta nella sezione <a href="#anatomia-di-un-processo">Anatomia di un processo</a>.</p>

<ul>
  <li><strong>Quale esecuzione?</strong> Un identificatore.</li>
  <li><strong>Da dove riprendere il lavoro?</strong> Un contesto di esecuzione.</li>
  <li><strong>Quali indirizzi di memoria può usare?</strong> Uno spazio di indirizzamento.</li>
  <li><strong>Dove conservare chiamate e dati dinamici?</strong> Stack e heap.</li>
  <li><strong>Quali risorse ha aperto?</strong> File e altri oggetti aperti.</li>
  <li><strong>Per conto di chi agisce e che cosa può fare?</strong> Credenziali e controlli dei permessi.</li>
  <li><strong>Può avanzare e quando riceverà la CPU?</strong> Stato di pianificazione.</li>
  <li><strong>Chi lo ha creato e con chi è collegato?</strong> Relazioni con altri processi.</li>
</ul>

<p align="justify">Nel modello Linux un processo è identificato da un <strong>PID</strong>. La relazione con il processo che lo ha creato è rappresentata dal <strong>PPID</strong>.</p>

<p align="justify">Collegamenti alla fonte tecnica:</p>

<ul>
  <li><a href="../../LINUX_PROGRAMMING.md#processi">Processi</a></li>
  <li><a href="../../LINUX_PROGRAMMING.md#process-ids">Process IDs</a></li>
  <li><a href="../../LINUX_PROGRAMMING.md#vedere-i-processi-attivi">Vedere i processi attivi</a></li>
</ul>

<!-- figure:01-programma-processi -->
<p align="center">
  <img src="../../assets/tpsi4/01-programma-processi.svg" alt="Lo stesso eseguibile avvia due processi con PID diversi e spazi di memoria distinti." width="960">
</p>
<p align="center"><em>Lo stesso eseguibile avvia due processi con PID diversi e spazi di memoria distinti.</em></p>

## Anatomia di un processo

<p align="justify">Seguiamo una sola esecuzione dell'applicazione iniziale: legge campioni da un sensore, calcola una media e salva i risultati in <code>misure.txt</code>. Mentre aspetta un campione, il computer deve poter eseguire anche altri programmi. Quando il campione arriva, l'applicazione deve riprendere con i propri dati, nel punto giusto e con il file ancora disponibile. Il solo file eseguibile non contiene queste informazioni: descrive le istruzioni, ma non la situazione raggiunta da questa particolare esecuzione.</p>

<table align="center">
<tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128214;</span> Che cosa significa “il processo possiede”:</strong> significa che una risorsa o un'informazione è associata a quell'esecuzione. Non significa che tutto sia dentro la sua memoria o che ogni risorsa sia esclusivamente sua. Il <strong>kernel</strong>, la parte del sistema operativo che gestisce processi e risorse, conserva strutture di controllo con valori e riferimenti. I manuali chiamano spesso questo modello <strong>PCB</strong> (<em>Process Control Block</em>): una scheda di gestione del processo. In un sistema reale le informazioni possono essere distribuite fra più strutture collegate.</p>
</td></tr>
</table>

<p align="justify">Distinguiamo quindi tre posti: la memoria accessibile al programma, le strutture protette del kernel e i registri fisici della CPU. Per ora immaginiamo un processo con un solo flusso di esecuzione. Quando introdurremo i thread, distingueremo le risorse del processo dal contesto e dallo stack di ciascun thread.</p>

### 1. Identificatore: distinguere questa esecuzione

<p align="justify">Avviamo due copie dell'applicazione, una per il sensore dell'aula e una per quello del laboratorio. Hanno lo stesso nome e lo stesso codice: per indicare quale interrompere o osservare, il nome non basta. Il <strong>PID</strong> (<em>Process ID</em>) è il numero con cui il sistema identifica un processo. Per esempio, le due esecuzioni potrebbero avere PID <code>4100</code> e <code>4101</code>; sono valori illustrativi, assegnati dal sistema e non scelti nel sorgente.</p>

<p align="justify">Il PID è registrato nelle strutture del kernel. Un programma Linux può conoscere il proprio con <code>getpid()</code>; gli strumenti di osservazione lo mostrano per collegare ogni riga a un'esecuzione precisa. È necessario perché richieste come “mostra lo stato” o “invia un segnale” devono avere un destinatario. Il numero può essere riutilizzato dopo che il vecchio processo è stato rimosso: non è un'identità permanente. In Linux l'unicità si riferisce allo spazio di identificatori, o <em>PID namespace</em>, in cui si osservano i processi.</p>

### 2. Contesto di esecuzione: riprendere senza ricominciare

<p align="justify">Supponiamo che l'applicazione venga sospesa mentre somma i campioni. Conservare soltanto l'array non basta: bisogna ricordare anche a quale istruzione è arrivata e quali valori intermedi sta usando. Il <strong>contesto di esecuzione</strong> è l'insieme delle informazioni necessarie a riprendere quel flusso di istruzioni.</p>

<ul>
  <li>Il <strong>contatore di programma</strong>, detto anche <em>program counter</em> o <em>instruction pointer</em>, indica la posizione dell'esecuzione nel codice macchina. Non è il numero di riga del sorgente C: una riga può produrre più istruzioni o essere trasformata dal compilatore.</li>
  <li>I <strong>registri</strong> sono piccole memorie interne alla CPU: contengono operandi, indirizzi e risultati intermedi. Per esempio, durante una somma possono contenere un campione e il totale parziale.</li>
  <li>Lo <strong>stack pointer</strong> è un registro che individua la posizione corrente nello stack. Altri registri conservano informazioni di controllo, come gli esiti dei confronti.</li>
</ul>

<p align="justify">I registri fisici appartengono alla CPU. Quando il kernel sospende un'esecuzione, salva i valori necessari in memoria; prima di riprenderla li ripristina. Il processo possiede dunque il proprio <strong>stato dei registri</strong>, non una CPU personale. Se ripristinassimo i valori dell'altra applicazione, potremmo sommare il campione sbagliato o tornare nel punto sbagliato. Questo è il motivo del cambio di contesto, che riprenderemo nella sezione sul ciclo di vita. Non comporta copiare tutta la memoria del processo a ogni passaggio.</p>

<p align="justify">Dopo aver chiarito spazio di indirizzamento, stack e heap, renderemo concreto questo modello con <a href="#dal-c-ai-registri-intel-x86-64">un esempio C e assembly su Intel x86-64</a>. Vedremo i nomi dei registri e seguiremo una sospensione fra due istruzioni.</p>

### 3. Spazio di indirizzamento: gli indirizzi che il programma vede

<p align="justify">Un indirizzo permette di individuare una posizione di memoria. Lo <strong>spazio di indirizzamento virtuale</strong> è l'insieme degli indirizzi che un processo può rappresentare; soltanto alcune sue regioni sono effettivamente mappate e accessibili. Fra queste troviamo il codice eseguibile, i dati globali, le librerie e le aree usate per stack e allocazioni dinamiche. Non immaginiamolo come un unico blocco di RAM già riservato interamente al programma.</p>

<p align="justify">Il sistema operativo organizza le mappature e le protezioni; l'hardware di gestione della memoria, la <strong>MMU</strong>, traduce gli indirizzi virtuali usando tabelle predisposte dal kernel. La memoria viene gestita in unità chiamate <strong>pagine</strong>. Per ogni accesso conta anche l'operazione richiesta: una regione può essere leggibile, scrivibile oppure eseguibile, secondo le sue protezioni.</p>

<p align="justify">Perché lo spazio è associato al processo? La variabile <code>media</code> dell'aula deve poter essere distinta da quella del laboratorio. Anche se due processi usassero lo stesso valore numerico di indirizzo, le rispettive traduzioni potrebbero condurre a memorie fisiche diverse. Un puntatore di un processo non permette quindi, da solo, di leggere la variabile dell'altro. Il sistema può anche predisporre pagine condivise: la condivisione dipende dalle mappature, non dall'uguaglianza dei numeri. Gli indirizzi effettivi possono cambiare fra esecuzioni.</p>

### 4. Stack e heap: due esigenze diverse nella stessa memoria

<p align="justify">All'interno dello spazio di indirizzamento servono organizzazioni adatte a durate diverse. Una chiamata di funzione deve ricordare come tornare al chiamante; un insieme di campioni può invece dover rimanere disponibile anche dopo il ritorno dalla funzione che lo ha allocato.</p>

<p align="justify">Lo <strong>stack</strong> è organizzato come una pila: l'ultima chiamata aperta è la prima a concludersi. Nel modello usuale, ogni chiamata dispone di un <strong>record di attivazione</strong>, o <em>stack frame</em>, con informazioni utili alla sua esecuzione e al ritorno. Può contenere variabili locali, valori salvati e informazioni di collegamento; la disposizione concreta dipende dall'architettura, dalle convenzioni di chiamata e dalle ottimizzazioni. Alcuni valori possono restare nei registri.</p>

```text
main chiama acquisisci, che chiama converti

frame di converti    <- chiamata più recente
frame di acquisisci
frame di main

converti termina: si torna ad acquisisci
acquisisci termina: si torna a main
```

<p align="justify">Anche due chiamate ricorsive della stessa funzione devono conservare separatamente il proprio stato. Quando una funzione termina, i suoi oggetti locali automatici cessano di esistere: restituire l'indirizzo di uno di essi non ne prolunga la durata.</p>

<p align="justify">L'<strong>heap</strong> indica, nel modello didattico, la memoria gestita con allocazioni dinamiche. Il programma chiede un blocco della dimensione necessaria, ottiene un puntatore e lo usa finché lo rilascia. In C si impiegano funzioni come <code>malloc</code> e <code>free</code>; l'allocatore gestisce blocchi occupati e liberi e richiede memoria al sistema quando serve. L'ordine di rilascio non deve seguire quello delle chiamate di funzione. In Linux le allocazioni possono usare anche mappature distinte dalla regione etichettata <code>[heap]</code>.</p>

```c
/* Frammento dentro una funzione; richiede <stdlib.h>. */
int *campioni = malloc(100 * sizeof *campioni);
if (campioni != NULL) {
    campioni[0] = 23;
    /* Qui si possono acquisire ed elaborare gli altri campioni. */
    free(campioni);
    campioni = NULL;
}
```

<p align="justify">La variabile locale <code>campioni</code> contiene un indirizzo; il blocco per cento interi è un oggetto diverso. Nel disegno semplificato il puntatore è nello stack e il blocco nell'heap, anche se il compilatore può tenere il puntatore in un registro. Il fallimento dell'allocazione è segnalato da <code>NULL</code>. Perdere l'unico puntatore senza liberare il blocco causa una perdita di memoria; usare il blocco dopo <code>free</code> è un errore. Stack e heap appartengono al processo perché sostengono le sue chiamate e i suoi dati; con più thread, ciascuno avrà il proprio stack, mentre l'heap sarà normalmente condiviso.</p>

### Dal C ai registri Intel x86-64

<p align="justify">Scegliamo come riferimento una CPU <strong>Intel in modalità a 64 bit (x86-64)</strong> con Linux. Le regole per passare argomenti e risultati alle funzioni sono quelle della <strong>System V AMD64 ABI</strong>: un accordo fra codice chiamante e chiamato. Il nome AMD64 identifica qui l'ABI usata anche sulle CPU Intel compatibili. L'architettura definisce le istruzioni disponibili; l'ABI stabilisce come usarle per far collaborare le funzioni. Su Windows le convenzioni di chiamata sono diverse.</p>

#### Il percorso dal sorgente alla CPU

```text
contesto.c  -> compilatore -> assembly -> assemblatore -> file oggetto
                                                        |
                           eseguibile <- linker e librerie
```

<p align="justify">Il compilatore traduce operazioni C in operazioni della macchina; l'assembly ne rende leggibili istruzioni e operandi. L'assemblatore le codifica in byte, mentre il linker collega il codice con le parti necessarie di altri moduli e librerie. La CPU esegue il <strong>codice macchina</strong>, non il testo C né il testo assembly. Possiamo chiedere al compilatore di fermarsi all'assembly per osservare la traduzione. Le ottimizzazioni possono modificarla: una variabile C non ha necessariamente un posto fisso in memoria e una chiamata può essere sostituita dal codice della funzione.</p>

#### I registri da riconoscere

<p align="justify">Un registro a 64 bit conserva un valore di 64 bit: può essere un numero oppure un indirizzo, secondo l'uso dell'istruzione. Ecco i nomi necessari per leggere l'esempio. I ruoli relativi ad argomenti e risultati dipendono dall'ABI scelta.</p>

<table align="center">
<thead><tr><th>Registro</th><th>Ruolo nel nostro modello</th><th>Perché interessa alla ripresa</th></tr></thead>
<tbody>
<tr><td><code>RIP</code></td><td>Posizione dell'esecuzione nel codice macchina.</td><td>Individua l'istruzione da cui proseguire.</td></tr>
<tr><td><code>RSP</code></td><td>Puntatore alla cima corrente dello stack.</td><td>Individua lo stack su cui continuare a lavorare.</td></tr>
<tr><td><code>RBP</code></td><td>Può essere usato come riferimento stabile del frame corrente.</td><td>Permette di ritrovare i dati del frame quando il codice lo usa così; il compilatore può anche usarlo diversamente.</td></tr>
<tr><td><code>RAX</code></td><td>Registro generale, usato anche per restituire interi e puntatori.</td><td>Può contenere un risultato ancora da utilizzare.</td></tr>
<tr><td><code>RDI, RSI, RDX, RCX, R8, R9</code></td><td>Primi sei argomenti interi o puntatori delle chiamate ordinarie nell'ABI scelta.</td><td>Possono contenere parametri, indirizzi o valori intermedi.</td></tr>
<tr><td><code>RBX, R10–R15</code></td><td>Altri registri generali.</td><td>Possono conservare stato del calcolo: non sono irrilevanti perché l'esempio ne usa pochi.</td></tr>
<tr><td><code>RFLAGS</code></td><td>Contiene flag di stato e controllo; per esempio <code>ZF</code> indica un risultato nullo.</td><td>Un salto condizionato deve ritrovare l'esito del confronto precedente.</td></tr>
<tr><td><code>CR3</code></td><td>Registro privilegiato che individua la radice delle tabelle delle pagine, con ulteriori campi di controllo.</td><td>Il kernel deve attivare le traduzioni di memoria corrette quando cambia spazio di indirizzamento.</td></tr>
</tbody>
</table>

<p align="justify"><code>EAX</code>, <code>EDI</code> ed <code>ESI</code> sono i nomi delle parti basse a 32 bit di <code>RAX</code>, <code>RDI</code> e <code>RSI</code>. Non sono altri registri indipendenti. Nei nostri esempi un <code>int</code> occupa 32 bit, un puntatore 64 bit; scrivere in <code>EAX</code> azzera anche i 32 bit alti di <code>RAX</code>. Il contesto reale comprende inoltre altro stato architetturale, per esempio quello dei calcoli in virgola mobile e vettoriali: questa tabella seleziona ciò che serve al primo esempio.</p>

#### Un programma C piccolo e completo

<p align="justify">Salva questo sorgente come <code>contesto.c</code>. La funzione riceve un puntatore e un incremento: legge il numero puntato, calcola il risultato e lo scrive nella stessa posizione. <code>main</code> alloca quel numero dinamicamente, chiama la funzione e libera il blocco.</p>

```c
#include <stdlib.h>

void incrementa(int *p, int delta)
{
    int nuovo = *p + delta;
    *p = nuovo;
}

int main(void)
{
    int *p = malloc(sizeof *p);
    if (p == NULL) {
        return 1;
    }
    *p = 20;
    incrementa(p, 3);
    int esito = (*p == 23) ? 0 : 2;
    free(p);
    return esito;
}
```

<p align="justify">Su Linux x86-64 con GCC, questi comandi producono prima l'assembly e poi l'eseguibile. <code>-S</code> si ferma prima dell'assemblaggio, <code>-masm=intel</code> sceglie la sintassi Intel, <code>-O0</code> evita le normali ottimizzazioni e <code>-fno-omit-frame-pointer</code> facilita il riconoscimento dei frame. Il programma non stampa: il codice di uscita atteso è <code>0</code> in caso di successo.</p>

```bash
gcc -std=c11 -Wall -Wextra -O0 -fno-omit-frame-pointer -masm=intel -S contesto.c -o contesto.s
gcc -std=c11 -Wall -Wextra -O0 -g contesto.c -o contesto
./contesto
echo $?
```

<p align="justify">Leggiamo prima una <strong>traduzione didattica compatta</strong> del corpo di <code>incrementa</code>. È assembly x86-64 in sintassi Intel, ma non è presentato come l'output esatto di GCC con quei comandi: il file generato può contenere frame, copie aggiuntive e direttive. In questa sintassi si scrive prima la destinazione, poi la sorgente; le parentesi quadre significano “accedi alla memoria all'indirizzo indicato”.</p>

```asm
# All'ingresso: RDI = p; ESI = delta
incrementa:
    mov eax, DWORD PTR [rdi]  # leggi l'int puntato da p
    add eax, esi              # somma delta al valore letto
    mov DWORD PTR [rdi], eax  # scrivi il risultato nello stesso int
    ret                       # torna al chiamante
```

<p align="justify"><code>DWORD PTR</code> indica un accesso di 4 byte. Se <code>RDI</code> contiene l'indirizzo del blocco inizializzato a <code>20</code> ed <code>ESI</code> vale <code>3</code>, la prima istruzione mette <code>20</code> in <code>EAX</code>, la seconda lo porta a <code>23</code> e la terza aggiorna il blocco in memoria. La variabile C <code>nuovo</code> non richiede qui uno spazio nello stack: il risultato passa attraverso <code>EAX</code>.</p>

#### Chiamata, ritorno e stack: che cosa fanno CALL e RET

<p align="justify">Prima della chiamata, il chiamante prepara il puntatore in <code>RDI</code> e l'incremento in <code>ESI</code>. Una normale <code>call incrementa</code> salva sullo stack l'indirizzo dell'istruzione successiva alla chiamata e trasferisce il controllo alla funzione. Nel nostro caso a 64 bit, questo salvataggio riduce <code>RSP</code> di 8 byte: lo stack cresce verso indirizzi minori. <code>ret</code> recupera quell'indirizzo e riporta <code>RSP</code> avanti di 8 byte.</p>

```text
Prima di CALL:          RSP = S
Dopo CALL:             RSP = S - 8; [RSP] = indirizzo di ritorno
Dopo RET:              RSP = S;     esecuzione ripresa nel chiamante
```

<p align="justify">Quando serve un frame esplicito, possiamo incontrare una sequenza come questa. È uno schema distinto dal corpo compatto precedente: mostra soltanto apertura e chiusura del frame, non una seconda funzione completa.</p>

```asm
push rbp          # RSP -= 8; salva il vecchio RBP nello stack
mov rbp, rsp      # fissa il riferimento del nuovo frame
sub rsp, 16       # riserva 16 byte per dati locali o temporanei
# ... corpo della funzione; per esempio un int in [rbp-4] ...
mov rsp, rbp      # abbandona lo spazio locale riservato
pop rbp           # recupera il riferimento del chiamante
ret               # recupera l'indirizzo di ritorno
```

<p align="justify">Qui <code>[rbp-4]</code> è un indirizzo calcolato sottraendo 4 al contenuto di <code>RBP</code>. I byte locali rimangono fisicamente in memoria finché non vengono sovrascritti, ma dopo il ritorno non sono più oggetti locali validi di quella chiamata. L'ABI impone anche regole di allineamento dello stack, rispettate dal codice generato dal compilatore.</p>

#### Dove sono codice, stack e heap

```text
CPU                         spazio virtuale del processo
RIP ----------------------> codice: mov, add, call, ret...
RSP ----------------------> stack: frame e indirizzi di ritorno
RBP ----------------------> riferimento del frame, se utilizzato
RDI (p nell'esempio) ------> blocco dinamico: [ int 20, poi 23 ]

CR3 -> tabelle delle pagine -> traduzione verso la memoria fisica
```

<p align="justify">Il disegno mostra collegamenti, non l'ordine delle regioni né una scala di indirizzi. Codice, dati globali, stack, allocazioni dinamiche e librerie occupano regioni virtuali; le traduzioni stabiliscono quali pagine fisiche corrispondono a quelle regioni. Non esiste un “registro heap” equivalente a <code>RSP</code>: gli indirizzi dei blocchi possono stare nei registri, nello stack, in variabili globali o in altri blocchi.</p>

<p align="justify">Quando <code>malloc</code> riesce, il puntatore restituito passa per <code>RAX</code> secondo l'ABI; il chiamante deve conservarlo dove necessario. <code>free</code> riceve quel puntatore come argomento. Quindi <strong>i registri permettono di raggiungere e manipolare gli oggetti; non contengono l'intero stack o l'intero heap</strong>. Preservare gli indirizzi senza mantenere valide le relative mappature e i dati non sarebbe sufficiente per riprendere il programma.</p>

### 5. File e altri oggetti aperti: riferimenti alle risorse

<p align="justify">Per salvare una media, l'applicazione deve aprire <code>misure.txt</code>. In Linux un <strong>descrittore di file</strong> è un piccolo intero che seleziona una voce della tabella dei descrittori del processo. La voce rimanda a strutture del kernel che rappresentano l'apertura e, per un file ordinario, conservano informazioni come posizione corrente e modalità di accesso. Il contenuto del file non diventa automaticamente una parte della memoria privata del processo.</p>

```text
processo A                    kernel                    risorsa
descrittore 3  ---------->  apertura del file  ------->  misure.txt
                           posizione, modalità
```

<p align="justify">Lo stesso meccanismo permette di riferirsi anche a pipe, terminali e socket. Per convenzione, <code>0</code>, <code>1</code> e <code>2</code> sono ingresso standard, uscita standard ed errori standard; possono essere rediretti. Il numero <code>3</code> in due processi non identifica necessariamente la stessa risorsa, perché ogni numero va interpretato nella relativa tabella. Viceversa, due descrittori possono riferirsi alla stessa apertura. Chiudere un descrittore rimuove quel riferimento: non significa cancellare il file.</p>

<p align="justify">Nell'esempio del sensore, ricordare il descrittore consente di continuare a scrivere sul file già aperto dopo una sospensione. Quando usiamo <code>fopen</code> in C, lavoriamo invece con un <code>FILE *</code>: un oggetto della libreria che aggiunge gestione del flusso e buffering sopra il descrittore.</p>

### 6. Credenziali e permessi: identità e autorizzazione

<p align="justify">Il PID distingue un'esecuzione; non dice per conto di quale utente essa agisca. Le <strong>credenziali</strong> sono informazioni di identità associate al processo, fra cui identificatori di utente (<strong>UID</strong>) e gruppo (<strong>GID</strong>) e gruppi supplementari. Il kernel le usa nei controlli di accesso. Più processi dello stesso utente possono quindi avere PID diversi e le stesse credenziali.</p>

<p align="justify">I <strong>permessi</strong> esprimono operazioni consentite sulle risorse. Per un file, per esempio, distinguiamo lettura, scrittura ed esecuzione per proprietario, gruppo e altri utenti. Il kernel confronta le credenziali con le regole applicabili all'operazione richiesta. I permessi di <code>misure.txt</code> sono proprietà della risorsa: non sono tutti contenuti nella scheda del processo.</p>

<p align="justify">Se l'applicazione può leggere il file ma non aprirlo in scrittura, conoscere il percorso non basta a ottenere il permesso. Linux distingue anche identità reali ed effettive; nei casi ordinari coincidono, mentre i dettagli dei controlli includono ulteriori meccanismi. Qui ci interessa la separazione: identificare il processo, identificare l'utente e autorizzare un'operazione sono tre problemi diversi.</p>

### 7. Stato di pianificazione: poter avanzare e ottenere la CPU

<p align="justify">La <strong>pianificazione</strong>, o <em>scheduling</em>, decide quale attività pronta eseguire sulle CPU disponibili. Il kernel conserva lo stato dell'attività e informazioni utili alla scelta, come politica e priorità di pianificazione. Le attività pronte sono organizzate in strutture che permettono allo <strong>scheduler</strong>, il componente incaricato della scelta, di individuarle.</p>

<p align="justify">Riprendiamo l'applicazione: mentre calcola la media è <strong>in esecuzione</strong>; se potrebbe continuare ma la CPU esegue altro, è <strong>pronta</strong>; se una lettura bloccante aspetta un campione non ancora disponibile, è <strong>in attesa</strong>. Nel terzo caso assegnarle tempo di CPU non risolverebbe la mancanza del dato. All'arrivo del campione torna pronta e attende di essere selezionata.</p>

<p align="justify">Questo stato appartiene alla singola attività perché due esecuzioni dello stesso programma possono trovarsi in condizioni diverse. Non va confuso con il contatore di programma: quello indica dove riprendere; lo stato indica se si può riprendere e se si sta già eseguendo. Il diagramma successivo rappresenta proprio queste transizioni. Linux pianifica i singoli thread: il modello a un solo flusso ci permette per ora di parlare di processo pronto o in esecuzione.</p>

### 8. Relazioni con altri processi: origine e coordinamento

<p align="justify">Quando avviamo l'applicazione da una shell, entra in gioco una relazione di creazione: un processo può creare un <strong>figlio</strong> e diventare il suo <strong>padre</strong>. Il <strong>PPID</strong> è l'identificatore del padre. Questi collegamenti permettono di rappresentare i processi come un albero; non indicano che la memoria del figlio sia contenuta in quella del padre.</p>

<p align="justify">Immaginiamo che l'applicazione affidi l'esportazione delle misure a un figlio. Il padre può continuare un'altra attività e poi raccoglierne l'esito con <code>wait</code> o <code>waitpid</code>. Il kernel deve ricordare la relazione per gestire questa attesa e conservare le informazioni di terminazione necessarie. La parentela non sincronizza automaticamente ogni operazione: se i due devono scambiarsi campioni, serve un meccanismo di comunicazione.</p>

<p align="justify">Esistono anche <strong>gruppi di processi</strong> e <strong>sessioni</strong>, usati fra l'altro dalla shell per gestire lavori e terminali. Non sono gruppi di utenti: descrivono un'altra relazione. Approfondiremo la creazione con <code>fork</code> e l'attesa nelle sezioni operative; per ora ricordiamo che un processo ha sia uno stato individuale sia legami che il sistema deve amministrare.</p>

### Ricomporre il modello

<p align="justify">Proviamo ora a sospendere idealmente l'applicazione e a descrivere ciò che rimane. Questa tabella collega ogni domanda al posto in cui cercare la risposta; è un modello concettuale, non il layout di una singola struttura del kernel.</p>

<table align="center">
<thead><tr><th>Domanda</th><th>Elemento</th><th>Organizzazione essenziale</th></tr></thead>
<tbody>
<tr><td>Quale esecuzione?</td><td>PID</td><td>Identificatore registrato dal kernel.</td></tr>
<tr><td>Da dove riprende?</td><td>Contesto</td><td>Valori dei registri attivi nella CPU o salvati in memoria.</td></tr>
<tr><td>Quali indirizzi vede?</td><td>Spazio di indirizzamento</td><td>Regioni virtuali, mappature e protezioni.</td></tr>
<tr><td>Come conserva chiamate e dati?</td><td>Stack e heap</td><td>Record di attivazione e blocchi allocati dinamicamente.</td></tr>
<tr><td>Su quali risorse opera?</td><td>Oggetti aperti</td><td>Descrittori che rimandano a strutture del kernel.</td></tr>
<tr><td>Per conto di chi agisce?</td><td>Credenziali</td><td>Identità usate insieme alle regole di accesso delle risorse.</td></tr>
<tr><td>Può avanzare adesso?</td><td>Stato di pianificazione</td><td>Stato e informazioni gestite dallo scheduler.</td></tr>
<tr><td>Con chi è collegato?</td><td>Relazioni</td><td>Padre, figli, gruppi di processi e sessioni.</td></tr>
</tbody>
</table>

<p align="justify"><strong><span style="font-size: 1.15em;">&#10067;</span> Fermati e ragiona:</strong> rispondi motivando, prima di aprire le soluzioni.</p>

<ol>
  <li>Due esecuzioni dello stesso programma devono avere la stessa media e gli stessi file aperti?</li>
  <li>Se salviamo l'array dei campioni ma perdiamo il contesto, possiamo riprendere con certezza dal punto corretto?</li>
  <li>La fine di una funzione libera automaticamente un blocco ottenuto con <code>malloc</code>?</li>
  <li>Un processo che aspetta un campione e uno che aspetta soltanto la CPU si trovano nello stesso stato?</li>
  <li>Conoscere il PID di un altro processo o il nome di un file concede automaticamente il diritto di usarli?</li>
</ol>

<details>
<summary>Confronta le risposte</summary>
<ol>
  <li>No: il codice comune non impone dati uguali o aperture uguali; le esecuzioni hanno una propria storia.</li>
  <li>No: mancano la posizione nel codice e i valori intermedi necessari alla ripresa.</li>
  <li>No: la durata del blocco allocato è distinta da quella della variabile locale che ne contiene l'indirizzo; bisogna gestirne il rilascio.</li>
  <li>No: il primo è in attesa di un evento, il secondo è pronto.</li>
  <li>No: un identificatore individua una risorsa o un'esecuzione; l'autorizzazione dipende da controlli separati.</li>
</ol>
</details>

## Stato e ciclo di vita di un processo

<p align="justify">Per ragionare sul sistema operativo è utile un modello semplificato a stati:</p>

<ul>
  <li><strong>Nuovo</strong>: il sistema sta creando le strutture necessarie.</li>
  <li><strong>Pronto</strong>: il processo può essere eseguito, ma aspetta la CPU.</li>
  <li><strong>In esecuzione</strong>: sta usando un processore.</li>
  <li><strong>In attesa</strong>: non può proseguire finché non avviene un evento, per esempio la disponibilità di dati.</li>
  <li><strong>Terminato</strong>: non esegue più istruzioni; alcune informazioni possono restare temporaneamente disponibili al padre.</li>
</ul>

<p align="justify">Nel diagramma, il completamento dell'evento riporta il processo in stato pronto; lo scheduler decide quando assegnargli la CPU. Il diagramma non descrive tutti i dettagli di un kernel reale. Serve a capire due idee:</p>

<ol>
  <li>un processo pronto non è necessariamente in esecuzione;</li>
  <li>un processo in attesa non deve consumare continuamente la CPU per controllare se l'evento è avvenuto.</li>
</ol>

### Cambio di contesto

<p align="justify">Torniamo alla traduzione compatta di <code>incrementa</code>. Immaginiamo una sospensione <strong>dopo <code>add eax, esi</code> e prima della scrittura in memoria</strong>. Il blocco contiene ancora <code>20</code>, ma <code>EAX</code> contiene già <code>23</code>. Se durante la pausa un altro processo usa <code>EAX</code>, non possiamo ricostruire la situazione conservando soltanto il contenuto dell'heap.</p>

<table align="center">
<thead><tr><th>Informazione di A alla sospensione</th><th>Che cosa deve ritrovare A</th></tr></thead>
<tbody>
<tr><td><code>RIP</code></td><td>L'istruzione <code>mov DWORD PTR [rdi], eax</code>, ancora da eseguire.</td></tr>
<tr><td><code>RAX</code> e <code>RDI</code></td><td>Il risultato <code>23</code> e l'indirizzo a cui scriverlo.</td></tr>
<tr><td><code>RSP</code>, eventuale <code>RBP</code></td><td>Lo stack corretto, compreso l'indirizzo che <code>ret</code> userà.</td></tr>
<tr><td>Altri registri e <code>RFLAGS</code></td><td>Lo stato architetturale necessario a proseguire senza alterare il calcolo.</td></tr>
<tr><td>Memoria e sue traduzioni</td><td>Il codice, lo stack e il blocco ancora contenente <code>20</code>, agli indirizzi attesi.</td></tr>
</tbody>
</table>

<p align="justify">Consideriamo una CPU logica e due processi A e B, ciascuno con un thread. Un'interruzione del timer può portare il controllo al kernel; lo scheduler può decidere di far avanzare B. Il percorso seguente descrive l'effetto complessivo, non una singola istruzione che salva magicamente tutto.</p>

<ol>
  <li><strong>Entrata nel kernel.</strong> La CPU conserva automaticamente una parte dello stato di ritorno dall'interruzione, fra cui posizione e flag; il codice di ingresso del kernel completa il salvataggio dei registri necessari. L'esecuzione privilegiata usa stack del kernel, distinti dallo stack utente illustrato sopra.</li>
  <li><strong>Sospensione di A.</strong> Il kernel mantiene il suo contesto nelle strutture e negli stack associati al thread. Se A è stato soltanto interrotto mentre poteva avanzare, rimane pronto; se aspetta un'operazione bloccante, è in attesa.</li>
  <li><strong>Selezione di B.</strong> Lo scheduler sceglie un'attività pronta. Il codice di cambio passa al contesto di esecuzione nel kernel di B, incluso il relativo stack.</li>
  <li><strong>Memoria corretta.</strong> Se occorre cambiare spazio di indirizzamento, il kernel attiva le traduzioni di B tramite i meccanismi che coinvolgono <code>CR3</code>. Non copia tutto l'heap o tutti i frame di A dentro B. Fra thread dello stesso processo, lo spazio utente è normalmente comune.</li>
  <li><strong>Ripresa di B e successivamente di A.</strong> Il percorso di ritorno ripristina lo stato utente dell'attività scelta. Quando toccherà nuovamente ad A, saranno ricostituiti i suoi valori: la scrittura memorizzerà <code>23</code> nel suo blocco e <code>ret</code> troverà il suo indirizzo di ritorno.</li>
</ol>

<p align="justify">I dettagli dipendono dal percorso di ingresso, dalle funzionalità della CPU e dal kernel: interruzioni e chiamate di sistema non salvano lo stato esattamente nello stesso modo. Entrare nel kernel, inoltre, non implica sempre passare a un altro processo. Il punto comune è preservare il contesto necessario alla ripresa. In Linux x86-64 la gestione è una collaborazione fra hardware e software; non coincide con il solo salvataggio eseguito dalla CPU all'arrivo dell'interruzione.</p>

<table align="center">
<tr><td>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128214;</span> Chiamata di funzione e cambio di contesto:</strong> <code>call</code> e <code>ret</code> operano normalmente nello stesso thread. L'ABI divide i registri fra quelli che la funzione chiamata deve preservare, come <code>RBX</code>, <code>RBP</code> e <code>R12–R15</code>, e quelli che può modificare, come <code>RAX</code> e i registri degli argomenti. Il chiamante protegge gli eventuali valori ancora necessari. Una sospensione può invece avvenire fra istruzioni qualsiasi: il sistema deve preservare lo stato necessario anche dei registri che una normale chiamata potrebbe modificare. Le due operazioni hanno quindi responsabilità diverse.</p>
</td></tr>
</table>

<p align="justify"><strong><span style="font-size: 1.15em;">&#10067;</span> Controlla il modello:</strong> se A riprendesse con <code>RAX</code> di B, quale dato scriverebbe? Se recuperasse <code>RAX</code> ma non il proprio <code>RDI</code>, dove tenterebbe di scriverlo? Se ripristinasse tutti i registri generali ma usasse traduzioni di memoria sbagliate, gli stessi indirizzi avrebbero ancora il significato atteso? Queste tre domande spiegano perché contesto della CPU e contesto della memoria devono essere coerenti.</p>

<p align="justify">Quando il sistema sospende un processo e ne esegue un altro, deve salvare e ripristinare il relativo contesto. Questo lavoro ha un costo. La concorrenza non rende automaticamente un programma più veloce: può migliorare reattività e utilizzo delle risorse, ma introduce anche overhead e complessità.</p>

<!-- figure:01-stati-processo -->
<p align="center">
  <img src="../../assets/tpsi4/01-stati-processo.svg" alt="Nuovo passa a pronto; lo scheduler porta pronto in esecuzione. Attesa di I/O porta in attesa; l&#x27;evento riporta a pronto. La preemption riporta il processo da in esecuzione a pronto; l&#x27;uscita porta a terminato." width="960">
</p>
<p align="center"><em>Nuovo passa a pronto; lo scheduler porta pronto in esecuzione. Attesa di I/O porta in attesa; l&#x27;evento riporta a pronto. La preemption riporta il processo da in esecuzione a pronto; l&#x27;uscita porta a terminato.</em></p>

## Risorse private e risorse condivise

<p align="justify">Una domanda fondamentale è: <strong>quale stato appartiene a una sola attività e quale è visibile a più attività?</strong></p>

<p align="justify">Con processi separati, lo spazio di indirizzamento è normalmente isolato. Dopo una creazione con <code>fork</code>, padre e figlio osservano inizialmente valori equivalenti, ma le modifiche ordinarie alla memoria di uno non diventano automaticamente modifiche nella memoria dell'altro.</p>

<p align="justify">Con più thread nello stesso processo, invece, sono tipicamente condivisi:</p>

<ul>
  <li>variabili globali;</li>
  <li>heap;</li>
  <li>descrittori e oggetti del processo;</li>
  <li>codice eseguibile.</li>
</ul>

<p align="justify">Ogni thread possiede almeno uno stack e un contesto di esecuzione separati.</p>

<table align="center">
<thead>
<tr>
<th>Elemento</th>
<th>Processi distinti</th>
<th>Thread dello stesso processo</th>
</tr>
</thead>
<tbody>
<tr>
<td>spazio di indirizzamento</td>
<td>isolato per impostazione predefinita</td>
<td>condiviso</td>
</tr>
<tr>
<td>stack</td>
<td>separato</td>
<td>separato per thread</td>
</tr>
<tr>
<td>heap</td>
<td>separato</td>
<td>condiviso</td>
</tr>
<tr>
<td>comunicazione</td>
<td>richiede un meccanismo IPC</td>
<td>può usare memoria condivisa</td>
</tr>
<tr>
<td>isolamento dei guasti</td>
<td>maggiore</td>
<td>minore</td>
</tr>
<tr>
<td>costo di coordinamento</td>
<td>spesso maggiore</td>
<td>spesso minore, ma più delicato</td>
</tr>
</tbody>
</table>

<p align="justify">L'isolamento riduce alcuni errori, ma rende necessaria una comunicazione esplicita. La condivisione facilita lo scambio di dati, ma può produrre race condition.</p>

<!-- figure:01-memoria-thread -->
<p align="center">
  <img src="../../assets/tpsi4/01-memoria-thread.svg" alt="Due processi hanno heap separati. Due thread di uno stesso processo condividono heap, globali e descrittori, ma conservano stack e registri propri." width="960">
</p>
<p align="center"><em>Due processi hanno heap separati. Due thread di uno stesso processo condividono heap, globali e descrittori, ma conservano stack e registri propri.</em></p>

## Sequenziale, concorrente e parallelo

<p align="justify">I termini non sono sinonimi.</p>

### Esecuzione sequenziale

<p align="justify">Una sola attività logica avanza alla volta secondo un ordine determinato dal programma.</p>

```text
A1 -> A2 -> A3 -> B1 -> B2
```

### Esecuzione concorrente

<p align="justify">Più attività sono in corso nello stesso intervallo di tempo. Su una sola CPU possono alternarsi:</p>

```text
A1 -> B1 -> A2 -> B2 -> A3
```

<p align="justify">La concorrenza riguarda la struttura e la possibilità di avanzamento indipendente.</p>

### Esecuzione parallela

<p align="justify">Due o più attività eseguono realmente istruzioni nello stesso istante su unità di calcolo diverse.</p>

```text
CPU 1: A1 -> A2 -> A3
CPU 2: B1 -> B2 -> B3
```

<p align="justify">Il parallelismo può aumentare le prestazioni, ma soltanto se il lavoro può essere suddiviso e il costo di comunicazione e sincronizzazione non annulla il beneficio.</p>

### Domanda di controllo

<p align="justify">Un programma con due thread su un computer a singolo core può essere concorrente? Sì. Può alternare i thread anche se non li esegue simultaneamente.</p>

<!-- figure:01-concorrenza-parallelismo -->
<p align="center">
  <img src="../../assets/tpsi4/01-concorrenza-parallelismo.svg" alt="Sequenziale: A termina prima di B. Concorrente su un core: A e B alternano i passi. Parallelo su due core: A e B eseguono passi nello stesso intervallo." width="960">
</p>
<p align="center"><em>Sequenziale: A termina prima di B. Concorrente su un core: A e B alternano i passi. Parallelo su due core: A e B eseguono passi nello stesso intervallo.</em></p>

## Gerarchia dei processi in Linux

<p align="justify">I processi formano relazioni di creazione. Un processo può creare un figlio; il figlio può crearne altri. Per osservare PID, PPID e comando:</p>

```bash
ps -e -o pid,ppid,state,command
```

<p align="justify">Per una vista ad albero, quando disponibile:</p>

```bash
pstree -p
```

<p align="justify">L'albero non implica che il padre controlli ogni istruzione del figlio. Indica una relazione utile per creazione, attesa, ereditarietà di alcune risorse e raccolta dello stato di terminazione.</p>

## Creazione di processi: `fork`, `exec` e `wait`

<p align="justify">In ambiente POSIX tre operazioni hanno ruoli distinti.</p>

### `fork`

<p align="justify"><code>fork()</code> crea un nuovo processo. Dopo la chiamata esistono due flussi che proseguono dall'istruzione successiva:</p>

<ul>
  <li>nel padre, il valore di ritorno è il PID del figlio;</li>
  <li>nel figlio, il valore di ritorno è <code>0</code>;</li>
  <li>in caso di errore, il padre riceve <code>-1</code> e il figlio non viene creato.</li>
</ul>

<p align="justify">La distinzione deve essere controllata esplicitamente.</p>

### `exec`

<p align="justify">La famiglia <code>exec</code> sostituisce il programma eseguito dal processo corrente. Se la chiamata riesce, il codice successivo alla <code>exec</code> non viene eseguito, perché il processo sta eseguendo un nuovo programma.</p>

### `wait` e `waitpid`

<p align="justify">Il padre usa <code>wait</code> o <code>waitpid</code> per attendere o raccogliere lo stato di un figlio. Se il figlio termina e il padre non ne raccoglie lo stato, resta temporaneamente un record chiamato comunemente <strong>zombie</strong>.</p>

<p align="justify">Collegamenti:</p>

<ul>
  <li><a href="../../LINUX_PROGRAMMING.md#creare-un-processo">Creare un processo</a></li>
  <li><a href="../../LINUX_PROGRAMMING.md#fork-exec"><code>fork()</code> e <code>exec()</code></a></li>
  <li><a href="../../LINUX_PROGRAMMING.md#aspettare-la-terminazione-di-un-processo">Aspettare la terminazione di un processo</a></li>
  <li><a href="../../LINUX_PROGRAMMING.md#processi-zombie">Processi zombie</a></li>
</ul>

<!-- figure:01-fork-exec-wait -->
<p align="center">
  <img src="../../assets/tpsi4/01-fork-exec-wait.svg" alt="fork crea un figlio con un PID nuovo; exec cambia il programma del figlio mantenendone il PID; waitpid nel padre raccoglie lo stato dopo la terminazione del figlio." width="960">
</p>
<p align="center"><em>fork crea un figlio con un PID nuovo; exec cambia il programma del figlio mantenendone il PID; waitpid nel padre raccoglie lo stato dopo la terminazione del figlio.</em></p>

## Esempio C originale: padre e figlio con uscita controllata

```c
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void) {
    pid_t child = fork();

    if (child < 0) {
        perror("fork");
        return EXIT_FAILURE;
    }

    if (child == 0) {
        puts("figlio: lavoro completato");
        return 7;
    }

    int status = 0;
    if (waitpid(child, &status, 0) < 0) {
        perror("waitpid");
        return EXIT_FAILURE;
    }

    if (WIFEXITED(status)) {
        printf("padre: codice del figlio = %d\n", WEXITSTATUS(status));
    } else {
        puts("padre: il figlio non e terminato normalmente");
    }

    return EXIT_SUCCESS;
}
```

<p align="justify">Osservazioni:</p>

<ul>
  <li>il ramo figlio termina con codice <code>7</code>;</li>
  <li>il padre non interpreta direttamente <code>status</code> come codice di uscita;</li>
  <li>le macro <code>WIFEXITED</code> e <code>WEXITSTATUS</code> verificano e decodificano lo stato;</li>
  <li>l'ordine delle prime stampe può cambiare in esempi più complessi, ma il padre stampa il risultato dopo <code>waitpid</code>.</li>
</ul>

<p align="justify">Compilazione:</p>

```bash
gcc -Wall -Wextra -Wpedantic -std=c17 process_wait.c -o process_wait
```

## Da processo a thread

<p align="justify">Un thread è un flusso di esecuzione all'interno di un processo. Più thread possono lavorare sugli stessi oggetti in memoria.</p>

<p align="justify">Usare thread può essere conveniente quando:</p>

<ul>
  <li>le attività condividono molti dati;</li>
  <li>si desidera mantenere reattiva un'applicazione;</li>
  <li>il lavoro può essere suddiviso;</li>
  <li>il costo della comunicazione tra processi sarebbe eccessivo.</li>
</ul>

<p align="justify">Usare processi può essere preferibile quando:</p>

<ul>
  <li>serve isolamento;</li>
  <li>i componenti hanno cicli di vita indipendenti;</li>
  <li>un guasto non deve corrompere tutto lo stato;</li>
  <li>si vogliono applicare permessi e limiti distinti.</li>
</ul>

<p align="justify">Collegamenti alla dispensa:</p>

<ul>
  <li><a href="../../LINUX_PROGRAMMING.md#i-thread">I Thread</a></li>
  <li><a href="../../LINUX_PROGRAMMING.md#creazione-di-un-thread">Creazione di un thread</a></li>
  <li><a href="../../LINUX_PROGRAMMING.md#passare-dati-ad-un-thread">Passare dati a un thread</a></li>
  <li><a href="../../LINUX_PROGRAMMING.md#attendere-la-terminazione-dei-thread">Attendere la terminazione dei thread</a></li>
  <li><a href="../../LINUX_PROGRAMMING.md#processi-vs-thread">Processi vs Thread</a></li>
</ul>

## Esempio concettuale POSIX thread

<p align="justify">Il frammento seguente mostra la forma essenziale. La sincronizzazione verrà approfondita nel modulo successivo.</p>

```c
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int first;
    int last;
    long result;
} SumTask;

static void *sum_range(void *raw_task) {
    SumTask *task = raw_task;
    long total = 0;

    for (int value = task->first; value <= task->last; ++value) {
        total += value;
    }

    task->result = total;
    return NULL;
}

int main(void) {
    SumTask left = {.first = 1, .last = 500000, .result = 0};
    SumTask right = {.first = 500001, .last = 1000000, .result = 0};
    pthread_t left_thread;
    pthread_t right_thread;

    if (pthread_create(&left_thread, NULL, sum_range, &left) != 0 ||
        pthread_create(&right_thread, NULL, sum_range, &right) != 0) {
        fputs("errore nella creazione dei thread\n", stderr);
        return EXIT_FAILURE;
    }

    pthread_join(left_thread, NULL);
    pthread_join(right_thread, NULL);

    printf("%ld\n", left.result + right.result);
    return EXIT_SUCCESS;
}
```

<p align="justify">Compilazione manuale:</p>

```bash
gcc -Wall -Wextra -Wpedantic -std=c17 -pthread sum_threads.c -o sum_threads
```

<p align="justify">Ogni thread scrive in un campo diverso. Il <code>join</code> garantisce che i risultati siano pronti prima della somma finale.</p>

## Confronto Java: `Runnable` e `join`

```java
final class SumTask implements Runnable {
    private final int first;
    private final int last;
    private long result;

    SumTask(int first, int last) {
        this.first = first;
        this.last = last;
    }

    @Override
    public void run() {
        long total = 0;
        for (int value = first; value <= last; value++) {
            total += value;
        }
        result = total;
    }

    long result() {
        return result;
    }
}

public final class ParallelSum {
    public static void main(String[] args) throws InterruptedException {
        SumTask left = new SumTask(1, 500_000);
        SumTask right = new SumTask(500_001, 1_000_000);

        Thread leftThread = new Thread(left, "sum-left");
        Thread rightThread = new Thread(right, "sum-right");

        leftThread.start();
        rightThread.start();
        leftThread.join();
        rightThread.join();

        System.out.println(left.result() + right.result());
    }
}
```

<p align="justify">Confronto:</p>

<table align="center">
<thead>
<tr>
<th>Concetto</th>
<th>POSIX C</th>
<th>Java</th>
</tr>
</thead>
<tbody>
<tr>
<td>funzione eseguita</td>
<td>funzione <code>void *(*)(void *)</code></td>
<td><code>Runnable.run()</code></td>
</tr>
<tr>
<td>handle</td>
<td><code>pthread_t</code></td>
<td>oggetto <code>Thread</code></td>
</tr>
<tr>
<td>avvio</td>
<td><code>pthread_create</code></td>
<td><code>start</code></td>
</tr>
<tr>
<td>attesa</td>
<td><code>pthread_join</code></td>
<td><code>join</code></td>
</tr>
<tr>
<td>passaggio dati</td>
<td>struttura e puntatore</td>
<td>campi dell'oggetto</td>
</tr>
<tr>
<td>errore</td>
<td>codice di ritorno</td>
<td>eccezioni e stato</td>
</tr>
</tbody>
</table>

<p align="justify">Il runner automatico Java della piattaforma è ancora pianificato. Questo esempio è quindi materiale di studio o laboratorio con correzione docente.</p>

## Descrivere la concorrenza con eventi e tracce

<p align="justify">Un programma concorrente non è descritto completamente da una sola sequenza globale. È utile individuare gli <strong>eventi</strong> importanti.</p>

<p align="justify">Esempio con due attività:</p>

```text
A1: legge x
A2: incrementa x
A3: scrive x

B1: legge x
B2: incrementa x
B3: scrive x
```

<p align="justify">All'interno di A vale l'ordine <code>A1 &lt; A2 &lt; A3</code>. All'interno di B vale <code>B1 &lt; B2 &lt; B3</code>. Fra eventi di thread diversi possono esistere molti interleaving.</p>

<p align="justify">Se <code>x</code> vale inizialmente <code>0</code>, entrambi possono leggere <code>0</code> e poi scrivere <code>1</code>. Due incrementi logici producono un solo incremento osservabile. Questo è un esempio di race condition.</p>

### Proprietà di sicurezza e di progresso

<ul>
  <li>Una proprietà di <strong>safety</strong> afferma che qualcosa di scorretto non deve accadere. Esempio: il saldo non deve diventare negativo.</li>
  <li>Una proprietà di <strong>liveness</strong> afferma che qualcosa di desiderato deve prima o poi accadere. Esempio: una richiesta accettata deve essere elaborata.</li>
</ul>

### Invariante

<p align="justify">Un invariante è una proprietà che deve restare vera nei punti significativi dell'esecuzione. Per un buffer limitato di capacità <code>N</code>:</p>

```text
0 <= elementi_presenti <= N
```

<p align="justify">La progettazione della sincronizzazione serve anche a preservare invarianti in tutti gli interleaving consentiti.</p>

## Errori frequenti

### Confondere `fork` con una normale funzione

<p align="justify">Dopo una <code>fork</code> riuscita esistono due processi. Se entrambi eseguono codice non previsto, possono duplicare stampe, file o altre operazioni.</p>

### Dimenticare il ramo di errore

<p align="justify"><code>fork</code>, <code>waitpid</code> e le funzioni thread restituiscono errori. Ignorarli produce programmi che sembrano funzionare soltanto nelle condizioni migliori.</p>

### Usare `sleep` come sincronizzazione

<p align="justify">Un ritardo non dimostra che un'altra attività abbia completato il lavoro. La macchina o il carico possono cambiare. È necessario un meccanismo di sincronizzazione esplicito.</p>

### Chiamare `run()` invece di `start()` in Java

<p align="justify">Invocare direttamente <code>run()</code> esegue il metodo nel thread corrente. <code>start()</code> crea il nuovo flusso e poi provoca l'esecuzione di <code>run()</code>.</p>

### Condividere una variabile senza contratto

<p align="justify">La condivisione non è sbagliata in sé. È sbagliato non stabilire chi può leggere o scrivere, quando e con quale sincronizzazione.</p>

### Credere che un output osservato sia l'unico possibile

<p align="justify">Una singola esecuzione non esplora tutti gli interleaving. Un bug concorrente può comparire raramente.</p>

## Esercizi graduati

### Livello A — osserva

<ol>
  <li>Avvia <code>sleep 30</code> in background e usa <code>ps</code> per individuarne PID e PPID.</li>
  <li>Esegui due volte lo stesso programma e verifica che i PID siano diversi.</li>
  <li>Compila l'esempio <code>process_wait.c</code> e annota quali righe appartengono al padre e quali al figlio.</li>
  <li>Disegna lo schema delle risorse private e condivise per due processi e per due thread.</li>
</ol>

### Livello B — modifica

<ol>
  <li>Modifica l'esempio padre-figlio affinché il figlio restituisca un codice letto da input.</li>
  <li>Crea due figli e attendili con due chiamate a <code>waitpid</code>.</li>
  <li>Nel programma POSIX thread, dividi l'intervallo in quattro parti.</li>
  <li>Nell'esempio Java, assegna nomi significativi ai thread e stampali con <code>Thread.currentThread().getName()</code>.</li>
</ol>

### Livello C — scrivi

<ol>
  <li>Scrivi un programma che crea un figlio; il figlio stampa i numeri pari e il padre i numeri dispari. Spiega perché l'ordine globale non è deterministico.</li>
  <li>Scrivi una funzione che costruisce una tabella con PID, PPID e ruolo del processo.</li>
  <li>Implementa una somma parallela con un numero di segmenti scelto da riga di comando.</li>
  <li>Realizza in Java due <code>Runnable</code>: uno conta le vocali e uno le consonanti della stessa stringa immutabile.</li>
</ol>

### Livello D — esegui il debug

<ol>
  <li>Correggi un programma che non distingue il valore di ritorno di <code>fork</code>.</li>
  <li>Individua perché una <code>printf</code> eseguita prima di <code>fork</code> può apparire più volte quando l'output è bufferizzato e non ancora scaricato.</li>
  <li>Correggi un programma Java che invoca <code>run()</code> e poi sostiene di usare due thread.</li>
  <li>Analizza una somma concorrente che usa un unico contatore condiviso senza sincronizzazione.</li>
</ol>

### Livello E — mini-progetto

<p align="justify">Costruisci un piccolo orchestratore che avvia tre programmi distinti, raccoglie il loro stato di uscita e produce un riepilogo. Definisci prima:</p>

<ul>
  <li>formato dei comandi;</li>
  <li>gestione degli errori;</li>
  <li>timeout previsto;</li>
  <li>significato dei codici di uscita;</li>
  <li>eventi da registrare.</li>
</ul>

### Livello F — progetto integrato

<p align="justify">Progetta un sistema di elaborazione di file composto da:</p>

<ul>
  <li>processo coordinatore;</li>
  <li>processi worker;</li>
  <li>protocollo di assegnazione dei file;</li>
  <li>gestione del worker terminato in errore;</li>
  <li>log strutturato;</li>
  <li>test dei casi limite.</li>
</ul>

<p align="justify">In questa fase è sufficiente produrre requisiti, diagramma e prototipo minimo. La comunicazione completa verrà sviluppata nel modulo successivo.</p>

## Laboratorio assegnabile: calcolo con `fork` e pipe

<p align="justify">Activity collegata:</p>

```text
tpsi4-activity-c-fork-pipe-square-001
```

<p align="justify">Obiettivo: il processo padre legge un intero, il figlio ne calcola il quadrato e invia il risultato al padre attraverso una pipe. Il padre attende il figlio e stampa soltanto il risultato ricevuto.</p>

<p align="justify">Il laboratorio verifica:</p>

<ul>
  <li>distinzione padre/figlio;</li>
  <li>chiusura delle estremità non usate della pipe;</li>
  <li>lettura e scrittura con controllo degli errori;</li>
  <li>uso di <code>waitpid</code>;</li>
  <li>output deterministico compatibile con il grader C esistente.</li>
</ul>

## Verifica rapida

<ol>
  <li>Qual è la differenza tra programma e processo?</li>
  <li>Un processo pronto sta necessariamente usando la CPU?</li>
  <li>Perché due processi non condividono automaticamente le normali variabili?</li>
  <li>Che cosa restituisce <code>fork()</code> nel figlio?</li>
  <li>Che cosa accade al processo quando una <code>exec</code> riesce?</li>
  <li>Perché il padre dovrebbe eseguire <code>wait</code> o <code>waitpid</code>?</li>
  <li>Qual è la differenza tra concorrenza e parallelismo?</li>
  <li>Quali aree sono normalmente condivise da thread dello stesso processo?</li>
  <li>Che cosa rappresenta un interleaving?</li>
  <li>Fornisci un esempio di proprietà di safety e uno di liveness.</li>
</ol>

## Sintesi inclusiva

<ul>
  <li>Un programma è un file; un processo è quel programma mentre viene eseguito.</li>
  <li>Ogni processo ha un PID e può avere un processo padre.</li>
  <li>Il contesto ricorda da dove riprendere; lo spazio di indirizzamento definisce gli indirizzi del processo e le sue mappature.</li>
  <li>Lo stack sostiene le chiamate di funzione; l'heap serve alle allocazioni dinamiche.</li>
  <li>I descrittori fanno riferimento alle risorse aperte; le credenziali identificano per conto di chi il processo agisce.</li>
  <li>Il sistema operativo alterna processi pronti e gestisce quelli in attesa.</li>
  <li>Processi distinti hanno memoria separata; i thread dello stesso processo condividono più stato.</li>
  <li>Concorrente significa che più attività avanzano nello stesso intervallo; parallelo significa che eseguono nello stesso istante.</li>
  <li><code>fork</code> crea un figlio, <code>exec</code> sostituisce il programma, <code>wait</code> raccoglie la terminazione.</li>
  <li>I thread sono più leggeri, ma la memoria condivisa richiede regole precise.</li>
  <li>L'ordine tra attività concorrenti può cambiare.</li>
  <li>Una soluzione corretta deve funzionare per tutti gli ordini consentiti, non soltanto per quello osservato una volta.</li>
</ul>

## Collegamento al modulo successivo

<p align="justify">Questo modulo introduce le attività concorrenti e il loro stato. Il modulo <a href="02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md">Comunicazione e sincronizzazione</a> affronta come scambiare dati, proteggere invarianti e risolvere i problemi classici di coordinamento.</p>

## Fonti e note di revisione

<ul>
  <li>Riferimento curricolare: indice pubblico del volume 2, usato solo per verificare la copertura.</li>
  <li>Fonte tecnica locale: <code>LINUX_PROGRAMMING.md</code>, a partire da <code>Linux Programming</code>.</li>
  <li>Identità, autorizzazioni e relazioni: <a href="https://man7.org/linux/man-pages/man2/getpid.2.html">getpid(2)</a>, <a href="https://man7.org/linux/man-pages/man7/credentials.7.html">credentials(7)</a> e <a href="https://man7.org/linux/man-pages/man2/wait.2.html">wait(2)</a>.</li>
  <li>Contesto e chiamate di funzione: manuale GDB, <a href="https://sourceware.org/gdb/current/onlinedocs/gdb.html/Registers.html">Registers</a> e <a href="https://sourceware.org/gdb/current/onlinedocs/gdb.html/Frames.html">Stack Frames</a>.</li>
  <li>Architettura di riferimento: <a href="https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html">Intel 64 and IA-32 Architectures Software Developer's Manuals</a>, volume 1 per registri e chiamate, volume 2 per istruzioni e volume 3 per memoria e interruzioni. Gli schemi selezionano gli elementi utili alla lezione.</li>
  <li>Convenzioni delle chiamate Linux x86-64: <a href="https://gitlab.com/x86-psABIs/x86-64-ABI">System V AMD64 ABI</a>. Generazione dell'assembly: <a href="https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html">GCC, Overall Options</a>. L'assembly commentato è una traduzione didattica, non un dump di una specifica versione del compilatore.</li>
  <li>Contesto nel kernel: <a href="https://docs.kernel.org/arch/x86/kernel-stacks.html">Linux, Kernel Stacks</a> e <a href="https://github.com/torvalds/linux/blob/master/arch/x86/entry/entry_64.S">codice di ingresso e cambio del contesto x86-64</a>. La sequenza descrive il comportamento complessivo senza riprodurre l'implementazione del kernel.</li>
  <li>Memoria e allocazioni: <a href="https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html">proc_pid_maps(5)</a> e <a href="https://man7.org/linux/man-pages/man3/malloc.3.html">malloc(3)</a>. La descrizione di stack e heap è un modello didattico, non una disposizione universale della memoria.</li>
  <li>Risorse aperte: <a href="https://man7.org/linux/man-pages/man2/open.2.html">open(2)</a> e <a href="https://man7.org/linux/man-pages/man5/proc_pid_fd.5.html">proc_pid_fd(5)</a>.</li>
  <li>Stato e distinzione processo/thread: <a href="https://man7.org/linux/man-pages/man5/proc_pid_status.5.html">proc_pid_status(5)</a> e <a href="https://man7.org/linux/man-pages/man7/pthreads.7.html">pthreads(7)</a>.</li>
  <li>Tutti gli esempi di questo modulo sono formulati ex novo per il pacchetto.</li>
  <li>Gli esempi della fonte Linux con intestazioni di copyright esterne non devono essere duplicati nelle activity senza averne verificato la licenza.</li>
  <li>Stato: <code>draft</code>; revisione docente richiesta prima della pubblicazione agli studenti.</li>
</ul>
