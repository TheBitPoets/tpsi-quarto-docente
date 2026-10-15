# Laboratorio Ubuntu: osservare e gestire i processi

<!--
status: draft
transformation: original-course-material
-->

## In questa unità impareremo

<!-- visual-orientation -->
<table align="center">
<tr><td>
<details>
<summary>&#129517; <strong>Orientamento della sezione</strong></summary>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128506;</span> Contesto:</strong> laboratorio sui processi nel terminale della macchina virtuale Ubuntu.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128736;</span> Prerequisiti:</strong> saper aprire il terminale e digitare un comando. Simboli e opzioni usati sono spiegati qui.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#127919;</span> Obiettivi:</strong> trovare il PID, inviare i segnali più comuni, distinguere attesa e sospensione, usare jobs, bg e fg.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128257;</span> Richiamo:</strong> un processo può esistere anche mentre non usa la CPU.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128064;</span> Anticipazione:</strong> nel modulo successivo vedremo come un programma può rispondere ai segnali.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#10145;</span> Prossimo passo:</strong> svolgere le tre prove guidate; gli approfondimenti finali sono facoltativi.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> Rimando:</strong> <a href="01_PROCESSI_E_CONCORRENZA.md">Processi, thread e concorrenza</a>; <a href="#fonti-e-note-di-revisione">fonti e note</a>.</p>
</details>
</td></tr>
</table>

<p align="justify">Useremo quasi sempre un solo comando: <code>sleep 300</code>. Aspetta 300 secondi, cioè cinque minuti, e poi termina. Durante l'attesa non stampa nulla: possiamo così provare i comandi sui processi senza scrivere un programma.</p>

## Prima di iniziare

<p align="justify">Apri il terminale nella VM Ubuntu 24.04.3 LTS del corso, con la shell Bash. Usa il tuo utente normale: <strong>non serve sudo</strong>. Esegui una riga alla volta e resta nello stesso terminale durante ciascuna prova. I blocchi mostrano i comandi da digitare; premi Invio dopo ogni riga. Quando trovi Ctrl+C o Ctrl+Z, tieni premuto Ctrl e premi la lettera indicata.</p>

<!-- definition -->
<table align="center">
<tr><td>
&#10071; <strong>Importante</strong>
<p align="justify">La <strong>shell</strong> è il programma che interpreta i comandi digitati nel terminale. Il <strong>prompt</strong> è il testo che mostra quando è pronta a ricevere un nuovo comando.</p>
<p align="justify">Un <strong>processo</strong> è un programma in esecuzione. Il <strong>PID</strong> è il numero che lo identifica nel sistema.</p>
<p align="justify">Un comando in <strong>primo piano</strong> fa attendere la shell prima di mostrare un nuovo prompt. Un comando in <strong>background</strong> lascia disponibile il prompt mentre prosegue.</p>
</td></tr>
</table>
<!-- /definition -->

<p align="justify">Se una prova dura più di cinque minuti, sleep può terminare da solo. In quel caso riparti dal suo avvio: ogni nuovo processo avrà un nuovo PID. Se compare <code>No such process</code> o <code>Nessun processo corrisponde</code>, controlla se il processo è già terminato.</p>

## Segnali: notificare, sospendere, riprendere, terminare

<!-- definition -->
<table align="center">
<tr><td>
&#10071; <strong>Importante</strong>
<p align="justify">Un <strong>segnale</strong> è una notifica inviata a un processo per comunicargli un evento o richiedere un'azione, come terminare, sospendersi o riprendere.</p>
</td></tr>
</table>
<!-- /definition -->

<p align="justify">Il comando <code>kill</code> invia segnali: il suo nome non implica sempre la terminazione. Per esempio, <code>kill -STOP</code> sospende un processo e <code>kill -CONT</code> lo fa riprendere. Vediamo prima un esempio completo.</p>

## Prova 1: avviare, osservare e terminare

### 1. Avvia il processo e conserva il PID

