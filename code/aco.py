from graph import Graph
from ant import Ant
import copy
from statistics import mean
import json


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

    def __init__(self, ALPHA, BETA, dataset, cycles, ant_numbers, evaporation, init_pheromone, seed):
        
        self.ALPHA = ALPHA
        self.ant_numbers = ant_numbers
        self.BETA = BETA
        self.cycles = cycles
        self.evaporation = evaporation
        self.seed = seed

        #Creates first Graph
        G = Graph(dataset, init_pheromone)
        self.current_G, node_names = G.getGraph()

    def releaseTheAnts(self):
        results_control = {}
        for cycle_number in range(self.cycles):
            fastest_time = 99999999
            longest_time = 0
            this_cycle_times = []
            next_G = copy.deepcopy(self.current_G)

            for ant_number in range(self.ant_numbers)
                ant = Ant(self.current_G, self.ALPHA, self.BETA, self.seed, extended_seed=ant_number)
                ant_path = ant.walk()
                path_time = self.__calculateMakespanTime(ant_path)
                pheromone_weight = self.__calculatePheromoneWeight(path_time)
                next_G.updatePheromone(ant_path, pheromone_weight)

                #Recording cycle values
                this_cycle_times.append(path_time)
                if path_time < fastest_time:
                    fastest_time = path_time
                if path_time > longest_time:
                    longest_time = path_time

            #evaporate
            next_G.evaporatePheromone(self.evaporation)

            #Set enviroment with update pheromones for next cycle
            self.current_G = copy.deepcopy(next_G)

            #save recorded values
            results_control.update(
                {cycle_number : [
                            min(this_cycle_times),
                            mean(this_cycle_times),
                            max(this_cycle_times)
            ]})
        json.dump( generation_results, open( "ACO_cycle_results.json", 'w' ) )

    def __calculateMakespanTime(self, path):
        return 2

    def __calculatePheromoneWeight(self, time):
        return 4
