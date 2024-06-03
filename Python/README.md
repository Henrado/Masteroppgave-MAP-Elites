# Python del:
Forklaring på de forskjellige python delene:
* Mapper:
*     ```EA``` Inneholder Kontrollerene og deres kontrollteknikker
*     ```Plot``` En samling av funksjoner brukt til forskjellige typer plot. Brukes av ```akumulertplott.py```.
*     ```Qutee_Interface``` Kommunikasjonen mellom Python og den fysiske roboten.
*     ```Unity``` Kommunikasjon mellom Python og Unity + sidechannels
*     ```conf``` Forskjellige konfigurasjonsfiler brukt i oppgaven 
*     ```utils``` Ulike funksjoner
* Filer:
*     ```akumulertplott.py``` Brukes til å summere opp alle like eksperimenter for å få et gjennomsnitt, enten i form av iterasjon over tid eller boxplot.
*     ```conf.yaml``` En generell konfigurasjonsfil 
*     ```csv_fixer.py``` For å gjøre om fra Mocapsystemet sit koordinatsystem til Unity sitt
*     ```main3.py``` Hovedprogrammet for oppgaven 
*     ```master_slurm.sh``` For å starte mange parallelle jobber. Trenger å kjøre slurm. Bruker ```slurm.sh```
*     ```pickle2json.py``` Gjør om pickle filene QDPY lager til json. ```main3.py``` kaller på denne. 
*     ```slurm.sh``` Brukes av master_slurm.sh for å starte parallelle jobber.
*     ```test_individ2.py``` Brukes til å teste/kjøre løsningene laget av ```main3.py```
*     ```test_individ3.py``` Ikke bruk. Var ment å bruke til å teste løsninger men gir feil svar.
*     ```track.py``` Sammenligne grafter laget i Mocap og fra Unity
