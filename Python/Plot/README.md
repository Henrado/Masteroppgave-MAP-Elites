# Forskjellige filser som blir brukt til å plotte
## akumulering_utils.py
En samling av util funksjoner og metoder som brukes av akumulertplott.py i /Python
Filen inneholder 4 hovedfunksjoner:
* do_it_all_boxsplot
    * Tar inn en liste med ordbøker for forskjellige eksperimenter og skal lage et boxplot med STD for hvert eksriemt. Leser av hvert eksperiment sin iterations.csv og henter ut data. Bruker her siste QD-Scoren fra evolusjonen og lager STD av hvert av de like eksperimentene. 
    * {"key1": "Gruppe1","key2": "Gruppe2", "label": "Navn","path":"G_S_B_exLimit"}
    Se i akumulertplott.py i /Python for hvodan brukes
* do_it_all_stdline
    * Skal gjøre det samme men gjør det heller over tid med linjer. Input er på samme måte som med do_it_all_boxsplot. 
* do_it_all_grid
    * Skal lage et grid med poengsummene til hver løsningen. Kan både lage et kvalitetskart og et aktivitetskart basert på inputen quality_array
    * Tar gjennomsittet/median/max av alle like ekspeimenter 
* do_it_all_grid_per_ex
    * Gjør det samme for hvert eksperiment. Dette er for å automatisere og gjøre det for flere eksperimenter


## plot_different_sim.py
Bir ikke brukt til noe nyttig. 
Burde hvert fjernet. Har blitt til track.py i /Python 


## plots.py
Inneholder modifikasjoner på QDPY sin summary og plots_grid
* min_summary:
    * Printer ut hele løsningen isteden for å stoppe etter 200 tegn. Dette er kjekt da HPC-er logger alt som blir skrevet ut og man kan da ha enda en sikkerhetskopi
* min_plots_grid:
    * Lager bare et qd-score kart i tilegg til de vanlige 
    * Lagrer også ALL data i csv filer for å kunne lese det av senere. IKKE bruk picle, da man ikke kan åpne det på forskjellige datamaskiner

## sin_and_tanh_compare.py
Brukes til å lage et illustrasjonsbilde i oppgaven 