```bash
sleep 300 &
pid=$!
echo "$pid"
```

<ul>
  <li><code>sleep 300</code> avvia l'attesa di cinque minuti.</li>
  <li><code>&amp;</code> alla fine avvia il comando in background: puoi subito digitare altro.</li>
  <li><code>$!</code> contiene il PID dell'ultimo processo avviato in background.</li>
  <li><code>pid=$!</code> conserva quel numero nella variabile chiamata <code>pid</code>. Scrivi l'assegnazione senza spazi intorno a <code>=</code>.</li>
  <li><code>echo "$pid"</code> stampa il numero conservato. <code>$pid</code> legge il valore della variabile; le virgolette lo mantengono come un unico argomento.</li>
</ul>

<p align="justify"><strong>Atteso:</strong> la shell mostra una riga simile a <code>[1] 12345</code>; echo stampa <code>12345</code>. I tuoi numeri saranno diversi. Il numero tra parentesi quadre servirà nella prova sui job; per ora usiamo il PID.</p>

### 2. Osserva il processo

```bash
ps -p "$pid" -o pid,stat,comm
```

<p align="justify"><code>ps</code> mostra una fotografia dei processi. <code>-p "$pid"</code> seleziona quello con il PID conservato; <code>-o pid,stat,comm</code> sceglie tre colonne: numero del processo, stato e nome del comando.</p>

```text
    PID STAT COMMAND
  12345 S    sleep
```

<p align="justify"><strong>Atteso:</strong> una riga con sleep e, normalmente, lo stato <code>S</code>: il processo sta aspettando. Non deve usare continuamente la CPU per essere ancora presente.</p>

### 3. Invia TERM e controlla

```bash
kill -TERM "$pid"
ps -p "$pid" -o pid,stat,comm
```

<p align="justify"><code>-TERM</code> sceglie il segnale di terminazione ordinaria; <code>"$pid"</code> indica a chi inviarlo. <strong>Atteso:</strong> la riga di sleep scompare. Può restare soltanto l'intestazione di ps e la shell può scrivere <code>Terminated</code> o un messaggio equivalente. Se la riga è ancora presente, ripeti ps dopo un istante.</p>

## Inviare segnali con kill e killall

<p align="justify">Per inviare un segnale con kill bastano il suo nome e il PID. Le tre forme seguenti richiedono tutte TERM; sono <strong>alternative</strong>, non una sequenza da eseguire:</p>

```bash
kill -TERM "$pid"
kill -s TERM "$pid"
kill "$pid"
```

<p align="justify">Con <code>-s</code> il nome del segnale si scrive come argomento successivo. Senza specificare un segnale, kill usa TERM. Nelle prove useremo la prima forma. Il nome completo è <code>SIGTERM</code>, ma nel comando possiamo scrivere <code>TERM</code>. Per selezionare i processi per nome esiste anche <a href="#selezionare-per-nome-con-killall">killall, descritto negli approfondimenti</a>.</p>

### I segnali più usati

<p align="justify">Gli esempi presuppongono un processo appena avviato e il suo PID salvato come nella prova 1. <strong>Non eseguire tutte le righe sullo stesso processo:</strong> molti segnali lo terminano.</p>

