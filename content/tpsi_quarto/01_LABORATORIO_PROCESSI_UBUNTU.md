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
<p align="justify"><strong><span style="font-size: 1.15em;">&#128506;</span> Contesto:</strong> laboratorio del modulo su processi e concorrenza, da svolgere nel terminale della macchina virtuale Ubuntu.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128736;</span> Prerequisiti:</strong> aprire un terminale, eseguire comandi, riconoscere PID, PPID e stati di un processo.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#127919;</span> Obiettivi:</strong> leggere l'output di ps, osservare con top, modificare il valore nice, inviare segnali a processi scelti per PID o nome.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128257;</span> Richiamo:</strong> un processo può esistere anche mentre non usa la CPU; il suo identificatore permette di individuarlo.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128064;</span> Anticipazione:</strong> i programmi possono gestire alcuni segnali; nel modulo successivo useremo queste notifiche per coordinare attività.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#10145;</span> Prossimo passo:</strong> svolgere le cinque prove e annotare comando, osservazione e spiegazione.</p>
<p align="justify"><strong><span style="font-size: 1.15em;">&#128279;</span> Rimando:</strong> <a href="01_PROCESSI_E_CONCORRENZA.md">Processi, thread e concorrenza</a>; <a href="#fonti-e-note-di-revisione">manuali e note di revisione</a>.</p>
</details>
</td></tr>
</table>

<p align="justify">Seguiremo un processo dalla sua creazione nel terminale fino alla terminazione. Prima lo osserviamo, poi proviamo a sospenderlo e riprenderlo, infine confrontiamo la selezione per PID con quella per nome. Le spiegazioni e gli esercizi sono originali; gli argomenti riprendono la sezione <a href="https://github.com/TheBitPoets/2cornot2c/blob/main/LINUX_PROGRAMMING.md#controllo-dei-processi">Controllo dei processi</a>, confrontata con i manuali Linux attuali.</p>

## Ambiente e preparazione

<p align="justify">La macchina virtuale del corso usa <strong>Ubuntu 24.04.3 LTS</strong>. Gli esempi usano <strong>Bash</strong>: esegui i comandi nel terminale Linux della VM. Per verificare distribuzione, kernel e shell:</p>

```bash
cat /etc/os-release
uname -r
printf '%s\n' "$BASH_VERSION"
```

<p align="justify"><code>PRETTY_NAME</code> indica la versione di Ubuntu; <code>uname -r</code> indica quella del kernel. Sono informazioni diverse. La scheda fa riferimento ai comandi di Ubuntu 24.04 LTS, la serie a cui appartiene la VM del corso; la verifica pratica è descritta nelle note finali.</p>

```bash
command -v ps top pgrep nice renice killall pstree
type -a kill
```

<p align="justify">In Bash, <code>kill</code> è normalmente un comando integrato nella shell; esiste anche un eseguibile esterno. Per il primo consulta <code>help kill</code>, per gli altri <code>man ps</code>, <code>man nice</code>, <code>man renice</code> e <code>man killall</code>. Esci dal manuale premendo <code>q</code>.</p>

<p align="justify">Se mancano strumenti, i pacchetti pertinenti sono <code>procps</code> per ps, top e pgrep, <code>psmisc</code> per killall e pstree, <code>coreutils</code> per nice e sleep. Sulle immagini minime può mancare anche <code>man-db</code>. Solo in quel caso, prepara la VM con:</p>

```bash
sudo apt update
sudo apt install procps psmisc coreutils util-linux man-db
```

<p align="justify"><strong>Per le prove usa l'utente normale, senza sudo.</strong> Agiremo sui processi creati da noi. Digita i blocchi nell'ordine indicato, mantenendo lo stesso terminale per tutta una prova: le variabili con i PID appartengono a quella shell. Esegui ogni prova fino alla chiusura prima di passare alla successiva.</p>

## Osservare: ps, pgrep e top

<p align="justify"><code>ps</code> produce una fotografia dei processi selezionati. Senza opzioni mostra una selezione legata all'utente e al terminale corrente: poche righe non significano che sul sistema esistano soltanto quei processi.</p>

