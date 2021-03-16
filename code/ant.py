from graph import Graph
import numpy as np

class Ant():
    """
    A individual responsible to find
    a walk on a enviroment represented
    by specific Graph.
    The decisions made by the individual
    are probabilistics using a function
    with the edges weights of the Graph.
    """
    def __init__(self, Enviroment, ALPHA, BETA, seed):
        self.seed = seed
        self.ALPHA = ALPHA
        self.BETA = BETA
        self.G, node_names = Enviroment.getEnviroment()
        self.not_visited = node_names
        self.current_node = (-1,-1)
        self.ant_path = []


    def walk(self):
        """
        The ant walks on every node
        of the graph without reapeating any.

        returns:
            array with edges followed in order
        """
        #Set seed for Ant decisions
        np.random.seed(self.seed)
        #Start the walk on graph proccess
        while self.not_visited:
            next_node = self.__chooseNextNode()
            self.ant_path.append((self.current_node, next_node))
            self.current_node = next_node
            self.not_visited.remove(next_node)
        return self.ant_path


    def __chooseNextNode(self):
        """
        With the not visited node
        probabilities chooses the
        next node to visit.

        returns:
            next_node
        """
        node_probabilities = self.__calculateNodeProbabilityChoices()
        next_node = np.random.choice(
                        list(node_probabilities.keys()), 
                        p=list(node_probabilities.values()))
        return next_node
        


    def __calculateNodeProbabilityChoices(self):
        """
        Visit every edge that directs to
        outher not visited nodes and
        uses it's pheromones and desirability
        to calculate the probability to follow
        each not visited node.

        returns:
            Dict: {not visited nodes -> choosing probability}
        """
        node_probabilities = dict()
        node_partial_probabilities = dict()
        probability_sum = 0
    
        #Calculates the partial probability to every not followed node edge
        for node in self.not_visited:
            desirability, pheromone = self.G[self.current_node][node]['weight']
            partial_probability = (pheromone ** self.ALPHA) * (desirability ** self.BETA)
            node_partial_probabilities.update({node : partial_probability})
            probability_sum += partial_probability
        
        #Calculate full probability over partial probability
        for node in node_partial_probabilities:
            node_probabilities.update({
                node : node_partial_probabilities[node] / (node_partial_probabilities[node] * probability_sum)
            })
        
        return node_probabilities