<table align="center">
<thead><tr><th>Segnale</th><th>Esempio</th><th>Che cosa succede normalmente</th></tr></thead>
<tbody>
<tr><td><code>SIGTERM</code></td><td><code>kill -TERM "$pid"</code></td><td>Chiede la terminazione. È la prima scelta per chiudere un processo.</td></tr>
<tr><td><code>SIGINT</code></td><td><code>kill -INT "$pid"</code></td><td>Interrompe e termina. È anche il segnale di Ctrl+C.</td></tr>
<tr><td><code>SIGQUIT</code></td><td><code>kill -QUIT "$pid"</code></td><td>Termina e può produrre un file diagnostico. Da tastiera: Ctrl+\.</td></tr>
<tr><td><code>SIGKILL</code></td><td><code>kill -KILL "$pid"</code></td><td>Forza la terminazione, senza permettere al programma di eseguire la propria procedura di chiusura.</td></tr>
<tr><td><code>SIGSTOP</code></td><td><code>kill -STOP "$pid"</code></td><td>Sospende: il processo resta presente, ma non prosegue.</td></tr>
<tr><td><code>SIGTSTP</code></td><td><code>kill -TSTP "$pid"</code></td><td>Sospende. È anche il segnale di Ctrl+Z.</td></tr>
<tr><td><code>SIGCONT</code></td><td><code>kill -CONT "$pid"</code></td><td>Fa riprendere un processo sospeso.</td></tr>
<tr><td><code>SIGHUP</code></td><td><code>kill -HUP "$pid"</code></td><td>Segnala normalmente la perdita del terminale. Di base termina; alcuni programmi lo usano per rileggere la configurazione.</td></tr>
<tr><td><code>SIGUSR1</code></td><td><code>kill -USR1 "$pid"</code></td><td>Azione scelta dal programma; se non è prevista una gestione, termina.</td></tr>
<tr><td><code>SIGUSR2</code></td><td><code>kill -USR2 "$pid"</code></td><td>Secondo segnale per un'azione scelta dal programma; di base termina.</td></tr>
<tr><td><code>SIGALRM</code></td><td><code>kill -ALRM "$pid"</code></td><td>Segnala normalmente la scadenza di un timer; di base termina. Qui lo inviamo manualmente.</td></tr>
</tbody>
</table>

<p align="justify">Un programma può cambiare la risposta a molti segnali, per esempio salvare dati prima di chiudersi con TERM. <strong>KILL e STOP non possono essere gestiti, ignorati o bloccati.</strong> Per questo STOP e TSTP, pur sospendendo normalmente entrambi, non sono equivalenti. Sleep termina con HUP, USR1 e USR2: non ha azioni personalizzate per questi segnali.</p>

<p align="justify">Puoi incontrare anche <code>kill -15</code> per TERM e <code>kill -9</code> per KILL. Preferisci i nomi: sono più leggibili e alcuni numeri cambiano tra architetture. Per vedere l'elenco disponibile:</p>

```bash
kill -l
```

### Altri segnali da riconoscere

<p align="justify">Questi segnali sono spesso generati dal sistema o dal programma stesso. Non è necessario provarli tutti; la sintassi per inviarli manualmente resta la stessa.</p>

<table align="center">
<thead><tr><th>Segnale</th><th>Esempio di invio</th><th>Situazione tipica e azione predefinita</th></tr></thead>
<tbody>
<tr><td><code>SIGCHLD</code></td><td><code>kill -CHLD "$pid"</code></td><td>Avvisa il padre di un cambiamento di stato di un figlio; di base è ignorato.</td></tr>
<tr><td><code>SIGPIPE</code></td><td><code>kill -PIPE "$pid"</code></td><td>Scrittura in un canale di comunicazione senza lettori; termina.</td></tr>
<tr><td><code>SIGABRT</code></td><td><code>kill -ABRT "$pid"</code></td><td>Richiesta di arresto anomalo da parte del programma; termina.</td></tr>
<tr><td><code>SIGSEGV</code></td><td><code>kill -SEGV "$pid"</code></td><td>Accesso non valido alla memoria; termina.</td></tr>
<tr><td><code>SIGFPE</code></td><td><code>kill -FPE "$pid"</code></td><td>Errore aritmetico, per esempio certe divisioni per zero; termina.</td></tr>
<tr><td><code>SIGWINCH</code></td><td><code>kill -WINCH "$pid"</code></td><td>Cambio delle dimensioni del terminale; di base è ignorato.</td></tr>
<tr><td><code>SIGTTIN</code>, <code>SIGTTOU</code></td><td><code>kill -TTIN "$pid"</code><br><code>kill -TTOU "$pid"</code></td><td>Accessi al terminale da un gruppo in background, in determinate condizioni; sospendono.</td></tr>
</tbody>
</table>