<table align="center">
<thead><tr><th>Comando</th><th>Che cosa osservare</th></tr></thead>
<tbody>
<tr><td><code>ps</code></td><td>Selezione predefinita del terminale corrente.</td></tr>
<tr><td><code>ps aux</code></td><td>Panoramica di tutti i processi, con consumo di CPU e memoria; queste opzioni BSD si scrivono senza trattino.</td></tr>
<tr><td><code>ps -ef</code></td><td>Tutti i processi in formato esteso, con PID e PPID.</td></tr>
<tr><td><code>ps -u "$(id -un)" -o pid,ppid,stat,ni,etime,time,args</code></td><td>Processi dell'utente corrente con colonne scelte esplicitamente.</td></tr>
<tr><td><code>ps -e -o pid,ppid,stat,ni,args --forest</code></td><td>Vista delle relazioni padre-figlio.</td></tr>
<tr><td><code>pstree -p</code></td><td>Albero dei processi con i PID.</td></tr>
<tr><td><code>pgrep -a -u "$(id -u)" -x sleep</code></td><td>PID e comandi dei propri processi con nome esattamente sleep.</td></tr>
</tbody>
</table>

<p align="justify">Preferisci <code>ps aux</code> a <code>ps -aux</code>, che ha un'interpretazione ambigua. Con <code>pgrep</code>, <code>-x</code> richiede il nome esatto; <code>-f</code> estenderebbe la ricerca all'intera riga di comando. Una ricerca senza corrispondenze non stampa righe e restituisce codice 1. <a href="https://man7.org/linux/man-pages/man1/ps.1.html">Manuale ps</a>; <a href="https://man7.org/linux/man-pages/man1/pgrep.1.html">manuale pgrep</a>.</p>

### Leggere le colonne senza confonderle

<table align="center">
<thead><tr><th>Campo</th><th>Lettura</th></tr></thead>
<tbody>
<tr><td><code>PID</code>, <code>PPID</code></td><td>Identificatore del processo e del padre.</td></tr>
<tr><td><code>STAT</code></td><td>Stato principale seguito da eventuali indicatori aggiuntivi.</td></tr>
<tr><td><code>NI</code></td><td>Valore nice; lo useremo nella prova sulle priorità.</td></tr>
<tr><td><code>ETIME</code>, <code>TIME</code></td><td>Tempo trascorso dall'avvio e tempo di CPU accumulato. Un processo può esistere da un minuto e aver usato pochissima CPU.</td></tr>
<tr><td><code>%CPU</code></td><td>In ps, rapporto fra tempo di CPU usato e tempo trascorso dalla partenza; non è una misura istantanea.</td></tr>
<tr><td><code>VSZ</code>, <code>RSS</code></td><td>Dimensione virtuale e memoria residente, espresse da ps in KiB. RSS può comprendere pagine condivise.</td></tr>
<tr><td><code>TTY</code>, <code>COMMAND</code></td><td>Terminale associato e comando; <code>?</code> indica l'assenza di un terminale di controllo.</td></tr>
</tbody>
</table>

<p align="justify">Per riconoscere gli <a href="01_PROCESSI_E_CONCORRENZA.md#stato-e-ciclo-di-vita-di-un-processo">stati già studiati</a>, leggi la prima lettera di <code>STAT</code>:</p>

<table align="center">
<thead><tr><th>Lettera</th><th>Significato in Linux</th></tr></thead>
<tbody>
<tr><td><code>R</code></td><td>In esecuzione oppure pronto a eseguire.</td></tr>
<tr><td><code>S</code></td><td>In attesa interrompibile, per esempio sleep che aspetta lo scadere del tempo.</td></tr>
<tr><td><code>D</code></td><td>In attesa non interrompibile, spesso legata all'I/O.</td></tr>
<tr><td><code>T</code></td><td>Sospeso da un segnale; <code>t</code> minuscolo indica una sospensione dovuta al tracciamento.</td></tr>
<tr><td><code>Z</code></td><td>Terminato, con stato di uscita ancora da raccogliere: zombie.</td></tr>
<tr><td><code>I</code></td><td>Thread del kernel inattivo.</td></tr>
</tbody>
</table>

<p align="justify">Per esempio, <code>SN</code> combina attesa interrompibile e priorità ridotta; <code>+</code> indica l'appartenenza al gruppo in primo piano del terminale. Uno zombie ha già finito di eseguire: inviare KILL non raccoglie il suo stato. Un processo in attesa non interrompibile può non sparire subito neppure dopo KILL. <a href="https://man7.org/linux/man-pages/man5/proc_pid_status.5.html">Stati esposti dal kernel</a>.</p>

