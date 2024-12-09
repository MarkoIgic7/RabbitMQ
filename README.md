# RabbitMQ
Ovaj ReadMe file sadrzi osnovne informacije o RabbitMQ-u, kako bi mogla da se stekne bolja slika i uvid u samu tehnologiju. Osim toga poseduje i delove koji su posveceni prakticnom radu, kako bi se blize pojasnili sami primeri iz repozitorijuma.


## Sta je RabbitMQ
RabbitMQ je sistem za razmenu poruka, koji prihvata i prosledjuje poruke izmedju aplikacija i servisa. Jednostavno receno to je software gde se definisu queue-ovi, za koje se “zakace” - povezu aplikacije kako bi ucestvovale u razmeni poruka. On se ponasa kao middleware koji se bazira na AMQP-u (Advance Message Queuing Protocol). Poruke koje se prenose mogu da prenose razlicite informacije. Mogu na primer da sadrze neku obicnu poruku, ali mogu da budu i neki task koji treba da bude pokrenut u nekoj drugoj aplikaciji.

## Kljucne karakteristike RabbitMQ-a
Osnovni pojmovi koji se koriste u RabbitMQ-u su:
**Producer** - program koji salje poruku
**Queue** - Struktura podataka kroz koju prolaze poruke do odredista (druga aplikacija/mikroservis). To je zapravo veliki bafer poruka, cija je velicina ogranicena memorijom diska (host-a). Jedan queue moze da koristi veci broj producer-a i consumer-a.
**Consumer** - program koji je zaduzen za prihvatanje i obrade poruke
**Exchange** - prihvata poruke od producera i prosledjuje ih do queue-eva u zavisnosti od pravila koja su definisana za taj exchange. Da bi primio poruku, queue mora da bude povezan na najmanje jedan exchange
**Binding** - veza izmedju Queue-a i Exchange-a.
**Routing key** - key koji sugerise Exchange-u kako treba da rutira poruku ka Queue-u.

