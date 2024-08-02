# Kommunikasjon med Unity
## UnityEvaluator.py
Er bindeleddet mellom min kode og ML-agents som videre kobler seg til Unity. 
* Starter det kjørbare programmet
* Starter Sidecannelsene 
* Sender og mottar kommandoer til simuleringen
* Regner ut rotasjonen til roboten. Legger sammen differansen mellom hvert steg
* Man bruker funksjonen evaluate for å kjøre en evaulering. Det er ikke anbefalt å bruke send_comand. Man skulle tro de ga samme svar da de fungerer på samme måte men neida...


## fitness_funtions.py
Inneholder fitnessfunksjonene
* basicFitness
    * Blir brukt i oppgaven. Blir brukt for å vurdere hvor lik start rotasjonen er. 
* circleFitness
    * Kommer fra forskjellige papers 


## ConfigSideChannel
For å sende ekstra data mellom Python og Unity som vekt, krefter og kuber