### Una vista che si aggiorna

```bash
top -d 1
```

<p align="justify">L'aggiornamento richiesto è di un secondo. Premi <code>P</code> per ordinare per CPU, <code>M</code> per memoria e <code>q</code> per uscire. Per osservare un solo processo, usa <code>top -d 1 -p "$lab_pid"</code> dopo aver assegnato la variabile nella prova 1. In top la percentuale di CPU si riferisce normalmente all'intervallo fra aggiornamenti; il primo campione può essere poco rappresentativo. <a href="https://man7.org/linux/man-pages/man1/top.1.html">Manuale top</a>.</p>

## Segnali: notificare, sospendere, riprendere, terminare

<!-- definition -->
<table align="center">
<tr><td>
&#10071; <strong>Importante</strong>
<p align="justify">Un <strong>segnale</strong> è una notifica che il sistema consegna a un processo o a un suo thread per comunicare un evento. Per ogni tipo di segnale esiste un'azione predefinita; per molti segnali il programma può scegliere di ignorarli o gestirli con una propria funzione.</p>
</td></tr>
</table>
<!-- /definition -->

<p align="justify">Un segnale può arrivare dal kernel, da un altro processo o da un'azione sul terminale. <code>kill</code> è uno strumento per inviarlo. Senza indicare il tipo invia TERM. Usa i nomi simbolici: alcuni numeri cambiano con l'architettura. Per vedere i nomi disponibili:</p>

```bash
kill -l
```

<table align="center">
<thead><tr><th>Segnale</th><th>Azione predefinita</th><th>Uso da ricordare</th></tr></thead>
<tbody>
<tr><td><code>SIGTERM</code></td><td>Termina.</td><td>Richiesta ordinaria di terminazione; il programma può gestirla per completare la chiusura.</td></tr>
<tr><td><code>SIGINT</code></td><td>Termina.</td><td>Normalmente Ctrl+C sul gruppo in primo piano.</td></tr>
<tr><td><code>SIGKILL</code></td><td>Termina forzatamente.</td><td>Non può essere catturato, ignorato o bloccato; il programma non esegue una propria procedura di chiusura.</td></tr>
<tr><td><code>SIGSTOP</code></td><td>Sospende.</td><td>Non può essere catturato, ignorato o bloccato.</td></tr>
<tr><td><code>SIGTSTP</code></td><td>Sospende.</td><td>Normalmente Ctrl+Z; può essere gestito o ignorato.</td></tr>
<tr><td><code>SIGCONT</code></td><td>Riprende un processo sospeso.</td><td>Permette di proseguire dopo STOP o TSTP.</td></tr>
<tr><td><code>SIGHUP</code></td><td>Termina.</td><td>Associato alla perdita del terminale; la rilettura della configurazione esiste solo se prevista dal programma.</td></tr>
<tr><td><code>SIGUSR1</code>, <code>SIGUSR2</code></td><td>Terminano.</td><td>Il programma può assegnare loro una funzione specifica.</td></tr>
<tr><td><code>SIGQUIT</code></td><td>Termina con possibile core dump.</td><td>Normalmente Ctrl+\; la produzione del dump dipende dalla configurazione.</td></tr>
<tr><td><code>SIGCHLD</code></td><td>Ignorato per default.</td><td>Notifica cambiamenti di stato dei figli; il padre deve comunque raccogliere la terminazione quando richiesto.</td></tr>
</tbody>
</table>

<p align="justify">Bloccare un segnale ne rinvia la consegna; ignorarlo scarta la notifica. Le occorrenze ripetute di uno stesso segnale standard pendente non costituiscono un contatore affidabile. Linux supporta anche segnali real-time, con regole diverse. L'effetto di ripresa di CONT avviene anche se il segnale è bloccato; un eventuale gestore può essere eseguito in seguito. <a href="https://man7.org/linux/man-pages/man7/signal.7.html">Manuale signal(7)</a>.</p>

<p align="justify">Negli esercizi inviamo segnali a <strong>PID positivi appena acquisiti</strong>. In condizioni ordinarie un utente può segnalare i propri processi; per altri utenti servono permessi adeguati. <code>kill -0 "$lab_pid"</code> controlla esistenza e permessi senza inviare una notifica: il successo non dimostra che il processo stia lavorando correttamente. Anche uno zombie può risultare presente. <a href="https://man7.org/linux/man-pages/man2/kill.2.html">Manuale kill(2)</a>.</p>

