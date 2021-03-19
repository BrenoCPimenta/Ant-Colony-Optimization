from aco import ACO

#Set parameters for model:
parameters = {
    "seed" : 0, #Random seed that allows replicating results
    "ALPHA" : 2, #Exponential weight of pheromone on walk probabilities
    "BETA" : 0.2, #Exponential weight of desirability on walk probabilities
    "init_pheromone" : 0.999, #Initial pheromone for all edges
    "pheromone_constant" : 1, #Constant that helps to calculate edge pheromone contribution
    "min_pheromone" : 0.001, #Minimun pheromone value of an edge
    "evaporation_rate" : 0.96, #Pheromone evaporatio rate per cycle
    "ant_numbers" : 100, #100, #Number of ants walking in a cycle
    "cycles" : 30,#30, #Number of cycles
    "dataset" : 'la01.txt' #File name that contains job/machine times
}


colony = ACO(
    ALPHA=parameters['ALPHA'], 
    BETA=parameters['BETA'],
    dataset=parameters['dataset'],
    cycles=parameters['cycles'],
    ant_numbers=parameters['ant_numbers'],
    init_pheromone=parameters['init_pheromone'],
    pheromone_constant=parameters['pheromone_constant'],
    min_pheromone=parameters['min_pheromone'],
    evaporation_rate=parameters['evaporation_rate'],
    seed=parameters['seed'])

colony.releaseTheAnts()  

