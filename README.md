# Utvikle et repertoar for en gående robot ved bruk av MAP-Elites
## Hva er målet med oppgaven:

 Hovedmålet med denne oppgaven er å undersøke virkelighetsgapet mellom spillmotoren Unity som simulator og den virkelige verden ved bruk av MAP-Elites.
 For å oppnå dette er oppgaven delt inn i flere delmål:
 1. Lage et robust og deterministisk miljø i Unity for Qutee-roboten som kan brukes til å trene evolusjonære algoritmer.
 
 2. Se på ulike kontrollere og hvordan antall variabler påvirker prestasjonen med hensyn til miljøet i Unity.
 
 3. Analysere om ulike hindringer i miljøet kan minske virkelighetsgapet mellom simulasjon og den fysiske roboten.

## Instalasjon:
Før du kan kjøre prosjektet vil du måtte ha:
1. Lastet ned prosjektet.
2. Lastet ned og installert Conda/Miniconda

### For å kjøre eksperimentene gjort i oppgaven:

1.  Lage et miljø med python 3.9, her kan env39 være hva som helst:
```bash
conda create -n env39 python=3.9 
```
2. Aktivere det lagde miljøet:
```bash
conda activte env39
```
3. Installere de forskjellige pakkene:
```bash
pip3 install -r requrement.txt
```
4. Installere QDPY separat:
```bash
pip3 install qdpy
```
5. For å kjøre programmet brukt i eksperiment 1 om determinisme:
```bash
python3 main3.py -c conf/Z\_TWoff\_B\_seeded.yaml
```

Det er forskjellige flagg man kan sende inn for å endre oppførselen på programmet. Disse overskriver det som blir sendt inn i configfilen: 
* ```--seed``` For å sette seeden til randomfunksjonene brukt i python. Påvirker ikke Unity sin random.
* ```-p```
* ```-n``` Antall steg Unity skal ta før episoden er ferdig. 1000 er 10 sekunder.
* ```-e``` Editor modus. Om man skal bruke Unity editoren eller det kompilerte programmet. Anbefaler bare å bruke utvikling av programmet.
* ```-hl``` Om man skal kjøre programmet uten bilde. Dette er for servere eller for datamaskiner uten kraftige grafikkort. 
* ```-c``` For å velge configfil å kjøre. Må velge en sti. 
* ```-o``` Sti til hvor resulatene skal legges. 
* ```-w``` Hvilken UDP port Unity og python skal kommunisere på. Brukes når man vil kjøre flere på samme datamaskin. 


## For å åpne/endre/forbedre Unity programmet:
1. Last ned Unity Hub
2. Last ned Unity editor version ```2021.3.8f1```. Dette er en LTS som begynner å bli gammel og burde egentlig bli byttet ut. Ikke anbefalt om man skal lage nye programmer. 
3. Åpne prosjektet i Unity Hub
4. Om det ikke skjer automatisk Ml-Agents pakken: Window --> Package Manager --> ML Agents ```2.0.1```