## Prova 1: seguire un processo con ps e kill

<p align="justify">Avvia un'attesa di cinque minuti in background e conserva subito il suo PID:</p>

```bash
sleep 300 &
lab_pid=$!
printf 'PID del laboratorio: %s\n' "$lab_pid"
ps -p "$lab_pid" -o pid,ppid,stat,ni,etime,time,args
```

<p align="justify"><code>&amp;</code> restituisce il prompt mentre il comando continua; <code>$!</code> contiene il PID dell'ultimo comando avviato in background. La riga di ps dovrebbe mostrare sleep in stato <code>S</code>, CPU quasi nulla e PPID della shell. <code>echo "$$"</code> mostra il PID di Bash.</p>

<p align="justify">Sospendi il processo, osserva, poi riprendilo e osserva ancora. Digita una riga alla volta:</p>

```bash
kill -STOP "$lab_pid"
ps -p "$lab_pid" -o pid,stat,args
kill -CONT "$lab_pid"
ps -p "$lab_pid" -o pid,stat,args
```

<p align="justify"><strong>Atteso:</strong> dopo STOP compare <code>T</code>; dopo CONT sleep torna normalmente in <code>S</code>, perché deve ancora attendere. Riprendere un processo non implica che stia usando la CPU. Se il campionamento è troppo rapido, ripeti ps.</p>

<p align="justify">Puoi anche leggere le informazioni esposte dal kernel:</p>

```bash
cat "/proc/$lab_pid/status"
tr '\0' ' ' < "/proc/$lab_pid/cmdline"
printf '\n'
```

<p align="justify">Cerca <code>Name</code>, <code>State</code>, <code>Pid</code> e <code>PPid</code>. Gli argomenti in cmdline sono separati da byte nulli; tr li rende leggibili. Ora termina e raccogli l'esito del figlio:</p>

```bash
kill -TERM "$lab_pid"
wait "$lab_pid"
lab_esito=$?
printf 'Esito raccolto da Bash: %s\n' "$lab_esito"
ps -p "$lab_pid" -o pid,stat,args
unset lab_pid lab_esito
```

<p align="justify"><strong>Atteso:</strong> Bash può stampare una notifica di terminazione; per TERM l'esito è normalmente 143, cioè 128 + 15. Dopo wait, ps non mostra più la riga. Il comando wait della shell attende un proprio figlio e ne raccoglie l'esito; qui non è la funzione C <code>wait()</code>. Se trascorrono cinque minuti, sleep può terminare da solo: riparti dall'avvio per ripetere la prova.</p>

## Prova 2: Ctrl+Z, jobs, bg e fg

<!-- definition -->
<table align="center">
<tr><td>
&#10071; <strong>Importante</strong>
<p align="justify">Un <strong>job della shell</strong> è un comando, o una pipeline di comandi, che Bash gestisce come un'unità. Il numero del job identifica quell'attività nella shell corrente; il PID identifica un processo nel sistema.</p>
</td></tr>
</table>
<!-- /definition -->

<p align="justify">In un terminale Bash nuovo esegui:</p>

```bash
sleep 300
```

<ol>
  <li>Premi <strong>Ctrl+Z</strong>: il comando viene sospeso e ritorna il prompt.</li>
  <li>Esegui <code>jobs -l</code>: annota numero del job, PID e stato.</li>
  <li>Esegui <code>bg %1</code>: riprende in background. Se jobs mostra un altro numero, sostituisci <code>%1</code>.</li>
  <li>Esegui <code>jobs -l</code>: il job risulta in esecuzione. Bash indica che non è sospeso, anche se sleep attende e ps mostra <code>S</code>.</li>
  <li>Esegui <code>fg %1</code>: riporta il job in primo piano; premi <strong>Ctrl+C</strong> per terminarlo.</li>
  <li>Esegui <code>jobs -l</code> per verificare che il job sia concluso.</li>
</ol>

<p align="justify"><code>%1</code> non significa PID 1. <code>jobs</code> conosce le attività avviate da quella shell, mentre ps osserva i processi del sistema. Le combinazioni di tasti agiscono sul gruppo di processi in primo piano, che può contenere più processi. <a href="https://man7.org/linux/man-pages/man1/bash.1.html">Manuale Bash, sezioni JOB CONTROL e SIGNALS</a>.</p>