<p align="justify">ABRT, SEGV e FPE possono anche produrre un file diagnostico, secondo la configurazione del sistema. Inviare SEGV con kill non provoca un vero accesso errato alla memoria: invia soltanto la notifica. Analogamente, inviare CHLD manualmente non crea né termina un figlio. <a href="https://man7.org/linux/man-pages/man7/signal.7.html">Riferimento sui segnali</a>.</p>

## Prova 2: sospendere, riprendere e provare altri segnali

### 1. Avvia un nuovo processo

```bash
sleep 300 &
pid=$!
```

<p align="justify">Il processo della prova 1 è terminato: questi comandi ne creano un altro e aggiornano la variabile pid.</p>

### 2. Sospendilo con STOP

```bash
kill -STOP "$pid"
ps -p "$pid" -o pid,stat,comm
```

<p align="justify"><strong>Atteso:</strong> compare <code>T</code>. Sleep esiste ancora, ma è sospeso. Se leggi ancora S, ripeti ps dopo un istante.</p>

### 3. Fallo riprendere con CONT

```bash
kill -CONT "$pid"
ps -p "$pid" -o pid,stat,comm
```

<p align="justify"><strong>Atteso:</strong> torna normalmente <code>S</code>, perché sleep continua ad aspettare la scadenza. Riprendere non significa necessariamente usare subito la CPU.</p>

### 4. Terminalo con KILL

```bash
kill -KILL "$pid"
ps -p "$pid" -o pid,stat,comm
```

<p align="justify"><strong>Atteso:</strong> la riga scompare; la shell può mostrare <code>Killed</code>. Qui usiamo KILL per impararne l'effetto. Nell'uso ordinario si prova prima TERM, così il programma può completare la propria chiusura.</p>

### 5. Ripeti con un altro segnale

<p align="justify">Per provare INT esegui questo piccolo blocco, sempre riga per riga nel terminale Bash:</p>

```bash
sleep 300 &
pid=$!
kill -INT "$pid"
ps -p "$pid" -o pid,stat,comm
```

<p align="justify"><strong>Atteso:</strong> sleep termina. Ripeti lo stesso blocco sostituendo soltanto <code>-INT</code> con <code>-HUP</code>, <code>-USR1</code>, <code>-USR2</code>, <code>-ALRM</code> oppure <code>-QUIT</code>, un segnale alla volta. Ogni volta avvia un nuovo sleep: anche questi segnali lo terminano. I messaggi stampati dalla shell possono cambiare.</p>

<p align="justify">Per provare <code>-TSTP</code>, ripeti invece i passi 1–4 sostituendo STOP con TSTP: osserverai sospensione, ripresa e terminazione. Queste prove vanno eseguite in un <strong>terminale Bash interattivo</strong>: uno script può trattare diversamente INT e QUIT per i comandi in background.</p>

## Primo piano, background e job: jobs, bg e fg

<!-- definition -->
<table align="center">
<tr><td>
&#10071; <strong>Importante</strong>
<p align="justify">Un <strong>job della shell</strong> è un'attività che la shell gestisce con un proprio numero. Può comprendere uno o più processi. Il numero del job vale soltanto nella shell che lo ha avviato; il PID identifica un processo nel sistema.</p>
</td></tr>
</table>
<!-- /definition -->

<table align="center">
<thead><tr><th>Comando o tasto</th><th>Che cosa fa</th></tr></thead>
<tbody>
<tr><td><code>jobs</code></td><td>Elenca i job del terminale corrente e il loro stato.</td></tr>
<tr><td><code>jobs -l</code></td><td>Aggiunge i PID all'elenco.</td></tr>
<tr><td><strong>Ctrl+Z</strong></td><td>Invia TSTP all'attività in primo piano: normalmente la sospende e restituisce il prompt.</td></tr>
<tr><td><code>bg %1</code></td><td>Riprende il job 1 sospeso, lasciando disponibile il prompt.</td></tr>
<tr><td><code>fg %1</code></td><td>Porta il job 1 in primo piano; se era sospeso, lo riprende.</td></tr>
<tr><td><strong>Ctrl+C</strong></td><td>Invia INT all'attività in primo piano: normalmente la termina.</td></tr>
</tbody>
</table>