![workflow-rabbitmq](https://github.com/user-attachments/assets/06fee73a-adc5-42e5-b01e-3c53d3da8164)

> ⚠️ Jedna aplikacija moze istovremeno da bude i producer i consumer.

### Osnovne karakteristike:

### 1. **Arhitektura zasnovana na queue-ovima**
   
   Queue u RabbitMQ-u je uredjena kolekcija poruka. Poruka se ubacuju i citaju iz queue-a po FIFO redosledu. (Ubacuju se ne kraj reda, a citaju se sa pocetka). Svaki queue ima ime na koje aplikacija moze da se referencira. Unutar aplikacije moze da se definise ime queue-a, a moguce je i da broker sam izgenerise ime. Imena queue-ova mogu da budu velicne do 255 byte-ova. U nastavku su navedene neka glavna podesavanja queue-ova.

  - **name** - ime queue-a
  - **durable** - definise da li ce queue da “prezivi” restart brokera
  - **exclusive** - definise da se queue koristi samo od strane jedne konekcije, i da se brise kada se ta konekcija zatvori
  - **auto-delete** - queue koji ima minimalno jednog consumera, ce da bude obrisan kada se taj consumer unsubscribe-uje

### 2. **Podrska za vise protokola**
   
   RabbitMQ po default-u koristi AMQP (0-9-1), ali ima podrsku i za MQTT i  STOMP protokole. AMQP se nametnuo kao pionir, pre svega zbog bogate mogucnosti za potvrdjivanje poruka, trajno skladistenje poruka kao i slozeno i napredno rutiranje poruka (pomocu exchange model-a)

### 3. **Integracija**
   
   RabbitMQ ima mogucnost integracije sa razlicitim programskim jezicima: Python, Java, Ruby, PHP, .NET, Javascript, Go, Swift …

### 4. **Slozen model rutiranja**
   
   Poruke se ne salju direktno na queue. Umesto toga producer salje poruke do exchange-a. Exchange je zaduzen za rutiranje poruka do razlictih queue-ova pomocu binding i routing key-eva. Binding je veza izmedju queue-a i exchange-a.

#### Flow slanja poruka u RabbitMQ-u
1. Producer salje poruku do Exchange-a. Kada se pravi Exchange mora da se definise njegov tip.

2. Exchange je prihvatio poruku i sada je zaduzen za njeno rutiranje do odgovarajuceg Queue-a.

3. Mora da se napravi veza izmedju Exchange-a i Queue-a.

4. Poruke ostaju u Queue-u sve dok ne budu handle-ovane

5. Consumer preuzima i obradjuje poruke

  ![Screenshot 2024-12-09 at 16 59 35](https://github.com/user-attachments/assets/876306ac-31da-456c-b865-27e745c0e068)

#### Tipovi exchange-a
1. Direct Exchange dostavlja poruku do Queue-a bazirano na routing key-u. Poruka ce da bude isporucena queue-evima ciji se binding key poklapa sa routing key-em poruke.
Poruka sa routing key-em: pdf_log, ce da bude prosledjena excahnge-u a on ce da je rutira to pdf_log_queue-a zato sto se routing key i binding key poklapaju. Ako se routing key ne poklapa ni sa jednim binding key-em, poruka se discarduje.

![Screenshot 2024-12-09 at 17 02 18](https://github.com/user-attachments/assets/20135df2-1efb-44ff-893f-244a1e3b46ce)

2. Fanout exchange kopira poruke i prosledjuje ih svim queue-ovima bez obzira na podudaranje routing i bindind key-eva. Ovaj tip exchange-a se uglavnom koristi kada je neophodno poruku proslediti svim consumerima (koji mogu na razlicite nacine da obradjuju tu poruku).

![Screenshot 2024-12-09 at 17 03 39](https://github.com/user-attachments/assets/8fe3c418-f055-4295-b902-d1e630ee3f1a)

3. Topic exchange vrsi rutiranje poruka u zavisnosti od poklapanja routing key-a sa definisanim sablonom. Routing key mora da bude lista reci razdvojenih tackom (.). Na primer : agreements.eu.serbia. Routing sablon moze da sadrzi zvezdicu (*), koja zamenjuje rec na odredjenoj poziciji (“agreements.*.*.nis.*”  se podudara sa  routing key-evima cija je priva rec agreements i cetvrta rec nis). Znak tarabe (#) ima znacenje - jedna ili vise reci. (routing sablon “agreements.balkan.serbia.#” se poklapa sa bilo kojim routing key-em koji pocinje sa “agreements.balkan.serbia”). Consumer navodi teme koje su mu od interesa po odgovarajucem sablonu. Ukoliko se routing key,poruke koja se salje, podudara sa temama consumera, poruka ce biti isporucena.

> 💡 Primer: Vrsi se slanje poruke sa routing key-em : agreements.eu.berlin. Poruka se prosledjuje Queue-u A, jer agreements.eu.berlin odgovara agreements.eu.berlin.#, prosledjuje se Queue-u B, jer agreements.eu.berlin odgovara agreements.#, ali se NE prosledjuje Queue-u C jer agreements.eu.berlin NE odgovara agreements.eu.*.store.

![Screenshot 2024-12-09 at 17 04 57](https://github.com/user-attachments/assets/a41db410-cd39-48d2-baaf-1e0f4563378a)

### 5. **Pouzdanost**

Prva stvar koja garantuje pouzdanost je to sto poruke nece biti izgubljene, uz odgovarajuca podesavanja zato sto RabbirMQ moze da skladisti poruke na disku i na taj nacin omogucava ponovno slanje nakon ponovnog pokretanja.

Potvrda isporuke je jos jedna od karakteristika pouzdanosti, zato sto RabbitMQ ima mogucnost potvrde isporuke, kako produceru tako i consumeru. Ukoliko consumer prestane sa radom tokom isporuke, moguce je da se poruka vrati u queue, i ponovo dodeli nekom od consumera.

Trajnost poruka (message durability) - omogucava da redovi opstaju nakon restartovanja servera (RabbitMQ servera) i da se poruke cuvaju na disku. Kombinacija ova dva omogucava visko stepen pouzdanosti. Medjutim ovo ne mora nuzno da garantuje da poruka nece da bude izbrisana, zato sto postoji vremenski slot izmedju trenutka kada RabbitMQ prihvati poruku i sacuva je - (moze da se desi da je sacuvao u cache-u ali ne i na disku). Ali ovo je za neke osnovne potrebe sasvim dovoljno, postoje i naprednije funkcionalnosti za veci stepen perzistencije.

## Prednosti Rabbit-a

- Centralizovan sistem, koji upravlja porukama na jednom mestu, cime se smanjuje slozenost sistema
- Podrzava razlicite tipove razmene poruka: direct, fanout, topic, headers
- Koristi mehanizam potvrde poruka (ACK) cime se osigurava isporuka poruka
- Nudi fleksibilne mogucnosti za rutiranje poruka (patterns)
- Open source projekat
- Sistem je u velikoj meri konfigurabilan (rutiranje, skaliranje)
- Poprilicno veliki obim poruka koje moze da isporuci (do 1 000 000 poruka u sekundi - uz adekvatnu konfiguraciju)
- Podrska za autentifikaciju (zasnovano na lozinkama) - cime se upravlja korisnickim pristupom

## Mane Rabbit-a

- Nije optimizovan za velike kolicine podataka (Big Data). U takvim slucajevim bolje solucija je Apache Kafka umesto Rabbit-a.
- Iako je sistem open-source i ne zahteva placanje, napredni servisi i profesionalna podrska mogu zahteati dodatne troskove
- Sistem je centralizovan (jedan klaster), gde u slucaju povecanja obima poruka, moze da dodje do zagusenja pri cemu performanse mogu poprilicno da padnu
- Horizontalna skalabilnost (dodavanje cvorova) ima ogranicenje, moze da postane dosta slozen sistem za odrzavanje sa velikim brojem cvorova.

## Kada izabrati RabbitMQ - problem koji resava

Osim RabbitMQ-a, postoje i drugi messaging brokeri, ali se sam RabbitMQ pokazao kao dobro resenje u nekim izazovima kao sto su : 

### Slozeno rutiranje

RabbitMQ je dobro resenje kada postoji problem sa slozenim rutiranjem, zato sto pruza potpunu kontrolu u procesu rutiranja poruka. On omogucava da se citav sistem konfigurise tako da se rutiranje vrsi u odnosu na neki od uslova - sadrzaj poruke, prioritet poruke ili neki personalizovan uslov.

### Prioritetni queue-ovi

Ovo omogucava prioretizovanje nekih poruka u odnosu na druge. Koriscenjem prioritetnih queue-ova, garantuje se da ce poruke koje su oznacene kao prioritetne, sigurno da budu prve procesirane bez obzira na opterecenost sistema.

### Protokoli

RabbitMQ pruza podrsku za rad sa razlicitim protokolima komunikacije.

### Pouzdanost

RabbitMQ ima mehanizme kojim se garantuje isporucivanje poruka. Ukoliko dodje do otkaza aplikacije (consumer-a), poruka ce se ponovo poslati od queue-a prema consumeru. Osim ovoga, podrzana je i funkcionalnost perzistiranja poruka, tj. trajno cuvanje poruka na disku.

### Obrada dugotrajnih zahteva

Kod dugotrajnih zadataka kao sto je uploadovanje dokumenata, slika i drugih medija, za koje je nophodno da postoji neka obrada, pogodno je koristiti Rabbit. On omogucava da se podesi konfiguracija tako da se uploadovanje - slanje podataka izvrsi tek nakon sto je obrada zavrsena. Osim toga moguce je da se slanje poruka vrsi, a da se obrada poruka vrsi u pozadini.

## Konkurenta resenja - uporediti

Osim RabbitMQ-a, messaging brokeri koji su se istakli i nametnuli na trzistu su i Apache Kafka i ActiveMQ. U nastavku ce biti uporedjeni ovi brokeri po odredjenim karakteristikama

### Performanse i skalabilnost

1. Kafka - upectaljiva po velikoj propusnosti i horizontalnoj skalabilnosti. Odlicna za obradu velike kolicine podataka
2. RabbitMQ - dobre performanse (za manje projekte), ali ne kao Kafka kad je rec o Big Data i velikoj propusnosti. Horizontalna skalabilnost
3. ActiveMQ - dobre performanse (za manje projekte), ali ne kao Kafka kada je rec o BigData i velikoj propusnosti

### Prioritizacija poruka

1. Kafka - nema ugradjenu funkcionalnost za prioretizaciju poruka, vec sve poruke tretira podjednako i distrubira ih do particija, respektivno
2. RabbitMQ - podrzava prioretizaciju poruka, tako sto se kreiraju queue-vi sa prioritetom. Umesto defaultnog FIFO redosleda, broker ce prosledjivati prvo poruka sa vecim prioritetom.
3. ActiveMQ - podrzava prioretizaciju poruka

### Trajnost poruka

1. Kafka - Trajnost poruka se ogleda u nacinu na koji Kafka upravlja porukama na disku i koliko ih dugo zadrzava. Kod Kafke je moguce definisati vreme zadrzavanje poruke ili maksimalnu velicinu diska koja ce da se koristi za svaku particiju. Takodje poruke mogu da budu oznacene kao trajne.
2. RabbitMQ - podrzano, kroz konfiguraciju (durable queues, persistent messages). Perzistente poruke se cuvaju na disku. Jos jedan mehanizam koji doprinosi trajnosti poruka je potvrdjivanje poruka da su dostavljene i obradjene od strane potrosaca. Ovo moze uticati na performanse sistema, tako da bi bilo dobri naci balans izmedju trajnosti poruka i brzine obrade poruka.
3. ActiveMQ - podrzano, kroz konfiguraciju (durable queues, persistent messages). Perzistente poruke se prvo cuvaju na disku, pa se tek onda prosledjuju consumeru.Ovo moze uticati na performanse sistema, tako da bi bilo dobri naci balans izmedju trajnosti poruka i brzine obrade poruka.

### Rutiranje poruka

1. Kafka - na osnovu particionasnja u okviru topica
2. RabbitMQ - pomocu exchange-a i bindinga
3. ActiveMQ - koristeci selektore i topice

### Replikacija

1. Kafka - ugradjena replikacija prilikom kreiranja topica (replication factor)
2. RabbitMQ - replikacija nad redovima. Mirrored Queues je klascina replikacija redova. Quorum queues koristi Raft algoritam (u pozadini ima jednog lidera i kopije), podaci se repliciraju na vise cvorova unutar klastera. Federated Queues omogucava replikaciju queue-ova izmedju klastera.
3. ActiveMQ - master/slave replikacija. Master prima poruke i salje ih do svih slave-ova. Ukoliko master otkaze, bira se slave.

## Projekti

U repozitorijumu nalazi se 5 (mini) projekta, kako bi se efikasnost i raznovrsnost Rabbit-a prikazala na najbolji moguci nacin.

Kako bi projekti bili pokrenuti neophodne je postaviti okruzenje kako bi bilo moguce reprodukovanje projekata. Inicijalno projekti su razvijeni na macOS-u. Neophodno je ispratiti sledece korake : 

**MacOS**
	
1. Instalirati python (preporucljivo od verzije 3.9 pa navise)
2. Instalirati homebrew (ukoliko ne postoji)
3. brew install rabbitmq		//instalacija rabbitmq-a
4. brew services start rabbitmq	//pokretanje rabbitmq servera
5. python3 -m pip install pika –upgrade	// Ovo se koristi za instalciju pika koji implementira AMQP
6. pokrenuti python skripte iz komandne linije

**Windows**

1. Instalirati python (preporucljivo od verzije 3.9 pa navise)
2. Preuzeti Erlang (https://www.erlang.org/downloads)
3. Dodati Erlang-ov bin direktorijum u sistemsku promenljivu PATH
4. Preuzeti RabbitMQ sa zvanicnog sajta
5. Instalacija RabbitMQ-a
6. Pokretanje RabbitMQ-a -> rabbitmq-server
7. (opciono) aktiviranje RabbitMQ Management plugin-a -> rabbitmq-plugins enable rabbitmq_management
8. Instaliranje “pika” biblioteke -> pip install pika
9. pokrenuti python skripte iz komande linije

*Pre pokretanja projekata neophodno je pokrenuti rabbitmq server, dok je preporuka po zavrsetku ugasiti ga kako ne bi trosio resurse nepotrebno. Postoji i GUI koji se pokrece na portu 15672 uz kredencijala username:guest, password: guest.*

### Round-Robin

Cilj ovog mini projekta je da se na najjednostavniji nacin prikaze na koji nacin tece komunikacija i razmena poruka (raspodela Taskova) izmedju Producera i Consumera. Task bi u realnom primeru mogla da bude obrada slika ili pdf dokumenta. Na taj nacin Taskovi ne bi cekali da Consumer zavrsi posao koji radi. Ovaj pristup se koristi cesto u web aplikacijama gde je nemoguce obraditi slozeni zahtev u kratkom vremenskom intervalu. Ovim se postize paralelizacija procesa, gde je skaliranje vrlo jednostavno dodavanjem novog cvora - Consumera. Kod ovog projekta kada bi se pokrenulo 2 ili vise Consumera poruke bi se prosledjivale po (defaultnom) Round-Robin principu.

Na ovom primeru moze da se vidi situacija gde je queue eksplicitno definisan (queue_name) i u Consumeru i u Produceru, tj. ne koristi se Exchange, pa nije neophodno da consumer bude pokrenut pre slanja poruka. Kako bi se simulirala situacija koja prikazuje Round-Robin raspodelu treba ispratiti sledeci flow:
1. Pokrenuti Consumera (python3 Consumer.py)
2. Pokrenuti drugog Consumera u novom terminalu (python3 Consumer.py)
3. Pokrenuti treceg Consumera u novom terminalu (python3 Consumer.py)
4. Pokrenuti nekoliko puta Producer-a, ali iz jedne linije kako bi se poslalo veci broj poruka istovremeno. Poruka koja se salje se prosledje kao prvi argument komande linije (python3 Producer.py Prva_poruka && python3 Producer.py Druga_poruka && python3 producer.py Treca_poruka && python3 Producer.py Cetvrta_poruka)

### Work queues

Ovaj projekat predstavlja neki vid nadogradnje prethodnog. U poredjenu sa prethodnim gde su se Taskovi tj. poruke dodeljivale po Round-Robin algoritmu, u ovom projektu se taskovi dodeljuju tek nakon sto je poruka obradjena (channel.basic._ack(prefetch_count=1)). Osim toga dodat je jedan vid trajnosti poruka (potvrdjivanje poruka) cime se garantuje isporuka poruka, tj da ce poruka da bude isporucena ukoliko queue ne dobije potvrdu za odredjenu poruku.

> 💡 : Ako Consumer crashuje,a nije poslao ACK poruku. To je znak RabbitMQ-u da je Consumer neplanirano stao i da poruka nije obradjena na adekvatan nacin, i RabbitMQ ce poruku da prosledi nekom drugom Consumeru. Acknowledgment poruka MORA da se posalje na isti kanal na koji je i stigla originalna poruka.

Ovaj projekat bi mogao da se poboljsa (sledece 2 slike) u situaciji kada RabbitMQ server prestane sa radom. Kako Queue-evi i poruke ne bi nestale, neophodno je oznaciti i Queue i poruke da se cuvaju (durable)
> ⚠️ RabbitMQ ne dozvoljava da se menjaju podesavanja vec postojecih Queue-ova!

Uputstvo za pokretanje Work queues projekta:
1. Pokrenuti Consumere (vise njih - svaki u zasebnom terminalu)
2. Pokrenuti Producera nekoliko puta odjednom. Svaka komanda za pokretanje Producera treba preko argumenta komande linije da primi String koji sadrzi nekoliko tacaka. Svaka tacka simulira vreme (u sekundama) koje je neophodno za obradu te poruke. Na ovaj nacin moze da se vidi da ce na primer prvi COnsumer da obradjuje poruku Prva_poruka…., a drugi Consumer poruke : Druga_poruka. i poruku Treca_poruka.

Kroz ovaj primer moze da se vidi kako je moguce da se poslovi ne dele po RoundRobin principuu, nego tek po obradjenom poslu da Consumer prima naredni zadatak(Task)
Ukoliko neki od Consumera prestane sa radom, poruka ce opet da se izgenerise ka nekom drugom Consumeru zbog auto_ack taga

### Publish/Subscribe

Umesto jednog Consumera kao sto je bilo implementirano u prethodnim projektima u ovom orjektu je situacija da se jedna poruka isporucuje vecem broju Consumera, poznatije kao i Publish/Subscribe princip. 

U principu sam smisao RabbitMQ-a je ta Producer NIKADA ne salje direktno poruku na Queue, vec da se to radi preko posrednika -> EXCHANGE. On je kao neki manager koji odredjue i zna sta ce da radi sa porukom i gde da je prosledi.

U prethodnim primerima exchange nije bio definisan, i “rutiranje” se radilo samo na osnovu imena Queue-a (sto nije slucaj u ovom primeru). U ovom primeru je iskoriscen mehanizam temporary queue-eva.

#### Temporary queues

Ako se posmatra iz perspektive Consumera, njemu je bitno da prima poruke. A posto se koristi fanout exchange koji ce da salje poruke na sve queue-ove, moze da se napravi neki queue(defaultno ime koje daje rabbitMQ) na consumer strani koji ce svakako da prima poruke. Kada se konekcija zatvori treba i Queue unistiti a to se radi  exclusive=True. 
Ovde je poenta da se Queue pravi kad se pravi konekcija a brise se kad se konekcija gasi, sto bi znacilo da ako ima nekih poruka koje su se poslale dok Subscriber nije bio aktivan, nece moci da ih primi naknadno.

Uputstvo za pokretanje: 
1. Pokrenuti nekoliko Subscriber-a (python3 Subscriber.py)
2. Pokrenuti Publisher-a (python3 Publisher.py) i pratiti flow iz terminala

> ⚠️ *Poruke ce stici samo Subscriberima koji su aktivni zbog koriscenje temporary queue-eva.*

### Routing

Prilikom bindovanja nekog Queue-a nekom Exchange-u, moze da se iskoristi i routing_key. Routing key ima smisla u zavisnosti od exchange tipa. Na primer kod fanout-a nema smisla jer on salje poruke svim queue-ovima. Primer za ovo (Logging System).

Cilj kod Routing-a je da se ogranici samo jedan queue ili servis koji moze da se slusa.

Uputstvo za pokretanje:
1. Pokrenuti Subscribere (svaki u zasebnom terminalu)
2. Pokrenuti Publishera

### Topics

Topic ima slicnu funkciju kao Routing, samo su podesavanja drugacija. Za binding key se koriste reci koje se odvajaju tackama.

Upustvo za pokretanje:
1. Pokrenuti nekoliko Subscriber-a (kroz terminal), i pratiti flow iz terminala
2. Pokrenuti Publisher skriptu (kroz terminal) i pratiti flow iz terminala