## Prova 3: nice e renice

<!-- definition -->
<table align="center">
<tr><td>
&#10071; <strong>Importante</strong>
<p align="justify">Il <strong>valore nice</strong> influenza la priorità relativa di CPU delle normali attività pianificate da Linux. Va da <strong>-20</strong>, più favorevole, a <strong>19</strong>, meno favorevole. Aumentare il numero riduce la priorità relativa.</p>
</td></tr>
</table>
<!-- /definition -->

<p align="justify"><code>nice</code> avvia un comando applicando un incremento al valore ereditato; <code>renice</code> interviene su un processo già esistente. In Ubuntu useremo <code>renice 15 -p PID</code> per impostare il valore assoluto 15: questa forma evita le differenze che l'opzione <code>-n</code> può avere in presenza di <code>POSIXLY_CORRECT</code>.</p>

```bash
ps -p "$$" -o pid,ni,args
nice -n 10 sleep 300 &
lab_pid=$!
ps -p "$lab_pid" -o pid,ni,stat,args
renice 15 -p "$lab_pid"
ps -p "$lab_pid" -o pid,ni,stat,args
```

<p align="justify"><strong>Atteso con shell a NI=0:</strong> il nuovo processo parte a 10 e passa a 15; <code>STAT</code> può mostrare <code>SN</code>. Per questa prova parti da una shell con NI=0. Se il valore iniziale è diverso, anche il risultato di nice cambia.</p>

<p align="justify">Con l'utente normale prova a riportarlo a zero:</p>

```bash
renice 0 -p "$lab_pid"
```

<p align="justify"><strong>Atteso nella configurazione ordinaria:</strong> permesso negato. Senza privilegi o limiti appositamente configurati puoi aumentare il nice dei tuoi processi, ma non diminuirlo, neppure per annullare la modifica precedente. Chiudi la prova:</p>

```bash
kill -TERM "$lab_pid"
wait "$lab_pid"
unset lab_pid
```

<p align="justify">Sleep rende visibile NI, ma non misura una differenza di prestazioni: attende senza contendere la CPU. Il nice non è un limite percentuale di CPU e non garantisce un rapporto fisso fra tempi di esecuzione; contano carico, CPU disponibili e raggruppamento delle attività. <a href="https://man7.org/linux/man-pages/man1/nice.1.html">Manuale nice</a>; <a href="https://manpages.ubuntu.com/manpages/noble/man1/renice.1.html">renice su Ubuntu</a>.</p>

## Prova 4: selezionare per nome con killall

<p align="justify">In Linux <code>killall</code> invia un segnale a tutti i processi che corrispondono ai nomi indicati. Senza segnale esplicito usa TERM. Per scegliere un solo processo usa il PID con kill; per scegliere un nome controlla prima le corrispondenze con pgrep.</p>

<p align="justify">Creiamo due copie in esecuzione di sleep con un nome temporaneo comune, così la prova seleziona soltanto queste. <code>mktemp</code> crea una directory nuova; <code>cp</code> vi copia l'eseguibile con un nome breve e distinto:</p>

```bash
lab_dir=$(mktemp -d /tmp/tpsi-XXXXXX)
lab_nome=${lab_dir##*/}
cp /usr/bin/sleep "$lab_dir/$lab_nome"
"$lab_dir/$lab_nome" 300 &
lab_pid_a=$!
"$lab_dir/$lab_nome" 300 &
lab_pid_b=$!
pgrep -a -u "$(id -u)" -x "$lab_nome"
```