<p align="justify"><strong><code>%1</code> significa «job numero 1», non «PID 1».</strong> Se jobs mostra <code>[2]</code>, usa <code>%2</code>. I tasti Ctrl+C e Ctrl+Z raggiungono il gruppo di processi in primo piano; nelle nostre prove quel gruppo contiene soltanto sleep.</p>

## Prova 3: Ctrl+Z, jobs, bg e fg

<p align="justify">Apri un <strong>nuovo terminale Bash</strong> e usalo per tutta questa prova: sarà più facile riconoscere l'unico job.</p>

### 1. Avvia in primo piano

```bash
sleep 300
```

<p align="justify">Questa volta manca <code>&amp;</code>. <strong>Atteso:</strong> il prompt non ritorna subito, perché la shell aspetta che sleep finisca. Il terminale non è bloccato.</p>

### 2. Sospendi e guarda l'elenco

<p align="justify">Premi <strong>Ctrl+Z</strong>. Quando ritorna il prompt, digita:</p>

```bash
jobs
jobs -l
```

<p align="justify"><strong>Atteso:</strong> una riga simile a questa nell'output di jobs -l:</p>

```text
[1]+ 12345 Stopped                 sleep 300
```

<p align="justify"><code>[1]</code> è il numero del job; <code>12345</code> è un PID di esempio; <code>Stopped</code> significa sospeso. Il simbolo <code>+</code> indica il job corrente, scelto dalla shell quando fg o bg vengono scritti senza numero. La lingua dei messaggi può variare.</p>

### 3. Riprendi in background

```bash
bg %1
jobs
```

<p align="justify"><strong>Atteso:</strong> jobs mostra <code>Running</code> e puoi ancora digitare comandi. Bg ha fatto riprendere il job con CONT. Running significa che il job non è sospeso: sleep sta ancora aspettando e ps può mostrarlo in S.</p>

### 4. Riporta in primo piano e termina

```bash
fg %1
```

<p align="justify"><strong>Atteso:</strong> il prompt torna a non essere disponibile. Premi <strong>Ctrl+C</strong> per terminare sleep, poi controlla:</p>

```bash
jobs
```

<p align="justify"><strong>Atteso:</strong> nessun job attivo. Se compare ancora una notifica di conclusione, esegui jobs una seconda volta.</p>

<p align="justify"><strong>Da ricordare:</strong> Ctrl+Z sospende; bg riprende lasciando libero il prompt; fg porta in primo piano; Ctrl+C normalmente termina. Jobs vede soltanto le attività di quella shell: un altro terminale ha un proprio elenco. <a href="https://man7.org/linux/man-pages/man1/bash.1.html">Manuale Bash, controllo dei job</a>.</p>

## Comprendere gli stati S, D, T e t di ps

<p align="justify">Per rileggere le prove basta guardare la prima lettera di <code>STAT</code>. Nei nostri esempi abbiamo osservato soprattutto S e T. Le definizioni seguenti spiegano anche D e t, senza doverli riprodurre.</p>

<!-- definition -->
<table align="center">
<tr><td>
&#10071; <strong>Importante</strong>
<p align="justify">Lo <strong>stato S</strong> indica un'attesa interrompibile: il processo aspetta un evento, ma può essere risvegliato anche da un segnale da trattare.</p>
<p align="justify">Lo <strong>stato D</strong> indica un'attesa non interrompibile nel kernel, cioè nel nucleo del sistema operativo: la normale consegna dei segnali non basta a far uscire il processo da quell'attesa.</p>
<p align="justify">Lo <strong>stato T</strong> indica un processo sospeso da un segnale di stop.</p>
<p align="justify">Lo <strong>stato t</strong>, minuscolo, indica un processo arrestato sotto il controllo di uno strumento di tracciamento o di un debugger, usato per esaminare l'esecuzione di un programma.</p>
</td></tr>
</table>
<!-- /definition -->

