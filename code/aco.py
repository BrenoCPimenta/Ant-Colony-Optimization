from enviroment import Enviroment
from ant import Ant
import copy
from statistics import mean, stdev
import json
import numpy as np


class ACO():
    """
    Class responsible to manage the
    entire proccess. 
    It creates and executes the graph enviroment
    all the ants, updates the pheromones and 
    at the registers the best solution found.

    returns:
        Best Makespam time of critical path.
        Sequence Job/Machine for this path.
    """ 

    def __init__(self, ALPHA, BETA, dataset, cycles, ant_numbers, init_pheromone, pheromone_constant, min_pheromone, evaporation_rate, seed):
        self.ALPHA = ALPHA
        self.ant_numbers = ant_numbers
        self.BETA = BETA
        self.cycles = cycles
        self.pheromone_constant = pheromone_constant
        self.evaporation_rate = evaporation_rate
        self.seed = seed

        #Inicialize the Enviroment and set data
        self.enviroment = Enviroment(dataset, init_pheromone, min_pheromone)
        self.time_of_executions = self.enviroment.getTimeOfExecutions()
        self.node_names = self.enviroment.getNodeNames()
        self.graph_edges = self.enviroment.getEdges()
    

    def releaseTheAnts(self):
        """
        Method responsible to create
        and execute all ants through
        the enviroment and update
        the pheromones.

        returns:
            - Print the best time.
            - Generate a file with the 
                time results of all cycles
                with this structure:
                {cycle : [Fastest, Mean, Longest], ...}
        """
        results_control = {}
        all_times = []
        fastest_path = []
        for cycle_number in range(self.cycles):
            this_cycle_times = []
            #Get the updated graph:
            this_cycle_Graph = self.enviroment.getGraph()
            #Create dict with each edge as a key and all values as zeros,
            #  so it can sum all edges contribution along this cycle:
            this_cycle_edges_contributions = dict.fromkeys(self.graph_edges,0) 

            for ant_number in range(self.ant_numbers):
                #Create Ant, make it walk through the graph and calculate makespan time for that walk
                ant = Ant(this_cycle_Graph, self.node_names, self.ALPHA, self.BETA, self.seed, extended_seed=ant_number)
                ant_path = ant.walk()
                path_time = self.enviroment.calculateMakespanTime(ant_path)
                #Recording the pheromone contribution for each edge of this walk
                for edge in ant_path:
                    this_cycle_edges_contributions[edge] += self.pheromone_constant/path_time
                #Recording cycle values:
                this_cycle_times.append(path_time)
                all_times.append(path_time)

            #Update pheromone on edges of the graph
            self.enviroment.updatePheromone(
                self.evaporation_rate,
                this_cycle_edges_contributions)

            #save recorded values
            results_control.update(
                {cycle_number : [
                            min(this_cycle_times),
                            mean(this_cycle_times),
                            max(this_cycle_times)
            ]})

        #generating file with fitness through cycles
        json.dump( results_control, open( "ACO_cycles_results.json", 'w' ) )
        #Print results:
        print("---------------------------------------------------")
        print("Mean: ", mean(all_times))
        print("Standard deviation: ", stdev(all_times))
        print("BEST PATH TIME: ", min(all_times), " seconds")
        print("---------------------------------------------------")
 