<p align="justify"><strong>Atteso:</strong> due righe con i PID appena creati. <code>${lab_dir##*/}</code> ricava il nome finale della directory. Invia TERM chiedendo conferma per ogni corrispondenza:</p>

```bash
LC_ALL=C killall -i -u "$(id -un)" -s TERM -- "$lab_nome"
```

<p align="justify">Rispondi <code>y</code> a entrambe le richieste. <code>LC_ALL=C</code> rende prevedibile la lingua della conferma; <code>-u</code> limita la selezione al tuo utente; <code>-i</code> chiede conferma. Controlla e rimuovi soltanto il materiale temporaneo di questa prova:</p>

```bash
wait "$lab_pid_a"
wait "$lab_pid_b"
pgrep -a -u "$(id -u)" -x "$lab_nome"
rm -- "$lab_dir/$lab_nome"
rmdir -- "$lab_dir"
unset lab_dir lab_nome lab_pid_a lab_pid_b
```

<p align="justify"><strong>Atteso:</strong> pgrep non trova più corrispondenze. Se rifiuti una conferma, quel processo continua: terminalo con il suo PID prima di eseguire wait. Evita nomi generici come bash: selezionerebbero anche altre sessioni. Il comportamento descritto riguarda killall di Linux; altri sistemi UNIX possono attribuire al comando significati diversi. <a href="https://manpages.ubuntu.com/manpages/noble/man1/killall.1.html">Manuale killall</a>.</p>

## Prova 5: un programma che gestisce TERM e USR1

<p align="justify">Qui osserviamo la differenza fra il segnale ricevuto e la risposta scelta dal programma. In un primo terminale esegui il blocco seguente. Avvia una Bash dedicata, che stampa il proprio PID e resta attiva al massimo circa un minuto:</p>

```bash
bash <<'BASH'
trap 'printf "Richiesta USR1 ricevuta\n"' USR1
trap 'printf "Chiusura richiesta con TERM\n"; exit 0' TERM
trap 'printf "Procedura finale eseguita\n"' EXIT
printf "Pronto. PID da usare nel secondo terminale: %s\n" "$$"
for ((passo=0; passo<60; passo++)); do
    sleep 1
done
BASH
```

<p align="justify">Attendi il messaggio <code>Pronto</code>. Nel secondo terminale assegna alla variabile il PID stampato, poi osserva il destinatario prima di inviargli segnali:</p>

```bash
read -r -p 'PID stampato nel primo terminale: ' lab_pid
ps -p "$lab_pid" -o pid,user,args
kill -USR1 "$lab_pid"
```

<p align="justify"><strong>Atteso nel primo terminale:</strong> compare il messaggio della richiesta e il processo continua. Invia poi:</p>

```bash
kill -TERM "$lab_pid"
unset lab_pid
```

<p align="justify">Il programma stampa il messaggio di chiusura, esegue la procedura finale e termina. Bash può rinviare il gestore finché il comando sleep corrente ritorna: la risposta può richiedere circa un secondo.</p>

<p align="justify">Ripeti l'avvio nel primo terminale, acquisisci il <strong>nuovo PID</strong> nel secondo e, dopo averlo verificato con ps, invia <code>kill -KILL "$lab_pid"</code>. Questa volta il programma non esegue i messaggi di chiusura né la procedura finale. La shell esterna può scrivere <code>Killed</code> e riportare il testo del comando terminato: quel testo non è l'esecuzione dei gestori. Elimina la variabile con <code>unset lab_pid</code>.</p>

<p align="justify">Il comando <code>trap</code> di Bash associa azioni ai segnali; in C useremo <code>sigaction</code>, con vincoli specifici sulle funzioni eseguibili nel gestore. Il trap EXIT è un evento della shell, non un segnale Linux. <a href="02_COMUNICAZIONE_E_SINCRONIZZAZIONE.md#segnali-notifiche-non-contenitori-generici">Prosegui con i segnali nel modulo 2</a>.</p>

## Che cosa aggiornare rispetto alle pagine storiche

<table align="center">
<thead><tr><th>Argomento</th><th>Indicazione per Ubuntu attuale</th></tr></thead>
<tbody>
<tr><td>ps, nice, renice, kill, killall</td><td>Sono ancora utilizzabili. Preferire opzioni esplicite, nomi dei segnali e PID acquisiti durante la prova.</td></tr>
<tr><td>Stato S</td><td>Indica attesa interrompibile; non va interpretato come un'attesa inferiore a 20 secondi.</td></tr>
<tr><td>RSS in ps</td><td>È espresso in KiB, non in numero di pagine.</td></tr>
<tr><td>CONT e maschera dei segnali</td><td>La ripresa avviene anche se CONT è bloccato; la consegna al gestore può restare pendente.</td></tr>
<tr><td>top</td><td>Impostare il periodo con <code>-d 1</code>; l'interfaccia e le opzioni attuali si consultano con <code>h</code> o <code>man top</code>.</td></tr>
<tr><td>init, xinetd e servizi</td><td>Nelle normali VM Ubuntu moderne PID 1 è systemd. Verifica con <code>ps -p 1 -o pid,comm,args</code>. Gli esempi sui vecchi servizi dipendono da ciò che è installato; per un servizio gestito da systemd si consulta prima <code>systemctl status NOME.service</code>.</td></tr>
<tr><td>HUP come “ricarica”</td><td>È una convenzione di alcuni programmi. Prima di usarlo controllare il manuale del servizio: l'azione predefinita è terminare.</td></tr>
<tr><td>Processi con molto carico</td><td>Osservare CPU, memoria e stato prima di intervenire. La sequenza didattica è identificare, inviare TERM, verificare e ricorrere a KILL soltanto se necessario.</td></tr>
</tbody>
</table>

<p align="justify">Per approfondire l'osservazione puoi consultare <code>man proc</code> e <code>man strace</code>. Quest'ultimo permette di avviare un programma sotto osservazione, per esempio <code>strace sleep 1</code>, se il pacchetto strace è installato. Le chiamate mostrate dipendono da kernel, architettura e librerie.</p>

## Verifica rapida

<ol>
  <li>Perché sleep compare in ps anche quando TIME è quasi zero?</li>
  <li>Quale differenza osservi fra STOP, CONT e TERM?</li>
  <li>Perché USR1 termina alcuni programmi e fa stampare un messaggio nella prova 5?</li>
  <li>Se il nice della shell vale 5, quale valore richiede <code>nice -n 10</code> per il nuovo comando? Che cosa imposta <code>renice 15 -p PID</code>?</li>
  <li>Quando useresti kill e quando killall? Quale controllo faresti prima?</li>
  <li>Perché Ctrl+Z non equivale a Ctrl+C? Perché il job “Running” può apparire come S in ps?</li>
</ol>

<p align="justify"><strong>Consegna:</strong> per ogni prova annota PID, comando e stato osservato. Allega una spiegazione della differenza fra sospensione, attesa e terminazione e verifica di aver chiuso i processi creati.</p>

## Fonti e note di revisione

<ul>
  <li>Spunto didattico: immagini del capitolo sul controllo dei processi del manuale di amministrazione di sistema di Nemeth e coautori, nella <a href="https://github.com/TheBitPoets/2cornot2c/blob/main/LINUX_PROGRAMMING.md#controllo-dei-processi">sezione indicata di 2cornot2c</a>, in particolare segnali, kill/killall, nice/renice e ps/top. Testo ed esercizi di questa scheda sono originali.</li>
  <li>Osservazione: <a href="https://man7.org/linux/man-pages/man1/ps.1.html">ps</a>, <a href="https://man7.org/linux/man-pages/man1/pgrep.1.html">pgrep</a>, <a href="https://man7.org/linux/man-pages/man1/top.1.html">top</a>, <a href="https://man7.org/linux/man-pages/man5/proc_pid_status.5.html">proc_pid_status</a>.</li>
  <li>Priorità: <a href="https://man7.org/linux/man-pages/man1/nice.1.html">nice</a> e <a href="https://manpages.ubuntu.com/manpages/noble/man1/renice.1.html">renice su Ubuntu 24.04</a>.</li>
  <li>Segnali e shell: <a href="https://man7.org/linux/man-pages/man7/signal.7.html">signal(7)</a>, <a href="https://man7.org/linux/man-pages/man2/kill.2.html">kill(2)</a>, <a href="https://manpages.ubuntu.com/manpages/noble/man1/killall.1.html">killall su Ubuntu 24.04</a>, <a href="https://man7.org/linux/man-pages/man1/bash.1.html">Bash</a>.</li>
  <li>Ambiente del corso: Ubuntu 24.04.3 LTS nella macchina virtuale, versione confermata dal docente.</li>
  <li>Verifica pratica del 26 settembre 2026: le cinque prove sono state eseguite su Ubuntu 24.04 in WSL, con utente senza privilegi, procps-ng 4.0.4 e util-linux 2.39.3. Verificati anche job control in un terminale e conferme interattive di killall. Il collaudo è stato svolto nell'ambiente locale WSL; l'esecuzione sulla VM del corso resta da effettuare.</li>
  <li>Stato: <code>draft</code>; documentazione consultata il 26 settembre 2026.</li>
</ul>