<table align="center">
<thead><tr><th>Stato</th><th>Esempio</th><th>Come prosegue</th></tr></thead>
<tbody>
<tr><td><code>S</code></td><td>Sleep aspetta lo scadere del tempo.</td><td>Scade il tempo, oppure arriva un segnale da trattare.</td></tr>
<tr><td><code>D</code></td><td>Attesa di alcune operazioni su dispositivi.</td><td>Deve diventare possibile uscire dall'attesa. Anche KILL può avere effetto solo in seguito.</td></tr>
<tr><td><code>T</code></td><td>Sleep dopo STOP o Ctrl+Z.</td><td>CONT, anche tramite bg o fg.</td></tr>
<tr><td><code>t</code></td><td>Programma fermato per esaminarlo con un debugger.</td><td>Lo strumento di tracciamento ne comanda la prosecuzione.</td></tr>
</tbody>
</table>

<p align="justify">S e D non distinguono attese brevi e lunghe; non tutte le attese su dispositivi sono D. T e t sono stati diversi. Un programma sotto debugger compare in t soltanto quando è effettivamente arrestato per il tracciamento. <a href="https://man7.org/linux/man-pages/man1/ps.1.html">Manuale ps, codici degli stati</a>.</p>

## Approfondimenti facoltativi

### Osservare tutti i processi con ps e top

<p align="justify">Per una panoramica dei processi del sistema:</p>

```bash
ps -ef
top
```

<p align="justify">In ps, <code>-e</code> seleziona tutti i processi e <code>-f</code> mostra più informazioni, tra cui <code>PPID</code>, il PID del processo padre. Top aggiorna la vista nel tempo: premi <code>q</code> per uscire e tornare al prompt.</p>

### Selezionare per nome con killall

<p align="justify">Kill usa il PID; <code>killall</code> seleziona i processi per nome e può quindi raggiungerne più di uno. Avvia un nuovo sleep e annota il PID stampato da echo. Poi cerca i tuoi processi sleep e chiedi conferma prima di terminarli:</p>

```bash
sleep 300 &
pid=$!
echo "$pid"
pgrep -a -u "$USER" -x sleep
killall -i -u "$USER" -s TERM sleep
```

<p align="justify"><code>pgrep</code> cerca processi: <code>-a</code> mostra PID e comando, <code>-u "$USER"</code> limita la ricerca al tuo utente e <code>-x sleep</code> richiede esattamente quel nome. <code>$USER</code> contiene il nome dell'utente della sessione. In killall, <code>-i</code> chiede conferma per ogni processo, <code>-u</code> sceglie l'utente e <code>-s TERM</code> sceglie il segnale. Conferma soltanto il PID della prova; la risposta da digitare è indicata nella domanda, normalmente <code>y</code> per sì o <code>n</code> per no. Ripeti pgrep per controllare il risultato. <a href="https://manpages.ubuntu.com/manpages/noble/man1/killall.1.html">Manuale killall</a>.</p>

### Cambiare la priorità con nice e renice

<!-- definition -->
<table align="center">
<tr><td>
&#10071; <strong>Importante</strong>
<p align="justify">Il <strong>valore nice</strong> influenza la priorità relativa di CPU di un normale processo Linux. Va da -20 a 19: un numero più alto corrisponde a una priorità meno favorevole.</p>
</td></tr>
</table>
<!-- /definition -->

<p align="justify">Nice avvia un processo con una priorità modificata; renice interviene su uno già avviato. Per questa prova controlla prima il nice della shell:</p>

```bash
ps -p "$$" -o pid,ni,comm
```

