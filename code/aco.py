from enviroment import Enviroment
from ant import Ant
import copy
import sys
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

    def __init__(self, ALPHA, BETA, dataset, cycles, ant_numbers, init_pheromone, seed):
        self.ALPHA = ALPHA
        self.ant_numbers = ant_numbers
        self.BETA = BETA
        self.cycles = cycles
        self.seed = seed

        #Calculating pheromone evaporation value through cycles 
        self.evaporation = (init_pheromone / cycles) - 0.0001

        #Creates the Enviroment and get global data
        self.enviroment = Enviroment(dataset, init_pheromone)
        self.time_of_executions = self.enviroment.getTimeOfExecutions()
        self.node_names = self.enviroment.getNodeNames()
    

    def releaseTheAnts(self):
        """
        Method responsible to create
        and execute all ants through
        the enviroment and update
        the pheromones.

        returns:
            - Print the best time.
            - Generate a file with the 
            time results all cycles:
                [Fastest, Mean, Longest]
        """
        results_control = {}
        fastest_time = sys.float_info.max  #1.7976931348623157e+308
        fastest_path = []
        for cycle_number in range(self.cycles):
            this_cycle_times = []
            this_cycle_Graph = self.enviroment.getGraph()

            for ant_number in range(self.ant_numbers)
                ant = Ant(this_cycle_Graph, self.ALPHA, self.BETA, self.seed, extended_seed=ant_number)
                ant_path = ant.walk()
                path_time = self.__calculateMakespanTime(ant_path)
                pheromone_weight = self.__calculatePheromoneWeight(path_time)
                self.enviroment.updatePheromone(ant_path, pheromone_weight)

                #Recording cycle values
                this_cycle_times.append(path_time)
                if path_time < fastest_time:
                    fastest_time = path_time
                    fastest_path = ant_path

            #evaporate
            self.enviroment.evaporatePheromone(self.evaporation)

            #Set enviroment with update pheromones for next cycle
            self.current_G = copy.deepcopy(next_G)

            #save recorded values
            results_control.update(
                {cycle_number : [
                            min(this_cycle_times),
                            mean(this_cycle_times),
                            max(this_cycle_times)
            ]})
        #generating file with fitness through cycles
        json.dump( results_control, open( "ACO_cycles_results.json", 'w' ) )

        print("BEST PATH: ")
        for edge in fastest_path:
            print(edge[0],"  ->  ", edge[1])
        print("---------------------------------------------------")
        print("BEST PATH TIME: ", fastest_time, " seconds")


    def __calculateMakespanTime(self, path):
        return 2

    def __calculatePheromoneWeight(self, time):
        return 4
