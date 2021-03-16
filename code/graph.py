import networkx as nx

class Enviroment():

    def __init__(self, file_name, init_pheromone):
        #Read Data
        self.data = self.__readData(file_name)
        #Create Graph
        self.G, self.node_names = self.__buildGraph(self.data, init_pheromone)


    def __readData(file_name):
    """
    Reads file and create a first data structure.
    Structure is a Matrix:
         Line:Jobs 
         Column: Machines
         Content:time of execution.
    returns:
        the matrix, the number of jobs and 
        number of machines.
    """        
    jobs = []
    with open("../test_instances/" + file_name,'r') as file: 
        for i, line in enumerate(file): 
            machines = {}
            this_machine = None
            for j,value in enumerate(line.split()):
                if j%2 != 0:
                    machines.update({this_machine : value})
                else:
                    this_machine = value
            jobs.append(machines)
    return jobs #Named as data outside method


    def __buildGraph(data, init_pheromone):
    """
    From the matrix returned on __readData() method
    creates a Direct, Weighted and FullConnected Graph 
    using networkx library.
    This library will facilitate working with edges.
    Will be added a virtual inital node (-1,-1) that connects
    to all others nodes.

    returns:
        Graph and all node names.
    """
    num_jobs = len(data)
    num_machines = len(data[0])
    num_nodes = num_jobs*num_machines + 1 #All machineXjobs pair plus the initial virtual node

    #Create directed and fully connected graph, with weight zero in every edge:
    init_desirabilty = 0
    unnamed_graph = nx.complete_graph(num_nodes,  nx.DiGraph(weight=0)

    #Giving proper names to the nodes:
    node_names = [(-1,-1)] #Add initial virtual node 
    for job in range(num_jobs):
        for machine in range(num_machines):
            node_names.append((job, machine))
    mapping = {i:nodename for i,nodename in enumerate(node_names)} #mapping: {0:(-1,-1), 1:(0,0), ...}
    G = nx.relabel_nodes(unnamed_graph,mapping)
    
    #Remove Edges that point to the  initial vitual node, 
    # so it only remains from initial to other nodes and not the other way arround:
    for job in range(num_jobs):
        for machine in range(num_machines):
            G.remove_edge((job, machine), (-1,-1))

    #Update Pheromone and desirability:
    for from_job in range(num_jobs):
        for from_machine in range(num_machines):
            for to_job in range(num_jobs):
                for to_machine in range(num_machines):
                    execution_time = data[to_job][to_machine]
                    desirability = 1/execution_time
                    G[(from_job,from_machine)][(to_job,to_machine)]['weight'] = (desirability, init_pheromone)

    node_names.remove((-1,-1)) #Remove initial virtual node from names
    return G, node_names


    def getEnviroment(self):
        """
        Returns Graph with updated
        pheromones and node names
        """
        return self.G, self.node_names

    #def updatePheromone(self, walk):
    # desirability
    #    time = self.__calculateTimeFromWalk(walk)

    #def __calculateTimeFromWalk(self, walk):
    #    pass