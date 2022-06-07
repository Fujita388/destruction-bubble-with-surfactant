# Simulation of the destruction of bubbles with surfactant at the gas-liquid interface

 atom 1: solution, atom 2: hydrophobic group, atom 3: wall

 In advance, prepare surfactant on the surface of bubble

→  Relax the system in no gravity (make_bubble.input)

→  Add gas phase and apply gravity (gravity.input)


## Prevention of parallel shift caused by gravity

 Create a wall that does not move with the atoms named number 3


## Concentration of surfactant
 
 Calculate concentration of surfactant from the ratio of the number of atom 1 and 2