<p align="justify"><code>$$</code> contiene il PID della shell; <code>NI</code> mostra il nice. Se vale 0, esegui:</p>

```bash
nice -n 10 sleep 300 &
pid=$!
ps -p "$pid" -o pid,ni,comm
renice 15 -p "$pid"
ps -p "$pid" -o pid,ni,comm
kill -TERM "$pid"
```

<p align="justify"><strong>Atteso:</strong> NI passa da 10 a 15. <code>nice -n 10</code> aggiunge 10 al valore ereditato; <code>renice 15 -p</code> imposta 15 sul PID indicato. Senza privilegi, normalmente puoi aumentare il nice dei tuoi processi ma non diminuirlo. Sleep permette di vedere il valore: poiché aspetta, non è una prova delle prestazioni della CPU.</p>

## Verifica rapida

<ol>
  <li>Quale comando invia TERM al processo il cui PID è salvato nella variabile pid?</li>
  <li>Che differenza c'è tra STOP, CONT e KILL?</li>
  <li>Dopo Ctrl+Z, come fai riprendere il job 1 lasciando disponibile il prompt?</li>
  <li>Come riporti il job 1 in primo piano? Come lo termini da tastiera?</li>
  <li>Perché jobs può mostrare Running mentre ps mostra S?</li>
</ol>

<p align="justify"><strong>Consegna breve:</strong> annota tre comandi, uno per terminare, uno per sospendere e uno per riprendere. Per ciascuno scrivi una frase sul risultato osservato. Alla fine controlla con jobs, in ciascun terminale usato, che non rimangano job attivi o sospesi. Se ne rimane uno della prova, usa fg con il suo numero e poi Ctrl+C.</p>

## Fonti e note di revisione

<ul>
  <li>Spunto didattico: <a href="https://github.com/TheBitPoets/2cornot2c/blob/main/LINUX_PROGRAMMING.md#controllo-dei-processi">Controllo dei processi in 2cornot2c</a>. Testo ed esercizi sono originali.</li>
  <li>Segnali: <a href="https://man7.org/linux/man-pages/man7/signal.7.html">signal(7)</a>; shell e job: <a href="https://man7.org/linux/man-pages/man1/bash.1.html">Bash</a>. Nel terminale si possono consultare anche <code>help kill</code>, <code>help jobs</code>, <code>help fg</code> e <code>help bg</code>.</li>
  <li>Comandi: <a href="https://man7.org/linux/man-pages/man1/ps.1.html">ps</a>, <a href="https://man7.org/linux/man-pages/man1/pgrep.1.html">pgrep</a>, <a href="https://man7.org/linux/man-pages/man1/top.1.html">top</a>, <a href="https://manpages.ubuntu.com/manpages/noble/man1/killall.1.html">killall</a>, <a href="https://man7.org/linux/man-pages/man1/nice.1.html">nice</a>, <a href="https://manpages.ubuntu.com/manpages/noble/man1/renice.1.html">renice</a>.</li>
  <li>Per approfondire la gestione dei segnali nei programmi: <a href="02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#segnali-notifiche-non-contenitori-generici">segnali nel modulo 2</a>.</li>
  <li>Revisione del 15 ottobre 2026: tre prove di base, esempi dei segnali più comuni, spiegazione di simboli e opzioni, approfondimenti facoltativi su ps/top, killall e nice/renice. Fonti sui segnali, Bash e ps ricontrollate.</li>
  <li>Collaudo del 15 ottobre 2026 su Ubuntu 24.04 in WSL, con utente senza privilegi, Bash 5.2.21 e procps-ng 4.0.4: verificati i segnali elencati, gli stati S/T, Ctrl+Z e Ctrl+C in un terminale interattivo, jobs/bg/fg, nice/renice e pgrep/killall con conferma. La verifica sulla VM del corso resta da svolgere.</li>
  <li>Ambiente previsto: VM Ubuntu 24.04.3 LTS del corso, con Bash interattiva. Stato: <code>draft</code>.</li>
</ul>
